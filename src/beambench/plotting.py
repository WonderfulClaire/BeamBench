"""Paper-ready, dependency-light experiment plots."""

from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def _condition_key(label: object) -> tuple[int, float | str]:
    match = re.search(r"[-+]?\d+(?:\.\d+)?", str(label))
    return (0, float(match.group())) if match else (1, str(label))


def _metric_title(metric: object) -> str:
    words = str(metric).replace("_", " ").split()
    acronyms = {
        "snr": "SNR",
        "si": "SI",
        "sdr": "SDR",
        "si-sdr": "SI-SDR",
        "mae": "MAE",
        "mse": "MSE",
        "rmse": "RMSE",
        "db": "dB",
        "ms": "ms",
    }
    return " ".join(acronyms.get(word.lower(), word.title()) for word in words)


def plot_metric_overview(summary: pd.DataFrame, output: str | Path) -> Path:
    """Plot one panel per metric with 95% confidence intervals."""
    metrics = list(summary["metric"].drop_duplicates())
    if not metrics:
        raise ValueError("cannot plot an empty summary")
    fig, axes = plt.subplots(1, len(metrics), figsize=(5.2 * len(metrics), 4.2), squeeze=False)
    palette = plt.get_cmap("Dark2")
    for axis, metric in zip(axes[0], metrics, strict=True):
        part = summary.loc[summary["metric"] == metric]
        conditions = sorted(part["condition"].drop_duplicates(), key=_condition_key)
        positions = np.arange(len(conditions))
        for index, (method, group) in enumerate(part.groupby("method", sort=True)):
            indexed = group.set_index("condition").reindex(conditions)
            axis.errorbar(
                positions,
                indexed["mean"],
                yerr=indexed["ci95"],
                marker="o",
                linewidth=2,
                capsize=3,
                color=palette(index % 8),
                label=str(method),
            )
        axis.set_title(_metric_title(metric), loc="left", fontweight="bold")
        axis.set_xticks(positions, conditions, rotation=20)
        axis.set_xlabel("Condition")
        axis.grid(axis="y", alpha=0.2)
        axis.spines[["top", "right"]].set_visible(False)
    axes[0][0].set_ylabel("Mean ± 95% CI")
    handles, labels = axes[0][-1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncols=max(1, len(labels)), frameon=False)
    fig.suptitle("BeamBench experiment overview", x=0.02, ha="left", fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destination, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return destination
