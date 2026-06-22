---
date: 2026-04-28
topic: team-review
---

# Team Review Skill

## Problem Frame

The `build-tr-team` skill drafts teams from scratch. There is no equivalent skill for evaluating a team you already have — whether that's a 6-pokemon build you're iterating toward tournament readiness or a partial skeleton you want honest meta feedback on before investing further. Without this, the coaching pipeline has no feedback loop: you build a team, run it, feel something's off, and have no structured way to diagnose why or what to change.

## Requirements

- R1. The skill accepts a file path to a team file (pokepaste or existing draft format) as its input argument.
- R2. The skill reads `data/config.json` to determine the current regulation and locates the latest meta scouting report, regulation JSON, Pokemon DB, and legal items list — same data load as `build-tr-team`.
- R3. The skill fires two specialist agents in parallel:
  - **team-coverage-analyst**: meta matchup breakdown — which archetypes the team beats/loses to, shared type weaknesses, structural gaps, archetypes the team drowns to, anything over-covered or under-covered
  - **team-improvement-advisor**: concrete suggestions — lineup substitutions (if full team) or additions (if partial), move slot changes, EV adjustments, item swaps, and lead recommendations per matchup. Produces both a change list and a revised Showdown paste with suggestions applied.
- R4. The skill synthesizes both agents' outputs into a single structured team report written to `data/teams/reviews/` with a datestamped filename.
- R5. For partial teams (fewer than 6 Pokemon), team-improvement-advisor suggests additions to complete the roster rather than substitutions.
- R6. Both agents receive: the team file, meta report path, regulation JSON path, Pokemon DB path, and legal items path. Agents must validate any suggested Pokemon against the regulation's `allowed_pokemon` list and any suggested items against `champions_items.json`.
- R7. The competitive reference docs (currently `skills/build-tr-team/competitive-reference.md`) are extended with hard rules and anti-patterns that constrain what agents can suggest — the primary quality control mechanism to prevent nonsense suggestions.

## Success Criteria

- Running `/review-team data/teams/drafts/my_team.md` produces a structured report I can act on in under 5 minutes of reading.
- Meta coverage section clearly names 3-5 archetypes from the current scouting report and tells me whether I beat or lose to each, and why.
- Improvement suggestions reference real Pokemon (legal in current regulation) with real move pools — no impossible sets.
- The revised paste is valid Showdown format and consistent with the change list.
- Partial team inputs (1-5 Pokemon) produce addition suggestions, not errors.

## Scope Boundaries

- No web search in this skill's agents — analysis is grounded in local meta report and Pokemon DB only. (Web search is already done by `scout-meta`; review uses that output.)
- No auto-apply of suggestions — the revised paste is a suggestion, not a replacement for the input file.
- No interactive back-and-forth with the user mid-run — skill runs to completion and outputs the report.
- Not a replacement for `build-tr-team` — does not draft teams from scratch.

## Key Decisions

- **File path only (no paste input):** Keeps input handling simple and consistent with how team drafts are stored in the project.
- **Multi-agent pipeline:** Two parallel specialists (coverage analyst + improvement advisor) makes each tunable independently, matches the `build-tr-team` critic pattern, and keeps prompts focused.
- **Matchup breakdown is primary output:** The meta coverage section leads the report; improvements follow. Reflects the primary use case of understanding where the team stands before deciding what to change.
- **Revised paste included in improvement output:** Convenience wins here, but the paste is clearly labeled as a suggestion and the change list is the canonical recommendation.
- **Quality control via reference docs:** Extending `competitive-reference.md` with hard rules and anti-patterns (not a validator agent) is the primary mechanism for keeping suggestions realistic. Simpler to maintain than a third critic agent.

## Dependencies / Assumptions

- A current meta scouting report exists in `data/meta/` — if not, skill should stop and direct the user to run `/scout-meta` first (same gate as `build-tr-team`).
- Input team file is readable and contains at least 1 Pokemon in pokepaste or draft format.
- `competitive-reference.md` needs meaningful extension before agents will reliably avoid nonsense suggestions — this is pre-work for planning.

## Outstanding Questions

### Resolve Before Planning

- None.

### Deferred to Planning

- [Affects R7][Needs research] What specific anti-patterns and hard rules should be added to `competitive-reference.md`? (Survey common failure modes from existing drafts.)
- [Affects R3][Technical] Should `team-coverage-analyst` and `team-improvement-advisor` be new agent files in `agents/coaching/`, or reuse/extend existing agents? Existing `meta-coverage-checker` is scoped to TR composition checks — likely needs a new, broader agent.
- [Affects R4][Technical] What is the output file format for the review report — match the existing draft `.md` structure, or a new review template?
- [Affects R5][Technical] How does the skill detect whether a team is partial (< 6 Pokemon) to switch between substitution vs. addition mode?

## Next Steps

→ `/plan` for structured implementation planning
