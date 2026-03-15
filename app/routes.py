from flask import Blueprint, request, jsonify
from app.vector_db_manager import VectorDBManager
from app.pdf_handler import PDFHandler
from app.ai_assistant import AIAssistant
from config.settings import AIAssistantConfig

# Create blueprints
main_bp = Blueprint('main', __name__)
assistant_bp = Blueprint('assistant', __name__, url_prefix='/api/assistant')
pdf_bp = Blueprint('pdf', __name__, url_prefix='/api/pdf')

# Initialize components
vector_db = VectorDBManager()
pdf_handler = PDFHandler()
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

@pdf_bp.route('/upload', methods=['POST'])
def upload_pdf():
    """Upload and index a PDF document"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and pdf_handler.allowed_file(file.filename):
        try:
            # Save file
            filepath = pdf_handler.save_file(file)

            # Extract text
            text_content = pdf_handler.extract_text(filepath)

            # Index in vector DB
            doc_id = vector_db.add_document(
                filename=file.filename,
                content=text_content
            )

            return jsonify({
                'status': 'success',
                'message': 'PDF uploaded and indexed successfully',
                'document_id': doc_id,
                'filename': file.filename
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400

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
