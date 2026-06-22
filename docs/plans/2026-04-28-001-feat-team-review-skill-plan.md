---
title: "feat: Add team-review skill with coverage analyst and improvement advisor"
type: feat
status: completed
date: 2026-04-28
origin: docs/brainstorms/2026-04-28-team-review-requirements.md
---

# feat: Add Team Review Skill

## Overview

Add a `/vgc:review-team` skill that takes a pokepaste file path as input, fires two parallel specialist agents (meta coverage analyst + improvement advisor), and synthesizes a structured team review report. Closes the feedback loop in the coaching pipeline: users can now evaluate teams they already have, not just generate new ones from scratch.

## Problem Frame

The `build-tr-team` skill drafts teams; nothing closes the loop by evaluating them. Whether iterating a tournament build or assessing whether a draft concept is worth developing, users currently have no structured way to diagnose team weaknesses or get concrete improvement suggestions grounded in the current meta. (See origin: `docs/brainstorms/2026-04-28-team-review-requirements.md`)

## Requirements Trace

- R1. Skill accepts a file path argument to a pokepaste or draft `.md` file
- R2. Skill loads `data/config.json` → current regulation → latest meta report, regulation JSON, Pokemon DB, and items list
- R3. Two parallel specialist agents: `team-coverage-analyst` (matchup/threat breakdown) and `team-improvement-advisor` (suggestions + revised paste)
- R4. Synthesized review report written to `data/teams/reviews/` datestamped
- R5. Partial teams (< 6 Pokemon) get addition suggestions, not substitutions
- R6. Both agents validate suggested Pokemon against `allowed_pokemon` and items against `champions_items.json`
- R7. `competitive-reference.md` (in `skills/build-tr-team/`) extended with hard rules and anti-patterns as the primary quality gate for agent suggestions

## Scope Boundaries

- No web search in either review agent — analysis grounded in local data only
- No auto-apply of suggestions — revised paste is advisory only
- No interactive mid-run prompts — skill runs to completion
- Does not replace `build-tr-team` — does not draft from scratch

## Context & Research

### Relevant Code and Patterns

- `agents/coaching/meta-coverage-checker.md` — closest existing agent; structured critique format with pass/fail grid. New `team-coverage-analyst` borrows structure but is broader (not TR-specific) and skips composition checks
- `agents/coaching/tr-viability-checker.md` — composition checklist pattern; improvement advisor's change-list section mirrors this format
- `skills/build-tr-team/SKILL.md` — orchestration pattern: load data → spawn parallel agents → synthesize → write to disk. `review-team` follows the same shape
- `skills/build-tr-team/competitive-reference.md` — shared reference doc, extended by Unit 1 before agents use it
- `skills/build-tr-team/team-template.md` — Showdown paste format spec; improvement advisor uses this when producing revised paste
- `data/config.json` — single source of truth for `current_regulation` and `current_meta`
- `data/meta/<YYYY-MM-DD>_<regulation_id>_report.md` — meta report format agents consume; same gate logic as `build-tr-team` (stop if no report exists)

### Institutional Learnings

- Agent quality degrades when reference docs are permissive — the existing `competitive-reference.md` already enforces specific rules (Life Orb illegal, Guts without Flame Orb illegal). Anti-pattern extension in Unit 1 is the highest-leverage quality intervention.
- Parallel agent pattern is established — fire both review agents in a single message with two Task calls

### External References

- No external research needed — local patterns are sufficient and the scope specifically excludes web search

## Key Technical Decisions

- **New agents, not reused:** `meta-coverage-checker` is scoped to TR build critics; extending it would muddy its responsibility. New agents with focused prompts are cleaner to tune independently.
- **Partial team detection via pokepaste line count:** Count `@ Item` occurrences in the input file. If < 6, set `mode=partial` and pass this flag to improvement-advisor, which switches from substitution to addition framing. Simple and requires no parsing library.
- **Review report as new format:** Distinct from the draft template — review sections are matchup-first, not build-first. New `review-template.md` companion file in `skills/review-team/`.
- **Skill name `vgc:review-team`:** Consistent with existing `vgc:` namespace. Command: `/vgc:review-team <file-path>`.
- **No revision loop:** Unlike `build-tr-team`, there is no re-spawn pass. Suggestions are advisory; the user decides what to apply. This also removes the risk of an infinite improvement cycle.
- **`competitive-reference.md` extension (not duplication):** The review agents reference the same file as `tr-architect`. Unit 1 adds anti-patterns to that shared doc so both pipelines benefit.

## Open Questions

### Resolved During Planning

- **New agents vs. reuse:** New agents. `meta-coverage-checker` is TR-build-specific; a general team review has different scope and framing (see decisions above).
- **Output file format:** New review template. Drafts and reviews have different information architecture — reviews lead with matchup verdict, drafts lead with win conditions.
- **Partial team detection:** Grep/count `@ ` occurrences in input file. Count < 6 → partial mode.
- **Anti-patterns to add to reference doc:** See Unit 1 scope below.

### Deferred to Implementation

- Exact Showdown paste parser edge cases (nickname, Mega Stone in item slot) — handle by grepping for `@ ` pattern rather than strict parsing
- Whether the review report should include a one-paragraph executive summary at the top — implementer can judge based on agent output verbosity

## High-Level Technical Design

> *This illustrates the intended approach and is directional guidance for review, not implementation specification. The implementing agent should treat it as context, not code to reproduce.*

```
/vgc:review-team <file-path>
    │
    ├── Load data/config.json → current_regulation
    ├── Glob data/meta/*_<reg>_report.md → pick most recent
    │   └── STOP if no report → "Run /vgc:scout-meta first"
    ├── Resolve data paths: regulation.json, pokemon_db, champions_items.json
    ├── Read input file → count "@ " occurrences → mode = full (6) or partial (<6)
    │
    ├── [PARALLEL] ─────────────────────────────────────────────────────────┐
    │   Task: team-coverage-analyst                                          │
    │   Task: team-improvement-advisor (+ mode flag)                        │
    │   └───────────────────────────────────────────────────────────────────┘
    │
    ├── Synthesize outputs into review report markdown
    ├── mkdir -p data/teams/reviews
    └── Write data/teams/reviews/<YYYY-MM-DD>-NNN_<reg>_review.md
```

Data paths passed to both agents:
- Input team file path
- Meta report path
- `data/regulations/<reg>.json`
- `data/pokemon_db/<reg>_pokemon.json`
- `data/stats/items/champions_items.json`
- Mode: `full` or `partial`

## Implementation Units

- [ ] **Unit 1: Extend competitive-reference.md with hard rules and anti-patterns**

**Goal:** Give both review agents (and the existing tr-architect) a concrete list of illegal suggestions to never make, reducing hallucinated or unplayable recommendations.

**Requirements:** R7

**Dependencies:** None

**Files:**
- Modify: `skills/build-tr-team/competitive-reference.md`

**Approach:**
Add a new top-level section `## Hard Rules — What NOT to Suggest` near the top of the file (after the intro, before the setter analysis). Cover:
- **Illegal items:** Life Orb, Flame Orb, Toxic Orb, Choice Scarf — not in `champions_items.json`. Never suggest. Substitutes: type boosters (Twisted Spoon, Black Belt, Charcoal, etc.) for offensive boost; status Orb combos have no legal activation item.
- **Ability + item dead combos:** Guts without a status orb is flavor-only. Poison Heal without Toxic Orb. Never suggest these as a damage strategy.
- **Move pool hallucinations:** Verify moves against the Pokemon DB before recommending. Do not invent coverage moves a Pokemon cannot learn.
- **Speed tie strategies:** Never suggest "run neutral Speed to tie" as a plan — ties are 50/50 and unreliable at tournament level.
- **Single-setter no-Plan-B:** Never recommend a team with 1 setter and no fast mode. Always require a Plan B.
- **Non-regulation Pokemon:** Every suggestion must be validated against `allowed_pokemon`. Do not suggest based on memory — read the file.

**Test scenarios:**
- Existing drafts do not recommend Life Orb, Flame Orb, or Toxic Orb after this change
- A future review agent using this doc does not suggest these items

**Verification:**
- `competitive-reference.md` contains a `## Hard Rules` section with all six anti-pattern categories documented
- The section is referenced in the intro or opening paragraph so agents load it before generating suggestions

---

- [ ] **Unit 2: Create `team-coverage-analyst` agent**

**Goal:** Agent that reads a team and the meta report, produces a structured matchup breakdown: which archetypes the team beats/loses to, top threat coverage grid, shared type weaknesses, and structural gaps. Does NOT suggest improvements.

**Requirements:** R3, R6

**Dependencies:** Unit 1 (reference doc must exist before agent prompt references it)

**Files:**
- Create: `agents/coaching/team-coverage-analyst.md`

**Approach:**
YAML frontmatter: `name: team-coverage-analyst`, tools: `Read, Glob, Grep, Bash`, model: inherit. No web search tools.

System prompt responsibilities:
1. Load all provided data paths (regulation, Pokemon DB, items list) before analysis
2. Count Pokemon in the input — note if partial team and caveat analysis accordingly
3. Produce structured sections (see review template in Unit 4 for exact headings)

Output sections:
- **Threat Grid** — top 10 meta threats from the report: ✅ PASS / 🟡 WEAK / 🔴 FAIL with specific evidence (which team member answers it and how)
- **Archetype Matchup Table** — for each dominant archetype in the report: Verdict (favored / even / unfavored), one-sentence why, suggested bring-4 or "no clean plan"
- **Type Vulnerability Audit** — list all shared weaknesses hitting 3+ team members
- **Structural Gaps** — over-covered (redundant coverage) and under-covered (missing answer)
- **Overall Verdict** — one paragraph: best matchup, worst matchup, is this team tournament-viable

Rules for the agent prompt:
- Be honest, not polite. Name the archetypes this team loses to.
- Concrete evidence only. "Weak to Fire" is lazy. Name the Pokemon, the move, and why the team can't answer it.
- Use the meta report's archetype names exactly — do not invent new archetype labels.
- No improvement suggestions — that's team-improvement-advisor's job.

**Patterns to follow:**
- `agents/coaching/meta-coverage-checker.md` — pass/fail grid format, severity labels, overall verdict structure

**Test scenarios:**
- Given a full team and a meta report, produces all 5 output sections
- Given a partial team (< 6 Pokemon), notes in each section that analysis is based on the provided members only
- Does not suggest Pokemon substitutions or item changes

**Verification:**
- Agent file exists at `agents/coaching/team-coverage-analyst.md` with correct frontmatter
- Output contains all required sections with concrete evidence, not vague type-chart observations

---

- [ ] **Unit 3: Create `team-improvement-advisor` agent**

**Goal:** Agent that reads a team, the meta report, and the coverage analyst's output (or operates independently), then produces: a prioritized change list and a revised Showdown paste with suggestions applied.

**Requirements:** R3, R5, R6

**Dependencies:** Unit 1 (reference doc), Unit 2 (coverage analyst runs in parallel — skill passes both the team and the meta report; this agent does its own matchup reading)

**Files:**
- Create: `agents/coaching/team-improvement-advisor.md`

**Approach:**
YAML frontmatter: `name: team-improvement-advisor`, tools: `Read, Glob, Grep, Bash`, model: inherit, skills: `vgc:build-tr-team` (to access `competitive-reference.md`).

The skill passes a `mode` flag: `full` (6 Pokemon) or `partial` (< 6). Agent prompt branches on this:
- **Full mode:** Suggest substitutions. For each CRITICAL gap: name one specific replacement pick (legal in regulation), explain the role it fills, why it's better than the current slot.
- **Partial mode:** Suggest additions to complete the roster. Name specific picks, roles, and how they complement existing members.

Output sections:
- **Change List** (prioritized: CRITICAL → IMPORTANT → POLISH)
  - For each suggestion: what to change, specific replacement/adjustment, why (which gap it closes or weakness it patches)
  - Item changes: exact item names from `champions_items.json` only
  - Move changes: verify move exists in Pokemon's legal move pool (grep Pokemon DB)
  - EV changes: provide the benchmark the spread aims to hit (survive X move from Y Pokemon)
  - Lead recommendations: 2-3 suggested lead pairs per archetype matchup
- **Revised Showdown Paste** — full 6-Pokemon paste with suggestions applied
  - Labeled clearly: `## Suggested Revision (apply selectively — this is advisory)`
  - If partial team, revised paste completes the roster to 6

Rules for the agent prompt:
- Every suggested Pokemon must be in `allowed_pokemon`. Check the regulation file — do not rely on memory.
- Every suggested item must be in `champions_items.json` by exact name. Load the file first.
- Verify move legality via the Pokemon DB before recommending any move.
- Do not suggest speed ties, illegal ability+item combos, or single-setter no-Plan-B teams (see `competitive-reference.md` Hard Rules section).
- The revised paste must be valid Showdown format: Level 50, EVs ≤ 508, nature listed, IVs only when non-31.

**Patterns to follow:**
- `agents/coaching/tr-viability-checker.md` — change list format with severity labels
- `skills/build-tr-team/team-template.md` — Showdown paste format spec

**Test scenarios:**
- Full team input → produces substitution suggestions, not additions
- Partial team input (mode=partial) → produces addition suggestions, no substitutions
- Revised paste is valid Showdown format (Level 50, EVs ≤ 508)
- No suggested item appears outside `champions_items.json`
- No suggested Pokemon missing from `allowed_pokemon`

**Verification:**
- Agent file exists at `agents/coaching/team-improvement-advisor.md` with correct frontmatter
- Change list has severity labels and specific evidence for each suggestion
- Revised paste section is clearly labeled as advisory

---

- [ ] **Unit 4: Create `review-template.md` and `data/teams/reviews/` output structure**

**Goal:** Define the review report format and establish the output directory.

**Requirements:** R4

**Dependencies:** Units 2 and 3 (template must reflect actual agent output sections)

**Files:**
- Create: `skills/review-team/review-template.md`
- Create (directory): `data/teams/reviews/` (via `mkdir -p` in skill)

**Approach:**
Review template structure (distinct from draft template — review-first, not build-first):

```markdown
# Team Review — <Regulation Name> — <YYYY-MM-DD-NNN>

## Team

<Showdown paste of the reviewed team>

## Meta Coverage Analysis

### Threat Grid
[From team-coverage-analyst]

### Archetype Matchup Table
[From team-coverage-analyst]

### Type Vulnerability Audit
[From team-coverage-analyst]

### Structural Gaps
[From team-coverage-analyst]

### Overall Verdict
[From team-coverage-analyst]

## Improvement Suggestions

### Change List
[From team-improvement-advisor — CRITICAL → IMPORTANT → POLISH]

### Suggested Leads by Matchup
[From team-improvement-advisor]

## Revised Paste (Advisory)

> Apply selectively. The change list above is the canonical recommendation.

<Revised Showdown paste from team-improvement-advisor>
```

Output filename sequence follows the draft pattern:
```bash
mkdir -p data/teams/reviews
today=$(date +%Y-%m-%d)
last_seq=$(ls data/teams/reviews/${today}-*_review.md 2>/dev/null | grep -oP "${today}-\K\d{3}" | sort -n | tail -1)
next_seq=$(printf "%03d" $(( ${last_seq:-0} + 1 )))
# Output: data/teams/reviews/<today>-<next_seq>_<regulation_id>_review.md
```

**Test scenarios:**
- Template file exists at `skills/review-team/review-template.md` with all required sections
- `data/teams/reviews/` directory is created by skill run (or `mkdir -p` in skill succeeds if it already exists)

**Verification:**
- Template sections match the actual output sections from Units 2 and 3
- Filename follows `YYYY-MM-DD-NNN_<regulation_id>_review.md` convention

---

- [ ] **Unit 5: Create `vgc:review-team` skill**

**Goal:** Orchestrator skill that loads data, detects partial/full team, fires both agents in parallel, synthesizes their output into the review template, and writes the report to disk.

**Requirements:** R1, R2, R3, R4, R5

**Dependencies:** Units 1–4 (agents and template must exist)

**Files:**
- Create: `skills/review-team/SKILL.md`

**Approach:**
Skill frontmatter: `name: vgc:review-team`, argument-hint: `<path-to-team-file>`.

Orchestration steps:

**Step 1: Validate input**
- Confirm argument is provided — if not, print usage and stop
- Confirm file exists — if not, print error and stop

**Step 2: Load data**
- Read `data/config.json` → `current_regulation`
- Glob `data/meta/*_<current_regulation>_report.md` → sort by date prefix → take most recent
- If no meta report found: STOP → "No meta scouting report found. Run `/vgc:scout-meta` first."
- Resolve: `data/regulations/<current_regulation>.json`, `data/pokemon_db/<current_regulation>_pokemon.json`, `data/stats/items/champions_items.json`

**Step 3: Detect partial/full team**
- Count occurrences of ` @ ` (space-at-space) in the input file — each is one Pokemon's item line
- If count < 6 → mode = `partial`; if count ≥ 6 → mode = `full`
- Confirm to user: "Reviewing [N]-Pokemon [partial/full] team..."

**Step 4: Fire parallel agents**
Single message, two Task calls:
```
Task vgc-download:coaching:team-coverage-analyst(
  Analyze this team's meta coverage against the current scouting report.
  Team file: <path>
  Meta report: <path>
  Regulation: <id>
  Regulation file: <path>
  Pokemon DB: <path>
  Legal items: <path>
  Mode: <full|partial>
  ...
)

Task vgc-download:coaching:team-improvement-advisor(
  Suggest improvements for this team.
  Team file: <path>
  Meta report: <path>
  Regulation: <id>
  Regulation file: <path>
  Pokemon DB: <path>
  Legal items: <path>
  Mode: <full|partial>
  ...
)
```

Wait for both to complete.

**Step 5: Synthesize and write report**
- Assemble the review template with both agents' outputs in the correct sections
- Determine output path with sequence number (see Unit 4 bash snippet)
- Write to `data/teams/reviews/<YYYY-MM-DD>-<NNN>_<regulation_id>_review.md`
- Confirm to user with file path + top 3 matchup verdicts from coverage analyst

**Patterns to follow:**
- `skills/build-tr-team/SKILL.md` — data load, gate logic, parallel Task pattern, disk write with sequence number

**Test scenarios:**
- No argument → prints usage, does not run agents
- File not found → prints error, does not run agents
- No meta report in `data/meta/` → stops with scout-meta prompt
- Full team (6 Pokemon) → both agents receive `mode=full`; improvement-advisor suggests substitutions
- Partial team (< 6 Pokemon) → both agents receive `mode=partial`; improvement-advisor suggests additions
- Report written to `data/teams/reviews/` with correct datestamped filename

**Verification:**
- `skills/review-team/SKILL.md` exists with all 5 steps documented
- Running skill with a known team file produces a report at the expected path
- Both agent Task calls appear in a single message (parallel, not sequential)

---

- [ ] **Unit 6: Install and smoke-test**

**Goal:** Push new files to installed location and verify the pipeline runs end-to-end.

**Requirements:** All

**Dependencies:** Units 1–5

**Files:**
- Run: `node bin/cli.mjs install` (copies skills/ and agents/ to ~/.claude/)

**Approach:**
- Run install script
- Restart Claude Code (required for new skills/agents to register)
- Run `/vgc:review-team` with one of the existing draft files (e.g., from `data/teams/drafts/`)
- Verify report appears in `data/teams/reviews/`
- Spot-check: no illegal items in revised paste, all suggested Pokemon in regulation

**Test scenarios:**
- Install script runs without error
- `/vgc:review-team` appears in slash command list after restart
- End-to-end run produces a report file

**Verification:**
- Report file exists and contains all required sections
- No item in revised paste is outside `champions_items.json`

## System-Wide Impact

- **Skill namespace:** `vgc:review-team` added to the `/` menu alongside `vgc:build-tr-team` and `vgc:scout-meta`
- **Shared reference doc:** `competitive-reference.md` is modified in Unit 1 — affects `tr-architect` (reads it via `vgc:build-tr-team` skill) and both new review agents. Change is additive (new section), not a rewrite, so no regression risk to existing pipeline.
- **New output directory:** `data/teams/reviews/` is created at runtime — no migration needed
- **Agent count:** Adds 2 new coaching agents; existing 8 unchanged
- **No data pipeline changes** — skill reads the same files as `build-tr-team`; no new data formats required

## Risks & Dependencies

- **Agent suggestion quality:** Even with extended reference docs, agents may hallucinate move pools for obscure Pokemon. Mitigation: the `competitive-reference.md` Hard Rules section + explicit "load Pokemon DB before suggesting" instruction in both agents.
- **Revised paste validity:** Improvement advisor produces a Showdown paste; paste validity is hard to verify mechanically without a parser. Mitigation: clear "advisory" labeling and canonical change list as the primary recommendation.
- **Meta report gate:** If user hasn't run `/vgc:scout-meta`, the skill stops. This is the right behavior but may surprise users — skill message should clearly point to the command.
- **Install step required after changes:** Any modification to `skills/` or `agents/` requires `node bin/cli.mjs install` + Claude Code restart. Document in the implementation notes for Unit 6.

## Sources & References

- **Origin document:** [docs/brainstorms/2026-04-28-team-review-requirements.md](docs/brainstorms/2026-04-28-team-review-requirements.md)
- Orchestration pattern: `~/.claude/skills/build-tr-team/SKILL.md`
- Coverage agent pattern: `~/.claude/agents/coaching/meta-coverage-checker.md`
- Paste format spec: `~/.claude/skills/build-tr-team/team-template.md`
- Reference doc to extend: `skills/build-tr-team/competitive-reference.md`
- Related plan: `docs/plans/2026-04-10-001-feat-meta-scout-tr-architect-agents-plan.md`
