from flask import Flask
from flask_cors import CORS
from config.settings import Config, PDFConfig
import os

def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Create upload folder if not exists
    os.makedirs(PDFConfig.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs('./vector_db', exist_ok=True)
    
    # Register blueprints
    from app.routes import main_bp, assistant_bp, pdf_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(assistant_bp)
    app.register_blueprint(pdf_bp)
    
    return app
