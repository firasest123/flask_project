"""
Routes principales de l'application
Gestion des produits, uploads, dashboard
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_required, current_user
from models import db, Product, FileUpload, User, ActivityLog
from forms import ProductForm, FileUploadForm
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard avec statistiques - Admin ou User"""
    # Si l'utilisateur est admin, afficher le dashboard admin complet
    if current_user.has_role('admin'):
        # Récupérer les statistiques globales
        stats = {
            'total_users': User.query.count(),
            'total_products': Product.query.count(),
            'total_uploads': FileUpload.query.count(),
            'total_activities': ActivityLog.query.count(),
        }
        
        # Activités récentes (toutes)
        recent_activities = ActivityLog.query.order_by(
            ActivityLog.created_at.desc()
        ).limit(10).all()
        
        stats['recent_activities'] = [{
            'id': log.id,
            'action': log.action,
            'description': log.description,
            'created_at': log.created_at.strftime('%d/%m/%Y %H:%M') if log.created_at else '',
            'user': log.user.username if log.user else 'System'
        } for log in recent_activities]
        
        # Produits par catégorie
        category_stats = db.session.query(
            Product.category,
            func.count(Product.id).label('count')
        ).filter(Product.category.isnot(None)).group_by(Product.category).all()
        
        stats['products_by_category'] = {cat: count for cat, count in category_stats if cat}
        
        return render_template('admin_dashboard.html', stats=stats)
    
    # Sinon, afficher le dashboard utilisateur personnalisé
    else:
        # Statistiques personnelles de l'utilisateur
        stats = {
            'my_products': Product.query.filter_by(user_id=current_user.id).count(),
            'my_uploads': FileUpload.query.filter_by(user_id=current_user.id).count(),
            'my_activities': ActivityLog.query.filter_by(user_id=current_user.id).count(),
            'member_since': current_user.created_at.strftime('%d/%m/%Y') if current_user.created_at else 'N/A'
        }
        
        # Produits récents de l'utilisateur
        stats['recent_products'] = Product.query.filter_by(
            user_id=current_user.id
        ).order_by(Product.created_at.desc()).limit(5).all()
        
        # Activités récentes de l'utilisateur
        recent_activities = ActivityLog.query.filter_by(
            user_id=current_user.id
        ).order_by(ActivityLog.created_at.desc()).limit(10).all()
        
        stats['my_recent_activities'] = [{
            'id': log.id,
            'action': log.action,
            'description': log.description,
            'created_at': log.created_at.strftime('%d/%m/%Y %H:%M') if log.created_at else ''
        } for log in recent_activities]
        
        # Fichiers récents de l'utilisateur
        stats['recent_uploads'] = FileUpload.query.filter_by(
            user_id=current_user.id
        ).order_by(FileUpload.uploaded_at.desc()).limit(5).all()
        
        return render_template('user_dashboard.html', stats=stats)

# ==================== ROUTES PRODUCTS ====================

@main_bp.route('/products')
@login_required
def products():
    """Liste des produits avec recherche et filtres"""
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Product.query
    
    # Filtres
    if search:
        query = query.filter(
            (Product.name.ilike(f'%{search}%')) | 
            (Product.description.ilike(f'%{search}%'))
        )
    
    if category:
        query = query.filter_by(category=category)
    
    products = query.order_by(Product.created_at.desc()).all()
    
    # Liste des catégories pour le filtre
    categories = db.session.query(Product.category).distinct().filter(
        Product.category.isnot(None)
    ).all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('products/list.html', products=products, categories=categories)

@main_bp.route('/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    """Créer un nouveau produit"""
    form = ProductForm()
    
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data or 0,
            category=form.category.data,
            image_url=form.image_url.data,
            user_id=current_user.id
        )
        
        db.session.add(product)
        db.session.commit()
        
        # Log de l'activité
        log = ActivityLog(
            user_id=current_user.id,
            action='create_product',
            description=f'Produit créé: {product.name}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        flash('Produit créé avec succès !', 'success')
        return redirect(url_for('main.products'))
    
    return render_template('products/form.html', form=form, product=None)

@main_bp.route('/products/<int:product_id>')
@login_required
def view_product(product_id):
    """Voir les détails d'un produit"""
    product = Product.query.get_or_404(product_id)
    return render_template('products/view.html', product=product)

@main_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    """Modifier un produit"""
    product = Product.query.get_or_404(product_id)
    
    # Vérifier que l'utilisateur est propriétaire ou admin
    if product.user_id != current_user.id and not current_user.has_role('admin'):
        flash('Vous n\'avez pas la permission de modifier ce produit.', 'danger')
        return redirect(url_for('main.products'))
    
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data or 0
        product.category = form.category.data
        product.image_url = form.image_url.data
        
        db.session.commit()
        
        # Log de l'activité
        log = ActivityLog(
            user_id=current_user.id,
            action='update_product',
            description=f'Produit mis à jour: {product.name}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        flash('Produit mis à jour avec succès !', 'success')
        return redirect(url_for('main.products'))
    
    return render_template('products/form.html', form=form, product=product)

@main_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    """Supprimer un produit"""
    product = Product.query.get_or_404(product_id)
    
    # Vérifier que l'utilisateur est propriétaire ou admin
    if product.user_id != current_user.id and not current_user.has_role('admin'):
        flash('Vous n\'avez pas la permission de supprimer ce produit.', 'danger')
        return redirect(url_for('main.products'))
    
    product_name = product.name
    db.session.delete(product)
    db.session.commit()
    
    # Log de l'activité
    log = ActivityLog(
        user_id=current_user.id,
        action='delete_product',
        description=f'Produit supprimé: {product_name}',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    flash('Produit supprimé avec succès !', 'success')
    return redirect(url_for('main.products'))

# ==================== ROUTES UPLOAD ====================

@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    """Upload de fichiers"""
    form = FileUploadForm()
    
    if form.validate_on_submit():
        file = form.file.data
        
        if file:
            # Sécuriser le nom du fichier
            filename = secure_filename(file.filename)
            
            # Créer un nom unique avec timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{timestamp}_{filename}"
            
            # Créer le dossier uploads s'il n'existe pas
            upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            
            # Sauvegarder le fichier
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)
            
            # Enregistrer dans la base de données
            file_upload = FileUpload(
                filename=unique_filename,
                original_filename=filename,
                file_path=file_path,
                file_size=os.path.getsize(file_path),
                mime_type=file.content_type,
                user_id=current_user.id
            )
            
            db.session.add(file_upload)
            db.session.commit()
            
            # Log de l'activité
            log = ActivityLog(
                user_id=current_user.id,
                action='upload_file',
                description=f'Fichier uploadé: {filename}',
                ip_address=request.remote_addr
            )
            db.session.add(log)
            db.session.commit()
            
            flash('Fichier uploadé avec succès !', 'success')
            return redirect(url_for('main.upload_file'))
    
    # Récupérer les fichiers de l'utilisateur
    if current_user.has_role('admin'):
        uploads = FileUpload.query.order_by(FileUpload.uploaded_at.desc()).all()
    else:
        uploads = FileUpload.query.filter_by(user_id=current_user.id).order_by(
            FileUpload.uploaded_at.desc()
        ).all()
    
    return render_template('upload.html', form=form, uploads=uploads)

@main_bp.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    """Télécharger un fichier"""
    file_upload = FileUpload.query.get_or_404(file_id)
    
    # Vérifier les permissions
    if file_upload.user_id != current_user.id and not current_user.has_role('admin'):
        flash('Vous n\'avez pas la permission de télécharger ce fichier.', 'danger')
        return redirect(url_for('main.upload_file'))
    
    upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    
    return send_from_directory(
        upload_folder, 
        file_upload.filename, 
        as_attachment=True,
        download_name=file_upload.original_filename
    )

@main_bp.route('/upload/<int:file_id>/delete', methods=['POST'])
@login_required
def delete_file(file_id):
    """Supprimer un fichier"""
    file_upload = FileUpload.query.get_or_404(file_id)
    
    # Vérifier les permissions
    if file_upload.user_id != current_user.id and not current_user.has_role('admin'):
        flash('Vous n\'avez pas la permission de supprimer ce fichier.', 'danger')
        return redirect(url_for('main.upload_file'))
    
    # Supprimer le fichier physique
    try:
        if os.path.exists(file_upload.file_path):
            os.remove(file_upload.file_path)
    except Exception as e:
        flash(f'Erreur lors de la suppression du fichier: {str(e)}', 'danger')
    
    # Supprimer de la base de données
    filename = file_upload.original_filename
    db.session.delete(file_upload)
    db.session.commit()
    
    # Log de l'activité
    log = ActivityLog(
        user_id=current_user.id,
        action='delete_file',
        description=f'Fichier supprimé: {filename}',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    flash('Fichier supprimé avec succès !', 'success')
    return redirect(url_for('main.upload_file'))
