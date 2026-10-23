"""Inspect JSONL without loading a model or printing toxic examples."""
import argparse
import json
from pathlib import Path


def validate(path: Path) -> dict:
    pairs = set()
    rows = 0
    with path.open(encoding="utf-8") as source:
        for number, line in enumerate(source, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"Line {number}: expected an object")
            for field in ("input", "output"):
                if not isinstance(row.get(field), str) or not row[field].strip():
                    raise ValueError(f"Line {number}: non-empty {field} is required")
            pairs.add((row["input"].strip(), row["output"].strip()))
            rows += 1
    if not rows:
        raise ValueError("The dataset is empty")
    return {"rows": rows, "unique_pairs": len(pairs), "duplicate_pairs": rows - len(pairs)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=Path(__file__).with_name("total.jsonl"))
    print(json.dumps(validate(parser.parse_args().path), ensure_ascii=False, indent=2))
