"""
Configuration de l'application Flask
Gère les différents environnements (développement, production)
"""
import os
from dotenv import load_dotenv
import pymysql

# Installer pymysql comme remplacement de MySQLdb
pymysql.install_as_MySQLdb()

# Charger les variables d'environnement
load_dotenv()

class Config:
    """Configuration de base pour l'application"""
    
    # Clé secrète pour les sessions et CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuration de la base de données SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+pymysql://root:Ningen%402024@localhost:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'pool_size': 10,
        'max_overflow': 20
    }
    
    # Configuration des uploads de fichiers
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    # Configuration Flask-Admin
    FLASK_ADMIN_SWATCH = 'cerulean'
    
    # Configuration de sécurité
    SESSION_COOKIE_SECURE = False  # True en production avec HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuration Flask-Talisman (sécurité HTTP)
    TALISMAN_FORCE_HTTPS = False  # True en production
    
class DevelopmentConfig(Config):
    """Configuration pour l'environnement de développement"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuration pour l'environnement de production"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    TALISMAN_FORCE_HTTPS = True

class TestingConfig(Config):
    """Configuration pour les tests"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

# Dictionnaire des configurations
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
