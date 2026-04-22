---
name: vgc:scout-meta
description: "Scout the current VGC metagame. Spawns four parallel analyst agents (usage, archetype, community, exploit) and synthesizes a dated scouting report. Use when the user says 'scout the meta', 'analyze the metagame', or 'meta report'."
argument-hint: "[regulation id]"
---

# Scout the Meta

Produce a comprehensive scouting report for the current VGC Doubles regulation by spawning four specialized analyst agents in parallel and synthesizing their findings into a dated report.

## What Makes a Good Meta Scouting Report

A good report goes beyond restating usage percentages. It synthesizes patterns:

- **Archetypes, not just Pokemon.** "Incineroar is #1" is a stat. "Intimidate pivot + Kyogre rain shell is 20% of the meta" is analysis.
- **Relationships matter.** Teammate correlation reveals team structure.
- **Speed context.** A fast meta favors TR. A slow meta punishes it. The report must answer which we're in.
- **Actionable weaknesses.** Answer "what can I exploit?" not just "what's popular?"

## Progress Tracking

Before starting, use `TaskList` to find any lingering tasks and delete them all with `TaskUpdate` (status: `deleted`). Then create fresh tasks upfront using `TaskCreate`. Mark each `in_progress` when starting and `completed` when done:

1. "Load configuration and data" (activeForm: "Reading config and stats files...")
2. "Assess data provenance" (activeForm: "Checking proxy data status...")
3. "Run parallel analyst agents" (activeForm: "Running usage, archetype, community, and exploit analysts...")
4. "Catalog unknown Pokemon" (activeForm: "Finding Pokemon with 0 usage...")
5. "Synthesize scouting report" (activeForm: "Assembling final report...")
6. "Write report to disk" (activeForm: "Writing markdown report...")

## Methodology

### Step 1: Load Data

Read `data/config.json` to find `current_regulation` and `current_meta`. Then load (for your own orchestration context):

- `data/stats/processed/<current_meta>.json` — usage stats
- `data/regulations/<current_regulation>.json` — regulation details, allowed Pokemon, dates
- `data/pokemon_db/<current_regulation>_pokemon.json` — base stats, types, abilities

Note the regulation name, date range, and exact file paths — you'll pass these to each agent.

### Step 2: Assess Data Provenance

Check the meta file's `source_metagame` field. If it doesn't match the current regulation (e.g., Reg I stats used for Reg M-A), this is **proxy data**. Capture:

- Which regulation the stats actually come from
- How many battles the data represents
- How many Pokemon matched out of the total regulation pool

You'll pass this provenance note to each agent so they caveat their output appropriately.

### Step 3: Run Parallel Analyst Agents

Fire all four analyst agents **in parallel** using the Task tool. Each agent gets the data paths, provenance note, and regulation context.

**CRITICAL:** Use a single message with four parallel Task tool calls so they run concurrently, not sequentially.

```
Task vgc-download:coaching:usage-analyst(
  Analyze the processed stats and report top threats, sets, teammates, and speed tiers.

  Regulation: <regulation_id> (<regulation name>)
  Stats file: data/stats/processed/<current_meta>.json
  Pokemon DB: data/pokemon_db/<current_regulation>_pokemon.json
  Regulation file: data/regulations/<current_regulation>.json

  Data provenance: <one line — real data or proxy from which metagame with how many battles>

  Return a structured markdown readout covering: Data Snapshot, Top Threats (top 20), Set Archetypes, Speed Tier Distribution, Item/Move/Ability Distribution Highlights.
)

Task vgc-download:coaching:archetype-analyst(
  Identify dominant cores, archetypes, and speed control structure from the processed stats.

  Regulation: <regulation_id> (<regulation name>)
  Stats file: data/stats/processed/<current_meta>.json
  Pokemon DB: data/pokemon_db/<current_regulation>_pokemon.json

  Data provenance: <same note>

  Return a structured markdown analysis covering: Dominant Cores, Dominant Archetypes (4–7), Speed Control Landscape, Archetype Matchup Matrix.
)

Task vgc-download:coaching:community-scout(
  Gather community sentiment, tournament results, and rising tech for the current Pokemon Champions regulation.

  Regulation: <regulation name> (<start_date> – <end_date>)
  Game: Pokemon Champions

  Return a structured markdown research digest covering: Tournament Results, Tier List Consensus, Rising Tech / Innovation, Meta Shifts / Narrative, Anti-Meta Strategies, Gaps & Caveats.

  CRITICAL: Always include "Pokemon Champions" in search queries.
)

Task vgc-download:coaching:exploit-finder(
  Cross-reference the top threats and archetypes to find shared weaknesses and anti-meta opportunities.

  Regulation: <regulation_id>
  Pokemon DB: data/pokemon_db/<current_regulation>_pokemon.json
  Regulation file: data/regulations/<current_regulation>.json
  Stats file: data/stats/processed/<current_meta>.json

  Data provenance: <same note>

  Note: If usage-analyst and archetype-analyst outputs are available in context, use them. Otherwise pull the top-usage Pokemon directly from the stats file.

  Return a structured markdown analysis covering: Shared Type Weaknesses, Structural Gaps, Archetype-Level Counters, Speed Control Vulnerabilities, Anti-Meta Pick Suggestions.
)
```

Wait for all four to complete before proceeding.

### Step 4: Catalog Unknown Pokemon

While the agents run (or after), compare the regulation's `allowed_pokemon` list against the Pokemon in the stats file. Any allowed Pokemon NOT in the stats data have zero usage — list them as unknowns, grouped by type or potential role.

These are surprise picks. They become section 8 of the report.

### Step 5: Synthesize the Scouting Report

Assemble the final report using the [report template](report-template.md) exactly. Map agent outputs to template sections:

| Report Section | Primary Source | Secondary Source |
|---|---|---|
| 1. Data Provenance | Your provenance note from Step 2 | usage-analyst's Data Snapshot |
| 2. Top Threats | usage-analyst's Top Threats | community-scout's tier list consensus (for divisive picks) |
| 3. Core Combinations | archetype-analyst's Dominant Cores | usage-analyst's teammate data |
| 4. Dominant Archetypes | archetype-analyst's Dominant Archetypes + Matchup Matrix | community-scout's Meta Shifts |
| 5. Speed Tier Breakdown | usage-analyst's Speed Tier Distribution | archetype-analyst's Speed Control Landscape |
| 6. Exploitable Weaknesses | exploit-finder (all sections) | community-scout's Anti-Meta Strategies |
| 7. Item, Move & Mechanic Trends | usage-analyst's Distribution Highlights | community-scout's Rising Tech |
| 8. Unknown Pokemon | Your Step 4 catalog | — |

Resolve contradictions with judgment:
- If the stats say one thing and community sentiment says another, present both with the data-side first and note the divergence.
- If community-scout returned "Gaps & Caveats" (thin web results), lean harder on stats and say so in Data Provenance.
- If data is proxy, add a prominent banner at the top of Data Provenance.

Write for a competitive player who:
- Knows VGC fundamentals (type chart, speed tiers, common moves)
- Needs analysis, not tutorials
- Wants to know what to build around and what to prepare for
- Appreciates opinionated takes backed by data

### Step 6: Write to Disk

Write the report to `data/meta/<YYYY-MM-DD>_<regulation_id>_report.md`. Create `data/meta/` if it doesn't exist (`mkdir -p`).

Confirm to the user with the file path and a 3-line summary: proxy vs real data, top archetype, headline exploitable weakness.

## Rules

- **Fire agents in parallel.** One message, four Task calls. Do not run them sequentially.
- **Agents don't know each other's output.** They run independently. The orchestrator (you) is the only place findings come together.
- **Data provenance is mandatory.** Every report must disclose where the stats come from. Proxy data gets a banner.
- **VGC is Doubles.** Synthesis must preserve Doubles framing — partner pivots, speed control, Fake Out pressure, redirection.
- **Never invent data.** If an agent returned thin output for a section, say "data is sparse for this section" in the report instead of filling it with fiction.
- **Pokemon Champions is the game.** Never cite results from Scarlet/Violet or older games.
