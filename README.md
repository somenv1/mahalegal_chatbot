# Maharashtra Traffic Law Advisor 🚦

An AI-powered chatbot that provides legal advice for traffic-related issues specifically for Maharashtra, India. Built using RAG (Retrieval-Augmented Generation) architecture with LangChain, ChromaDB, and OpenAI.

## Features

- **AI-Powered Legal Advice**: Get instant answers about Maharashtra traffic laws and regulations
- **Fine Verification**: Check exact fine amounts for traffic violations based on Motor Vehicles Act 2019
- **Citizen Rights Information**: Learn about your legal rights during traffic stops
- **Maharashtra-Specific**: Includes state-specific rules, RTO contacts, and local resources
- **RAG Architecture**: Accurate responses based on actual legal documents and regulations
- **User-Friendly Interface**: Clean React-based chat interface

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **LangChain**: Framework for LLM applications
- **ChromaDB**: Vector database for document storage
- **OpenAI GPT-4**: Language model for generating responses
- **Sentence Transformers**: For document embeddings

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Axios**: HTTP client
- **React Icons**: Icon library
- **React Markdown**: Markdown rendering

### Data Sources
- Motor Vehicles Act 2019
- Maharashtra State Traffic Rules
- Citizen Rights Documentation
- Official Fine Amounts (2024)

## Project Structure

```
mahalegal_chatbot/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── chat.py          # Chat and fine verification endpoints
│   │   ├── core/
│   │   │   ├── config.py            # Configuration management
│   │   │   └── rag_system.py        # RAG implementation
│   │   ├── models/
│   │   │   └── schemas.py           # Pydantic models
│   │   └── main.py                  # FastAPI application
│   ├── requirements.txt             # Python dependencies
│   └── Dockerfile                   # Backend container config
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js            # API client
│   │   ├── components/
│   │   │   ├── ChatMessage.jsx      # Chat message component
│   │   │   ├── FineVerifier.jsx     # Fine verification component
│   │   │   └── RightsPanel.jsx      # Rights information panel
│   │   ├── styles/
│   │   │   └── App.css              # Application styles
│   │   ├── App.jsx                  # Main application component
│   │   └── main.jsx                 # Entry point
│   ├── package.json                 # Node dependencies
│   ├── vite.config.js               # Vite configuration
│   └── Dockerfile                   # Frontend container config
├── data/
│   ├── maharashtra_fines_2024.json  # Fine amounts data
│   ├── maharashtra_traffic_rules.md # Traffic rules documentation
│   └── citizen_rights.md            # Citizen rights information
├── scripts/
│   └── ingest_documents.py          # Document ingestion script
├── docker-compose.yml               # Docker orchestration
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key
- Docker (optional, for containerized deployment)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/somenv1/mahalegal_chatbot.git
cd mahalegal_chatbot
```

#### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

#### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 4. Ingest Documents

Before starting the backend, ingest the documents into ChromaDB:

```bash
cd ..  # Back to project root
python scripts/ingest_documents.py
```

This will:
- Load all documents from the `data/` directory
- Split them into chunks
- Create embeddings
- Store them in ChromaDB

#### 5. Start Backend Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

#### 6. Frontend Setup

In a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Docker Deployment

For production deployment using Docker:

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Usage

### Chat Interface

1. Open the application in your browser (`http://localhost:3000`)
2. Type your question about Maharashtra traffic laws
3. The AI will provide detailed answers based on official documents

**Example Questions:**
- "What is the fine for not wearing a helmet in Maharashtra?"
- "What are my rights during a traffic stop?"
- "How do I contest a traffic challan?"
- "What is the speed limit in Mumbai?"

### Fine Verification

1. Click on the "Fine Verification" tab
2. Enter vehicle number and violation type
3. Get exact fine amount and applicable section

### Your Rights

1. Click on the "Your Rights" tab
2. View information about your legal rights
3. Find emergency contacts and resources

## API Endpoints

### Chat
```http
POST /api/v1/chat
Content-Type: application/json

{
  "message": "What is the fine for jumping a red light?",
  "conversation_history": []
}
```

### Verify Fine
```http
POST /api/v1/verify-fine
Content-Type: application/json

{
  "vehicle_number": "MH01AB1234",
  "violation_type": "helmet"
}
```

### List Violations
```http
GET /api/v1/violations?search=helmet
```

### Health Check
```http
GET /health
```

## Important Resources

- **E-Challan Payment**: [mahatrafficechallan.gov.in](https://mahatrafficechallan.gov.in)
- **Mumbai Traffic Police**: 103
- **Emergency**: 112
- **Anti-Corruption Bureau**: 1064
- **Highway Safety**: 1033

## Configuration

### Backend Configuration

Edit `.env` file or set environment variables:

```env
# OpenAI
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./chroma_db
COLLECTION_NAME=maharashtra_traffic_laws

# RAG Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
```

### Frontend Configuration

Create `.env` in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
```

## Development

### Adding New Documents

1. Add markdown or JSON files to `data/` directory
2. Run the ingestion script:
   ```bash
   python scripts/ingest_documents.py
   ```
3. Restart the backend server

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Troubleshooting

### Documents Not Loading
- Ensure you've run `ingest_documents.py`
- Check that `chroma_db/` directory exists
- Verify data files are present in `data/` directory

### API Connection Error
- Verify backend is running on port 8000
- Check CORS settings in backend config
- Ensure `VITE_API_URL` is set correctly in frontend

### OpenAI API Errors
- Verify your API key is correct
- Check you have sufficient credits
- Ensure you have access to the specified model

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Disclaimer

This chatbot provides general information only and should not be considered as legal advice. For specific legal matters, please consult a qualified legal professional. The information is based on Motor Vehicles Act 2019 and Maharashtra state regulations as of January 2024.

## License

This project is for educational and informational purposes.

## Acknowledgments

- Motor Vehicles Act 2019
- Maharashtra State Transport Department
- Mumbai Traffic Police
- OpenAI for GPT-4 API
- LangChain and ChromaDB communities

## Contact

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for safer roads in Maharashtra**
