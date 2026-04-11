# VGC Download

A Claude Code plugin for competitive Pokemon VGC coaching. Named after Porygon2's ability **Download**.

VGC Download turns raw usage data and regulation info into actionable competitive insight through AI-powered meta analysis and Trick Room team building.

## What It Does

- **Parse regulations** from Serebii.net into structured JSON
- **Process usage stats** from Smogon's chaos data, filtered by regulation legality and legal items
- **Scout the meta** with an AI agent that combines stats analysis with web research
- **Build Trick Room teams** with an AI agent grounded in competitive theory and current meta data

## Install

```bash
npx vgc-download install
```

This copies skills and agents to `~/.claude/`, and registers the MCP server in `~/.claude/mcp.json`. Restart Claude Code after installing.

```bash
npx vgc-download uninstall
```

## Skills

| Skill | Description |
|-------|-------------|
| `/vgc:parse-regulation <url>` | Parse a Serebii regulation page into `data/regulations/` |

## Agents

| Agent | Trigger | What It Does |
|-------|---------|--------------|
| **Meta Scout** | "scout the meta", "analyze the metagame" | Reads processed stats + regulation data, searches the web for community sentiment, writes a dated scouting report to `data/meta/` |
| **TR Architect** | "build a TR team", "draft a trick room team" | Reads a meta report + regulation + Pokemon database, searches the web for TR builds, writes a Showdown-pasteable team draft to `data/teams/drafts/` |

Both agents are loaded with companion skills containing competitive reference material (meta analysis methodology, TR team-building theory sourced from VGCGuide, Smogon, and Nugget Bridge).

## Scripts

Run with `uv run python scripts/<name>.py`.

| Script | Description |
|--------|-------------|
| `parse_regulation.py` | Parse Serebii regulation HTML into JSON |
| `parse_items.py` | Parse Serebii items page into JSON |
| `process_stats.py <raw_file> <reg_id>` | Filter raw Smogon chaos data by regulation + legal items |
| `check_matches.py <raw_file> <reg_id>` | Debug unmatched Pokemon with fuzzy matching |
| `fetch_pokemon_db.py` | Fetch all 1350 Pokemon from PokeAPI (base stats, types, abilities) |
| `filter_pokemon_db.py <reg_id>` | Filter the full pokedex to a regulation-specific subset |

## Data Layout

```
data/
├── config.json                 # Current regulation + meta pointers
├── regulation_template.json    # Schema for regulation files
├── my_team.json                # Active team roster
├── regulations/
│   └── reg_m-a.json            # Regulation M-A (259 Pokemon)
├── pokemon_db/
│   ├── pokedex.json            # Full PokeAPI database (1350 Pokemon)
│   └── reg_m-a_pokemon.json    # Filtered to Reg M-A (259 Pokemon)
├── stats/
│   ├── raw/                    # Raw Smogon chaos JSON
│   ├── items/                  # Legal items lists
│   └── processed/              # Filtered meta snapshots
├── meta/                       # Meta Scout scouting reports
└── teams/
    └── drafts/                 # TR Architect team drafts
```

## Workflow

### When a new regulation drops

1. `/vgc:parse-regulation <serebii-url>` — parse the new regulation
2. Paste raw Smogon chaos data into `data/stats/raw/`
3. `uv run python scripts/process_stats.py <raw_file> <reg_id>` — process stats
4. `uv run python scripts/filter_pokemon_db.py <reg_id>` — filter Pokemon database
5. Update `data/config.json` to point to the new regulation and meta

### When you want to build a team

1. Ask Claude to "scout the meta" — Meta Scout writes a report
2. Ask Claude to "build me a TR team" — TR Architect reads the report and builds a team
3. Test the team on [Pokemon Showdown](https://play.pokemonshowdown.com/)
4. Iterate

## Current State

- **Game:** Pokemon Champions
- **Regulation:** M-A (259 Pokemon, April 8 – June 17, 2026)
- **Stats source:** Reg I chaos data (623,191 battles) filtered to M-A legality
- **Pokemon matched:** 155 of 259 with usage data

## Requirements

- Node.js >= 18
- Python >= 3.11
- [uv](https://docs.astral.sh/uv/) for Python dependency management
- [Claude Code](https://claude.com/claude-code) CLI

## License

MIT
