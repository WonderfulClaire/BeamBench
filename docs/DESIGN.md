# Design notes

BeamBench is intentionally file-first. A CSV is readable without BeamBench, diffable in Git, and
portable across a lab's Python, MATLAB, and R workflows. The package adds validation and consistent
derivations without creating a new database or hosted dependency.

## Data flow

1. Experiment code emits tidy CSV rows.
2. `validate_results` rejects missing, empty, non-numeric, or duplicate measurements.
3. `summarize_results` aggregates repetitions without discarding the original rows.
4. `compare_to_baseline` inner-joins on metric, condition, and seed before computing improvements.
5. `build_report` writes machine-readable tables first, then visuals and prose derived from them.

Positive comparison deltas always mean “better,” including lower-is-better error and runtime
metrics. This makes dashboards easier to scan, while the direction rule remains explicit in the
output documentation.

