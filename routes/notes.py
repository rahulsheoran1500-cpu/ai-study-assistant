"""NOTES ROUTES - Notes generator functionality"""

from flask import Blueprint, render_template, request, jsonify, session
from models.models import db, Note, User
from services.ai_service import AIService
from utils.decorators import login_required
import logging

logger = logging.getLogger(__name__)

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')

@notes_bp.route('/')
@login_required
def notes():
    """Notes page"""
    user_id = session.get('user_id')
    user_notes = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).all()
    return render_template('notes.html', notes=user_notes)

@notes_bp.route('/generate', methods=['POST'])
@login_required
def generate():
    """Generate notes"""
    user_id = session.get('user_id')
    data = request.get_json()
    
    topic = data.get('topic', '').strip()
    detail_level = data.get('detail_level', 'medium')
    
    if not topic:
        return jsonify({'error': 'Topic required'}), 400
    
    try:
        content = AIService.generate_notes(topic, detail_level)
        
        # Save to database
        note = Note(user_id=user_id, topic=topic, content=content)
        db.session.add(note)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'note_id': note.id,
            'content': content
        })
    except Exception as e:
        logger.error(f"Notes error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@notes_bp.route('/<int:note_id>')
@login_required
def view_note(note_id):
    """View specific note"""
    user_id = session.get('user_id')
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    
    if not note:
        return jsonify({'error': 'Not found'}), 404
    
    return jsonify({
        'id': note.id,
        'topic': note.topic,
        'content': note.content,
        'created_at': note.created_at.isoformat()
    })

@notes_bp.route('/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    """Delete note"""
    user_id = session.get('user_id')
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    
    if not note:
        return jsonify({'error': 'Not found'}), 404
    
    try:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Delete error: {str(e)}")
        return jsonify({'error': str(e)}), 500
