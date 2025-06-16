# Environment Configuration

Create a `.env` file in the project root or export these variables:

| Variable | Purpose | Default |
|----------|---------|---------|
| `ENV` | `development` or `production` | `development` |
| `POSTGRES_DATABASE_URL` | local PostgreSQL connection | `postgresql://postgres:postgres@localhost:5432/postgres` |
| `DATABASE_URL` | overrides other URLs when set | *(unset)* |
| `SUPABASE_URL` / `SUPABASE_KEY` | Supabase credentials | *(unset)* |
| `SUPABASE_DATABASE_URL` | Supabase database connection | *(unset)* |
| `HF_API_TOKEN` | Hugging Face token for intent detection | *(unset)* |

See `setup_supabase_steps.txt` for details on connecting to Supabase.
