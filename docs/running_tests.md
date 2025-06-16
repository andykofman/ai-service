# Running Tests

Tests use **pytest** and reside in the `tests/` folder.

1. Install the dependencies from `requirements.txt`.
2. Run the suite:
   ```bash
   pytest
   ```

Tests that require Supabase credentials are skipped automatically when the variables are missing.
