"""Process raw Smogon chaos JSON into a filtered meta snapshot.

Filters Pokemon to those in the target regulation's allowed_pokemon list,
filters items to those in the Champions legal items list, converts raw counts
to percentages, and keeps only the most relevant data per Pokemon.

Usage:
    uv run python scripts/process_stats.py <raw_file> <regulation_id>

Example:
    uv run python scripts/process_stats.py reg_i_chaos.json reg_m-a
"""

import json
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

# How many entries to keep per category
TOP_ITEMS = 3
TOP_MOVES = 10
TOP_TEAMMATES = 10
TOP_SPREADS = 5


def normalize_name(name: str) -> str:
    """Normalize a name for comparison: lowercase, strip spaces/hyphens/punctuation."""
    return name.lower().replace(" ", "").replace("-", "").replace("'", "").replace(".", "")


def load_regulation(regulation_id: str) -> dict:
    path = DATA_DIR / "regulations" / f"{regulation_id}.json"
    if not path.exists():
        print(f"ERROR: Regulation file not found: {path}", file=sys.stderr)
        sys.exit(1)
    return json.loads(path.read_text())


def load_items() -> set[str]:
    path = DATA_DIR / "stats" / "items" / "champions_items.json"
    if not path.exists():
        print(f"ERROR: Items file not found: {path}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(path.read_text())
    return {normalize_name(item) for item in data["items"]}


def load_raw_stats(filename: str) -> dict:
    path = DATA_DIR / "stats" / "raw" / filename
    if not path.exists():
        print(f"ERROR: Raw stats file not found: {path}", file=sys.stderr)
        sys.exit(1)
    return json.loads(path.read_text())


def to_top_n_pct(counts: dict, n: int, total: int | None = None) -> list[dict]:
    """Convert a {name: count} dict to a sorted top-N list with percentages."""
    if total is None:
        total = sum(counts.values())
    if total == 0:
        return []

    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n]
    return [
        {"name": name, "usage": round(count / total * 100, 1)}
        for name, count in sorted_items
        if count > 0
    ]


def process_pokemon(name: str, data: dict, legal_items: set[str]) -> dict:
    raw_count = data.get("Raw count", 0)

    # Abilities — keep all, convert to percentages
    abilities = to_top_n_pct(data.get("Abilities", {}), n=99)

    # Items — filter to legal items, then top N
    raw_items = data.get("Items", {})
    legal_item_counts = {
        k: v for k, v in raw_items.items()
        if normalize_name(k) in legal_items and k != "nothing"
    }
    items = to_top_n_pct(legal_item_counts, TOP_ITEMS, total=raw_count)

    # Moves — top N
    moves = to_top_n_pct(
        {k: v for k, v in data.get("Moves", {}).items() if k},  # filter empty string
        TOP_MOVES,
        total=raw_count,
    )

    # Teammates — top N (already proper names in chaos data)
    teammates = to_top_n_pct(data.get("Teammates", {}), TOP_TEAMMATES, total=raw_count)

    # Spreads — top N
    raw_spreads = data.get("Spreads", {})
    sorted_spreads = sorted(raw_spreads.items(), key=lambda x: x[1], reverse=True)[:TOP_SPREADS]
    spreads_total = sum(raw_spreads.values())
    spreads = []
    for spread_str, count in sorted_spreads:
        # Format: "Nature:HP/Atk/Def/SpA/SpD/Spe"
        parts = spread_str.split(":")
        if len(parts) == 2:
            nature = parts[0]
            evs = parts[1]
            spreads.append({
                "nature": nature,
                "evs": evs,
                "usage": round(count / spreads_total * 100, 1) if spreads_total else 0,
            })

    return {
        "usage": round(data.get("usage", 0) * 100, 2),
        "abilities": abilities,
        "items": items,
        "moves": moves,
        "teammates": teammates,
        "spreads": spreads,
    }


def main():
    if len(sys.argv) != 3:
        print("Usage: uv run python scripts/process_stats.py <raw_file> <regulation_id>")
        print("Example: uv run python scripts/process_stats.py reg_i_chaos.json reg_m-a")
        sys.exit(1)

    raw_file = sys.argv[1]
    regulation_id = sys.argv[2]

    regulation = load_regulation(regulation_id)
    legal_items = load_items()
    raw_stats = load_raw_stats(raw_file)

    # Build lookups
    allowed = {normalize_name(p): p for p in regulation["allowed_pokemon"]}
    chaos_normalized = {normalize_name(n): n for n in raw_stats["data"]}

    # Match chaos data names to regulation names
    # 1. Exact normalized match
    # 2. Sub-form match: regulation "Rotom" matches chaos "Rotom-Wash", "Rotom-Heat", etc.
    #    In this case, include each sub-form as a separate entry under the parent name
    #    with the sub-form noted (e.g., "Rotom (Wash)")
    processed = {}
    matched = 0
    for norm_reg, canonical_name in allowed.items():
        if norm_reg in chaos_normalized:
            # Exact match
            chaos_name = chaos_normalized[norm_reg]
            processed[canonical_name] = process_pokemon(
                chaos_name, raw_stats["data"][chaos_name], legal_items
            )
            matched += 1
        else:
            # Check for sub-forms: chaos names that start with this regulation name
            # e.g., regulation "Rotom" matches "Rotom-Wash", "Rotom-Heat", etc.
            # Each sub-form gets its own entry — they run completely different sets
            sub_forms = []
            for norm_chaos, chaos_name in chaos_normalized.items():
                if norm_chaos.startswith(norm_reg) and norm_chaos != norm_reg:
                    sub_forms.append(chaos_name)

            if sub_forms:
                for chaos_name in sub_forms:
                    entry = process_pokemon(
                        chaos_name, raw_stats["data"][chaos_name], legal_items
                    )
                    processed[chaos_name] = entry
                matched += 1

    # Sort by usage descending
    processed = dict(sorted(processed.items(), key=lambda x: x[1]["usage"], reverse=True))

    output = {
        "regulation_id": regulation_id,
        "source_file": raw_file,
        "source_metagame": raw_stats.get("info", {}).get("metagame", "unknown"),
        "source_battles": raw_stats.get("info", {}).get("number of battles", 0),
        "pokemon_matched": matched,
        "pokemon_in_regulation": len(regulation["allowed_pokemon"]),
        "note": f"Stats from {raw_stats.get('info', {}).get('metagame', 'unknown')} filtered to {regulation_id} legal Pokemon and Champions legal items.",
        "pokemon": processed,
    }

    # Write to processed directory
    output_path = DATA_DIR / "stats" / "processed" / f"{regulation_id}_meta.json"
    output_path.write_text(json.dumps(output, indent=2) + "\n")
    print(f"Wrote {output_path}")
    print(f"Matched {matched}/{len(regulation['allowed_pokemon'])} regulation Pokemon")
    print(f"Source: {raw_stats.get('info', {}).get('metagame')} ({raw_stats.get('info', {}).get('number of battles')} battles)")


if __name__ == "__main__":
    main()
