"""Command-line interface."""

from __future__ import annotations

import argparse

from .report import build_report


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="beambench", description="Reproducible experiment reports")
    commands = root.add_subparsers(dest="command", required=True)
    summarize = commands.add_parser("summarize", help="validate results and generate a report")
    summarize.add_argument("source", help="CSV file, directory, or glob")
    summarize.add_argument("--output", "-o", default="beambench-report")
    summarize.add_argument("--baseline", required=True)
    return root


def main() -> None:
    args = parser().parse_args()
    if args.command == "summarize":
        paths = build_report(args.source, args.output, baseline=args.baseline)
        print(f"BeamBench report ready: {paths['report']}")


if __name__ == "__main__":
    main()
