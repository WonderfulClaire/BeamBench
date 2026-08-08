# HearWeave → BeamBench reproducible example

This example connects two deliberately separate layers:

1. [HearWeave](https://github.com/WonderfulClaire/HearWeave) creates a deterministic synthetic smart-glasses microphone-array experiment.
2. BeamBench validates the resulting tidy table, keeps comparisons aligned by condition and seed, and exports a reviewable report.

It answers a narrow engineering question: **can the complete experiment-to-report path be rerun from source without private audio or a notebook?** It is not a real-device benchmark and does not establish product performance.

## Reproduce locally

Clone the repositories beside each other, then install both editable packages:

```bash
git clone https://github.com/WonderfulClaire/HearWeave.git
git clone https://github.com/WonderfulClaire/BeamBench.git
cd BeamBench
python -m pip install -e . -e ../HearWeave
python scripts/generate_hearweave_demo.py
```

The command writes:

- `examples/hearweave_results.csv`: 90 tidy measurements with experiment metadata;
- `docs/hearweave-report/summary.csv`: repeat-aware descriptive statistics;
- `docs/hearweave-report/comparisons.csv`: condition- and seed-aligned changes versus one reference microphone;
- `docs/hearweave-report/overview.png`: two metric panels;
- `docs/hearweave-report/report.md`: a Markdown evidence summary.

## Fixed protocol

- Geometry: HearWeave `glasses_4mic`
- Source: deterministic speech-like synthetic probe at 35°
- Conditions: input SNR −5, 0, and +5 dB
- Repetitions: five fixed random seeds per condition
- Perturbation: independent noise plus small gain and timing mismatch
- Methods: one reference microphone, delay-and-sum, and HearWeave's reference MVDR
- Metrics: output SNR and SI-SDR

All inputs are generated in memory. Extra columns in the BeamBench contract preserve geometry, source angle, sample rate, and the explicit `deterministic synthetic demo` evidence scope.

## Interpretation boundary

The simulator uses a lightweight free-field plane-wave model. It does not include room impulse responses, head shadow, device enclosures, clock drift, speech datasets, or measured microphones. The checked-in numbers are useful for integration regression and workflow inspection only. Real-device claims require a separate registered protocol and traceable recordings.
