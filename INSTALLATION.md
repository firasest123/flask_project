# Guide d'installation et d'utilisation - Application Flask

## Installation automatique (Recommandé)

### Méthode 1 : Avec le script PowerShell
```powershell
# Exécuter le script d'installation
.\setup.ps1
```

Le script va :
1. Créer l'environnement virtuel
2. Installer toutes les dépendances
3. Initialiser la base de données
4. Créer un compte administrateur
5. Proposer de créer des données d'exemple
6. Lancer l'application

## Installation manuelle

### Étape 1 : Environnement virtuel
```powershell
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1
```

### Étape 2 : Installer les dépendances
```powershell
pip install -r requirements.txt
```

### Étape 3 : Configurer l'environnement
```powershell
# Le fichier .env contient déjà la configuration de base
# Vous pouvez modifier les valeurs si nécessaire
```

### Étape 4 : Initialiser la base de données
```powershell
$env:FLASK_APP = "app.py"
flask init-db
```

### Étape 5 : Créer l'administrateur
```powershell
flask create-admin
```

Credentials créés :
- Username: `admin`
- Password: `admin123`

### Étape 6 : (Optionnel) Créer des données d'exemple
```powershell
flask create-sample-data
```

### Étape 7 : Lancer l'application
```powershell
python app.py
```

## Accès à l'application

- **Site principal** : http://localhost:5000
- **Interface admin** : http://localhost:5000/admin
- **API REST** : http://localhost:5000/api/*

## Comptes de test

### Administrateur
- Username: `admin`
- Password: `admin123`
- Rôle: admin
- Accès: Complet (site + admin + API)

## Fonctionnalités à tester

### 1. API REST
```powershell
# Test de l'API
curl http://localhost:5000/api/ping

# Liste des produits
curl http://localhost:5000/api/products

# Produit spécifique
curl http://localhost:5000/api/products/1

# Statistiques
curl http://localhost:5000/api/stats/dashboard
```

### 2. Authentification
1. Aller sur http://localhost:5000/auth/register
2. Créer un compte utilisateur
3. Se connecter avec les identifiants
4. Tester la déconnexion

### 3. Gestion des produits
1. Se connecter
2. Aller sur "Produits"
3. Créer un nouveau produit
4. Modifier un produit
5. Supprimer un produit
6. Tester les filtres et la recherche

### 4. Upload de fichiers
1. Aller sur "Upload"
2. Glisser-déposer un fichier
3. Voir la liste des fichiers
4. Télécharger un fichier
5. Supprimer un fichier

### 5. Dashboard
1. Accéder au Dashboard
2. Observer les statistiques en temps réel
3. Consulter les graphiques
4. Voir les activités récentes

### 6. Interface Admin (admin uniquement)
1. Se connecter en tant qu'admin
2. Aller sur http://localhost:5000/admin
3. Explorer les différentes sections :
   - Utilisateurs
   - Produits
   - Fichiers
   - Rôles
   - Logs d'activité

## Résolution de problèmes

### Erreur : "Module not found"
```powershell
# Réactiver l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Erreur : "Database not found"
```powershell
# Réinitialiser la base de données
flask init-db
flask create-admin
```

### Erreur : "Port already in use"
```powershell
# Changer le port dans app.py (ligne avec app.run())
# Ou tuer le processus qui utilise le port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### L'environnement virtuel ne s'active pas
```powershell
# Autoriser l'exécution de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Commandes utiles

```powershell
# Lancer l'application
python app.py

# Lancer en mode debug
$env:FLASK_DEBUG = "1"
python app.py

# Accéder au shell Flask
flask shell

# Voir les routes disponibles
flask routes

# Créer un nouvel utilisateur (depuis le shell Flask)
flask shell
>>> from models import db, User, Role
>>> user = User(username='test', email='test@example.com')
>>> user.set_password('password')
>>> user.roles.append(Role.query.filter_by(name='user').first())
>>> db.session.add(user)
>>> db.session.commit()
```

## Structure de la base de données

Tables créées :
- `user` - Utilisateurs
- `role` - Rôles
- `user_roles` - Association users-roles
- `product` - Produits
- `file_upload` - Fichiers uploadés
- `activity_log` - Logs d'activité

## Tests de sécurité à vérifier

1. ✅ CSRF Protection sur tous les formulaires
2. ✅ Authentification requise pour les routes protégées
3. ✅ Vérification des permissions (utilisateur vs admin)
4. ✅ Mots de passe hashés
5. ✅ Sessions sécurisées
6. ✅ Headers de sécurité HTTP
7. ✅ Validation des uploads
8. ✅ Protection XSS dans les templates
9. ✅ Logs de toutes les actions sensibles

## Points d'évaluation couverts

✅ **API REST complète**
- GET, POST, PUT, DELETE
- Filtres et paramètres
- Authentification sur certains endpoints
- Format JSON

✅ **Fichiers statiques**
- CSS modulaire
- JavaScript interactif
- Serveur correctement

✅ **Templates Jinja2**
- Héritage de templates
- Filtres personnalisés
- Contexte dynamique

✅ **Redirections**
- Pattern POST/Redirect/GET
- Messages flash
- URLs "next"

✅ **Upload de fichiers**
- Validation du type
- Limitation de taille
- Stockage sécurisé
- Drag & drop

✅ **Sécurité HTTP**
- Flask-Talisman
- CSRF tokens
- Sessions HTTPOnly
- Content Security Policy

✅ **Authentification**
- Flask-Login
- Hash des mots de passe
- Remember me
- Protection des routes

✅ **Gestion des rôles**
- Plusieurs rôles
- Décorateurs personnalisés
- Vérification des permissions

✅ **Flask-Admin**
- Interface complète
- Protection par rôle
- CRUD sur toutes les entités

✅ **Dashboard**
- Statistiques en temps réel
- Graphiques Chart.js
- Activités récentes
- Design ergonomique

## Pour aller plus loin

- Ajouter des tests unitaires (pytest)
- Implémenter l'envoi d'emails
- Ajouter la récupération de mot de passe
- Implémenter OAuth2
- Ajouter la recherche full-text
- Créer une API GraphQL
- Ajouter WebSockets pour le temps réel
- Dockeriser l'application

---

Bon courage pour votre examen ! 🚀
