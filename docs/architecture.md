# Architecture Overview

This service is built with **FastAPI** and uses **SQLAlchemy** for ORM access. In development it connects to a local PostgreSQL database. In production you can point it to Supabase or another Postgres-compatible database.

```
client --HTTP--> FastAPI app --SQLAlchemy--> PostgreSQL/Supabase
```

The main components are:

- **app/main.py** – FastAPI application entry point
- **app/routes/** – Modular API routers for users, products and orders
- **app/ai/** – Contains the intent detection helper using Hugging Face
- **app/models/** – SQLAlchemy models
- **app/db/** – Database session and Supabase client utilities

There is also a minimal HTML client in `static/index.html` used to interact with the `/webhook` endpoint.
