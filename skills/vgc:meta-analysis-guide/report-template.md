# Meta Scouting Report Template

This template defines the required sections for every meta scouting report. Both the Meta Scout agent (which writes reports) and the TR Architect agent (which reads them) depend on these section headings. If you change this template, both agents must be updated.

## Output Path

```
data/meta/<YYYY-MM-DD>_<regulation_id>_report.md
```

Example: `data/meta/2026-04-10_reg_m-a_report.md`

## Required Sections

Every report must include all of the following sections, in this order:

```markdown
# Pokémon Champions Meta Scouting Report — <Regulation Name> — <Date>

## Data Provenance

Source: <source_metagame> (<source_battles> battles)
Raw file: <source_file>
Regulation: <regulation_id> (<pokemon_matched> of <pokemon_in_regulation> Pokemon matched)

> **Note:** <If source regulation differs from target, explain the proxy data situation.
> If source matches target, state "Stats are from the current regulation ladder.">

## Top Threats

Ranked list of the highest-usage Pokemon. For each entry:

1. **<Pokemon>** — <usage>% usage
   - **Sets:** <common moves, items, abilities>
   - **Strengths:** <what makes it dominant>
   - **Weaknesses:** <exploitable vulnerabilities>
   - **Common partners:** <frequent teammates>

Include at least the top 15 Pokemon by usage.

## Core Combinations

Identify the strongest duos and trios in the format (e.g., Fire/Water/Grass cores, Trick Room setter + abuser).

## Dominant Archetypes

Group the meta into major team archetypes and detail how they match up against each other. For each:

- **<Archetype Name>** (~<prevalence>%)
  - Core Pokemon: <list>
  - Win condition: <how it wins>
  - Strengths & Matchups: <why it's popular and what it beats>
  - Weaknesses: <what beats it>

Estimate prevalence from teammate correlation data and community reports.

## Speed Tier Breakdown

Organize Pokemon into speed tiers relevant to competitive play:

- **Fast (base 100+):** <Pokemon list with base speeds>
- **Mid (base 60-99):** <Pokemon list>
- **Slow (base 1-59):** <Pokemon list — TR candidates>

Note which Pokemon commonly run speed-modifying natures, Choice Scarf, or Tailwind.

## Exploitable Weaknesses

Cross-cutting vulnerabilities across the top meta:

- <Weakness 1: what the top archetypes share and how to exploit it>
- <Weakness 2>

Focus on vulnerabilities in defensive typing, over-reliance on speed control, or structural flaws.

## Item, Move & Mechanic Trends

Notable patterns in items, moves, and format mechanics (e.g., Mega Evolution):

- **Mechanic Usage:** <how top threats utilize mechanics like Mega Evolution, e.g., offensive sweeping or utility>
- **Rising items/moves:** <items and moves increasing in popularity>
- **Anti-meta tech:** <surprise items/moves being used to counter top threats>

## Unknown Pokemon

Regulation-legal Pokemon with no usage data. These are potential surprise picks.

List them grouped by type or role if possible. Note any that have competitive potential despite zero ladder representation.
```
