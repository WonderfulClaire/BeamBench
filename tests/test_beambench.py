from __future__ import annotations

import tempfile
import unittest

import numpy as np
import pandas as pd

from beambench import ResultsSchemaError, build_report, compare_to_baseline, summarize_results
from beambench.preprocessing import frame_signal, rms_normalize, trim_silence


def sample_results() -> pd.DataFrame:
    rows = []
    for method, values in {"DAS": [1.0, 2.0], "MVDR": [2.5, 3.5]}.items():
        for seed, value in enumerate(values):
            rows.append(
                {
                    "run_id": f"{method}-{seed}",
                    "method": method,
                    "metric": "snr_db",
                    "value": value,
                    "seed": seed,
                    "condition": "noise",
                }
            )
    return pd.DataFrame(rows)


class BeamBenchTests(unittest.TestCase):
    def test_schema_rejects_missing_columns(self) -> None:
        with self.assertRaises(ResultsSchemaError):
            summarize_results(pd.DataFrame({"value": [1.0]}))

    def test_summary_is_repeat_aware(self) -> None:
        summary = summarize_results(sample_results())
        das = summary.loc[summary["method"] == "DAS"].iloc[0]
        self.assertEqual(das["n"], 2)
        self.assertAlmostEqual(das["mean"], 1.5)

    def test_paired_comparison_reports_improvement(self) -> None:
        comparison = compare_to_baseline(sample_results(), "DAS")
        self.assertAlmostEqual(comparison.iloc[0]["delta_mean"], 1.5)
        self.assertEqual(comparison.iloc[0]["win_rate"], 1.0)

    def test_report_writes_all_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            paths = build_report(sample_results(), directory, baseline="DAS")
            self.assertTrue(all(path.exists() for path in paths.values()))
            self.assertIn("BeamBench experiment report", paths["report"].read_text("utf-8"))

    def test_preprocessing_shapes_and_levels(self) -> None:
        framed = frame_signal(np.arange(10), 4, 2)
        self.assertEqual(framed.shape, (4, 4))
        normalized = rms_normalize(np.ones(100), -20)
        self.assertAlmostEqual(float(np.sqrt(np.mean(normalized**2))), 0.1)
        trimmed = trim_silence([0, 0, 1, 0, 0])
        self.assertEqual(trimmed.tolist(), [1.0])


if __name__ == "__main__":
    unittest.main()
