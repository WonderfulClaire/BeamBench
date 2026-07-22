"""Validation for BeamBench's small, tidy experiment-results contract."""

from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = ("run_id", "method", "metric", "value", "seed", "condition")


class ResultsSchemaError(ValueError):
    """Raised when experiment results cannot be compared safely."""


def validate_results(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a normalized copy of *frame* or raise a readable schema error."""
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ResultsSchemaError(f"missing required columns: {', '.join(missing)}")

    clean = frame.copy()
    for column in ("run_id", "method", "metric", "condition"):
        clean[column] = clean[column].astype("string").str.strip()
        if clean[column].isna().any() or (clean[column] == "").any():
            raise ResultsSchemaError(f"column '{column}' contains empty values")

    clean["value"] = pd.to_numeric(clean["value"], errors="coerce")
    clean["seed"] = pd.to_numeric(clean["seed"], errors="coerce")
    if clean[["value", "seed"]].isna().any().any():
        raise ResultsSchemaError("columns 'value' and 'seed' must be numeric")
    if not clean["seed"].mod(1).eq(0).all():
        raise ResultsSchemaError("column 'seed' must contain integers")
    clean["seed"] = clean["seed"].astype(int)

    duplicate = clean.duplicated(subset=["run_id", "metric"], keep=False)
    if duplicate.any():
        example = clean.loc[duplicate, ["run_id", "metric"]].iloc[0]
        raise ResultsSchemaError(
            f"duplicate measurement for run_id={example['run_id']!r}, metric={example['metric']!r}"
        )
    return clean
