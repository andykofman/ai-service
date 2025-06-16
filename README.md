# AI Customer Service

A modern FastAPI-based service that provides CRUD APIs and an intelligent chat webhook interface. This project provides an easy way to explore FastAPI, SQLAlchemy and Hugging Face intents in action.

## Live Demo

Access the live application at [AI Service Demo](https://ai-service-katafast.vercel.app/)

## Features

- REST endpoints for managing users, products and orders
- Chat endpoint that uses Hugging Face to detect intent
- SQLAlchemy models with optional Supabase/PostgreSQL backend
- Minimal web interface in `static/index.html`

## Quick Start

### Option 1: Local Development

1. Clone the repository
   ```bash
   git clone <https://github.com/andykofman/ai-service.git>
   cd ai-service
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Start the development server from the project's terminal
   ```bash
   uvicorn app.main:app --reload
   ```

4. Access the application at `http://localhost:8000`

5. Access endpoints at `http://localhost:8000/docs`    

### Option 2: Docker Deployment

Run the application using Docker Compose:
```bash
docker compose up --build
```
### Option 3: Using Swagger UI
1. Access the live application at [AI Service Demo](https://ai-service-katafast.vercel.app/)

2. Access endpoints at [AI Service Endpoints](https://ai-service-katafast.vercel.app/docs)

## Documentation

- [Architecture Overview](docs/architecture.md) - System design and component interaction
- [API Reference](docs/api_reference.md) - Detailed API documentation and endpoints
- [Environment Setup](docs/environment.md) - Configuration and environment variables
- [Testing Guide](docs/testing_guide.md) - Comprehensive guide for testing the application, including chat examples
- [Deployment Guide](docs/deployment.md) - Deployment procedures and considerations

## Technology Stack

- FastAPI - Modern, fast web framework
- SQLAlchemy - SQL toolkit and ORM
- Alembic - Database migration tool
- Docker - Containerization
- Vercel - Deployment platform
- Pytest - Testing framework

## Contributing

Contribution are always wleomed. For major changes, please open an issue first to discuss proposed changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

