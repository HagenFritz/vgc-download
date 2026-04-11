"""
Fetch base stats, types, and abilities for all Pokemon from PokeAPI.
Writes to data/pokemon_db/pokedex.json.

Usage:
    uv run python scripts/fetch_pokemon_db.py
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Any

import httpx

API_BASE = "https://pokeapi.co/api/v2"
OUTPUT_DIR = Path("data/pokemon_db")
OUTPUT_FILE = OUTPUT_DIR / "pokedex.json"
CONCURRENCY = 10


def format_name(name: str) -> str:
    """Convert PokeAPI lowercase name to Showdown-style display name.

    Examples:
        charizard -> Charizard
        charizard-mega-x -> Charizard-Mega-X
        raichu-alola -> Raichu-Alola
        tauros-paldea-combat-breed -> Tauros-Paldea-Combat-Breed
        porygon2 -> Porygon2
        porygon-z -> Porygon-Z
        mr-mime -> Mr-Mime
    """
    return "-".join(part.capitalize() for part in name.split("-"))


def format_type(type_name: str) -> str:
    """Capitalize type name."""
    return type_name.capitalize()


def parse_pokemon(data: dict[str, Any]) -> dict[str, Any]:
    """Extract base stats, types, and abilities from a PokeAPI pokemon response."""
    stats = {}
    stat_map = {
        "hp": "hp",
        "attack": "atk",
        "defense": "def",
        "special-attack": "spa",
        "special-defense": "spd",
        "speed": "spe",
    }
    for stat in data["stats"]:
        key = stat_map[stat["stat"]["name"]]
        stats[key] = stat["base_stat"]

    types = [format_type(t["type"]["name"]) for t in sorted(data["types"], key=lambda t: t["slot"])]

    abilities = []
    for a in sorted(data["abilities"], key=lambda a: a["slot"]):
        abilities.append({
            "name": a["ability"]["name"].replace("-", " ").title(),
            "hidden": a["is_hidden"],
        })

    return {
        "types": types,
        "base_stats": stats,
        "abilities": abilities,
    }


async def fetch_pokemon_list(client: httpx.AsyncClient) -> list[dict[str, Any]]:
    """Fetch the full list of Pokemon names and URLs."""
    entries: list[dict[str, Any]] = []
    url = f"{API_BASE}/pokemon?limit=2000"
    while url:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
        entries.extend(data["results"])
        url = data.get("next")
    return entries


async def fetch_one(client: httpx.AsyncClient, semaphore: asyncio.Semaphore, url: str) -> dict[str, Any] | None:
    """Fetch a single Pokemon's data with concurrency limiting."""
    async with semaphore:
        try:
            resp = await client.get(url, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as e:
            print(f"  Failed: {url} — {e}", file=sys.stderr)
            return None


async def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    async with httpx.AsyncClient() as client:
        try:
            print("Fetching Pokemon list...")
            entries = await fetch_pokemon_list(client)
        except httpx.RequestError as e:
            print(f"Error: Failed to fetch Pokemon list — {e}", file=sys.stderr)
            sys.exit(1)

        print(f"Found {len(entries)} Pokemon (including forms)")

        semaphore = asyncio.Semaphore(CONCURRENCY)
        start = time.time()

        print(f"Fetching data for all {len(entries)} Pokemon ({CONCURRENCY} concurrent)...")
        tasks = [fetch_one(client, semaphore, entry["url"]) for entry in entries]
        results = await asyncio.gather(*tasks)

        elapsed = time.time() - start
        print(f"Fetched in {elapsed:.1f}s")

    pokedex: dict[str, Any] = {}
    failed = 0
    for entry, result in zip(entries, results):
        if result is None:
            failed += 1
            continue
        name = format_name(entry["name"])
        pokedex[name] = parse_pokemon(result)

    print(f"\nParsed {len(pokedex)} Pokemon ({failed} failed)")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(pokedex, f, indent=2)

    print(f"Written to {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
