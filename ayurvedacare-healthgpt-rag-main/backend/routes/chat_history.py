from flask import Blueprint, request, jsonify
from database.chat_history import ChatHistoryDB
import traceback
from datetime import datetime

chat_history_bp = Blueprint('chat_history', __name__)

@chat_history_bp.route('/conversations', methods=['GET'])
def get_conversations():
    """Get all conversations for a user session"""
    try:
        session_id = request.args.get('session_id')
        
        if not session_id:
            return jsonify({
                'error': 'Session ID is required',
                'code': 'MISSING_SESSION_ID'
            }), 400
        
        chat_db = ChatHistoryDB()
        conversations = chat_db.get_user_conversations(session_id)
        
        return jsonify({
            'conversations': conversations,
            'count': len(conversations)
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to get conversations',
            'code': 'GET_CONVERSATIONS_ERROR',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

@chat_history_bp.route('/conversations', methods=['POST'])
def create_conversation():
    """Create a new conversation"""
    try:
        data = request.get_json()
        
        if not data or 'session_id' not in data:
            return jsonify({
                'error': 'Session ID is required',
                'code': 'MISSING_SESSION_ID'
            }), 400
        
        session_id = data['session_id']
        title = data.get('title')
        metadata = data.get('metadata', {})
        
        chat_db = ChatHistoryDB()
        conversation_id = chat_db.create_conversation(session_id, title, metadata)
        
        return jsonify({
            'conversation_id': conversation_id,
            'message': 'Conversation created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to create conversation',
            'code': 'CREATE_CONVERSATION_ERROR',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

@chat_history_bp.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
def get_conversation_messages(conversation_id):
    """Get all messages for a conversation"""
    try:
        chat_db = ChatHistoryDB()
        messages = chat_db.get_conversation_messages(conversation_id)
        
        return jsonify({
            'messages': messages,
            'conversation_id': conversation_id,
            'message_count': len(messages)
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to get conversation messages',
            'code': 'GET_MESSAGES_ERROR',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

@chat_history_bp.route('/conversations/<int:conversation_id>/messages', methods=['POST'])
def add_message():
    """Add a message to a conversation"""
    try:
        data = request.get_json()
        
        if not data or 'conversation_id' not in data or 'role' not in data or 'content' not in data:
            return jsonify({
                'error': 'Conversation ID, role, and content are required',
                'code': 'MISSING_REQUIRED_FIELDS'
            }), 400
        
        conversation_id = data['conversation_id']
        role = data['role']
        content = data['content']
        metadata = data.get('metadata', {})
        
        # Validate role
        if role not in ['user', 'assistant']:
            return jsonify({
                'error': 'Role must be either "user" or "assistant"',
                'code': 'INVALID_ROLE'
            }), 400
        
        chat_db = ChatHistoryDB()
        message_id = chat_db.add_message(conversation_id, role, content, metadata)
        
        # Generate title if this is the first user message and conversation has no title
        title = chat_db.get_conversation_title(conversation_id)
        if not title and role == 'user':
            chat_db.generate_conversation_title(conversation_id)
        
        return jsonify({
            'message_id': message_id,
            'conversation_id': conversation_id,
            'message': 'Message added successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to add message',
            'code': 'ADD_MESSAGE_ERROR',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

@chat_history_bp.route('/conversations/<int:conversation_id>', methods=['PUT'])
def update_conversation(conversation_id):
    """Update conversation title"""
    try:
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({
                'error': 'Title is required',
                'code': 'MISSING_TITLE'
            }), 400
        
        title = data['title']
        
        chat_db = ChatHistoryDB()
        success = chat_db.update_conversation_title(conversation_id, title)
        
        if not success:
            return jsonify({
                'error': 'Conversation not found',
                'code': 'CONVERSATION_NOT_FOUND'
            }), 404
        
        return jsonify({
            'message': 'Conversation updated successfully',
            'conversation_id': conversation_id
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to update conversation',
            'code': 'UPDATE_CONVERSATION_ERROR',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

@chat_history_bp.route('/conversations/<int:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """Delete a conversation and all its messages"""
    try:
        chat_db = ChatHistoryDB()
        success = chat_db.delete_conversation(conversation_id)
        
        if not success:
            return jsonify({
                'error': 'Conversation not found',
                'code': 'CONVERSATION_NOT_FOUND'
            }), 404
        
        return jsonify({
            'message': 'Conversation deleted successfully',
            'conversation_id': conversation_id
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to delete conversation',
            'code': 'DELETE_CONVERSATION_ERROR',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

@chat_history_bp.route('/conversations/<int:conversation_id>/title', methods=['POST'])
def generate_title(conversation_id):
    """Generate a title for the conversation based on first user message"""
    try:
        chat_db = ChatHistoryDB()
        title = chat_db.generate_conversation_title(conversation_id)
        
        return jsonify({
            'title': title,
            'conversation_id': conversation_id
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to generate title',
            'code': 'GENERATE_TITLE_ERROR',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500
