"""Repeat-aware summary statistics."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .schema import validate_results


def summarize_results(frame: pd.DataFrame) -> pd.DataFrame:
    """Aggregate repetitions into mean, spread, SEM, and an approximate 95% CI."""
    clean = validate_results(frame)
    groups = ["metric", "method", "condition"]
    summary = clean.groupby(groups, sort=True, observed=True)["value"].agg(
        n="count", mean="mean", std="std"
    )
    summary["std"] = summary["std"].fillna(0.0)
    summary["sem"] = summary["std"] / np.sqrt(summary["n"])
    summary["ci95"] = 1.96 * summary["sem"]
    return summary.reset_index()
