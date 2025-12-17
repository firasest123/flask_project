"""
Script d'initialisation de la base de données MySQL
Crée les tables et les données de test
"""
from app import app, db
from models import User, Role, Product, FileUpload, ActivityLog
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()

def init_database():
    """Initialiser la base de données MySQL avec des données de test"""
    with app.app_context():
        # Supprimer toutes les tables existantes et les recréer
        print("Suppression des anciennes tables...")
        db.drop_all()
        
        print("Création des nouvelles tables...")
        db.create_all()
        
        print("\nCréation des rôles...")
        # Créer les rôles
        admin_role = Role(name='admin', description='Administrateur avec tous les droits')
        user_role = Role(name='user', description='Utilisateur standard')
        moderator_role = Role(name='moderator', description='Modérateur')
        
        db.session.add_all([admin_role, user_role, moderator_role])
        db.session.commit()
        print("✓ Rôles créés: admin, user, moderator")
        
        print("\nCréation des utilisateurs...")
        # Créer l'administrateur
        admin = User(
            username='admin',
            email='admin@example.com',
            active=True
        )
        admin.set_password('admin123')
        admin.roles.append(admin_role)
        
        # Créer un utilisateur standard
        user = User(
            username='user',
            email='user@example.com',
            active=True
        )
        user.set_password('user123')
        user.roles.append(user_role)
        
        # Créer un modérateur
        moderator = User(
            username='moderator',
            email='moderator@example.com',
            active=True
        )
        moderator.set_password('mod123')
        moderator.roles.append(moderator_role)
        
        db.session.add_all([admin, user, moderator])
        db.session.commit()
        print("✓ Utilisateurs créés:")
        print("  - admin/admin123 (Administrateur)")
        print("  - user/user123 (Utilisateur)")
        print("  - moderator/mod123 (Modérateur)")
        
        print("\nCréation des produits...")
        # Créer des produits
        products = [
            Product(
                name='Laptop Dell XPS 15',
                description='Ordinateur portable professionnel haute performance avec processeur Intel Core i7',
                price=1299.99,
                stock=15,
                category='Informatique',
                image_url='https://via.placeholder.com/300x200?text=Laptop+Dell',
                user_id=admin.id
            ),
            Product(
                name='iPhone 15 Pro',
                description='Smartphone Apple dernière génération avec puce A17 Pro',
                price=1199.99,
                stock=25,
                category='Téléphonie',
                image_url='https://via.placeholder.com/300x200?text=iPhone+15',
                user_id=admin.id
            ),
            Product(
                name='Sony WH-1000XM5',
                description='Casque audio sans fil avec réduction de bruit active',
                price=349.99,
                stock=30,
                category='Audio',
                image_url='https://via.placeholder.com/300x200?text=Sony+Headphones',
                user_id=user.id
            ),
            Product(
                name='Samsung Galaxy Tab S9',
                description='Tablette Android premium avec écran AMOLED 11 pouces',
                price=799.99,
                stock=20,
                category='Tablettes',
                image_url='https://via.placeholder.com/300x200?text=Galaxy+Tab',
                user_id=moderator.id
            ),
            Product(
                name='Logitech MX Master 3S',
                description='Souris sans fil ergonomique pour professionnels',
                price=99.99,
                stock=50,
                category='Accessoires',
                image_url='https://via.placeholder.com/300x200?text=Logitech+Mouse',
                user_id=admin.id
            )
        ]
        
        db.session.add_all(products)
        db.session.commit()
        print(f"✓ {len(products)} produits créés")
        
        print("\nCréation des logs d'activité...")
        # Créer des logs d'activité
        logs = [
            ActivityLog(
                user_id=admin.id,
                action='create_product',
                description=f'Création du produit: {products[0].name}',
                ip_address='127.0.0.1'
            ),
            ActivityLog(
                user_id=admin.id,
                action='create_product',
                description=f'Création du produit: {products[1].name}',
                ip_address='127.0.0.1'
            ),
            ActivityLog(
                user_id=user.id,
                action='login',
                description='Connexion réussie',
                ip_address='127.0.0.1'
            ),
            ActivityLog(
                user_id=admin.id,
                action='login',
                description='Connexion administrateur',
                ip_address='127.0.0.1'
            )
        ]
        
        db.session.add_all(logs)
        db.session.commit()
        print(f"✓ {len(logs)} logs d'activité créés")
        
        print("\n" + "="*60)
        print("✓ Base de données MySQL initialisée avec succès!")
        print("="*60)
        print("\nStatistiques:")
        print(f"  - Rôles: {Role.query.count()}")
        print(f"  - Utilisateurs: {User.query.count()}")
        print(f"  - Produits: {Product.query.count()}")
        print(f"  - Logs: {ActivityLog.query.count()}")
        print("\nConnectez-vous avec:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nBase de données: test (MySQL)")
        print("Host: localhost:3306")

if __name__ == '__main__':
    init_database()
