"""
Configuration Flask-Admin
Interface d'administration avec contrôle d'accès basé sur les rôles
"""
from flask import redirect, url_for, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from models import db, User, Product, FileUpload, Role, ActivityLog

class SecureAdminIndexView(AdminIndexView):
    """Vue d'index personnalisée avec protection admin"""
    
    @expose('/')
    def index(self):
        """Page d'accueil de l'admin - accessible uniquement aux admins"""
        if not current_user.is_authenticated or not current_user.has_role('admin'):
            flash('Accès refusé. Vous devez être administrateur.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Statistiques pour le dashboard admin
        stats = {
            'total_users': User.query.count(),
            'total_products': Product.query.count(),
            'total_uploads': FileUpload.query.count(),
            'total_roles': Role.query.count(),
            'active_users': User.query.filter_by(active=True).count(),
            'inactive_users': User.query.filter_by(active=False).count(),
        }
        
        return self.render('admin/index.html', stats=stats)

class SecureModelView(ModelView):
    """Vue de modèle sécurisée - accessible uniquement aux admins"""
    
    def is_accessible(self):
        """Vérifie si l'utilisateur a accès à cette vue"""
        return current_user.is_authenticated and current_user.has_role('admin')
    
    def inaccessible_callback(self, name, **kwargs):
        """Redirection si l'accès est refusé"""
        flash('Accès refusé. Vous devez être administrateur.', 'danger')
        return redirect(url_for('auth.login'))

class UserAdminView(SecureModelView):
    """Vue admin pour les utilisateurs"""
    
    # Colonnes à afficher dans la liste
    column_list = ['id', 'username', 'email', 'first_name', 'last_name', 'active', 'created_at', 'roles']
    
    # Colonnes recherchables
    column_searchable_list = ['username', 'email', 'first_name', 'last_name']
    
    # Colonnes filtrables
    column_filters = ['active', 'created_at', 'roles']
    
    # Colonnes à afficher par défaut
    column_default_sort = ('created_at', True)
    
    # Configuration du formulaire
    form_columns = ['username', 'email', 'first_name', 'last_name', 'active', 'roles']
    
    # Colonnes exclues du formulaire d'édition
    form_excluded_columns = ['password_hash', 'products', 'uploads', 'activities', 'last_login']
    
    # Labels personnalisés
    column_labels = {
        'username': 'Nom d\'utilisateur',
        'email': 'Email',
        'first_name': 'Prénom',
        'last_name': 'Nom',
        'active': 'Actif',
        'created_at': 'Date d\'inscription',
        'roles': 'Rôles'
    }
    
    # Descriptions
    column_descriptions = {
        'active': 'Décochez pour désactiver le compte utilisateur',
        'roles': 'Rôles attribués à l\'utilisateur'
    }
    
    # Pagination
    page_size = 50

class ProductAdminView(SecureModelView):
    """Vue admin pour les produits"""
    
    column_list = ['id', 'name', 'category', 'price', 'stock', 'creator', 'created_at']
    column_searchable_list = ['name', 'description', 'category']
    column_filters = ['category', 'price', 'stock', 'created_at']
    column_default_sort = ('created_at', True)
    
    form_columns = ['name', 'description', 'price', 'stock', 'category', 'image_url', 'user_id']
    
    column_labels = {
        'name': 'Nom',
        'description': 'Description',
        'price': 'Prix',
        'stock': 'Stock',
        'category': 'Catégorie',
        'image_url': 'URL Image',
        'creator': 'Créateur',
        'created_at': 'Date de création',
        'user_id': 'Utilisateur'
    }
    
    # Formatage personnalisé
    column_formatters = {
        'price': lambda v, c, m, n: f"{m.price:.2f} €"
    }
    
    page_size = 50

class FileUploadAdminView(SecureModelView):
    """Vue admin pour les fichiers uploadés"""
    
    column_list = ['id', 'original_filename', 'mime_type', 'file_size', 'uploader', 'uploaded_at']
    column_searchable_list = ['original_filename', 'mime_type']
    column_filters = ['mime_type', 'uploaded_at']
    column_default_sort = ('uploaded_at', True)
    
    # Exclure le chemin complet du fichier pour la sécurité
    form_excluded_columns = ['file_path']
    
    column_labels = {
        'original_filename': 'Nom du fichier',
        'filename': 'Nom stocké',
        'mime_type': 'Type',
        'file_size': 'Taille',
        'uploader': 'Uploadé par',
        'uploaded_at': 'Date d\'upload'
    }
    
    # Formatage de la taille de fichier
    def _format_file_size(view, context, model, name):
        size = model.file_size
        if size is None:
            return '-'
        elif size < 1024:
            return f"{size} B"
        elif size < 1048576:
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size / 1048576:.2f} MB"
    
    column_formatters = {
        'file_size': _format_file_size
    }
    
    page_size = 50

class RoleAdminView(SecureModelView):
    """Vue admin pour les rôles"""
    
    column_list = ['id', 'name', 'description']
    column_searchable_list = ['name', 'description']
    
    form_columns = ['name', 'description']
    
    column_labels = {
        'name': 'Nom du rôle',
        'description': 'Description'
    }
    
    column_descriptions = {
        'name': 'Nom unique du rôle (ex: admin, user, moderator)',
        'description': 'Description du rôle et de ses permissions'
    }

class ActivityLogAdminView(SecureModelView):
    """Vue admin pour les logs d'activité"""
    
    # Lecture seule pour les logs
    can_create = False
    can_edit = False
    can_delete = True
    
    column_list = ['id', 'user', 'action', 'description', 'ip_address', 'created_at']
    column_searchable_list = ['action', 'description', 'ip_address']
    column_filters = ['action', 'created_at', 'user']
    column_default_sort = ('created_at', True)
    
    column_labels = {
        'user': 'Utilisateur',
        'action': 'Action',
        'description': 'Description',
        'ip_address': 'Adresse IP',
        'created_at': 'Date'
    }
    
    page_size = 100

def init_admin(app):
    """Initialise Flask-Admin avec l'application"""
    admin = Admin(
        app,
        name='Administration',
        template_mode='bootstrap4',
        index_view=SecureAdminIndexView(),
        base_template='admin/custom_base.html'
    )
    
    # Ajouter les vues admin
    admin.add_view(UserAdminView(User, db.session, name='Utilisateurs', category='Gestion'))
    admin.add_view(ProductAdminView(Product, db.session, name='Produits', category='Gestion'))
    admin.add_view(FileUploadAdminView(FileUpload, db.session, name='Fichiers', category='Gestion'))
    admin.add_view(RoleAdminView(Role, db.session, name='Rôles', category='Sécurité'))
    admin.add_view(ActivityLogAdminView(ActivityLog, db.session, name='Logs d\'activité', category='Sécurité'))
    
    return admin
