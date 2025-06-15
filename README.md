# AI Service

This repository contains a small FastAPI service that demonstrates basic CRUD operations and a chat webhook backed by a simple intent detection model.

## Features
- REST endpoints for managing users, products and orders
- Chat endpoint that uses Hugging Face to detect intent
- SQLAlchemy models with optional Supabase/PostgreSQL backend
- Minimal web interface in `static/index.html`

## Getting Started
1. Clone the repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure your environment variables. See [Environment Configuration](docs/environment.md).
3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Open `http://localhost:8000` to view the sample chat UI.

## Running with Docker
You can also start the service using Docker Compose, which sets up the
application, a Postgres database and the mock API all at once:

```bash
docker compose up --build
```

After the containers start, open `http://localhost:8000` to use the service.

## Documentation
- [Architecture Overview](docs/architecture.md)
- [API Reference](docs/api_reference.md)
- [Environment Configuration](docs/environment.md)
- [Running Tests](docs/running_tests.md)

Additional steps for connecting to Supabase can be found in `setup_supabase_steps.txt`.

## Running Tests
Follow the instructions in [Running Tests](docs/running_tests.md) to execute the unit tests.
