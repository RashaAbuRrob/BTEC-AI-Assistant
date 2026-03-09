#!/usr/bin/env python3
"""Script to upload existing BTEC.pdf to the vector database"""

import os
import sys

def upload_existing_pdf():
    """Upload the existing BTEC.pdf file to vector database"""
    try:
        from app.pdf_handler import PDFHandler
        from app.vector_db_manager import VectorDBManager
        
        pdf_path = "uploads/BTEC.pdf"
        
        # Check if file exists
        if not os.path.exists(pdf_path):
            print(f"❌ Error: {pdf_path} not found!")
            return False
        
        print(f"📄 Found: {pdf_path}")
        
        # Initialize handlers
        pdf_handler = PDFHandler()
        vector_db = VectorDBManager()
        
        # Extract text from PDF
        print("🔍 Extracting text from PDF...")
        text_content = pdf_handler.extract_text(pdf_path)
        
        if not text_content:
            print("❌ Error: Could not extract text from PDF")
            return False
        
        print(f"✅ Extracted {len(text_content)} characters")
        
        # Add to vector database
        print("📦 Adding to vector database...")
        doc_id = vector_db.add_document(
            filename="BTEC.pdf",
            content=text_content
        )
        
        # Display results
        word_count = len(text_content.split())
        print("\n" + "="*50)
        print("✅ PDF Successfully Uploaded to Vector Database!")
        print("="*50)
        print(f"📋 Document ID: {doc_id}")
        print(f"📄 Filename: BTEC.pdf")
        print(f"📊 Word Count: {word_count} words")
        print(f"📈 Character Count: {len(text_content)} characters")
        print(f"💾 Stored in: vector_db/index.json")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error uploading PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Uploading BTEC.pdf to Vector Database...\n")
    success = upload_existing_pdf()
    sys.exit(0 if success else 1)
