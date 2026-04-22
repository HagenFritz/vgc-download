"""Fetch Pokemon Champions VGC tournament stats from Pikalytics and emit a
chaos-JSON-shaped file that process_stats.py can consume.

Pikalytics exposes AI-optimized markdown per Pokemon at:
    https://www.pikalytics.com/ai/pokedex/championstournaments/<Name>

And an index at:
    https://www.pikalytics.com/ai/pokedex/championstournaments

This script parses the index for the ranked Pokemon list, fetches each
Pokemon's AI markdown, and synthesizes a chaos-shaped JSON with counts derived
from a fixed synthetic battle total (counts are only relative — percentages
come out the same through process_stats.py).

Usage:
    uv run python scripts/fetch_pikalytics_champions.py

Output:
    data/stats/raw/reg_m-a_chaos.json

Then run:
    uv run python scripts/process_stats.py reg_m-a_chaos.json reg_m-a

Source: Pikalytics (https://www.pikalytics.com) — CC BY-NC 4.0.
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_PATH = DATA_DIR / "stats" / "raw" / "reg_m-a_chaos.json"

INDEX_URL = "https://www.pikalytics.com/ai/pokedex/championstournaments"
POKEMON_URL_TEMPLATE = "https://www.pikalytics.com/ai/pokedex/championstournaments/{slug}"

# Synthetic battle total. Process_stats.py converts raw counts back to
# percentages per Pokemon, so the absolute number is arbitrary. Pick something
# large enough that 0.01% still rounds to a non-zero integer.
SYNTHETIC_BATTLES = 100_000

# Pikalytics rate-limiting: be polite.
REQUEST_DELAY_SEC = 0.5

USER_AGENT = "vgc-download/0.1 (github.com/HagenFritz/vgc-download)"


def normalize_key(name: str) -> str:
    """Match process_stats.py's name-normalization for moves/items/abilities."""
    return (
        name.lower()
        .replace(" ", "")
        .replace("-", "")
        .replace("'", "")
        .replace(".", "")
    )


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_index(markdown: str) -> list[tuple[str, str, float]]:
    """Extract (display_name, url_slug, usage_pct) from the index markdown.

    Index rows look like:
        | 1 | **Incineroar** | 51.18% | [View](...Incineroar) | [AI](.../Incineroar) |
    """
    pattern = re.compile(
        r"^\|\s*\d+\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*([\d.]+)%\s*\|.*?/([^/)]+)\)\s*\|",
        re.MULTILINE,
    )
    results = []
    for match in pattern.finditer(markdown):
        display_name = match.group(1).strip()
        usage_pct = float(match.group(2))
        # The last captured URL-tail is the AI slug; verify.
        slug = match.group(3).strip()
        results.append((display_name, slug, usage_pct))
    return results


def parse_percent_section(markdown: str, section: str) -> dict[str, float]:
    """Extract a `## <section>` block's `- **Name**: NN.NNN%` bullets.

    Returns {name: percentage}.
    """
    heading = re.escape(section)
    block_re = re.compile(
        rf"##\s+{heading}\s*\n(.*?)(?=\n##\s+|\Z)",
        re.DOTALL | re.IGNORECASE,
    )
    block_match = block_re.search(markdown)
    if not block_match:
        return {}
    block = block_match.group(1)

    entries = {}
    # Match lines like: - **Fake Out**: 99.047%
    line_re = re.compile(r"^-\s*\*\*([^*]+)\*\*\s*:\s*([\d.]+)%", re.MULTILINE)
    for m in line_re.finditer(block):
        name = m.group(1).strip()
        pct = float(m.group(2))
        entries[name] = pct
    return entries


def pct_to_count(pct: float, total: int) -> int:
    return max(1, round(pct / 100.0 * total))


def build_pokemon_block(markdown: str, usage_pct: float) -> dict:
    """Synthesize a chaos-shaped dict for one Pokemon from its AI markdown."""
    raw_count = pct_to_count(usage_pct, SYNTHETIC_BATTLES)

    # Per-Pokemon sections: percentages are relative to the Pokemon's own
    # appearance count (i.e., they roughly sum to 400% for moves since a mon
    # runs 4 moves, 100% for items/abilities, sum of teammate %s up to 500%).
    # We scale them back to counts using raw_count.
    moves_pct = parse_percent_section(markdown, "Common Moves")
    abilities_pct = parse_percent_section(markdown, "Common Abilities")
    items_pct = parse_percent_section(markdown, "Common Items")
    teammates_pct = parse_percent_section(markdown, "Common Teammates")

    # Pikalytics data sometimes includes typo'd variants of the same item
    # (e.g., "Floettite", "floettite", "Floetitte" for the Mega Stone). Sum
    # counts into the normalized key instead of overwriting.
    def accumulate(pct_map: dict[str, float]) -> dict[str, int]:
        out: dict[str, int] = {}
        for name, pct in pct_map.items():
            key = normalize_key(name)
            out[key] = out.get(key, 0) + pct_to_count(pct, raw_count)
        return out

    moves = accumulate(moves_pct)
    abilities = accumulate(abilities_pct)
    items = accumulate(items_pct)
    # Teammates: keep display names (process_stats.py treats teammate keys as
    # Pokemon names, not normalized move/item keys).
    teammates = {k: pct_to_count(v, raw_count) for k, v in teammates_pct.items()}

    return {
        "Raw count": raw_count,
        "Viability Ceiling": [0, 0, 0, 0],
        "Abilities": abilities,
        "Items": items,
        "Spreads": {},  # Not exposed by Pikalytics AI markdown
        "Moves": moves,
        "Tera Types": {},  # Not relevant for Champions
        "Happiness": {},
        "Teammates": teammates,
        "Checks and Counters": {},
        "usage": usage_pct / 100.0,
    }


def main() -> int:
    print(f"Fetching index: {INDEX_URL}", file=sys.stderr)
    try:
        index_md = fetch(INDEX_URL)
    except urllib.error.URLError as e:
        print(f"ERROR: failed to fetch index: {e}", file=sys.stderr)
        return 1

    entries = parse_index(index_md)
    if not entries:
        print("ERROR: parsed no Pokemon from index — site format may have changed", file=sys.stderr)
        return 1

    print(f"Found {len(entries)} Pokemon in index. Fetching each...", file=sys.stderr)

    pokemon_blocks: dict[str, dict] = {}
    for i, (display_name, slug, usage_pct) in enumerate(entries, 1):
        url = POKEMON_URL_TEMPLATE.format(slug=slug)
        print(f"  [{i}/{len(entries)}] {display_name} ({usage_pct}%) — {slug}", file=sys.stderr)
        try:
            md = fetch(url)
        except urllib.error.URLError as e:
            print(f"    WARN: skip {display_name} — {e}", file=sys.stderr)
            continue

        pokemon_blocks[display_name] = build_pokemon_block(md, usage_pct)
        time.sleep(REQUEST_DELAY_SEC)

    output = {
        "info": {
            "metagame": "championstournaments",
            "cutoff": 0,
            "cutoff deviation": 0,
            "team type": None,
            "number of battles": SYNTHETIC_BATTLES,
            "source": "pikalytics.com",
            "source_url": INDEX_URL,
            "license": "CC BY-NC 4.0",
        },
        "data": pokemon_blocks,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n")

    print(f"\nWrote {OUTPUT_PATH}", file=sys.stderr)
    print(f"Pokemon captured: {len(pokemon_blocks)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
