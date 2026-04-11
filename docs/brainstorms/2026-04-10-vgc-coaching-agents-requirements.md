---
date: 2026-04-10
topic: vgc-coaching-agents
---

# VGC Coaching Agents: Meta Scout + TR Architect

## Problem Frame

The data pipeline exists (regulations, items, usage stats), but there's no layer that turns raw data into actionable competitive insight. A player looking at `reg_m-a_meta.json` sees usage percentages — not archetypes, exploitable trends, or team suggestions. Two agents fill this gap: one that understands the meta landscape, and one that builds Trick Room teams to beat it.

## Requirements

- R1. **Meta Scout agent** — reads processed stats from `data/stats/processed/` and regulation data from `data/regulations/`, searches the web for current community sentiment (tournament results, tier lists, meta discussions), and synthesizes a dated markdown scouting report.
- R2. **Meta Scout output** — writes to `data/meta/<YYYY-MM-DD>_<regulation_id>_report.md`. Each run produces a new dated file, preserving meta history over time.
- R3. **Meta Scout requires no user input** — it reads the current regulation from `data/config.json`, loads the corresponding processed stats and regulation file, and runs autonomously.
- R4. **Meta Scout static docs** — the agent has supporting documentation that defines what a good meta analysis looks like: how to identify archetypes, rank threats, analyze speed tiers, spot exploitable weaknesses.
- R5. **TR Architect agent** — reads a meta report (from Meta Scout) + regulation data, searches the web specifically for current Trick Room builds/tech/innovations, and produces full team suggestions with strategic reasoning.
- R6. **TR Architect input** — accepts an optional file path argument pointing to a specific meta report. If not provided, picks up the most recent report from `data/meta/` or uses conversation context.
- R7. **TR Architect output** — writes complete team drafts to `data/teams/drafts/` with dated filenames. Each team includes 6 Pokemon with moves, items, EVs, natures, and abilities, plus strategic reasoning for each pick.
- R8. **TR Architect static docs** — the agent has supporting documentation covering Trick Room team-building theory: setter criteria, speed tier math, role coverage, anti-meta selection, and win condition planning. This framework needs to be defined collaboratively.
- R9. **TR Architect web research** — searches specifically for Trick Room strategies, builds, and innovations (not general meta analysis). Different lens from Meta Scout's broader meta research.
- R10. **Independent invocation** — both agents run as separate commands. They share data through files (`data/meta/` reports), not through direct chaining.

## Success Criteria

- Meta Scout produces a report that a competitive player would find genuinely useful for understanding the current meta landscape — not just a restatement of usage percentages
- TR Architect produces team drafts with specific enough detail to paste into Pokemon Showdown (or at minimum, start testing immediately)
- A new regulation drop requires only re-running the existing data pipeline + invoking Meta Scout — no agent changes needed

## Scope Boundaries

- TR Architect is a Trick Room specialist only — not a general team builder
- Agents do not modify the data pipeline (scripts stay as-is)
- Agents do not auto-chain — the user decides when to run each
- MCP server is out of scope for this brainstorm (remains a stub)
- No matchup simulation or damage calc — agents reason qualitatively, not quantitatively

## Key Decisions

- **Markdown over JSON for reports**: Meta reports are for human reading first, agent consumption second. Markdown is the right format.
- **Dated files over overwriting**: Both agents write dated output files, preserving history so the user can track how the meta and team ideas evolve.
- **Drafts folder for teams**: Teams go to `data/teams/drafts/` — the user promotes a draft to `data/my_team.json` when they're happy with it.
- **Both agents search the web**: Meta Scout for broad meta sentiment, TR Architect for TR-specific builds and tech. Different research lenses.

## Resolved Questions

- **Meta report sections** (R4): Top Threats (ranked with sets/strengths/weaknesses), Dominant Archetypes (with prevalence), Speed Tier Breakdown, Exploitable Weaknesses, Item & Move Trends.
- **TR theory framework** (R8): Draft framework covers core roles (setter, abuser, redirector, speed control backup, anti-meta pick), speed tier rules, team composition checks (Taunt/Imprison answers, Plan B without TR), and win condition planning. Exact content to be collaboratively refined during implementation.
- **Static docs for both agents**: Both Meta Scout and TR Architect need supporting static documentation. Content will be authored collaboratively during implementation.

## Outstanding Questions

### Deferred to Planning

- [Affects R7][Technical] What format should team draft files use? (Showdown paste format, custom JSON, or both)
- [Affects R5][Needs research] How should agents be defined in the Claude Code plugin system — what goes in `agents/*.md` vs skills vs CLAUDE.md?
- [Affects R2][Technical] Should `data/meta/` be added to `.gitignore` since reports are generated and personal, or tracked for history?

## Next Steps

→ `/ce:plan` for structured implementation planning
