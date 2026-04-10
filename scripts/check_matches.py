"""Check which regulation Pokemon didn't match chaos data and find close matches.

Usage:
    uv run python scripts/check_matches.py reg_i_chaos.json reg_m-a
"""

import json
import sys
from pathlib import Path
from difflib import get_close_matches

DATA_DIR = Path(__file__).parent.parent / "data"


def normalize_name(name: str) -> str:
    return name.lower().replace(" ", "").replace("-", "").replace("'", "").replace(".", "")


def main():
    raw_file = sys.argv[1]
    regulation_id = sys.argv[2]

    reg = json.loads((DATA_DIR / "regulations" / f"{regulation_id}.json").read_text())
    raw = json.loads((DATA_DIR / "stats" / "raw" / raw_file).read_text())

    # Build lookups
    chaos_names = list(raw["data"].keys())
    chaos_normalized = {normalize_name(n): n for n in chaos_names}

    reg_pokemon = reg["allowed_pokemon"]

    matched = []
    unmatched = []

    for reg_name in reg_pokemon:
        norm = normalize_name(reg_name)
        if norm in chaos_normalized:
            matched.append(reg_name)
        else:
            # Find close matches using difflib
            close = get_close_matches(reg_name, chaos_names, n=3, cutoff=0.5)
            unmatched.append((reg_name, close))

    print(f"Matched: {len(matched)}/{len(reg_pokemon)}")
    print(f"Unmatched: {len(unmatched)}")
    print()
    print("=== UNMATCHED POKEMON ===")
    print()
    for reg_name, close in unmatched:
        if close:
            print(f"  {reg_name:30s} -> close matches: {close}")
        else:
            print(f"  {reg_name:30s} -> no close matches in chaos data")


if __name__ == "__main__":
    main()
