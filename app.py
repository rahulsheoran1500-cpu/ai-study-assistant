"""MAIN FLASK APPLICATION - Entry point for AI Study Assistant"""

import os
from flask import Flask, render_template, session, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # 25MB
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('database', exist_ok=True)
os.makedirs('flask_session', exist_ok=True)

# Initialize extensions
from models.models import db
db.init_app(app)
Session(app)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Context processor
@app.context_processor
def inject_user():
    """Make current user available in templates"""
    user_id = session.get('user_id')
    if user_id:
        from models.models import User
        user = User.query.get(user_id)
        return {'current_user': user}
    return {'current_user': None}

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return jsonify({'error': 'Server error'}), 500

# Main routes
@app.route('/')
def index():
    """Landing page"""
    if session.get('user_id'):
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Student dashboard"""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    from models.models import User, Conversation, Note, Quiz, Flashcard
    
    user = User.query.get(user_id)
    conversations = Conversation.query.filter_by(user_id=user_id).order_by(Conversation.updated_at.desc()).limit(5).all()
    notes = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).limit(5).all()
    quizzes = Quiz.query.filter_by(user_id=user_id).order_by(Quiz.created_at.desc()).limit(5).all()
    flashcards = Flashcard.query.filter_by(user_id=user_id).limit(10).all()
    
    stats = {
        'total_chats': Conversation.query.filter_by(user_id=user_id).count(),
        'total_notes': Note.query.filter_by(user_id=user_id).count(),
        'total_quizzes': Quiz.query.filter_by(user_id=user_id).count(),
        'total_flashcards': Flashcard.query.filter_by(user_id=user_id).count(),
    }
    
    return render_template('dashboard.html', user=user, conversations=conversations, notes=notes, quizzes=quizzes, flashcards=flashcards, stats=stats)

def register_blueprints():
    """Register all route blueprints"""
    from routes.auth import auth_bp
    from routes.chat import chat_bp
    from routes.notes import notes_bp
    from routes.pdf_summarizer import pdf_bp
    from routes.quiz import quiz_bp
    from routes.flashcards import flashcards_bp
    from routes.study_plan import study_plan_bp
    from routes.history import history_bp
    from routes.profile import profile_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(pdf_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(flashcards_bp)
    app.register_blueprint(study_plan_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(profile_bp)

if __name__ == '__main__':
    register_blueprints()
    
    with app.app_context():
        db.create_all()
        logger.info("✅ Database ready")
    
    port = int(os.getenv('FLASK_PORT', 5000))
    logger.info(f"🚀 Starting AI Study Assistant on http://localhost:{port}")
    app.run(debug=True, port=port)
