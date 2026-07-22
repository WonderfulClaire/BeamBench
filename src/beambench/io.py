"""Input helpers for one CSV file, a directory, or a glob pattern."""

from __future__ import annotations

from glob import glob
from pathlib import Path

import pandas as pd

from .schema import validate_results


def _resolve_csvs(source: str | Path) -> list[Path]:
    text = str(source)
    path = Path(text)
    if path.is_dir():
        files = sorted(path.glob("*.csv"))
    elif any(mark in text for mark in "*?[]"):
        files = sorted(Path(item) for item in glob(text))
    else:
        files = [path]
    files = [item for item in files if item.suffix.lower() == ".csv" and item.is_file()]
    if not files:
        raise FileNotFoundError(f"no CSV result files found for: {source}")
    return files


def load_results(source: str | Path) -> pd.DataFrame:
    """Load and validate one or more tidy result CSV files."""
    files = _resolve_csvs(source)
    frames = []
    for path in files:
        frame = pd.read_csv(path)
        frame["source_file"] = path.name
        frames.append(frame)
    return validate_results(pd.concat(frames, ignore_index=True))
