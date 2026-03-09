# مساعد BTEC الذكي - BTEC Smart Assistant

An intelligent AI assistant for BTEC qualifications with PDF document handling and vector database integration.

## Features

- 📄 **PDF Upload**: Upload PDF documents for indexing
- 🔍 **Vector Database**: Store and retrieve document embeddings
- 🤖 **AI Assistant**: Ask questions about your documents
- 🌐 **REST API**: Easy-to-use API endpoints
- 🇸🇦 **Arabic Support**: Full Arabic interface and support

## Project Structure

```
BTEC AI Assistant/
├── app/                      # Main application code
│   ├── __init__.py          # App initialization
│   ├── routes.py            # API endpoints
│   ├── pdf_handler.py       # PDF processing
│   ├── vector_db_manager.py # Vector database management
│   └── ai_assistant.py      # AI assistant logic
├── config/                   # Configuration files
│   └── settings.py          # App settings
├── uploads/                 # PDF uploads directory
├── vector_db/               # Vector database storage
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Installation

1. **Clone or create the project**
   ```bash
   cd "BTEC AI Assistant"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

## Configuration

Edit `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
FLASK_PORT=5000
VECTOR_DB_PATH=./vector_db
MAX_PDF_SIZE_MB=50
```

## Usage

### Start the Application

```bash
python run.py
```

The application will start at `http://localhost:5000`

### API Endpoints

#### 1. Upload PDF
```bash
curl -F "file=@document.pdf" http://localhost:5000/api/pdf/upload
```

#### 2. Query the Assistant
```bash
curl -X POST http://localhost:5000/api/assistant/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is BTEC?"}'
```

#### 3. List Documents
```bash
curl http://localhost:5000/api/assistant/documents
```

## API Response Examples

### Upload Response
```json
{
  "status": "success",
  "message": "PDF uploaded and indexed successfully",
  "document_id": "doc_1",
  "filename": "btec_guide.pdf"
}
```

### Query Response
```json
{
  "status": "success",
  "query": "What is BTEC?",
  "response": "BTEC is a qualification...",
  "context_sources": [
    {
      "id": "doc_1",
      "filename": "btec_guide.pdf",
      "score": 5,
      "preview": "BTEC qualifications are..."
    }
  ]
}
```

## Development

### Requirements
- Python 3.8+
- Flask 3.0.0
- PyPDF2 4.0.1
- OpenAI API key (for full functionality)

### Adding New Features

1. Add routes in `app/routes.py`
2. Implement logic in respective modules
3. Update requirements.txt if adding new dependencies
4. Test via API endpoints

## Future Enhancements

- [ ] Integration with proper vector embeddings (OpenAI embeddings)
- [ ] Advanced document chunking
- [ ] Multi-language support
- [ ] User authentication
- [ ] Document versioning
- [ ] Web UI dashboard
- [ ] Advanced search filtering

## Troubleshooting

### Port Already in Use
```bash
python run.py --port 5001
```

### PDF Extraction Issues
- Ensure PyPDF2 is installed: `pip install PyPDF2`
- Check file is a valid PDF

### API Key Errors
- Verify OpenAI API key in `.env`
- Check API key has proper permissions

## License

This project is created for BTEC qualification assistance.

## Support

For issues or suggestions, please create an issue in the project repository.

---

**مساعد BTEC الذكي** | BTEC Smart Assistant
