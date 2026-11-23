#!/usr/bin/env python3
"""Regression checks: supplemental catalogs survive refresh_from_llms rewriting."""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "refresh_from_llms.py"


def load_refresh():
    spec = importlib.util.spec_from_file_location("refresh_from_llms", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


class SupplementalPreservationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mod = load_refresh()

    def test_extract_supplemental_section(self) -> None:
        prior = (
            "# Salesforce Developer Documentation — Content List (Index)\n\n"
            "| # | Status | Product | Folder | Description |\n"
            "|---|---|---------|---------------|--------------|\n"
            "| 1 | ✅ | Code Analyzer | [folder](code-analyzer/) | Static analysis. |\n\n"
            "## Supplemental catalogs (outside `llms.txt`)\n\n"
            "These folders are maintained by hand.\n\n"
            "| Status | Product | Folder | Description |\n"
            "|---|---|---|---|\n"
            "| ✅ | SF Pi | [folder](sf-pi/) | Pi bundle. |\n"
        )
        got = self.mod.extract_supplemental_section(prior)
        self.assertTrue(got.startswith("## Supplemental catalogs (outside `llms.txt`)"))
        self.assertIn("[folder](sf-pi/)", got)
        self.assertNotIn("| 1 | ✅ | Code Analyzer", got)

    def test_sf_pi_not_reported_as_disappeared(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("code-analyzer", "sf-pi", "retired-area"):
                d = root / name
                d.mkdir()
                (d / "index.md").write_text("# index\n", encoding="utf-8")
            (root / "scripts").mkdir()
            old_root = self.mod.ROOT
            try:
                self.mod.ROOT = root
                gone = self.mod.disappeared_slugs({"code-analyzer"})
            finally:
                self.mod.ROOT = old_root
            self.assertEqual(gone, ["retired-area"])
            self.assertNotIn("sf-pi", gone)

    def test_rewritten_list_keeps_supplement(self) -> None:
        """Simulate the list-file rewrite path without network fetches."""
        prior = (
            "# old\n\n"
            "| # | Status | Product | Folder | Description |\n"
            "|---|---|---------|---------------|--------------|\n"
            "| 1 | ✅ | X | [folder](x/) | d |\n\n"
            "## Supplemental catalogs (outside `llms.txt`)\n\n"
            "| Status | Product | Folder | Description |\n"
            "|---|---|---|---|\n"
            "| ✅ | SF Pi | [folder](sf-pi/) | keep me |\n"
        )
        supplemental = self.mod.extract_supplemental_section(prior)
        rows = ["| 1 | ✅ | Code Analyzer | [folder](code-analyzer/) | Static analysis. |"]
        gone = ["retired-area"]
        lst = [
            "# Salesforce Developer Documentation — Content List (Index)",
            "",
            "| # | Status | Product | Folder | Description |",
            "|---|---|---------|---------------|--------------|",
            *rows,
            "",
            "## No longer listed in llms.txt",
            "",
            *[f"- [{g}]({g}/) — kept as an archived snapshot" for g in gone],
            "",
        ]
        if supplemental:
            if lst[-1] != "":
                lst.append("")
            lst.append(supplemental.rstrip("\n"))
            lst.append("")
        out = "\n".join(lst)
        self.assertIn("## Supplemental catalogs (outside `llms.txt`)", out)
        self.assertIn("[folder](sf-pi/)", out)
        self.assertIn("retired-area", out)
        # Supplement must appear after the numbered table rewrite, not be dropped.
        self.assertGreater(out.index("## Supplemental catalogs"), out.index("code-analyzer"))


if __name__ == "__main__":
    sys.exit(0 if unittest.main(verbosity=2) else 1)
