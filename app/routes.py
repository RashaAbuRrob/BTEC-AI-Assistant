from flask import Blueprint, request, jsonify
from app.vector_db_manager import VectorDBManager
from app.ai_assistant import AIAssistant
from config.settings import AIAssistantConfig

# Create blueprints
main_bp = Blueprint('main', __name__)
assistant_bp = Blueprint('assistant', __name__, url_prefix='/api/assistant')

# Initialize components
vector_db = VectorDBManager()
ai_assistant = AIAssistant()

@main_bp.route('/')
def index():
    """Home page"""
    return jsonify({
        'status': 'success',
        'message': f'Welcome to {AIAssistantConfig.ASSISTANT_NAME}',
        'assistant_name_en': AIAssistantConfig.ASSISTANT_NAME_EN
    })

@assistant_bp.route('/query', methods=['POST'])
def query():
    """Query the AI assistant - answer BTEC questions"""
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({'error': 'Query required'}), 400
    
    user_query = data['query']
    
    try:
        # Retrieve relevant documents from vector DB
        relevant_docs = vector_db.search(user_query, top_k=3)
        
        # Generate response using AI
        response = ai_assistant.generate_response(
            query=user_query,
            context=relevant_docs
        )
        
        return jsonify({
            'status': 'success',
            'query': user_query,
            'response': response,
            'context_sources': relevant_docs
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@assistant_bp.route('/documents', methods=['GET'])
def list_documents():
    """List all indexed documents"""
    try:
        documents = vector_db.list_documents()
        return jsonify({
            'status': 'success',
            'documents': documents,
            'total': len(documents)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
