from flask import Blueprint, request, jsonify
from database.vector_store import VectorStore
from database.chat_history import ChatHistoryDB
from llm.groq_client import GroqClient
from llm.language_detector import LanguageDetector
from config import Config
import traceback

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Query is required',
                'code': 'MISSING_QUERY'
            }), 400
        
        query = data['query']
        session_id = data.get('session_id', 'default')
        conversation_id = data.get('conversation_id')
        
        if not query or not query.strip():
            return jsonify({
                'error': 'Query cannot be empty',
                'code': 'EMPTY_QUERY'
            }), 400
        
        # Initialize chat history database
        chat_db = ChatHistoryDB()
        
        # Get or create conversation
        if conversation_id:
            # Verify conversation exists for this session
            conversations = chat_db.get_user_conversations(session_id)
            conv_exists = any(conv['id'] == conversation_id for conv in conversations)
            
            if not conv_exists:
                conversation_id = chat_db.create_conversation(session_id)
        else:
            # Create new conversation
            conversation_id = chat_db.create_conversation(session_id)
        
        # Store user message
        chat_db.add_message(conversation_id, 'user', query)
        
        # Detect the language of the query
        detected_language = LanguageDetector.detect_language(query)
        language_name = LanguageDetector.get_language_name(detected_language)
        
        # Process the query with RAG
        vector_store = VectorStore()
        groq_client = GroqClient()
        
        retrieved_docs = vector_store.query(query, n_results=Config.MAX_RETRIEVED_DOCS)
        
        if not retrieved_docs or not retrieved_docs.get('documents') or not retrieved_docs['documents'][0]:
            # Multilingual fallback responses
            fallback_responses = {
                'en': "I don't have enough information to answer that question based on the provided documents.",
                'hi': "मेरे पास दिए गए दस्तावेज़ों के आधार पर उस प्रश्न का उत्तर देने के लिए पर्याप्त जानकारी नहीं है।",
                'mr': "दिलेल्या दस्तऐवजांच्या आधारावर त्या प्रश्नाचे उत्तर देण्यासाठी माझ्याकडे पुरेसी माहिती नाही."
            }
            response = fallback_responses.get(detected_language, fallback_responses['en'])
            sources = []
            fallback = True
        else:
            context_documents = retrieved_docs['documents'][0]
            sources = retrieved_docs['metadatas'][0]
            
            try:
                response = groq_client.get_response_with_context(query, context_documents)
                fallback = False
            except Exception as llm_error:
                response = f"LLM service unavailable: {str(llm_error)}"
                sources = []
                fallback = True
        
        # Store assistant response
        chat_db.add_message(conversation_id, 'assistant', response, {
            'sources': sources,
            'fallback': fallback,
            'model_used': Config.GROQ_MODEL
        })
        
        # Generate title if this is the first exchange
        title = chat_db.get_conversation_title(conversation_id)
        if not title:
            chat_db.generate_conversation_title(conversation_id)
        
        return jsonify({
            'response': response,
            'sources': sources,
            'conversation_id': conversation_id,
            'session_id': session_id,
            'model_used': Config.GROQ_MODEL,
            'fallback': fallback,
            'detected_language': detected_language,
            'language_name': language_name
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

@chat_bp.route('/status', methods=['GET'])
def status():
    try:
        vector_store = VectorStore()
        doc_count = vector_store.get_collection_count()
        
        return jsonify({
            'status': 'healthy',
            'documents_count': doc_count,
            'embedding_model': Config.EMBEDDING_MODEL,
            'llm_model': Config.GROQ_MODEL,
            'fallback_enabled': Config.FALLBACK_TO_OLLAMA,
            'ollama_model': Config.OLLAMA_MODEL
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Status check failed',
            'code': 'STATUS_ERROR',
            'details': str(e)
        }), 500
