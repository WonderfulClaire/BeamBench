"""Paired baseline comparisons that keep seed and condition aligned."""

from __future__ import annotations

import pandas as pd

from .schema import validate_results


def metric_higher_is_better(metric: str) -> bool:
    """Apply a conservative naming heuristic for common error/cost metrics."""
    name = metric.lower()
    lower_tokens = ("error", "mae", "mse", "rmse", "wer", "latency", "runtime", "cost")
    return not any(token in name for token in lower_tokens)


def compare_to_baseline(
    frame: pd.DataFrame,
    baseline: str,
    *,
    higher_is_better: dict[str, bool] | None = None,
) -> pd.DataFrame:
    """Compute paired improvement and win rate against *baseline*."""
    clean = validate_results(frame)
    if baseline not in set(clean["method"]):
        raise ValueError(f"baseline method not found: {baseline}")
    directions = higher_is_better or {}
    keys = ["metric", "condition", "seed"]
    base = clean.loc[clean["method"] == baseline, keys + ["value"]].rename(
        columns={"value": "baseline_value"}
    )
    candidates = clean.loc[clean["method"] != baseline, keys + ["method", "value"]]
    paired = candidates.merge(base, on=keys, validate="many_to_one")
    if paired.empty:
        return pd.DataFrame(
            columns=[
                "metric",
                "method",
                "baseline",
                "condition",
                "pairs",
                "delta_mean",
                "delta_std",
                "win_rate",
            ]
        )
    direction = paired["metric"].map(
        lambda metric: directions.get(str(metric), metric_higher_is_better(str(metric)))
    )
    paired["improvement"] = paired["value"] - paired["baseline_value"]
    paired.loc[~direction, "improvement"] *= -1.0
    paired["win"] = paired["improvement"] > 0.0
    output = paired.groupby(["metric", "method", "condition"], observed=True).agg(
        pairs=("improvement", "count"),
        delta_mean=("improvement", "mean"),
        delta_std=("improvement", "std"),
        win_rate=("win", "mean"),
    )
    output["delta_std"] = output["delta_std"].fillna(0.0)
    output = output.reset_index()
    output.insert(2, "baseline", baseline)
    return output
