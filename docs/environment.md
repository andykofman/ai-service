# Environment Configuration

Configuration is managed with environment variables. Create a `.env` file in the project root or set these variables in your deployment environment.

Required variables:

- `ENV` – set to `development` or `production` (default: `development`)
- `POSTGRES_DATABASE_URL` – connection string for local PostgreSQL
- `DATABASE_URL` – overrides other database URLs when set (useful on platforms like Vercel)
- `SUPABASE_URL` and `SUPABASE_KEY` – Supabase project credentials
- `SUPABASE_DATABASE_URL` – connection string to the Supabase database
- `HF_API_TOKEN` – Hugging Face API token used for intent detection

See `setup_supabase_steps.txt` for detailed instructions on connecting to Supabase.
