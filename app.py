"""
Application Flask principale
Point d'entrée de l'application avec configuration complète
"""
import os
from flask import Flask, render_template
from flask_login import LoginManager
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from config import config
from models import db, User
from api import api_bp
from routes_auth import auth_bp
from routes_main import main_bp
from admin import init_admin

def create_app(config_name='default'):
    """Factory pour créer l'application Flask"""
    
    app = Flask(__name__)
    
    # Charger la configuration
    app.config.from_object(config[config_name])
    
    # Initialiser les extensions
    db.init_app(app)
    
    # Initialiser la protection CSRF
    csrf = CSRFProtect(app)
    
    # Configuration Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Charge l'utilisateur depuis la base de données"""
        return User.query.get(int(user_id))
    
    # Configuration Flask-Talisman pour la sécurité HTTP
    # Note: désactivé en développement, activé en production
    if app.config.get('TALISMAN_FORCE_HTTPS'):
        Talisman(app, 
                force_https=True,
                strict_transport_security=True,
                session_cookie_secure=True,
                content_security_policy={
                    'default-src': "'self'",
                    'script-src': ["'self'", "'unsafe-inline'", 'cdn.jsdelivr.net', 'cdnjs.cloudflare.com'],
                    'style-src': ["'self'", "'unsafe-inline'", 'cdn.jsdelivr.net', 'cdnjs.cloudflare.com'],
                    'img-src': ["'self'", 'data:', 'https:'],
                    'font-src': ["'self'", 'cdnjs.cloudflare.com']
                })
    else:
        # En développement, Talisman avec HTTPS désactivé
        Talisman(app, 
                force_https=False,
                content_security_policy=None)
    
    # Enregistrer les blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp)
    
    # Initialiser Flask-Admin
    init_admin(app)
    
    # Gestionnaire d'erreur 404
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    # Gestionnaire d'erreur 403
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403
    
    # Gestionnaire d'erreur 500
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Contexte de template global
    @app.context_processor
    def inject_globals():
        """Injecte des variables globales dans tous les templates"""
        return {
            'app_name': 'Flask Application',
            'app_version': '1.0.0'
        }
    
    # Commandes CLI personnalisées
    @app.cli.command()
    def init_db():
        """Initialise la base de données"""
        from models import Role
        
        db.create_all()
        
        # Créer les rôles par défaut si ils n'existent pas
        roles = ['admin', 'user', 'moderator']
        for role_name in roles:
            if not Role.query.filter_by(name=role_name).first():
                role = Role(
                    name=role_name,
                    description=f'Rôle {role_name}'
                )
                db.session.add(role)
        
        db.session.commit()
        print('✓ Base de données initialisée avec succès !')
        print('✓ Rôles créés: admin, user, moderator')
    
    @app.cli.command()
    def create_admin():
        """Crée un utilisateur administrateur"""
        from models import Role
        
        # Vérifier si un admin existe déjà
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            print('✗ Erreur: Exécutez d\'abord "flask init-db"')
            return
        
        # Créer l'admin
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print('✗ Un utilisateur "admin" existe déjà')
            return
        
        admin = User(
            username='admin',
            email='admin@example.com',
            first_name='Admin',
            last_name='User'
        )
        admin.set_password('admin123')  # Mot de passe par défaut
        admin.roles.append(admin_role)
        
        db.session.add(admin)
        db.session.commit()
        
        print('✓ Administrateur créé avec succès !')
        print('  Username: admin')
        print('  Password: admin123')
        print('  ⚠️  CHANGEZ CE MOT DE PASSE EN PRODUCTION !')
    
    @app.cli.command()
    def create_sample_data():
        """Crée des données d'exemple pour tester l'application"""
        from models import Product
        
        print('Création de données d\'exemple...')
        
        # Trouver un utilisateur
        user = User.query.first()
        if not user:
            print('✗ Aucun utilisateur trouvé. Créez d\'abord un utilisateur.')
            return
        
        # Produits d'exemple
        sample_products = [
            {
                'name': 'Laptop Dell XPS 15',
                'description': 'Ordinateur portable haute performance avec écran 4K',
                'price': 1499.99,
                'stock': 10,
                'category': 'Électronique',
                'image_url': 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400'
            },
            {
                'name': 'iPhone 15 Pro',
                'description': 'Smartphone Apple dernière génération',
                'price': 1199.00,
                'stock': 25,
                'category': 'Électronique',
                'image_url': 'https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=400'
            },
            {
                'name': 'Chaise de bureau ergonomique',
                'description': 'Chaise confortable pour le travail',
                'price': 299.99,
                'stock': 15,
                'category': 'Mobilier',
                'image_url': 'https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=400'
            },
            {
                'name': 'Livre: Python Programming',
                'description': 'Guide complet de programmation Python',
                'price': 39.99,
                'stock': 50,
                'category': 'Livres',
                'image_url': 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=400'
            },
            {
                'name': 'Casque audio Sony WH-1000XM5',
                'description': 'Casque sans fil avec réduction de bruit',
                'price': 349.99,
                'stock': 20,
                'category': 'Électronique',
                'image_url': 'https://images.unsplash.com/photo-1545127398-14699f92334b?w=400'
            }
        ]
        
        for product_data in sample_products:
            product = Product(user_id=user.id, **product_data)
            db.session.add(product)
        
        db.session.commit()
        print(f'✓ {len(sample_products)} produits d\'exemple créés !')
    
    return app

# Créer l'application
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Lancer le serveur de développement
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
