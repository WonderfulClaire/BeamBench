"""BeamBench public API."""

from .aggregate import summarize_results
from .compare import compare_to_baseline
from .io import load_results
from .report import build_report
from .schema import ResultsSchemaError, validate_results

__all__ = [
    "ResultsSchemaError",
    "build_report",
    "compare_to_baseline",
    "load_results",
    "summarize_results",
    "validate_results",
]

__version__ = "0.1.0"
