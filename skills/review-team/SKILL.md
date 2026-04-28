---
name: vgc:review-team
description: "Review an existing team against the current VGC meta. Takes a pokepaste file path, performs inline analysis (threat grid, archetype matchups, improvement suggestions, revised paste), and writes a structured review report. All analysis happens in this conversation context so you can ask follow-up questions."
argument-hint: "<path-to-team-file>"
---

# Review Team

Evaluate an existing team — full, draft, or partial — against the current meta. All analysis runs inline in this conversation so follow-up questions work.

## What Makes a Good Team Review

- **Matchup-first.** Know where the team wins and loses before suggesting changes.
- **Concrete threats, not type charts.** Name the Pokemon, the move, and the interaction — not just "weak to Fire."
- **Grounded improvements.** Every suggestion is validated against legal Pokemon, legal items, and real move pools.
- **Draft-aware.** A team with missing items or EVs gets completion suggestions, not error flags.
- **Partial-team aware.** A 3-Pokemon skeleton gets additions, not substitutions.

## Progress Tracking

Before starting, use `TaskList` to find any lingering tasks and delete them with `TaskUpdate` (status: `deleted`). Then create fresh tasks using `TaskCreate`. Mark each `in_progress` when starting and `completed` when done:

1. "Validate input and load data" (activeForm: "Validating team file and loading data...")
2. "Assess team completeness" (activeForm: "Checking team completeness...")
3. "Load competitive truths" (activeForm: "Loading competitive truths...")
4. "Analyze meta coverage" (activeForm: "Analyzing meta coverage...")
5. "Generate improvement suggestions" (activeForm: "Generating improvements...")
6. "Write report to disk" (activeForm: "Writing review report...")

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
   Run /vgc:scout-meta first — the review needs a current meta report to evaluate matchups.
   ```

Resolve all data paths and read them now:
- `data/regulations/<current_regulation>.json` — allowed Pokemon list
- `data/pokemon_db/<current_regulation>_pokemon.json` — base stats, types, abilities
- `data/stats/items/champions_items.json` — legal Champions items list
- The team file itself — read the full contents

Read the meta scouting report in full.

Confirm to the user:
```
Loaded:
- Team file: <filename>
- Meta report: <report filename>
- Regulation: <current_regulation>
```

### Step 3: Assess Team Completeness

Read the team file and parse each Pokemon entry. A Pokemon entry in Showdown paste format looks like:

```
[Pokemon name] @ [Item]
Ability: [Ability]
Level: 50
EVs: [EV spread]
[Nature] Nature
- [Move 1]
...
```

Check each Pokemon slot for:
1. **Item** — does the line contain ` @ ` followed by an item name? If the item is missing or the line is just `[Pokemon name]` with no ` @ `, the slot is missing an item.
2. **EVs** — does the EV line contain non-zero values? If the line is `EVs: 0` or missing entirely, the slot has no EVs.
3. **Roster count** — count the number of Pokemon (each Pokemon starts a new block with a name line).

Classify the team:
- **`complete`** — 6 Pokemon, all have items and non-zero EVs
- **`draft`** — 6 Pokemon, but one or more slots are missing an item or have no/zero EVs
- **`partial`** — fewer than 6 Pokemon (regardless of items/EVs)

A `draft` or `partial` team is NOT broken. These are works-in-progress that need completion suggestions.

Print the team assessment:
```
Team: [N] Pokemon — mode: [complete/draft/partial]
[If draft: "Incomplete slots: [list Pokemon names with missing items/EVs]"]
[If partial: "Missing [6-N] slots — will suggest additions"]
```

### Step 4: Load Competitive Truths

Read `data/competitive-truths.md` if it exists. If missing, skip silently.

When the file exists: treat every fact in it as **authoritative ground truth** that overrides your own priors. When the file asserts an ability, move restriction, or playstyle rule, use that over whatever you would otherwise assume.

Note that you have loaded the truths file (or that it was not found) so the user knows:
```
Competitive truths: loaded (or "not found — using defaults")
```

### Step 5: Inline Meta Coverage Analysis

You are now Claude operating in the main conversation context. Perform the full meta coverage analysis by reading the scouting report and team data you have already loaded. Do not spawn agents.

Produce the following five sections. Frame each section to reflect the team's completeness mode — `draft` and `partial` teams get notes like "this gap may be addressed by completing [slot]" rather than hard CRITICAL flags for incomplete slots.

**Important data limitations to acknowledge:**
- The Pokemon DB does not store move pools — `moves` arrays are empty for all Pokemon. Do not cite the DB as move legality authority. For move suggestions, rely on general competitive knowledge and note that you cannot mechanically verify move legality from the DB.
- Some Champions Mega abilities are missing from the DB (`"abilities": []`). Use `data/competitive-truths.md` as the authoritative source for these.

#### Threat Grid

Identify the top 10 meta threats from the scouting report. For each threat, evaluate how this team handles it:

| Threat | Usage | Coverage | Answer | Severity if missing |
|--------|-------|----------|--------|---------------------|
| [Pokemon] | [X%] | ✅ / 🟡 / 🔴 | [How the team handles it] | — / IMPORTANT / CRITICAL |

Coverage ratings:
- ✅ — Team has a reliable answer (resist + KO threat, or priority + speed control)
- 🟡 — Team can handle it but requires specific positioning
- 🔴 — Team has no reliable answer

#### Archetype Matchup Table

For each dominant archetype in the meta report, assess the matchup:

**[Archetype Name]** (~X%): **[Favored / Even / Unfavored]**
- **Why:** [Specific win condition or liability — name Pokemon and moves]
- **Bring-4:** [Which 4 Pokemon to bring for this matchup and why]

#### Type Vulnerability Audit

List types that hit 3 or more team members super-effectively:

- **[Type]** — hits [Pokemon A], [Pokemon B], [Pokemon C] super-effectively. [Note on whether this creates a practical exploitation risk given the meta.]

#### Structural Gaps

**Over-covered:**
- [Roles or threats the team addresses redundantly]

**Under-covered:**
- [Roles or threats the team lacks a reliable answer to]

For `draft` mode: note which gaps might be resolved by completing the open slots.

#### Overall Verdict

One paragraph: the team's best matchup, worst matchup, and a frank tournament viability assessment. Name the archetypes. Be opinionated.

---

### Step 6: Inline Improvement Suggestions

Produce three subsections. Follow the competitive truths file — if a truth says "never run X on Y," do not suggest X on Y.

**Hard constraints on every suggestion:**
- Every suggested Pokemon must be in `allowed_pokemon` from the regulation file (verify against the file)
- Every suggested item must be in `champions_items.json` by exact name (verify against the file)
- Do not suggest Life Orb, Flame Orb, Toxic Orb, or Choice Scarf — not legal in Champions
- Do not suggest Guts as a damage strategy (no legal activation item)
- Do not suggest speed ties as a plan
- Do not leave the team with one setter and no Plan B
- For move suggestions: note that move legality cannot be mechanically verified from the DB; rely on competitive knowledge and flag the limitation

#### Change List

Prioritized improvements:

**🔴 CRITICAL** — Structural fix. The team loses games without this.
**🟡 IMPORTANT** — Meaningful upgrade. The team is uncomfortable in key matchups without this.
**🔵 POLISH** — Optimization. Marginal improvement that sharpens specific matchups.

For each suggestion:
```
**[Priority] [Change Type]: [What to Change]**
- **Specific change:** [Exact replacement/adjustment]
- **Why:** [Which gap this closes — name the specific threat or archetype]
- **Verification:** [e.g., "Tornadus is in allowed_pokemon ✓", "Leftovers is in champions_items.json ✓"]
```

#### Completion Suggestions (draft and partial mode only)

For **`draft` mode** — for each Pokemon slot with missing item or EVs:

```
**[Pokemon name] — Complete This Slot**
- **Recommended item:** [Item from champions_items.json] — [Why this item for this Pokemon on this team]
- **EV spread target:** [EVs] — [Benchmark: e.g., "survive [Move] from [Threat] at [HP%]" or "hit [speed tier]"]
- **Nature:** [Nature] — [Why]
```

For **`partial` mode** — for each missing slot (6 minus current count):

```
**Slot [N]: [Recommended Pokemon]**
- **Role:** [What this Pokemon does for the team]
- **Item:** [Item] — must be in champions_items.json
- **Key moves:** [2-3 moves that enable the role]
- **Why this pick:** [Which gap it closes given the rest of the team]
- **Verification:** [Pokemon is in allowed_pokemon ✓]
```

#### Suggested Leads by Matchup

For 2-3 key archetypes from the meta report:

**vs. [Archetype]:** Lead [Pokemon A] + [Pokemon B] — [One sentence: what they accomplish turn 1 and why these two answer this matchup]

---

### Step 7: Revised Showdown Paste

Produce a complete 6-Pokemon Showdown paste with all CRITICAL and IMPORTANT suggestions applied:

> Apply selectively. The Change List above is the canonical recommendation. This paste applies all suggested changes — review each before importing.

```
[Pokemon name] @ [Item]
Ability: [Ability]
Level: 50
EVs: [EV spread — must total ≤ 508]
[Nature] Nature
IVs: [Only list non-31 IVs, e.g., 0 Spe for TR abusers]
- [Move 1]
- [Move 2]
- [Move 3]
- [Move 4]

[Next Pokemon...]
```

Rules:
- Level is always 50
- EVs must total 508 or less
- Only list IVs when non-standard (0 Spe for TR abusers, 0 Atk for special-only)
- Every item must be in `champions_items.json` by exact name
- For `draft` mode: fill in items and EVs for incomplete slots using completion suggestions
- For `partial` mode: complete the roster to 6 using suggested additions

---

### Step 8: Write Report to Disk

Determine the output filename:
```bash
mkdir -p data/teams/reviews
today=$(date +%Y-%m-%d)
last_seq=$(ls data/teams/reviews/${today}-*_review.md 2>/dev/null | grep -oP "${today}-\K\d{3}" | sort -n | tail -1)
next_seq=$(printf "%03d" $(( ${last_seq:-0} + 1 )))
output_path="data/teams/reviews/${today}-${next_seq}_<current_regulation>_review.md"
```

Assemble the review report using the template at `skills/review-team/review-template.md`. Fill in all sections from the inline analysis above.

Write the complete report to `$output_path`.

Confirm to the user:
```
Review complete: <output_path>

Top matchup verdicts:
- vs. [Archetype 1]: [Verdict]
- vs. [Archetype 2]: [Verdict]
- vs. [Archetype 3]: [Verdict]

Critical findings: [N] (see Change List in report)

Ask me follow-up questions — all the data is in this conversation context.
```
