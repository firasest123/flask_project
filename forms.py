"""
Formulaires de l'application avec Flask-WTF
Validation côté serveur avec WTForms
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, TextAreaField, FloatField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from models import User

class LoginForm(FlaskForm):
    """Formulaire de connexion"""
    username = StringField('Nom d\'utilisateur', 
                          validators=[DataRequired(message='Le nom d\'utilisateur est requis')])
    password = PasswordField('Mot de passe', 
                            validators=[DataRequired(message='Le mot de passe est requis')])
    remember = BooleanField('Se souvenir de moi')

class RegisterForm(FlaskForm):
    """Formulaire d'inscription"""
    username = StringField('Nom d\'utilisateur', 
                          validators=[
                              DataRequired(message='Le nom d\'utilisateur est requis'),
                              Length(min=3, max=80, message='Le nom doit contenir entre 3 et 80 caractères')
                          ])
    email = StringField('Email', 
                       validators=[
                           DataRequired(message='L\'email est requis'),
                           Email(message='Email invalide')
                       ])
    first_name = StringField('Prénom', 
                            validators=[Length(max=50)])
    last_name = StringField('Nom', 
                           validators=[Length(max=50)])
    password = PasswordField('Mot de passe', 
                            validators=[
                                DataRequired(message='Le mot de passe est requis'),
                                Length(min=6, message='Le mot de passe doit contenir au moins 6 caractères')
                            ])
    confirm_password = PasswordField('Confirmer le mot de passe', 
                                    validators=[
                                        DataRequired(message='Veuillez confirmer le mot de passe'),
                                        EqualTo('password', message='Les mots de passe ne correspondent pas')
                                    ])
    
    def validate_username(self, username):
        """Vérifie que le nom d'utilisateur n'existe pas déjà"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris. Veuillez en choisir un autre.')
    
    def validate_email(self, email):
        """Vérifie que l'email n'est pas déjà utilisé"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà enregistré. Veuillez en utiliser un autre.')

class ProductForm(FlaskForm):
    """Formulaire pour créer/modifier un produit"""
    name = StringField('Nom du produit', 
                      validators=[
                          DataRequired(message='Le nom du produit est requis'),
                          Length(max=100, message='Le nom ne peut pas dépasser 100 caractères')
                      ])
    description = TextAreaField('Description', 
                               validators=[Optional()])
    price = FloatField('Prix', 
                      validators=[DataRequired(message='Le prix est requis')])
    stock = IntegerField('Stock', 
                        validators=[Optional()],
                        default=0)
    category = StringField('Catégorie', 
                          validators=[Length(max=50)])
    image_url = StringField('URL de l\'image', 
                           validators=[Length(max=200)])

class FileUploadForm(FlaskForm):
    """Formulaire d'upload de fichiers"""
    file = FileField('Fichier', 
                    validators=[
                        FileRequired(message='Veuillez sélectionner un fichier'),
                        FileAllowed(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'], 
                                   message='Format de fichier non autorisé')
                    ])
