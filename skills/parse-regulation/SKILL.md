---
name: vgc:parse-regulation
description: 'Parse a VGC regulation page from Serebii.net into structured JSON. Use when the user provides a Serebii URL for a regulation set (e.g., Regulation G, Regulation H) or says "parse regulation", "add regulation", or "load regulation".'
argument-hint: "<serebii regulation URL>"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, AskUserQuestion, TaskCreate, TaskUpdate, TaskList
---

# Parse VGC Regulation

Parse a Serebii.net VGC regulation page into structured JSON and save it to `data/regulations/`.

## Progress Tracking

Before starting, use `TaskList` to find any lingering tasks and delete them all with `TaskUpdate` (status: `deleted`). Then create fresh tasks upfront using `TaskCreate` so the user can see the full checklist. Mark each task `in_progress` when you start it and `completed` when done. Create these tasks:

1. "Fetch regulation page" (activeForm: "Downloading HTML...")
2. "Inspect HTML structure" (activeForm: "Reading page structure...")
3. "Extract Pokemon list" (activeForm: "Running extraction script...")
4. "Verify output" (activeForm: "Checking for duplicates and errors...")
5. "Review with user" (activeForm: "Awaiting confirmation...")
6. "Save regulation" (activeForm: "Writing JSON...")

## Input

The user provides a Serebii regulation URL. Example:
`https://www.serebii.net/scarletviolet/competitivepokemon/regulationh.shtml`

If no URL is provided, ask the user for one.

## Steps

### 1. Fetch the Page

Use `curl` via Bash to download the raw HTML:
```bash
curl -s -o /tmp/regulation_page.html "<url>"
```

Do NOT use WebFetch — it summarizes content and drops Pokemon entries. We need the raw HTML.

### 2. Inspect the HTML Structure

Read the downloaded HTML file (`/tmp/regulation_page.html`) and identify:
- The regulation name/letter (e.g., "Regulation H")
- The game version
- Doubles ruleset details: team size, level rules, timers, restrictions
- Any Pokemon usage restrictions (allowed, banned, restricted)
- Item restrictions, move restrictions

We only care about **Doubles** (VGC format). Ignore Singles rules entirely.

Pay particular attention to the Pokemon tables — these can contain 600+ entries. Identify the exact HTML structure (table rows, list items, divs, etc.) that contains the Pokemon names and any form distinctions.

### 3. Extract Pokemon List

The existing script at `scripts/parse_regulation.py` handles Serebii's table format. It uses image filename suffixes to detect forms:
- `-a` = Alolan, `-g` = Galarian, `-h` = Hisuian, `-p` = Paldean, `-e` = Eternal
- `-m` = Mega, `-mx` = Mega X, `-my` = Mega Y

If the HTML structure has changed from what the script expects, update the script to match the new structure. Otherwise, run it as-is:
```bash
uv run python scripts/parse_regulation.py
```

### 4. Verify the Output

Check:
- The Pokemon count looks reasonable for the regulation
- No obvious duplicates
- No garbage entries

**Never assume a Pokemon or form does not exist.** If the page lists it, include it.

### 5. Review with User

Show the user:
- Regulation name
- Total number of allowed/restricted Pokemon
- A summary of the key Doubles rules

Wait for the user to confirm before saving.

### 6. Save Regulation

Write the regulation JSON to `data/regulations/reg_<id>.json` using the template at `data/regulation_template.json`.

Ask the user if this should be set as the current regulation. If yes, update `data/config.json`.

## Naming Conventions for Pokemon Forms

- Regional forms: `Raichu-Alola`, `Rapidash-Galar`
- Alternate forms: `Urshifu-Rapid-Strike`, `Urshifu-Single-Strike`
- Mega/Primal: `Charizard-Mega-X`, `Kyogre-Primal`
- Use Showdown-compatible names when possible
