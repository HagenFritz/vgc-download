---
name: vgc:review-team
description: "Review an existing team against the current VGC meta. Takes a pokepaste file path, fires two parallel specialist agents (meta coverage analyst + improvement advisor), and writes a structured review report. Use when the user wants to evaluate, critique, or improve a team they already have."
argument-hint: "<path-to-team-file>"
---

# Review Team

Evaluate an existing team — full or partial — against the current meta by firing two parallel specialist agents and synthesizing a structured review report.

## What Makes a Good Team Review

- **Matchup-first.** Know where the team wins and loses before suggesting changes.
- **Concrete threats, not type charts.** Name the Pokemon, the move, and the interaction — not just "weak to Fire."
- **Grounded improvements.** Every suggestion is validated against legal Pokemon, legal items, and real move pools.
- **Partial-team aware.** A 3-Pokemon skeleton gets additions, not substitutions.

## Progress Tracking

Before starting, use `TaskList` to find any lingering tasks and delete them with `TaskUpdate` (status: `deleted`). Then create fresh tasks using `TaskCreate`. Mark each `in_progress` when starting and `completed` when done:

1. "Validate input and load data" (activeForm: "Validating team file and loading data...")
2. "Detect team size" (activeForm: "Checking team size...")
3. "Run parallel review agents" (activeForm: "Running coverage analyst and improvement advisor...")
4. "Synthesize review report" (activeForm: "Assembling final report...")
5. "Write report to disk" (activeForm: "Writing review report...")

## Methodology

### Step 1: Validate Input

Check the argument:
- If no argument provided, STOP and print:
  ```
  Usage: /vgc:review-team <path-to-team-file>
  Example: /vgc:review-team data/teams/drafts/2026-04-28-001_reg_m-a_tr_team.md
  ```
- If argument provided, confirm the file exists (use `Bash: ls <path>`). If not found, STOP and print: `File not found: <path>. Check the path and try again.`

### Step 2: Load Data

Identify the meta scouting report:
1. Read `data/config.json` to get `current_regulation`
2. Glob for `data/meta/*_<current_regulation>_report.md` and pick the most recent by date prefix
3. If no report exists, STOP and tell the user:
   ```
   No meta scouting report found for <current_regulation>.
   Run /vgc:scout-meta first — the review agents need a current meta report to evaluate matchups.
   ```

Resolve all data paths:
- `data/regulations/<current_regulation>.json` — allowed Pokemon list
- `data/pokemon_db/<current_regulation>_pokemon.json` — base stats, types, abilities, move pools
- `data/stats/items/champions_items.json` — legal Champions items list

### Step 3: Detect Team Size

Count occurrences of ` @ ` (space-at-space) in the input file:
```bash
grep -c " @ " <team-file-path>
```

- If count ≥ 6: `mode = full`
- If count < 6: `mode = partial`

Confirm to the user:
```
Reviewing [N]-Pokemon [full/partial] team: <filename>
Meta report: <report filename>
Regulation: <current_regulation>
```

### Step 4: Run Parallel Review Agents

Fire both agents **in parallel** in a single message with two Task calls. Do NOT run them sequentially.

```
Task vgc-download:coaching:team-coverage-analyst(
  Analyze this team's meta coverage against the current scouting report.

  Team file: <path to team file>
  Meta report: <path to meta report>
  Regulation: <current_regulation>
  Regulation file: data/regulations/<current_regulation>.json
  Pokemon DB: data/pokemon_db/<current_regulation>_pokemon.json
  Legal items: data/stats/items/champions_items.json
  Mode: <full|partial>

  Produce a structured markdown analysis with these five sections:
  1. Threat Grid — top 10 meta threats with ✅/🟡/🔴 coverage rating and severity
  2. Archetype Matchup Table — Favored/Even/Unfavored for each dominant archetype with bring-4
  3. Type Vulnerability Audit — types hitting 3+ team members super-effectively
  4. Structural Gaps — over-covered and under-covered roles
  5. Overall Verdict — best matchup, worst matchup, tournament viability

  Reference: agents/coaching/team-coverage-analyst.md for full instructions.
)

Task vgc-download:coaching:team-improvement-advisor(
  Suggest concrete improvements for this team based on the current meta.

  Team file: <path to team file>
  Meta report: <path to meta report>
  Regulation: <current_regulation>
  Regulation file: data/regulations/<current_regulation>.json
  Pokemon DB: data/pokemon_db/<current_regulation>_pokemon.json
  Legal items: data/stats/items/champions_items.json
  Mode: <full|partial>

  Produce:
  1. Change List — prioritized CRITICAL/IMPORTANT/POLISH suggestions with specific changes and verification
  2. Suggested Leads by Matchup — 2-3 lead pairs for key archetypes
  3. Revised Showdown Paste — full 6-Pokemon paste with all suggestions applied, clearly labeled advisory

  Every suggested Pokemon must be in allowed_pokemon. Every suggested item must be in champions_items.json by exact name. Every suggested move must be in the Pokemon's move pool in the Pokemon DB. Do not suggest Life Orb, Flame Orb, Toxic Orb, or Choice Scarf.

  Reference: agents/coaching/team-improvement-advisor.md for full instructions.
)
```

Wait for both agents to complete before proceeding.

### Step 5: Synthesize and Write Report

Assemble the review report using the template at `skills/review-team/review-template.md`:

1. **Header:** Fill in regulation name, date-sequence, input file path, mode, meta report path
2. **Team section:** Extract and paste the Showdown paste from the input file (the raw paste block only — not the full draft format)
3. **Meta Coverage Analysis:** Insert the full output from `team-coverage-analyst` into the corresponding subsections
4. **Improvement Suggestions:** Insert the Change List and Suggested Leads from `team-improvement-advisor`
5. **Revised Paste:** Insert the Revised Showdown Paste from `team-improvement-advisor`, preserving the advisory label

Determine the output filename:
```bash
mkdir -p data/teams/reviews
today=$(date +%Y-%m-%d)
last_seq=$(ls data/teams/reviews/${today}-*_review.md 2>/dev/null | grep -oP "${today}-\K\d{3}" | sort -n | tail -1)
next_seq=$(printf "%03d" $(( ${last_seq:-0} + 1 )))
output_path="data/teams/reviews/${today}-${next_seq}_<current_regulation>_review.md"
```

Write the complete report to `$output_path`.

Confirm to the user:
```
Review complete: <output_path>

Top matchup verdicts:
- vs. [Archetype 1]: [Verdict]
- vs. [Archetype 2]: [Verdict]
- vs. [Archetype 3]: [Verdict]

Critical findings: [N] (see Change List in report)
```
