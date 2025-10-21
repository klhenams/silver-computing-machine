# Support System API

A modern support system that combines REST APIs with Large Language Models (LLMs) and vector databases to deliver context-aware answers from company documentation, tickets, and FAQs.

## Features

- 🤖 **AI-Powered Responses**: Uses Hugging Face LLMs for intelligent query processing
- 🔍 **Vector Search**: Semantic search using pgvector for finding relevant content
- 📚 **Multi-Source Knowledge**: Combines documents, FAQs, and tickets for comprehensive answers
- 🏗️ **Clean Architecture**: Domain-driven design with clear separation of concerns
- 🐳 **Containerized**: Docker and Docker Compose for easy deployment
- 📊 **Analytics**: Query analytics and feedback tracking
- 🔄 **Real-time**: Async FastAPI for high performance

## Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with pgvector extension
- **LLM Provider**: Hugging Face Inference API
- **Embeddings**: Sentence Transformers
- **Containerization**: Docker & Docker Compose
- **Architecture**: Clean Architecture (Domain, Application, Infrastructure, Presentation)

## Project Structure

```
src/support_system/
├── domain/                 # Business logic and entities
│   ├── entities/          # Domain models
│   ├── repositories/      # Repository interfaces
│   └── services/          # Domain service interfaces
├── application/           # Use cases and application logic
│   ├── dtos/             # Data transfer objects
│   ├── interfaces/       # Application service interfaces
│   └── use_cases/        # Business use cases implementation
├── infrastructure/       # External concerns
│   ├── database/         # Database models and configuration
│   ├── external_services/# Hugging Face integration
│   ├── repositories/     # Repository implementations
│   ├── config.py         # Configuration management
│   └── container.py      # Dependency injection
└── presentation/         # API layer
    ├── api/              # FastAPI endpoints
    ├── schemas/          # Request/response schemas
    └── main.py           # Application entry point
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)
- Hugging Face API key (optional, for LLM features)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd special-pancake
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` file with your configuration:

```bash
# Required
DATABASE_URL=postgresql://postgres:password@localhost:5432/support_system

# Optional - for LLM features
HUGGINGFACE_API_KEY=your-huggingface-api-key-here
```

### 3. Start with Docker Compose

```bash
docker-compose up -d
```

This will start:
- PostgreSQL with pgvector extension (port 5432)
- Support System API (port 8000)
- Nginx reverse proxy (port 80)

### 4. Verify Installation

```bash
curl http://localhost/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## API Documentation

Once the application is running, you can access:

- **API Documentation**: http://localhost/docs (Swagger UI)
- **Alternative Docs**: http://localhost/redoc (ReDoc)
- **Health Check**: http://localhost/health

## API Endpoints

### Documents
- `POST /api/v1/documents/` - Create document
- `GET /api/v1/documents/{id}` - Get document
- `GET /api/v1/documents/` - List documents
- `PUT /api/v1/documents/{id}` - Update document
- `DELETE /api/v1/documents/{id}` - Delete document
- `POST /api/v1/documents/search` - Search documents

### FAQs
- `POST /api/v1/faqs/` - Create FAQ
- `GET /api/v1/faqs/{id}` - Get FAQ
- `GET /api/v1/faqs/` - List FAQs
- `GET /api/v1/faqs/popular/` - Get popular FAQs
- `PUT /api/v1/faqs/{id}` - Update FAQ
- `DELETE /api/v1/faqs/{id}` - Delete FAQ
- `POST /api/v1/faqs/search` - Search FAQs
- `POST /api/v1/faqs/{id}/helpful` - Mark FAQ as helpful

### Tickets
- `POST /api/v1/tickets/` - Create ticket
- `GET /api/v1/tickets/{id}` - Get ticket
- `GET /api/v1/tickets/` - List tickets
- `GET /api/v1/tickets/user/{user_id}` - Get user tickets
- `PUT /api/v1/tickets/{id}` - Update ticket
- `DELETE /api/v1/tickets/{id}` - Delete ticket

### Queries (AI-Powered)
- `POST /api/v1/queries/` - Process query with AI
- `GET /api/v1/queries/{id}` - Get query
- `GET /api/v1/queries/` - List queries
- `GET /api/v1/queries/user/{user_id}` - Get user queries
- `POST /api/v1/queries/{id}/feedback` - Provide feedback
- `GET /api/v1/queries/analytics/` - Get analytics

## Usage Examples

### Create a Document

```bash
curl -X POST "http://localhost/api/v1/documents/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Getting Started Guide",
    "content": "This guide helps you get started with our platform...",
    "category": "tutorials",
    "tags": ["beginner", "setup"]
  }'
```

### Ask an AI-Powered Query

```bash
curl -X POST "http://localhost/api/v1/queries/" \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "How do I reset my password?",
    "user_id": "user123"
  }'
```

The AI will search through documents, FAQs, and tickets to provide a contextual answer.

### Search Documents

```bash
curl -X POST "http://localhost/api/v1/documents/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "password reset",
    "limit": 5,
    "category": "tutorials"
  }'
```

## Development

### Local Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database (requires PostgreSQL with pgvector)
export DATABASE_URL=postgresql://postgres:password@localhost:5432/support_system

# Run the application
uvicorn src.support_system.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Setup

For local development, you need PostgreSQL with the pgvector extension:

```sql
-- Connect to PostgreSQL and run:
CREATE DATABASE support_system;
\c support_system;
CREATE EXTENSION vector;
```

### Environment Variables

Key environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `HUGGINGFACE_API_KEY`: Optional, for LLM features
- `DEBUG`: Enable debug mode (true/false)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Architecture

This project follows Clean Architecture principles:

1. **Domain Layer**: Core business logic, entities, and interfaces
2. **Application Layer**: Use cases and application services
3. **Infrastructure Layer**: External integrations (database, APIs)
4. **Presentation Layer**: HTTP endpoints and request/response handling

### Key Design Patterns

- **Dependency Injection**: Using a container for loose coupling
- **Repository Pattern**: Abstracting data access
- **Service Layer**: Encapsulating business logic
- **DTO Pattern**: Separating internal models from API contracts

## Production Considerations

### Security
- Change default passwords and secret keys
- Use environment variables for sensitive configuration
- Implement authentication and authorization
- Set up HTTPS with proper certificates
- Configure CORS appropriately

### Performance
- Set up connection pooling for the database
- Implement caching for frequently accessed data
- Use CDN for static assets
- Monitor and optimize query performance

### Monitoring
- Set up logging aggregation
- Implement health checks
- Monitor API metrics and performance
- Set up alerts for system issues

### Scaling
- Use horizontal scaling for the API service
- Implement database read replicas
- Set up load balancing
- Consider message queues for async processing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the existing architecture
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions and support, please:
1. Check the API documentation at `/docs`
2. Review existing issues and discussions
3. Create a new issue with detailed information

## Roadmap

- [ ] Authentication and authorization
- [ ] Rate limiting
- [ ] Caching layer
- [ ] Enhanced analytics dashboard
- [ ] Multi-language support
- [ ] Advanced search filters
- [ ] Automated testing suite
- [ ] Performance monitoring