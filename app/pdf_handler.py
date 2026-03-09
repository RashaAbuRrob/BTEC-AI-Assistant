import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from config.settings import PDFConfig

class PDFHandler:
    """Handle PDF file operations"""
    
    def __init__(self):
        self.upload_folder = PDFConfig.UPLOAD_FOLDER
        self.allowed_extensions = PDFConfig.ALLOWED_EXTENSIONS
        self.max_size = PDFConfig.MAX_CONTENT_LENGTH
        
    def allowed_file(self, filename):
        """Check if file is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def save_file(self, file):
        """Save uploaded file"""
        os.makedirs(self.upload_folder, exist_ok=True)
        filename = secure_filename(file.filename)
        filepath = os.path.join(self.upload_folder, filename)
        file.save(filepath)
        return filepath
    
    def extract_text(self, filepath):
        """Extract text from PDF"""
        text = ""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error extracting PDF text: {str(e)}")
    
    def delete_file(self, filename):
        """Delete uploaded file"""
        filepath = os.path.join(self.upload_folder, secure_filename(filename))
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
