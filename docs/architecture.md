# Architecture Overview

The service is built with **FastAPI** and uses **SQLAlchemy** to talk to a PostgreSQL or Supabase database. Incoming requests go through the API routers which call small service modules and persist data through SQLAlchemy models.

```
client -> FastAPI -> services -> database
```

Main packages:

- **app/main.py** – application setup and route registration
- **app/routes/** – routers for users, products, orders and the chat webhook
- **app/services/** – business logic and conversation handling
- **app/models/** – SQLAlchemy models defining the tables
- **app/ai/** – wraps the Hugging Face intent detection
- **app/db/** – database session utilities

Static files in `static/` provide a basic chat UI that posts messages to `/webhook`.
