"""
Routes d'authentification
Gestion de l'inscription, connexion, déconnexion et profil utilisateur
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Role, ActivityLog
from forms import LoginForm, RegisterForm
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Inscription d'un nouvel utilisateur"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Créer le nouvel utilisateur
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        
        # Assigner le rôle "user" par défaut
        user_role = Role.query.filter_by(name='user').first()
        if user_role:
            user.roles.append(user_role)
        
        db.session.add(user)
        db.session.commit()
        
        # Log de l'activité
        log = ActivityLog(
            user_id=user.id,
            action='register',
            description=f'Nouvel utilisateur enregistré: {user.username}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Connexion d'un utilisateur"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.active:
                flash('Votre compte a été désactivé. Contactez l\'administrateur.', 'danger')
                return redirect(url_for('auth.login'))
            
            # Connexion de l'utilisateur
            login_user(user, remember=form.remember.data)
            
            # Mise à jour de la date de dernière connexion
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Log de l'activité
            log = ActivityLog(
                user_id=user.id,
                action='login',
                description=f'Connexion de {user.username}',
                ip_address=request.remote_addr
            )
            db.session.add(log)
            db.session.commit()
            
            # Redirection vers la page demandée ou dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            flash(f'Bienvenue {user.username} !', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Déconnexion de l'utilisateur"""
    # Log de l'activité
    log = ActivityLog(
        user_id=current_user.id,
        action='logout',
        description=f'Déconnexion de {current_user.username}',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    logout_user()
    flash('Vous avez été déconnecté avec succès.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
@login_required
def profile():
    """Page de profil de l'utilisateur"""
    return render_template('auth/profile.html', user=current_user)
