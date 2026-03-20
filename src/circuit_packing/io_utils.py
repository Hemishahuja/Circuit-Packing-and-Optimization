from __future__ import annotations

import csv
import json
from pathlib import Path


def ensure_output_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_counts_csv(path: Path, separated_counts: list[dict[str, int]]) -> None:
    rows: list[dict[str, str | int]] = []
    for copy_index, counts in enumerate(separated_counts, start=1):
        for bitstring, value in sorted(counts.items()):
            rows.append({"copy": copy_index, "bitstring": bitstring, "count": value})

    with path.open("w", newline="", encoding="utf-8") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=["copy", "bitstring", "count"])
        writer.writeheader()
        writer.writerows(rows)
