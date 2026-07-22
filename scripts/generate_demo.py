"""Generate deterministic illustrative results and their BeamBench report."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from beambench import build_report

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    rng = np.random.default_rng(20260722)
    rows: list[dict[str, object]] = []
    method_effects = {
        "DAS": (0.0, 0.0, 0.0),
        "MVDR": (3.8, -5.4, 1.8),
        "Binaural-PF": (2.4, -3.1, 0.9),
    }
    for condition in (-5, 0, 5):
        for seed in range(8):
            for method, (snr_gain, mae_gain, runtime_gain) in method_effects.items():
                run_id = f"snr{condition:+d}-seed{seed}-{method.lower()}"
                values = {
                    "output_snr_db": condition + 6.5 + snr_gain + rng.normal(0, 0.55),
                    "localization_mae_deg": 17.0 - 0.55 * condition + mae_gain + rng.normal(0, 1.1),
                    "runtime_ms": 3.2 + runtime_gain + rng.normal(0, 0.18),
                }
                for metric, value in values.items():
                    rows.append(
                        {
                            "run_id": run_id,
                            "method": method,
                            "metric": metric,
                            "value": round(float(max(0.01, value)), 5),
                            "seed": seed,
                            "condition": f"input SNR {condition:+d} dB",
                        }
                    )
    destination = ROOT / "examples" / "demo_results.csv"
    destination.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(destination, index=False)
    build_report(destination, ROOT / "docs" / "demo-report", baseline="DAS")


if __name__ == "__main__":
    main()
