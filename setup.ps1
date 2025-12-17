# Script d'installation et de lancement de l'application Flask
# Exécutez ce script dans PowerShell

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Installation de l'application Flask" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Créer l'environnement virtuel
Write-Host "[1/6] Création de l'environnement virtuel..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  -> Environnement virtuel déjà existant" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "  -> Environnement virtuel créé avec succès" -ForegroundColor Green
}

# 2. Activer l'environnement virtuel
Write-Host "`n[2/6] Activation de l'environnement virtuel..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "  -> Environnement virtuel activé" -ForegroundColor Green

# 3. Installer les dépendances
Write-Host "`n[3/6] Installation des dépendances..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "  -> Dépendances installées avec succès" -ForegroundColor Green

# 4. Initialiser la base de données
Write-Host "`n[4/6] Initialisation de la base de données..." -ForegroundColor Yellow
$env:FLASK_APP = "app.py"
flask init-db
Write-Host "  -> Base de données initialisée" -ForegroundColor Green

# 5. Créer l'administrateur
Write-Host "`n[5/6] Création du compte administrateur..." -ForegroundColor Yellow
flask create-admin
Write-Host "  -> Administrateur créé" -ForegroundColor Green

# 6. Créer des données d'exemple
Write-Host "`n[6/6] Création de données d'exemple..." -ForegroundColor Yellow
$response = Read-Host "Voulez-vous créer des données d'exemple? (O/N)"
if ($response -eq "O" -or $response -eq "o") {
    flask create-sample-data
    Write-Host "  -> Données d'exemple créées" -ForegroundColor Green
} else {
    Write-Host "  -> Étape ignorée" -ForegroundColor Yellow
}

# Afficher les informations de connexion
Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "  Installation terminée avec succès!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Informations de connexion administrateur:" -ForegroundColor Yellow
Write-Host "  Username: admin" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "Pour lancer l'application:" -ForegroundColor Yellow
Write-Host "  python app.py" -ForegroundColor White
Write-Host ""
Write-Host "L'application sera accessible sur:" -ForegroundColor Yellow
Write-Host "  http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "Interface d'administration:" -ForegroundColor Yellow
Write-Host "  http://localhost:5000/admin" -ForegroundColor White
Write-Host ""

# Proposer de lancer l'application
$launch = Read-Host "Voulez-vous lancer l'application maintenant? (O/N)"
if ($launch -eq "O" -or $launch -eq "o") {
    Write-Host "`nLancement de l'application..." -ForegroundColor Green
    python app.py
}
