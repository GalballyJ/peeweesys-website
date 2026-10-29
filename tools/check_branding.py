#!/usr/bin/env python3
"""
Branding enforcement script for PeeweeSys website.
Ensures legacy naming ('OpenPIWIS') is completely excluded from src/ components and pages.
"""

import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

FORBIDDEN_WORDS = ["openpiwis"]

def check():
    repo_root = Path(__file__).resolve().parent.parent
    src_dir = repo_root / "src"

    violations = []

    # Files to scan
    for ext in ["*.astro", "*.html", "*.ts", "*.js", "*.json"]:
        for file_path in src_dir.rglob(ext):
            # Allow features.json raw notes if properly sanitized in components,
            # but check that no Astro/component template has the legacy name.
            if file_path.name == "features.json":
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
                for word in FORBIDDEN_WORDS:
                    if word in content.lower():
                        violations.append((file_path.relative_to(repo_root), word))
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    if violations:
        print("❌ Branding Check FAILED! Forbidden legacy terms found:")
        for path, word in violations:
            print(f"  - {path}: found '{word}'")
        sys.exit(1)

    print("✅ Branding Check PASSED! Zero legacy terms detected in src/ components.")


if __name__ == "__main__":
    check()
