"""One-off script to parse a Serebii regulation page HTML into structured JSON.

Reads /tmp/regulation_page.html (downloaded via curl) and extracts Pokemon names
using the image filename suffixes to identify forms:
  - No suffix: base form
  - -a: Alolan
  - -g: Galarian
  - -h: Hisuian
  - -p: Paldean
  - -m: Mega
  - -mx: Mega X
  - -my: Mega Y
"""

import json
import re
from bs4 import BeautifulSoup

FORM_SUFFIXES = {
    "-a": "Alola",
    "-g": "Galar",
    "-h": "Hisui",
    "-p": "Paldea",
    "-e": "Eternal",
    "-mx": "Mega-X",
    "-my": "Mega-Y",
    "-m": "Mega",
}

def parse_pokemon_table(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")

    # Find the "Newly Useable Pokemon" table — it's the table with class="tab"
    # that comes after the h2 containing "Newly Useable"
    pokemon_table = None
    for h2 in soup.find_all("h2"):
        if "Newly Useable" in h2.get_text():
            # The table follows this h2's parent <p>
            parent = h2.parent
            pokemon_table = parent.find_next("table", class_="tab")
            break

    if not pokemon_table:
        print("ERROR: Could not find the Pokemon table", flush=True)
        return []

    pokemon_names = []
    rows = pokemon_table.find_all("tr")

    for row in rows:
        cells = row.find_all("td", class_="fooinfo")
        if len(cells) < 3:
            continue

        # Cell 0: dex number
        # Cell 1: image (contains the form suffix info)
        # Cell 2: name link
        img_cell = cells[1]
        name_cell = cells[2]

        # Get the Pokemon name from the link text (before the <br>)
        link = name_cell.find("a")
        if not link:
            continue

        # The link contains "Name<br/>Japanese" — get just the English name
        name_text = link.decode_contents()
        english_name = name_text.split("<br")[0].strip()

        # Get the image filename to detect forms
        img = img_cell.find("img")
        if not img:
            continue

        img_src = img.get("src", "")
        # Extract the filename part: e.g., "003-m.png" -> "003-m"
        filename = img_src.split("/")[-1].replace(".png", "")

        # Check for form suffix
        form_suffix = ""
        # Check longest suffixes first to avoid -m matching before -mx/-my
        for suffix in sorted(FORM_SUFFIXES.keys(), key=len, reverse=True):
            if filename.endswith(suffix):
                form_suffix = suffix
                break

        # Get the base Pokemon name from the URL (always the base form name)
        href = link.get("href", "")
        # e.g., "/pokedex-champions/charizard/" -> "charizard"
        url_name = href.strip("/").split("/")[-1]
        base_name = url_name.replace("-", " ").title().replace(" ", "")

        # Build the final name
        if form_suffix:
            form_label = FORM_SUFFIXES[form_suffix]
            # Use english_name for base forms since URL loses capitalization nuance
            # But for Mega/regional, derive from english_name stripped of prefix
            if form_label.startswith("Mega"):
                # Strip "Mega " and any trailing " X"/" Y" from display name
                clean = re.sub(r"^Mega\s+", "", english_name)
                clean = re.sub(r"\s+[XY]$", "", clean)
                final_name = f"{clean}-{form_label}"
            else:
                final_name = f"{english_name}-{form_label}"
        else:
            final_name = english_name

        if final_name:
            pokemon_names.append(final_name)

    return pokemon_names


def main():
    with open("/tmp/regulation_page.html", "r", encoding="latin-1") as f:
        html = f.read()

    names = parse_pokemon_table(html)

    # Check for duplicates
    seen = set()
    dupes = []
    for name in names:
        if name in seen:
            dupes.append(name)
        seen.add(name)

    output = {
        "total_count": len(names),
        "unique_count": len(seen),
        "duplicates": dupes,
        "pokemon": names,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
