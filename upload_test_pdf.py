#!/usr/bin/env python3
"""Script to create a test PDF and upload it to the vector database"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
import json

def create_test_pdf():
    """Create a sample PDF about BTEC"""
    pdf_path = "uploads/BTEC_Guide.pdf"
    
    os.makedirs("uploads", exist_ok=True)
    
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "BTEC Smart Assistant")
    c.drawString(50, height - 80, "مساعد BTEC الذكي")
    
    # Content
    c.setFont("Helvetica", 12)
    y_position = height - 120
    
    content = [
        "",
        "What is BTEC?",
        "BTEC stands for Business and Technology Education Council.",
        "BTEC qualifications are internationally recognized qualifications.",
        "",
        "BTEC Qualifications:",
        "- BTEC Level 1 Introductory",
        "- BTEC Level 2 First",
        "- BTEC Level 3 National",
        "- BTEC Higher National Diploma (HND)",
        "- BTEC Higher National Certificate (HNC)",
        "",
        "Benefits of BTEC:",
        "- Practical, real-world learning experience",
        "- Industry-relevant skills and knowledge",
        "- Work-based learning opportunities",
        "- Recognized by employers worldwide",
        "- Flexible progression pathways",
        "",
        "BTEC Subjects:",
        "- Business and Commerce",
        "- Engineering",
        "- Health and Social Care",
        "- Information Technology",
        "- Hospitality and Tourism",
        "- Art and Design",
        "",
        "Assessment Methods:",
        "- Assignments and projects",
        "- Practical demonstrations",
        "- Written examinations",
        "- Presentations",
        "- Work experience",
    ]
    
    for line in content:
        if y_position < 50:
            c.showPage()
            y_position = height - 50
        c.drawString(50, y_position, line)
        y_position -= 20
    
    c.save()
    print(f"✅ Test PDF created: {pdf_path}")
    return pdf_path

def upload_to_database(pdf_path):
    """Upload PDF to vector database"""
    try:
        from app.pdf_handler import PDFHandler
        from app.vector_db_manager import VectorDBManager
        
        pdf_handler = PDFHandler()
        vector_db = VectorDBManager()
        
        # Extract text
        text_content = pdf_handler.extract_text(pdf_path)
        
        # Add to database
        filename = os.path.basename(pdf_path)
        doc_id = vector_db.add_document(
            filename=filename,
            content=text_content
        )
        
        print(f"✅ PDF uploaded to vector database")
        print(f"   Document ID: {doc_id}")
        print(f"   Filename: {filename}")
        print(f"   Words: {len(text_content.split())}")
        
        return doc_id
    except Exception as e:
        print(f"❌ Error uploading to database: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Creating and uploading test PDF...")
    pdf_path = create_test_pdf()
    upload_to_database(pdf_path)
    print("✅ Done! Your PDF is ready in the database.")
