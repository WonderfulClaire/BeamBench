# Contributing

Keep changes small, reproducible, and easy to audit.

```bash
python -m pip install -e ".[dev]"
ruff check .
python -m unittest discover -s tests -v
python scripts/generate_demo.py
```

Open an issue before adding a large dependency or changing the required result columns. New
statistics should state assumptions and include a test with a hand-checkable example. Never commit
private participant data, credentials, or third-party datasets without redistribution rights.

