"""Turn tidy measurements into reviewable artifacts."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .aggregate import summarize_results
from .compare import compare_to_baseline
from .io import load_results
from .manifest import build_manifest, write_manifest
from .plotting import plot_metric_overview
from .schema import validate_results


def _markdown_table(frame: pd.DataFrame, limit: int = 18) -> str:
    shown = frame.head(limit).copy()
    if shown.empty:
        return "_No rows._"
    for column in shown.select_dtypes(include="number"):
        shown[column] = shown[column].map(lambda value: f"{value:.4g}")
    headers = [str(column) for column in shown.columns]
    rows = [[str(value) for value in row] for row in shown.itertuples(index=False, name=None)]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def build_report(
    results: pd.DataFrame | str | Path,
    output_dir: str | Path,
    *,
    baseline: str,
) -> dict[str, Path]:
    """Write normalized results, comparisons, a plot, and a Markdown report."""
    source = results if isinstance(results, (str, Path)) else None
    frame = load_results(results) if source is not None else validate_results(results)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    summary = summarize_results(frame)
    comparisons = compare_to_baseline(frame, baseline)
    paths = {
        "summary": destination / "summary.csv",
        "comparisons": destination / "comparisons.csv",
        "figure": destination / "overview.png",
        "report": destination / "report.md",
        "manifest": destination / "manifest.json",
    }
    summary.to_csv(paths["summary"], index=False)
    comparisons.to_csv(paths["comparisons"], index=False)
    plot_metric_overview(summary, paths["figure"])
    manifest = build_manifest(
        source=source,
        baseline=baseline,
        rows=len(frame),
        methods=frame["method"].unique().tolist(),
        metrics=frame["metric"].unique().tolist(),
    )
    write_manifest(paths["manifest"], manifest)
    report = f"""# BeamBench experiment report

> Generated from a validated tidy-results table. Statistical summaries are descriptive;
> this report does not claim significance or replace a preregistered analysis plan.

## Dataset

- Measurements: **{len(frame)}**
- Methods: **{frame["method"].nunique()}**
- Metrics: **{frame["metric"].nunique()}**
- Conditions: **{frame["condition"].nunique()}**
- Baseline: **{baseline}**

![Experiment overview](overview.png)

## Aggregated results

{_markdown_table(summary)}

## Paired baseline comparison

Positive `delta_mean` means the candidate improved over the baseline. Direction is inferred
from common metric names and can be overridden through the Python API.

{_markdown_table(comparisons)}

## Reproducibility manifest

The accompanying [`manifest.json`](manifest.json) records input file hashes, the Git commit
and dirty state when available, Python/platform information, package versions, and the baseline
used for this report. Absolute local paths and Git remote URLs are intentionally not stored.

## Reproduce

```bash
beambench summarize path/to/results.csv --output report --baseline "{baseline}"
```
"""
    paths["report"].write_text(report, encoding="utf-8")
    return paths
