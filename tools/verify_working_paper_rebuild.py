#!/usr/bin/env python3
"""Rebuild designated derived artifacts and verify byte identity without Git metadata."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "docs/research/working-paper"
TARGETS = [
    PACKAGE / "WHU_WORKING_PAPER_EXACT_NUMBER_MANIFEST.json",
    PACKAGE / "WHU_WORKING_PAPER_MANUSCRIPT.html",
    *sorted((PACKAGE / "figures").glob("*.svg")),
]


def main() -> None:
    before = {path: path.read_bytes() for path in TARGETS}
    subprocess.run([sys.executable, "tools/build_working_paper_artifacts.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "tools/render_working_paper.py"], cwd=ROOT, check=True)
    changed = [path.relative_to(ROOT).as_posix() for path, content in before.items() if path.read_bytes() != content]
    if changed:
        print("FAIL")
        for path in changed:
            print(f"- rebuilt bytes differ: {path}")
        raise SystemExit(1)
    print("PASS: 6 figures, exact-number manifest, and manuscript HTML rebuilt byte-identically")


if __name__ == "__main__":
    main()
