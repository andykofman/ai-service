# Deployment

Use Docker Compose to run the app with a local database and the mock API:

```bash
docker compose up --build
```

This starts the FastAPI service, Postgres and a small mock API. Browse to `http://localhost:8000` after the containers finish starting.

For production, build the image and supply your own Postgres or Supabase database.
