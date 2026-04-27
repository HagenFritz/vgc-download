# VGC Download

A Claude Code plugin for competitive Pokemon VGC coaching. Named after Porygon2's ability **Download**.

VGC Download turns raw usage data and regulation info into actionable competitive insight through AI-powered meta analysis and Trick Room team building.

## What It Does

- **Parse regulations** from Serebii.net into structured JSON
- **Process usage stats** from Smogon's chaos data, filtered by regulation legality and legal items
- **Scout the meta** with an AI agent that combines stats analysis with web research
- **Build Trick Room teams** with an AI agent grounded in competitive theory and current meta data

## Install

### From a local clone

```bash
git clone https://github.com/HagenFritz/vgc-download.git
cd vgc-download
node bin/cli.mjs install
```

### Via npx (once published)

```bash
npx vgc-download install
```

The install script copies skills and agents into `~/.claude/skills/` and `~/.claude/agents/`, and registers the MCP server in `~/.claude/mcp.json`. **Restart Claude Code after installing** for the skills to appear.

### Uninstall

```bash
node bin/cli.mjs uninstall
# or: npx vgc-download uninstall
```

## Updating Skills

After editing any file in `skills/` or `agents/`, reinstall to push the changes to Claude Code:

```bash
node bin/cli.mjs install
```

Then restart Claude Code. The install script overwrites `~/.claude/skills/` and `~/.claude/agents/` with the current repo contents.

## Skills

| Skill | Description |
|-------|-------------|
| `/vgc:parse-regulation <url>` | Parse a Serebii regulation page into `data/regulations/` |
| `/vgc:scout-meta` | Scout the metagame — spawns Meta Scout agent to analyze stats, search the web, and write a scouting report |
| `/vgc:build-tr-team [archetype preference]` | Build a Trick Room team — optionally steer the draft with a preference like `"Oranguru setter + Mega Golurk abuser"` |

## Agents

Skills orchestrate specialized agents. Agents are focused specialists; skills wire them together.

**Scout-meta** (`/vgc:scout-meta`) spawns four analysts in parallel:

| Agent | Role |
|-------|------|
| **usage-analyst** | Quantitative stats — top threats, sets, teammates, speed tiers |
| **archetype-analyst** | Cores, dominant archetypes, speed control landscape |
| **community-scout** | Tournament results, tier lists, rising tech (web) |
| **exploit-finder** | Shared weaknesses, structural gaps, anti-meta picks |

The skill then synthesizes their outputs into a dated report at `data/meta/`.

**Build-tr-team** (`/vgc:build-tr-team`) uses a builder + parallel critics pattern:

| Agent | Role |
|-------|------|
| **tr-architect** | Drafts the initial team (Showdown paste + roster breakdown + bring-4s). Called again to revise if critics flag critical issues. |
| **meta-coverage-checker** | Evaluates the draft against the scouting report — what does this team lose to? |
| **tr-viability-checker** | Runs the 8 TR composition checks (Taunt / Imprison / Fake Out answers, Plan B, type coverage, spread moves, item diversity) |
| **speed-math-auditor** | Audits EV totals, IVs, natures, and verifies underspeed benchmarks |

The skill fires the three critics in parallel, synthesizes severity-ranked findings, re-spawns `tr-architect` once if there are critical issues, and writes the final draft to `data/teams/drafts/`.

Skills contain methodology and competitive reference material (meta analysis methodology, TR team-building theory sourced from VGCGuide, Smogon, and Nugget Bridge).

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

1. `/vgc:scout-meta` — Meta Scout writes a scouting report
2. `/vgc:build-tr-team` — TR Architect reads the report and builds a team
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
