"""Parse the Serebii Pokemon Champions items page into structured JSON.

Downloads and parses /tmp/champions_items.html (fetched via curl).
Extracts item names from the Hold Items, Mega Stones, and Berries sections.
Skips Miscellaneous Items (non-battle items like Affinity Tickets).

Usage:
    curl -s -o /tmp/champions_items.html "https://www.serebii.net/pokemonchampions/items.shtml"
    uv run python scripts/parse_items.py
"""

import json
from bs4 import BeautifulSoup

# Sections that contain battle-relevant items
BATTLE_SECTIONS = {"Hold Items", "Mega Stone", "Berries"}


def parse_items(html: str) -> dict[str, list[str]]:
    soup = BeautifulSoup(html, "html.parser")

    sections: dict[str, list[str]] = {}
    current_section = None

    # Each section is a <font size="4"><b><u>Section Name</u></b></font>
    # followed by a <table> with item rows
    for font_tag in soup.find_all("font", attrs={"size": "4"}):
        u_tag = font_tag.find("u")
        if not u_tag:
            continue

        section_name = u_tag.get_text().strip()
        if section_name not in BATTLE_SECTIONS:
            continue

        # Find the next table after this section header
        table = font_tag.find_parent("div").find_next("table")
        if not table:
            continue

        items = []
        for row in table.find_all("tr"):
            cells = row.find_all("td", class_="fooinfo")
            if not cells:
                continue

            # First fooinfo cell contains the item name as a link
            link = cells[0].find("a")
            if link:
                item_name = link.get_text().strip()
                if item_name:
                    items.append(item_name)

        sections[section_name] = items

    return sections


def main():
    with open("/tmp/champions_items.html", "r", encoding="latin-1") as f:
        html = f.read()

    sections = parse_items(html)

    # Combine all battle-relevant items into a flat list
    all_items = []
    for section_name in BATTLE_SECTIONS:
        if section_name in sections:
            all_items.extend(sections[section_name])

    # Deduplicate while preserving order
    seen = set()
    unique_items = []
    for item in all_items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)

    output = {
        "game": "Pokemon Champions",
        "source_url": "https://www.serebii.net/pokemonchampions/items.shtml",
        "total_count": len(unique_items),
        "by_section": {name: len(items) for name, items in sections.items()},
        "items": unique_items,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
