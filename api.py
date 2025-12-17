"""
API REST pour accéder aux données
Fournit des endpoints JSON pour les opérations CRUD
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import db, Product, FileUpload, User, ActivityLog
from functools import wraps

api_bp = Blueprint('api', __name__, url_prefix='/api')

def admin_required(f):
    """Décorateur pour restreindre l'accès aux administrateurs"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.has_role('admin'):
            return jsonify({'error': 'Accès non autorisé. Rôle administrateur requis.'}), 403
        return f(*args, **kwargs)
    return decorated_function

# ==================== ENDPOINTS PRODUCTS ====================

@api_bp.route('/products', methods=['GET'])
def get_products():
    """
    GET /api/products - Récupère tous les produits
    Query params: category, min_price, max_price, limit
    """
    try:
        # Récupérer les paramètres de filtre
        category = request.args.get('category')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        limit = request.args.get('limit', type=int)
        
        # Construction de la requête avec filtres
        query = Product.query
        
        if category:
            query = query.filter_by(category=category)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        if limit:
            query = query.limit(limit)
        
        products = query.all()
        
        return jsonify({
            'success': True,
            'count': len(products),
            'products': [product.to_dict() for product in products]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """GET /api/products/<id> - Récupère un produit spécifique"""
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify({
            'success': True,
            'product': product.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@api_bp.route('/products', methods=['POST'])
@login_required
def create_product():
    """POST /api/products - Crée un nouveau produit"""
    try:
        data = request.get_json()
        
        # Validation des données
        if not data or 'name' not in data or 'price' not in data:
            return jsonify({'error': 'Nom et prix requis'}), 400
        
        # Création du produit
        product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price']),
            stock=int(data.get('stock', 0)),
            category=data.get('category', ''),
            image_url=data.get('image_url', ''),
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
        
        return jsonify({
            'success': True,
            'message': 'Produit créé avec succès',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/products/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    """PUT /api/products/<id> - Met à jour un produit"""
    try:
        product = Product.query.get_or_404(product_id)
        
        # Vérifier que l'utilisateur est propriétaire ou admin
        if product.user_id != current_user.id and not current_user.has_role('admin'):
            return jsonify({'error': 'Accès non autorisé'}), 403
        
        data = request.get_json()
        
        # Mise à jour des champs
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = float(data['price'])
        if 'stock' in data:
            product.stock = int(data['stock'])
        if 'category' in data:
            product.category = data['category']
        if 'image_url' in data:
            product.image_url = data['image_url']
        
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
        
        return jsonify({
            'success': True,
            'message': 'Produit mis à jour avec succès',
            'product': product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/products/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    """DELETE /api/products/<id> - Supprime un produit"""
    try:
        product = Product.query.get_or_404(product_id)
        
        # Vérifier que l'utilisateur est propriétaire ou admin
        if product.user_id != current_user.id and not current_user.has_role('admin'):
            return jsonify({'error': 'Accès non autorisé'}), 403
        
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
        
        return jsonify({
            'success': True,
            'message': 'Produit supprimé avec succès'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== ENDPOINTS USERS ====================

@api_bp.route('/users', methods=['GET'])
@login_required
@admin_required
def get_users():
    """GET /api/users - Récupère tous les utilisateurs (admin seulement)"""
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'count': len(users),
            'users': [{
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'active': user.active,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'roles': [role.name for role in user.roles]
            } for user in users]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    """GET /api/users/<id> - Récupère un utilisateur spécifique"""
    try:
        # L'utilisateur peut voir son propre profil, admin peut voir tous
        if current_user.id != user_id and not current_user.has_role('admin'):
            return jsonify({'error': 'Accès non autorisé'}), 403
        
        user = User.query.get_or_404(user_id)
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'active': user.active,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'roles': [role.name for role in user.roles]
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# ==================== ENDPOINTS UPLOADS ====================

@api_bp.route('/uploads', methods=['GET'])
@login_required
def get_uploads():
    """GET /api/uploads - Récupère les fichiers de l'utilisateur"""
    try:
        if current_user.has_role('admin'):
            uploads = FileUpload.query.all()
        else:
            uploads = FileUpload.query.filter_by(user_id=current_user.id).all()
        
        return jsonify({
            'success': True,
            'count': len(uploads),
            'uploads': [upload.to_dict() for upload in uploads]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ENDPOINTS STATISTIQUES ====================

@api_bp.route('/stats/dashboard', methods=['GET'])
@login_required
def get_dashboard_stats():
    """GET /api/stats/dashboard - Récupère les statistiques pour le dashboard"""
    try:
        stats = {
            'total_users': User.query.count(),
            'total_products': Product.query.count(),
            'total_uploads': FileUpload.query.count(),
            'total_activities': ActivityLog.query.count(),
            'recent_activities': []
        }
        
        # Récupérer les activités récentes
        recent_logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(10).all()
        stats['recent_activities'] = [{
            'id': log.id,
            'action': log.action,
            'description': log.description,
            'created_at': log.created_at.isoformat() if log.created_at else None,
            'user': log.user.username if log.user else 'System'
        } for log in recent_logs]
        
        # Statistiques par catégorie de produits
        from sqlalchemy import func
        category_stats = db.session.query(
            Product.category,
            func.count(Product.id).label('count')
        ).group_by(Product.category).all()
        
        stats['products_by_category'] = {cat: count for cat, count in category_stats if cat}
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ENDPOINT TEST ====================

@api_bp.route('/ping', methods=['GET'])
def ping():
    """GET /api/ping - Endpoint de test"""
    return jsonify({
        'success': True,
        'message': 'API is running',
        'authenticated': current_user.is_authenticated
    }), 200
