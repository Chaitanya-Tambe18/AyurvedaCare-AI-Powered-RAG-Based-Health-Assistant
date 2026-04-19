from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import traceback
import warnings

# Disable all telemetry and warnings before importing other modules
os.environ['ANONYMIZED_TELEMETRY'] = 'False'
os.environ['CHROMA_TELEMETRY'] = 'False'
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

from database.vector_store import VectorStore
from llm.groq_client import GroqClient
from routes.chat import chat_bp
from routes.chat_history import chat_history_bp

load_dotenv()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Ensure Unicode characters are properly encoded
CORS(app)

app.register_blueprint(chat_bp, url_prefix='/api')
app.register_blueprint(chat_history_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({
        "message": "HealthGPT API is running!",
        "version": "2.0",
        "status": "operational"
    })

@app.route('/health')
def health_check():
    try:
        vector_store = VectorStore()
        doc_count = vector_store.get_collection_count()
        return jsonify({
            "status": "healthy",
            "documents_count": doc_count,
            "services": {
                "vector_store": "operational",
                "embeddings": "operational",
                "llm": "operational"
            }
        })
    except Exception as e:
        return jsonify({
            "status": "degraded",
            "error": str(e)
        }), 503

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "code": "NOT_FOUND"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "code": "INTERNAL_ERROR"
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
