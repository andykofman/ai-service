# Running Tests

The project uses **pytest**. Tests are located in the `tests/` directory.

Create a virtual environment and install dependencies:

```bash
pip install -r requirements.txt
pip install pytest
```

Run all tests:

```bash
pytest
```

Some tests that require Supabase credentials will be skipped automatically if the credentials are not configured.
