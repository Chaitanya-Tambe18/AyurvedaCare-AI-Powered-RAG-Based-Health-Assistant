# HealthGPT - AI Health Assistant

A Retrieval-Augmented Generation (RAG) system that acts as a safe health guide using user-provided PDFs. Built with Flask backend, React frontend, Groq API, Ollama embeddings, and ChromaDB.

## 🎯 Features

- **ChatGPT-style Interface**: Modern dark UI with chat bubbles, typing indicators, and auto-scroll
- **RAG System**: Answers based ONLY on retrieved documents from your PDFs
- **Safe AI**: Medical safety prompts with disclaimers and no diagnosis
- **Local Embeddings**: Uses Ollama's `nomic-embed-text` model
- **Fast LLM**: Powered by Groq's `llama3-70b-8192` model
- **Vector Database**: ChromaDB for efficient document retrieval
- **Windows Compatible**: Tested on Windows with Python 3.10

## 📋 Prerequisites

1. **Python 3.10+**
2. **Node.js 16+**
3. **Ollama** (for local embeddings)
4. **Groq API Key**

## 🚀 Setup Instructions

### 1. Install Ollama

Download and install Ollama from [https://ollama.ai/download](https://ollama.ai/download)

After installation, pull the embedding model:
```bash
ollama pull nomic-embed-text
```

### 2. Set Up Backend

```bash
# Navigate to backend directory
cd health_rag_guide/backend

# Install dependencies
python setup.py

# Create .env file with your Groq API key
cp .env.example .env
# Edit .env and add your Groq API key:
# GROQ_API_KEY=your_groq_api_key_here

# Ingest PDFs (place your health PDFs in data/health_pdfs/)
python database/ingest.py

# Start the backend server
python app.py
```

The backend will run on `http://localhost:5000`

### 3. Set Up Frontend

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will run on `http://localhost:3000`

## 📁 Adding Your PDFs

1. Place your health-related PDF files in `data/health_pdfs/`
2. Run the ingestion script to process them:
   ```bash
   python backend/database/ingest.py
   ```
3. The system will automatically chunk the documents and create embeddings

## 🏥 Usage

1. Open `http://localhost:3000` in your browser
2. You'll see the HealthGPT interface
3. Ask health-related questions
4. The system will provide answers based on your uploaded PDFs
5. Each response includes sources from the original documents

## 🔧 API Endpoints

### POST /api/chat
Accepts: `{ "query": "your health question here" }`
Returns: `{ "response": "answer", "sources": [...] }`

### GET /api/status
Returns system status and document count

## 🛡️ Safety Features

- **No Medical Diagnosis**: System explicitly avoids providing diagnoses
- **Document-based Only**: Answers come only from uploaded PDFs
- **Disclaimers**: Every response includes medical disclaimer
- **Fallback Response**: "I don't have enough information" when context is missing
- **No Hallucination**: LLM is constrained to retrieved documents

## 📊 Architecture

```
health_rag_guide/
├── backend/                 # Flask API server
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── database/           # Vector store and ingestion
│   ├── llm/               # Groq client and prompts
│   ├── routes/            # API routes
│   └── utils/             # PDF processing utilities
├── frontend/               # React Vite application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   └── styles/        # CSS styling
├── data/health_pdfs/       # Place your PDFs here
└── database/chroma_db/     # Vector database storage
```

## 🔍 How It Works

1. **Document Ingestion**: PDFs are chunked and embedded using Ollama
2. **Vector Storage**: Embeddings stored in ChromaDB for fast retrieval
3. **Query Processing**: User questions are embedded and matched against documents
4. **Context Retrieval**: Top 5 most relevant document chunks are retrieved
5. **LLM Generation**: Groq generates response using only retrieved context
6. **Safety Filtering**: System prompts ensure safe, document-based responses

## 🐛 Troubleshooting

### Backend Issues
- Ensure Ollama is running: `ollama list`
- Check Groq API key in `.env` file
- Verify PDFs are in correct directory

### Frontend Issues
- Check that backend is running on port 5000
- Verify proxy configuration in `vite.config.js`
- Clear browser cache if needed

### Embedding Issues
- Make sure `nomic-embed-text` is pulled: `ollama pull nomic-embed-text`
- Check Ollama service status

## 📄 License

This project is for educational purposes. Always consult healthcare professionals for medical advice.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Verify all prerequisites are met
- Ensure all services are running correctly
