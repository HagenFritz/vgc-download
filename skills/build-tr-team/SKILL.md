---
name: vgc:build-tr-team
description: "Build a Trick Room team for the current VGC regulation. Spawns tr-architect to draft a team, then fires three parallel critics (meta coverage, TR viability, speed math) and revises if needed. Use when the user says 'build a TR team', 'draft a trick room team', or 'build me a team'."
argument-hint: "[archetype preference]"
---

# Build a Trick Room Team

Produce a complete, tournament-viable Trick Room team draft for the current VGC Doubles regulation using a builder + parallel critics pattern modeled on `/review`.

## What Makes a Good TR Team

- **Sets TR reliably.** Mental Herb, redirection, or Magic Bounce against Taunt. Setter survives common attacks.
- **Wins without TR.** At least one Pokemon viable outside TR — Tailwind/Icy Wind speed control, or a fast attacker. TR expires; the game doesn't.
- **Answers the current meta.** Picks aren't generic — they counter the top threats from the scouting report.
- **Has clean set math.** EVs total ≤508, 0 Spe IVs on abusers, speed tiers actually underspeed the TR mirror.
- **Passes the 8 composition checks.** Taunt answer, Imprison answer, Fake Out answer, Plan B, type coverage, spread moves, item diversity, reliable TR setup.

## Progress Tracking

Before starting, use `TaskList` to find lingering tasks and delete them with `TaskUpdate` (status: `deleted`). Then create fresh tasks using `TaskCreate`. Mark each `in_progress` when starting and `completed` when done:

1. "Load meta report and regulation data" (activeForm: "Reading data files...")
2. "Spawn tr-architect for initial draft" (activeForm: "Drafting initial team...")
3. "Run parallel critics" (activeForm: "Running meta coverage, TR viability, and speed math critics...")
4. "Synthesize critique" (activeForm: "Consolidating findings...")
5. "Revise if critical findings" (activeForm: "Re-spawning tr-architect for revision...")
6. "Write final draft to disk" (activeForm: "Writing Showdown paste draft...")

## Methodology

### Step 1: Load Data

Identify the meta scouting report:
1. Read `data/config.json` to get `current_regulation`
2. Glob for `data/meta/*_<current_regulation>_report.md` and pick the most recent by date prefix
3. If no report exists, STOP and tell the user to run `/vgc:scout-meta` first — the critics cannot evaluate against threats they don't know about

Also gather paths for the agents:
- `data/regulations/<current_regulation>.json` — allowed Pokemon list
- `data/pokemon_db/<current_regulation>_pokemon.json` — base stats, types, abilities
- `data/stats/items/champions_items.json` — legal Champions items list (117 items). Pass this path to all agents.

**Capture the archetype argument (if provided):**
If the user supplied an archetype preference argument (e.g., `"Oranguru setter + Mega Golurk abuser"`), capture it as `<user_archetype_preference>`. If no argument was given, `<user_archetype_preference>` is absent — omit the `User Archetype Preference:` field from all Task prompts below.

### Step 2: Spawn tr-architect for Initial Draft

Fire the builder. Pass the meta report path and all data paths as context.

```
Task vgc-download:coaching:tr-architect(
  Produce a complete Trick Room team draft for the current regulation.

  Regulation: <regulation_id> (<regulation name>, <start_date> – <end_date>)
  Meta report: <path to scouting report>
  Regulation file: data/regulations/<current_regulation>.json
  Pokemon DB: data/pokemon_db/<current_regulation>_pokemon.json
  Legal items: data/stats/items/champions_items.json
  User Archetype Preference: <user_archetype_preference>  ← include this line only when provided; omit entirely if absent

  Requirements:
  - 6 Pokemon, all from regulation's allowed_pokemon list
  - Showdown paste format (item, ability, level 50, EVs, nature, IVs, 4 moves)
  - Every item must appear in data/stats/items/champions_items.json by exact name — load the file before assigning any items
  - Roster breakdown: role, why this pick, key interactions, EV rationale per Pokemon
  - Win conditions: primary, secondary, anti-meta
  - Bring-4 guidelines for 3-4 common matchups
  - Threats and weaknesses section

  Follow the team template at skills/build-tr-team/team-template.md exactly. Consult skills/build-tr-team/competitive-reference.md for setter/abuser analysis, EV math, and counterplay.
)
```

Wait for the draft to come back. Capture it in context — you'll pass it to all three critics.

### Step 3: Run Parallel Critics

Fire all three critics **in parallel** using a single message with three Task tool calls. Each gets the same draft plus the context it needs to evaluate its specific axis.

**CRITICAL:** Single message, three parallel Task calls. Do NOT run them sequentially.

```
Task vgc-download:coaching:meta-coverage-checker(
  Evaluate this TR team draft against the current meta scouting report.

  Meta report: <path to scouting report>
  Regulation: <regulation_id>
  Regulation file: data/regulations/<current_regulation>.json
  Pokemon DB: data/pokemon_db/<current_regulation>_pokemon.json

  Draft team:
  <paste the full tr-architect output here: Showdown paste + roster breakdown + win conditions>

  Return a structured markdown critique covering: Top-Threat Coverage (pass/fail grid for top 10), Archetype Matchup Analysis, Anti-Meta Pick Audit, Critical Gaps, Overall Verdict.
)

Task vgc-download:coaching:tr-viability-checker(
  Run the 9 TR composition checks on this draft team.

  Regulation file: data/regulations/<current_regulation>.json
  Pokemon DB: data/pokemon_db/<current_regulation>_pokemon.json
  Legal items: data/stats/items/champions_items.json

  Draft team:
  <paste the full tr-architect output here>

  Return a structured markdown checklist with pass/fail for each of the 9 checks (TR Setup, Plan B, Taunt answer, Imprison answer, Type coverage, Fake Out answer, Spread moves, Item diversity, Item legality) plus a Summary Panel with critical failures and weak points. Any check failure is a 🔴 CRITICAL.
)

Task vgc-download:coaching:speed-math-auditor(
  Audit EV spreads, IVs, natures, and speed tiers on this draft team.

  Pokemon DB: data/pokemon_db/<current_regulation>_pokemon.json
  Top meta threats (for underspeed benchmarks): <list top 10 from scouting report>

  Draft team:
  <paste the full tr-architect output here>

  Return a structured markdown audit covering: Per-Pokemon Set Check, Underspeed Verification, Bulk/Offense Benchmark Check, Nature/Ability/Item Combo Sanity, Summary Panel with critical math errors.
)
```

Wait for all three to complete before proceeding.

### Step 4: Synthesize Critique

Consolidate all findings into a severity-ranked list:

- **🔴 CRITICAL** — team autoloses to a top meta threat, has no Taunt/Imprison/Fake Out answer, all 6 Pokemon are slow (no Plan B), 3+ stacked type weaknesses, duplicate items, illegal items (not in champions_items.json), or EV math errors that make a set illegal
- **🟡 IMPORTANT** — uncomfortable matchups, weak Plan B, missing spread move coverage, suboptimal EV benchmarks (underspeed margin too tight)
- **🔵 POLISH** — spread refinements, item reshuffles, cosmetic improvements

Walk each finding and ask: does this change the team's tournament viability? If yes → CRITICAL or IMPORTANT. If no → POLISH.

Dedupe overlapping findings (e.g., tr-viability-checker and meta-coverage-checker both flagging "no Taunt answer" count as one CRITICAL, not two).

### Step 5: Revise if Critical Findings

**If any 🔴 CRITICAL findings:** re-spawn tr-architect with the full critique as input for a revision pass.

```
Task vgc-download:coaching:tr-architect(
  Revise your previous TR team draft to address the critical findings below. Keep what works; fix what's broken.

  Previous draft: <paste previous full draft>

  Critical findings to address:
  <paste CRITICAL findings from the synthesis>

  Important findings to consider:
  <paste IMPORTANT findings>

  Constraints:
  - Still 6 Pokemon from the regulation's allowed_pokemon list
  - Preserve win conditions and strategic identity where possible
  - Every pick and set change must address a specific finding
  - User-specified picks (from archetype preference, if any) are soft preferences — work around them (adjust teammates, items, EV spreads, bring-4 guidelines) rather than replacing them. Surface their known weaknesses in the Threats and Weaknesses section explicitly.

  Return the revised team in the same Showdown paste + roster breakdown + win conditions format.
)
```

Wait for the revision. Do NOT re-run critics — one revision pass is the limit. A second revision cycle tends to make the team worse (critics and builder disagree on tradeoffs). If the revision still has CRITICAL issues, surface them in the final report as "Known Weaknesses" rather than looping.

**If no CRITICAL findings:** skip the revision, go directly to Step 6 with the original draft.

**If only IMPORTANT or POLISH findings:** incorporate them into the "Threats and Weaknesses" and "Tech Options" sections of the final draft; don't re-spawn.

### Step 6: Write Final Draft to Disk

Create the output path if needed:
```bash
mkdir -p data/teams/drafts
```

Write the final (revised or original) draft to:
```
data/teams/drafts/<YYYY-MM-DD>_<regulation_id>_tr_team.md
```

Follow the [team template](team-template.md) exactly. Append a new section at the end titled **## Critique & Revisions** with:
- Summary of findings from each critic (one paragraph each)
- List of CRITICAL issues that triggered a revision (if any)
- List of IMPORTANT/POLISH findings that informed the Threats & Weaknesses section
- Whether a revision was performed

Confirm to the user with:
- The file path
- Top 3 win conditions
- Headline matchup (best and worst)
- Whether revision was triggered
- User-specified picks vs. architect picks (only when `<user_archetype_preference>` was provided)

## Rules

- **Builder → critics → revise → write.** That's the whole flow. No more, no less.
- **Fire critics in parallel.** One message, three Task calls. Sequential defeats the purpose.
- **Scouting report is a prerequisite.** If no meta report exists, stop and tell the user to run `/vgc:scout-meta` first — you can't critique matchup coverage against threats you don't know about.
- **One revision cycle max.** Re-running critics after revision causes infinite polish loops. Accept IMPORTANT/POLISH findings as documented weaknesses.
- **Cross-reference the allowed list.** Every Pokemon on the final team must be in the regulation's `allowed_pokemon`. The critics check this; you verify before writing.
- **VGC is Doubles.** Every decision accounts for partner interactions, speed control, bring-4 strategy.
- **Never assume a Pokemon or form doesn't exist.** Trust the regulation data. If the regulation lists Mega Clefable, Mega Clefable is legal.
- **Pokemon Champions is the game.** No Scarlet/Violet historical sets or older-format bias.

## Reference Material

For the team template, see [team-template.md](team-template.md). For detailed TR competitive theory (setter analysis, abuser archetypes, EV math, counterplay, bring-4 strategy), see [competitive-reference.md](competitive-reference.md).
