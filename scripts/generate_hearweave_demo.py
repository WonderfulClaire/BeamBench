"""Run a deterministic HearWeave experiment and build a BeamBench report."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from hearweave import (
    apply_microphone_mismatch,
    delay_and_sum,
    glasses_4mic,
    mvdr_beamform,
    si_sdr_db,
    simulate_plane_wave,
    snr_db,
)
from hearweave.geometry import relative_arrival_delays
from hearweave.simulation import speech_like_probe

from beambench import build_report

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = ROOT / "examples" / "hearweave_results.csv"
DEFAULT_REPORT = ROOT / "docs" / "hearweave-report"


def run_experiment() -> pd.DataFrame:
    """Return tidy measurements for a small synthetic wearable-array experiment."""
    sample_rate_hz = 16_000
    azimuth_deg = 35.0
    geometry = glasses_4mic()
    reference = speech_like_probe(sample_rate_hz, duration_s=0.75)
    first_microphone = int(np.argmin(relative_arrival_delays(geometry, azimuth_deg)))
    rows: list[dict[str, object]] = []

    for input_snr_db in (-5, 0, 5):
        condition = f"synthetic input SNR {input_snr_db:+d} dB"
        for seed in range(5):
            microphones = simulate_plane_wave(
                reference,
                geometry,
                sample_rate_hz,
                azimuth_deg,
                snr_db=float(input_snr_db),
                rng=np.random.default_rng(seed),
            )
            microphones = apply_microphone_mismatch(
                microphones,
                sample_rate_hz,
                gain_std_db=0.5,
                delay_jitter_std_s=5e-6,
                rng=np.random.default_rng(10_000 + seed),
            )
            outputs = {
                "Reference mic": microphones[first_microphone],
                "DAS": delay_and_sum(
                    microphones, geometry, sample_rate_hz, look_azimuth_deg=azimuth_deg
                ),
                "MVDR": mvdr_beamform(
                    microphones, geometry, sample_rate_hz, look_azimuth_deg=azimuth_deg
                ),
            }
            for method, output in outputs.items():
                run_id = f"snr{input_snr_db:+d}-seed{seed}-{method.lower().replace(' ', '-')}"
                measurements = {
                    "output_snr_db": snr_db(reference, output),
                    "si-sdr_db": si_sdr_db(reference, output),
                }
                for metric, value in measurements.items():
                    rows.append(
                        {
                            "run_id": run_id,
                            "method": method,
                            "metric": metric,
                            "value": round(float(value), 6),
                            "seed": seed,
                            "condition": condition,
                            "array": geometry.name,
                            "source_azimuth_deg": azimuth_deg,
                            "sample_rate_hz": sample_rate_hz,
                            "evidence_scope": "deterministic synthetic demo",
                        }
                    )
    return pd.DataFrame(rows)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    command.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return command


def main() -> None:
    args = parser().parse_args()
    results = run_experiment()
    args.results.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(args.results, index=False)
    paths = build_report(results, args.report, baseline="Reference mic")
    print(f"HearWeave results: {args.results}")
    print(f"BeamBench report: {paths['report']}")


if __name__ == "__main__":
    main()
