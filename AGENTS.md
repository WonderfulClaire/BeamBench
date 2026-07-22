# Project guide

BeamBench is a file-first research utility. Preserve the six-column tidy-results contract, keep
baseline comparisons seed-aligned, and never turn bundled synthetic examples into research claims.

Before committing, run:

```bash
ruff check .
python -m unittest discover -s tests -v
python scripts/generate_demo.py
```

Generated demo artifacts in `examples/` and `docs/demo-report/` are intentionally versioned and
must be refreshed when report logic or presentation changes.

