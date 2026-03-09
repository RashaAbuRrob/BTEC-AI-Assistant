import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    FLASK_PORT = int(os.environ.get('FLASK_PORT', 5000))
    
class VectorDBConfig:
    """Vector Database configuration"""
    DB_PATH = os.environ.get('VECTOR_DB_PATH', './vector_db')
    EMBEDDING_MODEL = 'text-embedding-ada-002'
    
class PDFConfig:
    """PDF Upload configuration"""
    UPLOAD_FOLDER = './uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_PDF_SIZE_MB', 50)) * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf'}
    
class AIAssistantConfig:
    """AI Assistant configuration"""
    ASSISTANT_NAME = "مساعد BTEC الذكي"
    ASSISTANT_NAME_EN = "BTEC Smart Assistant"
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    MODEL = 'gpt-3.5-turbo'
    TEMPERATURE = 0.7
    MAX_TOKENS = 500
