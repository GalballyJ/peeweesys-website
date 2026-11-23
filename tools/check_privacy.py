#!/usr/bin/env python3
"""Fail-closed privacy gate for D:\peeweesys-website.

Blocks real owner VINs and UK registration plates from leaking into src/ or public/.
Allows:
  - Explicitly masked placeholder VINs (WP0ZZZ98Z1S000000, WP0CB29811U62xxxx)
  - The technical ECU ROM filename 'y966ohc' / 'y966ohc.ori' ONLY inside public/developers/
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCAN_DIRS = [ROOT / "src", ROOT / "public"]
TEXT_EXTS = {".html", ".astro", ".js", ".ts", ".json", ".md", ".txt", ".a2l", ".xdf", ".css", ".svg"}

ALLOWED_VINS = {
    "WP0ZZZ98Z1S000000",
    "WP0CB29811U62XXXX",
}

BLOCKED_VINS = [
    re.compile(r"WP0ZZZ98Z1S641241", re.I),
    re.compile(r"WP0ZZZ99Z1V000996", re.I),
    re.compile(r"WP0ZZZ98Z1V000986", re.I),
]
ANY_WP0 = re.compile(r"WP0[A-Z0-9]{14}", re.I)
REG_SPACED = re.compile(r"\bY966\s+OHC\b", re.I)
REG_UPPER = re.compile(r"\bY966OHC\b")
ROM_NAME = re.compile(r"y966\s*ohc", re.I)


def main() -> int:
    violations = []
    for base in SCAN_DIRS:
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file() or p.suffix.lower() not in TEXT_EXTS:
                continue
            rel = p.relative_to(ROOT).as_posix()
            txt = p.read_text(encoding="utf-8", errors="ignore")

            for rx in BLOCKED_VINS:
                if rx.search(txt):
                    violations.append(f"{rel}: blocked real/demo VIN matched ({rx.pattern})")

            for m in ANY_WP0.finditer(txt):
                val = m.group(0).upper()
                if val not in ALLOWED_VINS:
                    violations.append(f"{rel}: unmasked WP0 VIN found ({val})")

            if REG_SPACED.search(txt) or REG_UPPER.search(txt):
                violations.append(f"{rel}: UK registration plate (Y966 OHC / Y966OHC) found")

            if not rel.startswith("public/developers/") and ROM_NAME.search(txt):
                violations.append(f"{rel}: 'y966ohc' referenced outside public/developers/")

    if violations:
        print("PRIVACY GATE FAILED:")
        for v in violations:
            print("  -", v)
        return 1

    print("PRIVACY GATE PASS: 0 unmasked VINs or registration leaks in src/ and public/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
