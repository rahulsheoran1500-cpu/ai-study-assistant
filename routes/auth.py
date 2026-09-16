"""AUTH ROUTES - User registration, login, logout"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.models import db, User
from utils.decorators import login_required, logout_required
from utils.helpers import validate_email
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    """Register new user"""
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not all([email, name, password, confirm_password]):
            flash('❌ All fields required', 'error')
            return render_template('register.html')
        
        if not validate_email(email):
            flash('❌ Invalid email format', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('❌ Passwords do not match', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('❌ Password must be at least 6 characters', 'error')
            return render_template('register.html')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('❌ Email already registered', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(email=email, name=name)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('✅ Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Registration error: {str(e)}")
            flash('❌ Registration failed. Try again.', 'error')
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    """Login user"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('❌ Email and password required', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_name'] = user.name
            flash(f'✅ Welcome, {user.name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('❌ Invalid email or password', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    session.clear()
    flash('✅ You have been logged out', 'success')
    return redirect(url_for('index'))
