# Contract Management SaaS - Backend

A FastAPI-based backend for a contract management SaaS platform with AI-powered document processing and natural language querying.

## Features

- **Authentication**: JWT-based multi-user authentication
- **Document Upload**: Support for PDF, TXT, and DOCX files
- **Document Processing**: Mock LlamaCloud integration for document parsing
- **Vector Search**: PostgreSQL + pgvector for semantic search
- **RAG Workflow**: Natural language querying of contract documents
- **Multi-tenant**: Complete user isolation for all operations

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL + pgvector
- **Authentication**: JWT with bcrypt password hashing
- **ORM**: SQLAlchemy
- **Document Processing**: Mock LlamaCloud simulation
- **Vector Embeddings**: Mock embedding generation

## Project Structure

```
backend/
├── app/
│   ├── main.py            # FastAPI application entry point
│   ├── auth.py            # Authentication and JWT handling
│   ├── database.py        # Database connection and pgvector setup
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic request/response schemas
│   ├── routes/
│   │   ├── contracts.py   # Contract management endpoints
│   │   ├── upload.py      # File upload and processing
│   │   └── query.py       # Natural language query endpoints
│   └── utils/
│       ├── llama_mock.py  # Mock LlamaCloud document parser
│       └── embeddings.py  # Mock embedding generation
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
└── README.md
```

## Database Schema

### Users Table
- `user_id` (UUID, Primary Key)
- `username` (String, Unique)
- `email` (String, Unique)
- `password_hash` (String)
- `created_at` (DateTime)

### Documents Table
- `doc_id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key)
- `filename` (String)
- `original_filename` (String)
- `file_size` (Integer)
- `file_type` (String)
- `uploaded_on` (DateTime)
- `contract_name` (String)
- `parties` (Text)
- `expiry_date` (DateTime)
- `status` (String) - Active, Renewal Due, Expired
- `risk_score` (String) - Low, Medium, High
- `processing_status` (String)

### Chunks Table
- `chunk_id` (UUID, Primary Key)
- `doc_id` (UUID, Foreign Key)
- `user_id` (UUID, Foreign Key)
- `text_chunk` (Text)
- `embedding` (Vector[384])
- `page_number` (Integer)
- `chunk_index` (Integer)
- `confidence_score` (Float)
- `metadata` (Text/JSON)
- `created_at` (DateTime)

## API Endpoints

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### Contracts
- `GET /api/contracts` - List user's contracts (with pagination, search, filters)
- `GET /api/contracts/{doc_id}` - Get contract details with insights
- `DELETE /api/contracts/{doc_id}` - Delete contract
- `GET /api/contracts/{doc_id}/chunks` - Get contract chunks

### Upload
- `POST /api/upload` - Upload and process document
- `GET /api/upload/status/{doc_id}` - Get processing status

### Query
- `POST /api/ask` - Natural language query
- `GET /api/ask/suggestions` - Get query suggestions
- `GET /api/ask/history` - Get query history

## Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL 12+ with pgvector extension
- pip or conda

### Local Development

1. **Clone and navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL with pgvector**
   ```sql
   CREATE DATABASE contract_db;
   CREATE EXTENSION vector;
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t contract-backend .
   ```

2. **Run with Docker Compose** (recommended)
   ```yaml
   version: '3.8'
   services:
     db:
       image: pgvector/pgvector:pg15
       environment:
         POSTGRES_DB: contract_db
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD: password
       ports:
         - "5432:5432"
     
     backend:
       build: .
       ports:
         - "8000:8000"
       environment:
         DATABASE_URL: postgresql://postgres:password@db:5432/contract_db
       depends_on:
         - db
   ```

### Production Deployment

The backend is configured for deployment on:
- **Render**: Use the included Dockerfile
- **Heroku**: Add Procfile: `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Fly.io**: Use the included Dockerfile

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@localhost:5432/contract_db` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-change-in-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration | `30` |
| `DEBUG` | Debug mode | `True` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

## Mock Data Generation

The backend includes sophisticated mock data generation:

- **Document Parsing**: Simulates LlamaCloud parsing with realistic contract chunks
- **Embeddings**: Generates semantic embeddings with clustering for similar terms
- **Contract Metadata**: Auto-generates contract names, parties, expiry dates, and risk scores
- **AI Insights**: Provides contextual insights and recommendations based on contract content

## Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Multi-tenant data isolation
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- File type and size validation
- CORS configuration

## Performance Considerations

- Database indexing on user_id and doc_id
- Vector similarity search with pgvector
- Pagination for large result sets
- Async/await for I/O operations
- Connection pooling with SQLAlchemy

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
