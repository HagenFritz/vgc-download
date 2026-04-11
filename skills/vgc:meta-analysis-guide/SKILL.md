---
name: vgc:meta-analysis-guide
description: "Reference documentation for VGC meta analysis methodology. Not a user command — loaded into the Meta Scout agent as domain knowledge."
user-invocable: false
---

# VGC Meta Analysis Guide

This document defines how to analyze a VGC Doubles metagame and produce a useful scouting report. It is loaded into the Meta Scout agent as reference knowledge.

## What Makes a Good Meta Analysis

A good meta report goes beyond restating usage percentages. It synthesizes patterns:

- **Archetypes, not just Pokemon.** "Incineroar is #1" is a stat. "Intimidate pivot + fast special attacker is the dominant shell" is analysis.
- **Relationships matter.** Which Pokemon appear together? What does high teammate correlation reveal about team structure?
- **Speed context.** Raw usage without speed tier context is incomplete. A player needs to know whether the meta is fast (Tailwind-heavy) or slow (TR-viable) to plan their team.
- **Actionable weaknesses.** The report should answer: "What can I exploit?" not just "What's popular?"

## Progress Tracking

Before starting, use `TaskList` to find any lingering tasks and delete them all with `TaskUpdate` (status: `deleted`). Then create fresh tasks upfront using `TaskCreate` so the user can see the full checklist. Mark each task `in_progress` when you start it and `completed` when done. Create these tasks:

1. "Load configuration and data" (activeForm: "Reading config and stats files...")
2. "Assess data provenance" (activeForm: "Checking proxy data status...")
3. "Analyze stats (Threats, Cores, Archetypes, Tiers)" (activeForm: "Analyzing usage stats...")
4. "Search community sentiment" (activeForm: "Searching web for meta discussion...")
5. "Identify exploitable weaknesses" (activeForm: "Cross-referencing vulnerabilities...")
6. "Catalog unknown Pokemon" (activeForm: "Finding Pokemon with 0 usage...")
7. "Write scouting report" (activeForm: "Writing markdown report...")

## Methodology

### Step 1: Load Data

Read `data/config.json` to find `current_regulation` and `current_meta`. Then load:

- `data/stats/processed/<current_meta>.json` — usage stats
- `data/regulations/<current_regulation>.json` — regulation details and allowed Pokemon list
- `data/pokemon_db/<current_regulation>_pokemon.json` — base stats, types, and abilities for all regulation-legal Pokemon. Use this for speed tier breakdowns and type analysis.

### Step 2: Assess Data Provenance

Check the meta file's `source_metagame` field. If it doesn't match the current regulation (e.g., Reg I stats used for Reg M-A), this is **proxy data** and must be disclosed prominently. Note:

- Which regulation the stats actually come from
- How many battles the data represents
- How many Pokemon matched out of the total regulation pool
- What this means for the analysis (some Pokemon may be over/underrepresented)

### Step 3: Analyze the Stats

Work through the processed stats systematically:

**Top Threats**: Sort Pokemon by `usage` percentage. For each of the top 15-20:
- List their common abilities, items, and moves from the stats data
- Assess their competitive role (sweeper, support, setter, tank)
- Identify their key strengths and weaknesses in a Doubles context

**Core Combinations**: Look beyond single Pokémon to identify the strongest duos and trios in the format (e.g., Fire/Water/Grass cores, Trick Room setter + abuser). Use the `teammates` data to spot these pairings.

**Mechanic Trends**: Analyze how the format's primary mechanics (like Mega Evolution) are being utilized. Which Megas are dominating, and are they being used as the primary win condition or for utility?

**Dominant Archetypes**: Look for patterns in Pokemon that frequently appear together:
- **Speed control archetypes**: Tailwind teams, Trick Room teams, weather teams
- **Offensive cores**: which 2-3 Pokemon form the damage backbone?
- **Defensive structures**: Intimidate cycling, redirection, Follow Me
Assess how these top archetypes match up against each other. Validate against community reports.

**Speed Tier Breakdown**: Organize the meta by base speed into fast (100+), mid (60-99), and slow (1-59). Note Pokemon that commonly run speed-modifying natures, Choice Scarf, or Tailwind. This is critical for EVing and Trick Room candidate identification.

### Step 4: Search the Web

Search for current VGC community sentiment to supplement the stats:

- Recent tournament results and top-cut teams
- Tier list discussions and community rankings
- Meta shift articles or threads
- Any "anti-meta" strategies gaining traction

Useful search terms:
- `"Pokemon Champions" VGC <regulation name> meta analysis`
- `"Pokemon Champions" VGC tier list`
- `"Pokemon Champions" VGC <regulation> tournament results top cut`

**CRITICAL**: Always explicitly include `"Pokemon Champions"` in your search queries to avoid pulling incorrect data from older games like Scarlet & Violet.

If web results are sparse (common for brand-new regulations), note the gap and proceed with stats-only analysis. Never block on empty web results.

### Step 5: Identify Exploitable Weaknesses

Cross-reference the top threats and archetypes to find:

- Shared type weaknesses across top Pokemon
- Common defensive gaps in popular team structures
- Over-reliance on specific strategies or abilities
- Speed control vulnerabilities (especially relevant for TR viability)

### Step 6: Catalog Unknown Pokemon

Compare the regulation's `allowed_pokemon` list against the Pokemon in the meta file. Any allowed Pokemon NOT in the meta data have zero usage data — list them as unknowns. Group by type or potential role if possible. These are potential surprise picks.

### Step 7: Write the Report

Follow the [report template](../skills/vgc:meta-analysis-guide/report-template.md) exactly. Include all 8 required sections:

1. Data Provenance
2. Top Threats
3. Core Combinations
4. Dominant Archetypes
5. Speed Tier Breakdown
6. Exploitable Weaknesses
7. Item, Move & Mechanic Trends
8. Unknown Pokemon

Write for a competitive player who:
- Knows VGC fundamentals (type chart, speed tiers, common moves)
- Needs analysis, not tutorials
- Wants to know what to build around and what to prepare for
- Appreciates opinionated takes backed by data

## Output

Write the report to `data/meta/<YYYY-MM-DD>_<regulation_id>_report.md`.

Create the `data/meta/` directory if it doesn't exist (use `mkdir -p`).
