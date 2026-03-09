import os
import json
from datetime import datetime
from config.settings import VectorDBConfig

class VectorDBManager:
    """Manage vector database operations using ChromaDB"""
    
    def __init__(self):
        self.db_path = VectorDBConfig.DB_PATH
        self.documents_index = os.path.join(self.db_path, 'index.json')
        os.makedirs(self.db_path, exist_ok=True)
        self._init_index()
        
    def _init_index(self):
        """Initialize documents index"""
        if not os.path.exists(self.documents_index):
            with open(self.documents_index, 'w', encoding='utf-8') as f:
                json.dump({'documents': []}, f)
    
    def add_document(self, filename, content):
        """Add document to vector database"""
        try:
            doc_id = self._generate_doc_id()
            
            # Store document metadata
            doc_data = {
                'id': doc_id,
                'filename': filename,
                'content_preview': content[:500],
                'full_content': content,
                'timestamp': datetime.now().isoformat(),
                'word_count': len(content.split())
            }
            
            # Save to index
            with open(self.documents_index, 'r', encoding='utf-8') as f:
                index = json.load(f)
            
            index['documents'].append(doc_data)
            
            with open(self.documents_index, 'w', encoding='utf-8') as f:
                json.dump(index, f, ensure_ascii=False, indent=2)
            
            return doc_id
        except Exception as e:
            raise Exception(f"Error adding document: {str(e)}")
    
    def search(self, query, top_k=3):
        """Search for relevant documents"""
        try:
            with open(self.documents_index, 'r', encoding='utf-8') as f:
                index = json.load(f)
            
            # Simple keyword matching (can be enhanced with proper embeddings)
            results = []
            query_terms = query.lower().split()
            
            for doc in index['documents']:
                score = 0
                content_lower = doc['full_content'].lower()
                
                for term in query_terms:
                    score += content_lower.count(term)
                
                if score > 0:
                    results.append({
                        'id': doc['id'],
                        'filename': doc['filename'],
                        'score': score,
                        'preview': doc['content_preview']
                    })
            
            # Sort by score and return top_k
            results.sort(key=lambda x: x['score'], reverse=True)
            return results[:top_k]
        except Exception as e:
            raise Exception(f"Error searching documents: {str(e)}")
    
    def list_documents(self):
        """List all documents"""
        try:
            with open(self.documents_index, 'r', encoding='utf-8') as f:
                index = json.load(f)
            
            return [{
                'id': doc['id'],
                'filename': doc['filename'],
                'word_count': doc['word_count'],
                'timestamp': doc['timestamp']
            } for doc in index['documents']]
        except Exception as e:
            raise Exception(f"Error listing documents: {str(e)}")
    
    def _generate_doc_id(self):
        """Generate unique document ID"""
        with open(self.documents_index, 'r', encoding='utf-8') as f:
            index = json.load(f)
        
        return f"doc_{len(index['documents']) + 1}"
