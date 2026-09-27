"""Reproducibility manifest for generated experiment reports."""

from __future__ import annotations

import glob
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_files(source: str | Path | None) -> list[Path]:
    if source is None:
        return []
    raw = str(source)
    candidate = Path(raw)
    if candidate.is_file():
        return [candidate.resolve()]
    if candidate.is_dir():
        return sorted(path.resolve() for path in candidate.glob("*.csv"))
    return sorted(Path(path).resolve() for path in glob.glob(raw) if Path(path).is_file())


def _git_state(cwd: Path | None = None) -> dict[str, Any]:
    def run(*args: str) -> str | None:
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=cwd,
                check=True,
                capture_output=True,
                text=True,
                timeout=3,
            )
        except (OSError, subprocess.SubprocessError):
            return None
        return result.stdout.strip()

    commit = run("rev-parse", "HEAD")
    if not commit:
        return {"available": False}
    status = run("status", "--porcelain")
    branch = run("rev-parse", "--abbrev-ref", "HEAD")
    return {
        "available": True,
        "commit": commit,
        "branch": branch,
        "dirty": bool(status),
    }


def build_manifest(
    *,
    source: str | Path | None,
    baseline: str,
    rows: int,
    methods: list[str],
    metrics: list[str],
) -> dict[str, Any]:
    files = _source_files(source)
    packages = {}
    for name in ("beambench", "numpy", "pandas", "matplotlib"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None

    return {
        "schema_version": 1,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "command": {
            "baseline": baseline,
            "source": str(source) if source is not None else None,
        },
        "dataset": {
            "rows": int(rows),
            "methods": sorted(map(str, methods)),
            "metrics": sorted(map(str, metrics)),
            "source_files": [
                {
                    "path": path.name,
                    "size_bytes": path.stat().st_size,
                    "sha256": _sha256(path),
                }
                for path in files
            ],
        },
        "runtime": {
            "python": sys.version.split()[0],
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "packages": packages,
        },
        "git": _git_state(),
    }


def write_manifest(path: str | Path, manifest: dict[str, Any]) -> Path:
    destination = Path(path)
    destination.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return destination
