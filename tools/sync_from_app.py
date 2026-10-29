#!/usr/bin/env python3
"""
Sync OpenPIWIS features from features.yaml into src/data/features.json.
Allows the public peeweesys.com website to accurately reflect live vehicle testing,
bench extraction, and roadmap milestones from the core diagnostic engine.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Warning: pyyaml is not installed. Trying to read via json or fallback.")
    yaml = None


def find_features_yaml():
    env_path = os.environ.get("OPENPIWIS_FEATURES_YAML")
    if env_path and os.path.exists(env_path):
        return Path(env_path)

    candidates = [
        Path("D:/PIWIS Reverse Engineering/docs/features.yaml"),
        Path("../PIWIS Reverse Engineering/docs/features.yaml"),
        Path("../../PIWIS Reverse Engineering/docs/features.yaml"),
        Path(__file__).resolve().parent.parent / "data_source" / "features.yaml",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def sync():
    repo_root = Path(__file__).resolve().parent.parent
    output_path = repo_root / "src" / "data" / "features.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    yaml_path = find_features_yaml()

    if not yaml_path:
        print("Warning: Could not locate features.yaml in standard locations.")
        if output_path.exists():
            print(f"Keeping existing {output_path}")
            return
        else:
            print("Creating starter features.json fallback.")
            data = {
                "last_synced": datetime.now(timezone.utc).isoformat(),
                "stats": {"total": 0, "done": 0, "percent": 0},
                "items": []
            }
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return

    print(f"Reading features from {yaml_path}...")
    if yaml is None:
        print("Error: PyYAML required to parse features.yaml. Run: pip install pyyaml")
        sys.exit(1)

    with open(yaml_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    milestones = raw.get("milestones", {})
    items = raw.get("items", [])

    total = len(items)
    done_count = sum(1 for item in items if item.get("status") == "done")
    percent = round((done_count / total * 100), 1) if total > 0 else 0

    # Categorize highlights for the web UI
    categorized = {
        "car_verified_9x6": [],
        "bench_extracted_9x7": [],
        "power_features": [],
        "safety_and_reports": [],
        "all_items": items,
    }

    for item in items:
        status = item.get("status", "pending")
        item_id = item.get("id", "")
        platform = item.get("platform", "")
        title = item.get("title", "")

        # Map to display categories
        if platform == "9x6" and status == "done":
            categorized["car_verified_9x6"].append(item)
        if platform in ["9x7", "E1"]:
            categorized["bench_extracted_9x7"].append(item)
        if any(kw in title.lower() or kw in item_id.lower() for kw in ["rom", "gauge", "speedo", "over-rev", "mileage", "hours", "coding", "ram"]):
            categorized["power_features"].append(item)
        if any(kw in title.lower() or kw in item_id.lower() for kw in ["report", "clear", "safe", "fault", "dtc", "freeze"]):
            categorized["safety_and_reports"].append(item)

    payload = {
        "last_synced": datetime.now(timezone.utc).isoformat(),
        "stats": {
            "total": total,
            "done": done_count,
            "percent": percent
        },
        "milestones": milestones,
        "summary": {
            "car_verified_count": len(categorized["car_verified_9x6"]),
            "bench_extracted_count": len(categorized["bench_extracted_9x7"]),
            "power_features_count": len(categorized["power_features"]),
        },
        "highlighted": {
            "car_verified_9x6": categorized["car_verified_9x6"][:10],
            "bench_extracted_9x7": categorized["bench_extracted_9x7"][:10],
            "power_features": categorized["power_features"][:10],
            "safety_and_reports": categorized["safety_and_reports"][:10],
        },
        "items": items
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"Successfully synced {total} features ({done_count} completed, {percent}%) to {output_path}")


if __name__ == "__main__":
    sync()
