# Application Flask - Projet Mini-Examen

## 📋 Description

Application web complète développée avec le Framework Flask intégrant toutes les fonctionnalités avancées demandées pour l'examen :

- ✅ **API REST** complète pour accéder aux données
- ✅ **Fichiers statiques** (CSS, JavaScript, images)
- ✅ **Templates Jinja2** avec héritage et rendu dynamique
- ✅ **Redirections** gérées avec Flask
- ✅ **Upload de fichiers** avec validation
- ✅ **Sécurité HTTP** (Flask-Talisman, CSRF, sessions sécurisées)
- ✅ **Authentification** avec Flask-Login
- ✅ **Gestion des rôles** (Admin, User, Moderator)
- ✅ **Interface d'administration** avec Flask-Admin
- ✅ **Dashboard ergonomique** avec statistiques en temps réel

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Étapes d'installation

1. **Cloner ou extraire le projet**
```powershell
cd "c:\Users\FE48V\Desktop\flask _project"
```

2. **Créer un environnement virtuel (recommandé)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Installer les dépendances**
```powershell
pip install -r requirements.txt
```

4. **Initialiser la base de données**
```powershell
flask init-db
```

5. **Créer un compte administrateur**
```powershell
flask create-admin
```
Credentials par défaut:
- Username: `admin`
- Password: `admin123` (⚠️ À changer en production!)

6. **(Optionnel) Créer des données d'exemple**
```powershell
flask create-sample-data
```

## 🏃 Lancement de l'application

```powershell
python app.py
```

L'application sera accessible sur : **http://localhost:5000**

## 📁 Structure du projet

```
flask_project/
├── app.py                  # Point d'entrée principal
├── config.py              # Configuration (dev, prod, test)
├── models.py              # Modèles SQLAlchemy
├── forms.py               # Formulaires WTForms
├── api.py                 # Routes API REST
├── routes_auth.py         # Routes d'authentification
├── routes_main.py         # Routes principales
├── admin.py               # Configuration Flask-Admin
├── requirements.txt       # Dépendances
├── .env                   # Variables d'environnement
├── static/
│   ├── css/
│   │   └── style.css      # Styles personnalisés
│   └── js/
│       └── script.js      # JavaScript interactif
├── templates/
│   ├── base.html          # Template de base
│   ├── index.html         # Page d'accueil
│   ├── dashboard.html     # Dashboard
│   ├── auth/              # Templates authentification
│   ├── products/          # Templates produits
│   ├── admin/             # Templates Flask-Admin
│   └── errors/            # Pages d'erreur
└── uploads/               # Dossier des fichiers uploadés
```

## 🔐 Sécurité implémentée

### 1. Protection CSRF
- Tous les formulaires sont protégés avec Flask-WTF
- Tokens CSRF automatiques

### 2. Sécurité HTTP (Flask-Talisman)
- Headers de sécurité HTTP
- Content Security Policy (CSP)
- HTTPS forcé en production
- Protection XSS et clickjacking

### 3. Sessions sécurisées
- Cookies HTTPOnly
- Cookies Secure (en production)
- SameSite protection

### 4. Authentification
- Mots de passe hashés avec Werkzeug
- Flask-Login pour la gestion des sessions
- Protection des routes avec `@login_required`

### 5. Contrôle d'accès basé sur les rôles
- Décorateurs personnalisés (`@admin_required`)
- Vérification des permissions à chaque action
- Logs de toutes les activités

## 🌐 API REST Endpoints

### Produits
- `GET /api/products` - Liste tous les produits
- `GET /api/products/<id>` - Récupère un produit
- `POST /api/products` - Crée un produit (auth requise)
- `PUT /api/products/<id>` - Met à jour un produit
- `DELETE /api/products/<id>` - Supprime un produit

### Utilisateurs
- `GET /api/users` - Liste des utilisateurs (admin)
- `GET /api/users/<id>` - Récupère un utilisateur

### Uploads
- `GET /api/uploads` - Liste des fichiers uploadés

### Statistiques
- `GET /api/stats/dashboard` - Statistiques du dashboard

### Test
- `GET /api/ping` - Test de l'API

**Exemples d'utilisation:**

```bash
# Récupérer tous les produits
curl http://localhost:5000/api/products

# Filtrer par catégorie
curl http://localhost:5000/api/products?category=Électronique

# Récupérer un produit spécifique
curl http://localhost:5000/api/products/1
```

## 👥 Système de rôles

### Rôles disponibles
- **admin** : Accès complet (interface admin, toutes les opérations)
- **user** : Accès standard (CRUD sur ses propres ressources)
- **moderator** : Permissions intermédiaires

### Permissions
- Les utilisateurs ne peuvent modifier/supprimer que leurs propres ressources
- Les admins ont un accès complet à toutes les ressources
- L'interface Flask-Admin est réservée aux administrateurs

## 📤 Upload de fichiers

### Formats acceptés
- Documents : PDF, TXT, DOC, DOCX
- Images : PNG, JPG, JPEG, GIF

### Fonctionnalités
- Taille maximale : 16 MB
- Noms de fichiers sécurisés
- Drag & drop supporté
- Validation côté serveur
- Stockage avec timestamp unique

## 📊 Dashboard

Le dashboard affiche :
- Statistiques en temps réel (utilisateurs, produits, uploads, activités)
- Graphiques des produits par catégorie (Chart.js)
- Activités récentes avec détails
- Actions rapides
- Rafraîchissement automatique (30 secondes)

## 🛠️ Interface d'administration Flask-Admin

Accessible sur : **http://localhost:5000/admin** (admin uniquement)

### Fonctionnalités
- **Utilisateurs** : CRUD complet, gestion des rôles
- **Produits** : Gestion complète
- **Fichiers** : Visualisation et suppression
- **Rôles** : Création et modification
- **Logs d'activité** : Surveillance (lecture seule)

### Caractéristiques
- Interface Bootstrap 4
- Recherche et filtres avancés
- Pagination automatique
- Export de données
- Actions en masse

## 🎨 Fonctionnalités techniques

### Templates Jinja2
- Héritage de templates (`{% extends %}`)
- Inclusions (`{% include %}`)
- Filtres personnalisés
- Macros réutilisables
- Contexte global

### Fichiers statiques
- CSS modulaire et responsive
- JavaScript avec fetch API
- Animations et transitions
- Design moderne et ergonomique

### Redirections
- Après actions (POST/Redirect/GET pattern)
- Gestion des URLs "next"
- Messages flash catégorisés

## 🧪 Tests et validation

### Commandes disponibles
```powershell
# Initialiser la base de données
flask init-db

# Créer un administrateur
flask create-admin

# Créer des données d'exemple
flask create-sample-data
```

## 📝 Variables d'environnement (.env)

```env
SECRET_KEY=votre_cle_secrete_tres_complexe
DATABASE_URI=sqlite:///app.db
FLASK_ENV=development
FLASK_DEBUG=True
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
```

## 🔄 Modes de déploiement

### Développement
```powershell
$env:FLASK_ENV="development"
python app.py
```

### Production
```powershell
$env:FLASK_ENV="production"
# Utiliser un serveur WSGI comme Gunicorn ou uWSGI
```

## 📚 Technologies utilisées

- **Flask 3.0** - Framework web
- **SQLAlchemy** - ORM
- **Flask-Login** - Gestion des sessions
- **Flask-Admin** - Interface d'administration
- **Flask-WTF** - Formulaires et CSRF
- **Flask-Talisman** - Sécurité HTTP
- **Chart.js** - Graphiques
- **Font Awesome** - Icônes

## 🎯 Critères d'évaluation satisfaits

✅ **API REST** : Endpoints complets avec CRUD
✅ **Fichiers statiques** : CSS et JavaScript servis
✅ **Templates Jinja2** : Rendu dynamique avec héritage
✅ **Redirections** : Implémentées partout
✅ **Upload de fichiers** : Gestion complète et sécurisée
✅ **Sécurité HTTP** : Flask-Talisman + CSRF + sessions
✅ **Plusieurs modes de sécurisation** : CSRF, rôles, permissions, logs
✅ **Flask-Login** : Authentification complète
✅ **Gestion des rôles** : Admin, User, Moderator
✅ **Flask-Admin** : Interface d'administration fonctionnelle
✅ **Dashboard ergonomique** : Statistiques et graphiques en temps réel


