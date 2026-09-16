"""CHAT ROUTES - AI chat functionality"""

from flask import Blueprint, render_template, request, jsonify, session
from models.models import db, Conversation, Message, User
from services.ai_service import AIService
from utils.decorators import login_required
import logging

logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('/')
@login_required
def chat():
    """Chat page"""
    user_id = session.get('user_id')
    conversations = Conversation.query.filter_by(user_id=user_id).order_by(Conversation.updated_at.desc()).all()
    return render_template('chat.html', conversations=conversations)

@chat_bp.route('/new', methods=['POST'])
@login_required
def new_conversation():
    """Create new conversation"""
    user_id = session.get('user_id')
    
    conversation = Conversation(user_id=user_id, title='New Chat')
    db.session.add(conversation)
    db.session.commit()
    
    return jsonify({'success': True, 'conversation_id': conversation.id})

@chat_bp.route('/send-message', methods=['POST'])
@login_required
def send_message():
    """Send message and get AI response"""
    user_id = session.get('user_id')
    data = request.get_json()
    
    conversation_id = data.get('conversation_id')
    message_text = data.get('message', '').strip()
    
    if not message_text:
        return jsonify({'error': 'Empty message'}), 400
    
    if not conversation_id:
        return jsonify({'error': 'No conversation selected'}), 400
    
    # Verify conversation belongs to user
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=user_id).first()
    if not conversation:
        return jsonify({'error': 'Conversation not found'}), 403
    
    try:
        # Save user message
        user_msg = Message(conversation_id=conversation_id, sender='user', content=message_text)
        db.session.add(user_msg)
        db.session.commit()
        
        # Get AI response
        ai_response = AIService.answer_question(message_text)
        
        # Save AI message
        ai_msg = Message(conversation_id=conversation_id, sender='assistant', content=ai_response)
        db.session.add(ai_msg)
        conversation.updated_at = db.func.now()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'user_message': message_text,
            'ai_message': ai_response,
            'user_msg_id': user_msg.id,
            'ai_msg_id': ai_msg.id
        })
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/history/<int:conversation_id>')
@login_required
def get_history(conversation_id):
    """Get conversation history"""
    user_id = session.get('user_id')
    
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=user_id).first()
    if not conversation:
        return jsonify({'error': 'Not found'}), 404
    
    messages = Message.query.filter_by(conversation_id=conversation_id).all()
    
    messages_data = [{
        'id': msg.id,
        'sender': msg.sender,
        'content': msg.content,
        'created_at': msg.created_at.isoformat()
    } for msg in messages]
    
    return jsonify({
        'conversation_id': conversation.id,
        'title': conversation.title,
        'messages': messages_data
    })

@chat_bp.route('/delete/<int:conversation_id>', methods=['DELETE'])
@login_required
def delete_conversation(conversation_id):
    """Delete conversation"""
    user_id = session.get('user_id')
    
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=user_id).first()
    if not conversation:
        return jsonify({'error': 'Not found'}), 404
    
    try:
        db.session.delete(conversation)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Delete error: {str(e)}")
        return jsonify({'error': str(e)}), 500
