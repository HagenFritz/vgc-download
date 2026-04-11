"""
Filter the full pokedex to a regulation-specific subset.
Matches regulation allowed_pokemon names against the pokedex.

Usage:
    uv run python scripts/filter_pokemon_db.py <regulation_id>

Example:
    uv run python scripts/filter_pokemon_db.py reg_m-a
"""

import json
import sys
from difflib import get_close_matches
from pathlib import Path
from typing import Any

POKEDEX_FILE = Path("data/pokemon_db/pokedex.json")
REGULATIONS_DIR = Path("data/regulations")
OUTPUT_DIR = Path("data/pokemon_db")

# When a regulation lists a base name (e.g., "Aegislash") but PokeAPI stores
# specific forms ("Aegislash-Shield", "Aegislash-Blade"), prefer these suffixes
# as the default/base form.
DEFAULT_FORM_SUFFIXES = [
    "-Male", "-Shield", "-Midday", "-Disguised", "-Zero",
    "-Full-Belly", "-Average", "-Family-Of-Three",
    "-Combat-Breed",
]


def normalize(name: str) -> str:
    """Normalize a name for fuzzy matching."""
    return name.lower().replace("-", "").replace(" ", "").replace(".", "")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: uv run python scripts/filter_pokemon_db.py <regulation_id>", file=sys.stderr)
        print("Example: uv run python scripts/filter_pokemon_db.py reg_m-a", file=sys.stderr)
        sys.exit(1)

    regulation_id = sys.argv[1]
    reg_file = REGULATIONS_DIR / f"{regulation_id}.json"

    if not POKEDEX_FILE.exists():
        print(f"Error: {POKEDEX_FILE} not found. Run fetch_pokemon_db.py first.", file=sys.stderr)
        sys.exit(1)

    if not reg_file.exists():
        print(f"Error: {reg_file} not found.", file=sys.stderr)
        sys.exit(1)

    pokedex: dict[str, Any] = json.loads(POKEDEX_FILE.read_text())
    regulation: dict[str, Any] = json.loads(reg_file.read_text())

    allowed = regulation.get("allowed_pokemon", [])
    print(f"Regulation: {regulation.get('regulation', regulation_id)}")
    print(f"Allowed Pokemon: {len(allowed)}")
    print(f"Pokedex entries: {len(pokedex)}")

    # Build normalized lookup for pokedex
    norm_to_name: dict[str, str] = {}
    for name in pokedex:
        norm_to_name[normalize(name)] = name

    # Build prefix lookup: "aegislash" -> ["Aegislash-Shield", "Aegislash-Blade"]
    prefix_to_names: dict[str, list[str]] = {}
    for name in pokedex:
        base = name.split("-")[0]
        norm_base = normalize(base)
        prefix_to_names.setdefault(norm_base, []).append(name)

    matched: dict[str, Any] = {}
    unmatched: list[str] = []

    for reg_name in allowed:
        # Try exact match first
        if reg_name in pokedex:
            matched[reg_name] = pokedex[reg_name]
            continue

        # Try normalized match
        norm = normalize(reg_name)
        if norm in norm_to_name:
            pokedex_name = norm_to_name[norm]
            matched[reg_name] = pokedex[pokedex_name]
            continue

        # Try prefix match: regulation says "Aegislash" but pokedex has
        # "Aegislash-Shield" and "Aegislash-Blade". Pick the default form.
        norm_base = normalize(reg_name.split("-")[0]) if "-" in reg_name else norm
        candidates = prefix_to_names.get(norm_base, [])
        matching = [c for c in candidates if normalize(c).startswith(norm)]
        if matching:
            pick = None
            for suffix in DEFAULT_FORM_SUFFIXES:
                for c in matching:
                    if c.endswith(suffix):
                        pick = c
                        break
                if pick:
                    break
            if not pick:
                # Fallback: alphabetical first. May not be the ideal default.
                pick = sorted(matching)[0]
                print(f"  Warning: no default suffix matched for {reg_name}, fell back to {pick}", file=sys.stderr)
            else:
                print(f"  Form resolved: {reg_name} -> {pick}")
            matched[reg_name] = pokedex[pick]
            continue

        # No match
        unmatched.append(reg_name)

    print(f"\nMatched: {len(matched)}/{len(allowed)}")

    if unmatched:
        print(f"Unmatched: {len(unmatched)}", file=sys.stderr)
        all_norm = list(norm_to_name.keys())
        for name in unmatched:
            close = get_close_matches(normalize(name), all_norm, n=3, cutoff=0.7)
            suggestions = [norm_to_name[c] for c in close]
            if suggestions:
                print(f"  {name} — close matches: {', '.join(suggestions)}", file=sys.stderr)
            else:
                print(f"  {name} — no close matches", file=sys.stderr)

    output_file = OUTPUT_DIR / f"{regulation_id}_pokemon.json"
    output = {
        "regulation_id": regulation_id,
        "regulation": regulation.get("regulation", regulation_id),
        "total_in_regulation": len(allowed),
        "total_matched": len(matched),
        "unmatched": unmatched,
        "pokemon": matched,
    }

    output_file.write_text(json.dumps(output, indent=2))
    print(f"\nWritten to {output_file}")


if __name__ == "__main__":
    main()
