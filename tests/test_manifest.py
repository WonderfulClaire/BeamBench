from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from beambench.manifest import build_manifest, write_manifest


class ManifestTests(unittest.TestCase):
    def test_manifest_hashes_source_and_records_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "results.csv"
            source.write_text("a,b\n1,2\n", encoding="utf-8")
            manifest = build_manifest(
                source=source,
                baseline="DAS",
                rows=1,
                methods=["DAS"],
                metrics=["snr_db"],
            )
            self.assertEqual(manifest["schema_version"], 1)
            self.assertEqual(manifest["command"]["baseline"], "DAS")
            self.assertEqual(manifest["dataset"]["rows"], 1)
            self.assertEqual(len(manifest["dataset"]["source_files"]), 1)
            self.assertEqual(len(manifest["dataset"]["source_files"][0]["sha256"]), 64)
            self.assertIn("python", manifest["runtime"])
            self.assertIn("git", manifest)

            output = Path(directory) / "manifest.json"
            write_manifest(output, manifest)
            loaded = json.loads(output.read_text("utf-8"))
            self.assertEqual(loaded["dataset"]["methods"], ["DAS"])


if __name__ == "__main__":
    unittest.main()
