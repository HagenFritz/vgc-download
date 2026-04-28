---
title: "fix: Improve review-team skill — inline analysis, completion mode, and competitive truths"
type: fix
status: active
date: 2026-04-28
---

# fix: Improve review-team Skill

## Overview

Four improvements to `/vgc:review-team` based on first-run feedback:

1. **Remove subagents, do everything inline** — agents run in isolated context windows; follow-up questions after the review are impossible. Rewrite the skill to do all analysis in the main conversation context.
2. **Expand "partial team" to include missing EVs and items** — a pokepaste with 6 Pokemon but no EVs/items should be treated as a draft-in-progress, not a broken team. Suggest completions, don't flag missing data as errors.
3. **Competitive truths file** — a user-editable `data/competitive-truths.md` the skill reads before analysis. Lets the user assert known facts (e.g., "Incineroar never runs Protect") that override or supplement the AI's priors.
4. **Document Mega ability gap + seed initial truths** — `Meganium-Mega` has `"abilities": []` in the DB because PokeAPI doesn't have Pokemon Champions Mega data. Document this limitation and seed the truths file with known Mega Sol facts and the Incineroar/Protect correction.

## Problem Frame

After the first real run of `/vgc:review-team`:
- Subagent isolation killed the conversation — the user couldn't ask follow-up questions because context was split across three processes.
- A bare pokepaste (Pokemon + moves only, no EVs or items) was flagged as a broken team rather than a draft to be completed.
- The skill recommended `Protect` on Incineroar — a well-known anti-pattern with no good mechanism to override.
- `Meganium-Mega` ability `Mega Sol` (Drought-like sun-setter) is not in the DB, causing incorrect move legality flags for Weather Ball and Solar Beam.

## Requirements Trace

- R1. Skill executes all analysis inline (no Task spawns) so the user can ask follow-up questions in the same conversation.
- R2. "Partial team" means any team with missing Pokemon, missing items, or missing EV spreads. All three cases produce completion suggestions, not error flags.
- R3. Skill reads `data/competitive-truths.md` before analysis and treats its contents as ground truth that overrides AI priors.
- R4. `data/competitive-truths.md` exists with initial entries: Mega Sol ability on Meganium-Mega, and Incineroar anti-pattern (no Protect).
- R5. CLAUDE.md documents the Mega ability gap in the Pokemon DB so future agents know not to trust empty abilities arrays for Pokemon Champions Megas.

## Scope Boundaries

- Do not rebuild the subagent files (team-coverage-analyst.md, team-improvement-advisor.md) — they can remain for potential future use, but the skill no longer calls them.
- Do not fix the Pokemon DB fetch script to pull Pokemon Champions Mega data — that's a separate effort requiring a non-PokeAPI data source.
- Do not add a UI for editing competitive-truths.md — it's a flat markdown file the user edits directly.
- Do not change the output format or file path convention for review reports.

## Context & Research

### Relevant Code and Patterns

- `skills/review-team/SKILL.md` — the orchestrator being rewritten (currently 155 lines, spawns two Task agents)
- `skills/build-tr-team/SKILL.md` — reference for inline data loading pattern and progress tracking style
- `skills/vgc:tr-theory/competitive-reference.md` — model for a static reference doc the skill reads; truths file follows similar loading pattern
- `agents/coaching/team-coverage-analyst.md` + `agents/coaching/team-improvement-advisor.md` — their analysis structure and output sections are preserved, just moved inline into the skill
- `data/pokemon_db/reg_m-a_pokemon.json` — `"abilities": []` for Meganium-Mega; `"moves": []` for all Pokemon (move pools not stored)
- CLAUDE.md — documents project-wide conventions; Mega ability gap belongs here

### Key DB Facts Discovered

- **Move pools are universally empty** in the DB — the DB stores base stats, types, and abilities only. Move verification cannot be done against the DB. The Hard Rules section in `competitive-reference.md` says to verify moves against the DB — this is misleading and should be softened in truths doc guidance.
- **Some Mega abilities are empty** — specifically Pokemon Champions Megas whose base forms don't exist in PokeAPI (e.g., Meganium-Mega with Mega Sol). Standard Gen 1–6 Megas (Venusaur-Mega, Alakazam-Mega, etc.) have correct abilities from PokeAPI.
- **Incineroar's `moves` array is empty** — so the "Protect is not in Incineroar's move pool" statement was wrong; Protect is actually a universal TM move and Incineroar can learn it. The real reason not to run Protect on Incineroar is competitive: it wastes the Fake Out + Parting Shot + Intimidate cycling turns that make Incineroar valuable. This is a competitive truth, not a legality issue.

### Institutional Learnings

- Agent quality degrades when reference docs are permissive — the truths file extends this same principle with user-defined facts
- The Hard Rules section added in the previous PR is the right quality gate pattern; truths file is its user-editable companion

## Key Technical Decisions

- **Inline skill, not subagents:** The user explicitly wants to ask follow-up questions after the review. Inline analysis fills the context window but that's acceptable — the user said so.
- **Truths file is markdown, not JSON:** Easy for the user to edit without tooling. The skill reads it as raw text and instructs itself to treat it as authoritative. Format: simple bullet list of facts organized by Pokemon or category.
- **Truths file location: `data/competitive-truths.md`:** Lives in `data/` alongside other user-maintained files (my_team.json, regulations). Not in `skills/` because it's user data, not skill logic.
- **Partial team = any incomplete set**: Missing member (< 6), missing item (bare `@ ` or no item line), or missing/zero EVs. All trigger "completion suggestion" mode for that slot. The skill reads the team inline and assesses completeness per-Pokemon, not just roster count.
- **Mega Sol documented in truths file, not DB fix:** DB fix requires a non-PokeAPI data source. For now, the truths file carries the known-fact ("Meganium-Mega ability is Mega Sol — a Drought-like ability that summons sun and enables Weather Ball and Solar Beam") and the skill treats it as authoritative.

## Open Questions

### Resolved During Planning

- **How does the inline skill handle the volume of output?** It produces all analysis sections sequentially in its own context — same sections as before (threat grid, archetype table, structural gaps, change list, revised paste), just without the subagent round-trip. Context fills up but that's acceptable per user preference.
- **Should truths file be per-regulation?** No — keep it global for now. Most truths (Incineroar playstyle, Mega Sol ability) apply across regulations. The user can add regulation tags as freetext if needed.
- **Does the skill still write the review report to disk?** Yes — behavior unchanged. Analysis fills the context; the written file is the durable artifact.
- **Incineroar + Protect: legality vs. competitive truth?** Competitive truth, not legality. Protect is legal on Incineroar. The truths file should say "Incineroar should not run Protect — its turns are better spent on Fake Out, Parting Shot, and Intimidate cycling."

### Deferred to Implementation

- Whether to remove the Task-based progress tracking steps from SKILL.md entirely or keep them as inline status messages — implementer can judge based on what reads more naturally in a single-context skill.
- Exact wording of the "completion suggestion" framing for missing EVs/items — should feel like a coach filling in gaps, not a validator reporting errors.

## Implementation Units

- [ ] **Unit 1: Rewrite `skills/review-team/SKILL.md` as inline analysis**

**Goal:** Remove all Task agent spawning. The skill does all analysis steps directly: read team file inline, read meta report inline, perform matchup analysis, produce improvements — all in the main conversation context.

**Requirements:** R1, R2

**Dependencies:** None

**Files:**
- Modify: `skills/review-team/SKILL.md`

**Approach:**
The rewritten skill has the same five logical steps but executes them all inline:

1. **Validate + load data** — same gate logic (check arg, check file exists, find meta report, resolve data paths). Read and print the team file contents inline.
2. **Assess team completeness** — per-Pokemon check: does each entry have an item? non-zero EVs? Is the roster 6 Pokemon? Classify the team:
   - `complete` — 6 Pokemon, all have items and EVs
   - `draft` — 6 Pokemon but some missing items or EVs (suggest completions for incomplete slots)
   - `partial` — fewer than 6 Pokemon (suggest additions)
   A `draft` team is not flagged as broken; incomplete slots get completion suggestions alongside the rest of the review.
3. **Load competitive truths** — read `data/competitive-truths.md`. If it exists, treat its contents as authoritative facts that override AI priors during analysis. If missing, skip silently.
4. **Inline meta coverage analysis** — the skill (running as Claude in main context) reads the meta report and produces:
   - Threat grid (top 10 threats vs. this team)
   - Archetype matchup table
   - Type vulnerability audit
   - Structural gaps
   - Overall verdict
   Frame the Threat Grid and Structural Gaps sections to account for team completeness mode — draft/partial teams get "this gap may be addressed by completing [slot]" notes rather than hard CRITICAL flags for incomplete slots.
5. **Inline improvement suggestions** — produce:
   - Change list (CRITICAL → IMPORTANT → POLISH)
   - For `draft` mode: completion suggestions for each incomplete slot (item recommendation, EV spread target, move suggestion if moves are also bare)
   - For `partial` mode: addition suggestions for missing slots
   - Suggested leads by matchup
   - Revised Showdown paste
6. **Write report to disk** — same output path logic as before

Remove the parallel Task call pattern entirely. Remove agent references in the step descriptions.

Keep the progress tracking task list (it provides good UX for a long inline operation).

**Patterns to follow:**
- `skills/build-tr-team/SKILL.md` — inline data loading and synthesis; all analysis done by the orchestrating skill, not subagents

**Test scenarios:**
- Full complete team → all sections produced, no "completion suggestion" sections
- Full team with missing items/EVs on some Pokemon → those slots get completion suggestions in the improvement section; not flagged as CRITICAL structural errors
- Partial team (< 6 Pokemon) → addition suggestions for missing slots
- Competitive truths file present → truths are noted in analysis ("Per competitive-truths.md: Incineroar should not run Protect")
- No meta report → stops and prompts to run `/vgc:scout-meta`

**Verification:**
- SKILL.md contains no `Task vgc-download:` calls
- Skill produces all required report sections (threat grid, archetype table, type audit, structural gaps, verdict, change list, leads, revised paste)
- Running the skill leaves a complete review report in `data/teams/reviews/`

---

- [ ] **Unit 2: Create `data/competitive-truths.md` with initial entries**

**Goal:** Give the user a home for known competitive facts that override AI priors. Seed it with the two facts that surfaced from the first run: Mega Sol on Meganium-Mega, and Incineroar + Protect anti-pattern.

**Requirements:** R3, R4

**Dependencies:** None (can run in parallel with Unit 1)

**Files:**
- Create: `data/competitive-truths.md`

**Approach:**
Format: a flat markdown file with a brief header, then facts organized into labeled sections. The skill reads the whole file as raw context — no parsing needed. Sections:

- `## Mega Abilities (Pokemon Champions)` — for Mega forms whose abilities are missing from the Pokemon DB because PokeAPI doesn't have Pokemon Champions data
- `## Move Restrictions` — moves a Pokemon can legally learn but should never run for competitive reasons
- `## Item Restrictions` — items that are legal but widely considered anti-competitive for specific Pokemon
- `## Playstyle Rules` — broader strategic truths about specific Pokemon's role

Initial entries:
- **Mega Sol (Meganium-Mega):** Ability is "Mega Sol" — a Drought-equivalent that sets harsh sunlight on switch-in. This makes Weather Ball Fire-type (90 BP) and enables Solar Beam without a charge turn. Meganium-Mega is a Grass/Fairy type with this ability.
- **Incineroar no Protect:** Incineroar can learn Protect but should never run it in VGC. Its turns are worth more on Fake Out (turn 1 flinch), Parting Shot (pivot + Intimidate reset), and Knock Off/Flare Blitz. A turn spent on Protect is a turn wasted on Incineroar.

**Test scenarios:**
- File exists at `data/competitive-truths.md` after this unit
- Contains the Mega Sol section with Meganium-Mega ability documented
- Contains a playstyle or move restriction entry for Incineroar + Protect

**Verification:**
- `data/competitive-truths.md` exists with both initial entries
- Format is human-readable and editiable without tooling

---

- [ ] **Unit 3: Document Mega ability gap in CLAUDE.md**

**Goal:** Make the Pokemon DB's Mega ability limitation a known, documented fact so future agents and developers don't make incorrect assumptions about the DB's completeness for Pokemon Champions Megas.

**Requirements:** R5

**Dependencies:** None

**Files:**
- Modify: `CLAUDE.md`

**Approach:**
Add a note in the `## Data` section under the Pokemon DB entry. The note should explain:
- The DB fetches from PokeAPI, which doesn't have Pokemon Champions Mega data
- Pokemon Champions Megas that don't exist in PokeAPI (or have different abilities) will have `"abilities": []` in the DB
- The `data/competitive-truths.md` file is the authoritative source for these abilities
- Move pools (`moves` array) are empty for all Pokemon in the DB — the DB currently stores only types, base stats, and abilities. Do not cite the DB as move legality authority.

**Test scenarios:**
- CLAUDE.md contains a note about the DB limitation under the Pokemon DB documentation
- The note references `data/competitive-truths.md` as the override

**Verification:**
- CLAUDE.md updated with two-point note: (1) Mega ability gap for Champions Megas, (2) move pools not stored in DB

---

- [ ] **Unit 4: Install and commit**

**Goal:** Push all changes to the installed location, commit, and update the PR.

**Requirements:** All

**Dependencies:** Units 1, 2, 3

**Files:**
- Run: `node bin/cli.mjs install`

**Approach:**
- Run `node bin/cli.mjs install` to push updated `skills/review-team/SKILL.md` to `~/.claude/`
- Commit all four changed/created files: SKILL.md, competitive-truths.md, CLAUDE.md, and plan doc
- Push to the existing `feat/review-team-skill` branch (PR #12 is already open)

**Test scenarios:**
- Install runs without error
- `~/.claude/skills/review-team/SKILL.md` reflects the updated inline version (no Task calls)

**Verification:**
- `grep -r "Task vgc-download" ~/.claude/skills/review-team/` returns nothing
- `data/competitive-truths.md` exists and is readable

## System-Wide Impact

- **`vgc:tr-theory` skill:** `competitive-reference.md` has a note saying "verify moves against the Pokemon DB" — this is now known to be impossible since move pools are empty. Unit 2's truths file partially addresses this, but the reference doc note is misleading. Implementer should soften or remove that instruction from `competitive-reference.md`'s Hard Rule #3 during Unit 1 implementation.
- **`team-coverage-analyst.md` and `team-improvement-advisor.md`:** These agent files remain on disk but are no longer called. They can be left in place — they document the analysis structure and may be useful if the subagent approach is revisited.
- **`build-tr-team` pipeline:** Not affected. The truths file is read only by the `review-team` skill (for now).

## Risks & Dependencies

- **Inline skill context length:** Doing everything in one context means a full analysis of a 6-Pokemon team against a detailed meta report will consume significant context. For the current team size (6 Pokemon) and meta report length, this should be fine — the user has explicitly accepted this tradeoff.
- **Truths file growing unwieldy:** As the user adds more facts, the truths file could become large enough to slow analysis. Mitigation: keep sections focused; the user controls what goes in.
- **Move pool void:** The DB has no move pools. The skill cannot mechanically verify move legality. The skill should acknowledge this explicitly in its analysis framing rather than pretending to verify moves it cannot check. Document this in the truths file header.

## Sources & References

- Related PR: #12 (feat/review-team-skill branch)
- Existing skill: `skills/review-team/SKILL.md`
- Existing agents (retained but unused): `agents/coaching/team-coverage-analyst.md`, `agents/coaching/team-improvement-advisor.md`
- Pattern reference: `skills/build-tr-team/SKILL.md`
- DB gap confirmed: `data/pokemon_db/reg_m-a_pokemon.json` → `Meganium-Mega.abilities = []`, all `moves = []`
