---
title: "feat: Add Meta Scout and TR Architect coaching agents"
type: feat
status: active
date: 2026-04-10
origin: docs/brainstorms/2026-04-10-vgc-coaching-agents-requirements.md
---

# feat: Add Meta Scout and TR Architect Coaching Agents

## Overview

Add two Claude Code subagents that turn the existing data pipeline output into actionable competitive insight. Meta Scout synthesizes usage stats + web research into a meta scouting report. TR Architect reads that report and builds Trick Room teams. Both are independent, invoked separately, and share data through files.

## Problem Statement / Motivation

The data pipeline produces `reg_m-a_meta.json` with raw usage percentages, but a competitive player needs archetypes, exploitable weaknesses, speed tier analysis, and concrete team suggestions. These agents close the gap between "data" and "coaching." (See origin: `docs/brainstorms/2026-04-10-vgc-coaching-agents-requirements.md`)

## Proposed Solution

Two subagents in `agents/coaching/`, each with a companion skill for static reference docs:

1. **Meta Scout** (`agents/coaching/meta-scout.md`) — reads processed stats + regulation data, searches the web for community sentiment, writes a dated markdown report to `data/meta/`.
2. **TR Architect** (`agents/coaching/tr-architect.md`) — reads a meta report + regulation data, searches the web for TR-specific builds/tech, writes full team drafts to `data/teams/drafts/`.

Each agent's system prompt references a companion skill that provides static reference documentation (meta analysis methodology, TR theory framework). These skills are not user-invocable — they exist solely to inject domain knowledge into the agent's context.

## Technical Considerations

### Agent File Format

Claude Code agents use markdown with YAML frontmatter in `agents/<category>/agent-name.md`. Key frontmatter fields:

```yaml
---
name: meta-scout
description: "..."
model: inherit
tools: Read, Write, Bash, Glob, Grep, WebSearch, WebFetch
skills:
  - vgc:meta-analysis-guide
---
```

The body is the agent's system prompt — its full instructions. The `skills` field preloads companion skill content into the agent's context at startup.

### Companion Skills (Static Docs)

Each agent gets a non-user-invocable skill that holds reference documentation:

```
skills/
  vgc:meta-analysis-guide/
    SKILL.md              # Meta analysis methodology
    report-template.md    # Report section headings (contract between agents)
  vgc:tr-theory/
    SKILL.md              # TR team-building framework
    team-template.md      # Team draft format template
```

Frontmatter includes `user-invocable: false` so these don't appear in the `/` menu.

### Data Flow

```
data/config.json
    ↓ (current_regulation, current_meta)
data/stats/processed/<regulation_id>_meta.json  +  data/regulations/<regulation_id>.json
    ↓ (Meta Scout reads both)
data/meta/<YYYY-MM-DD>_<regulation_id>_report.md
    ↓ (TR Architect reads report + regulation)
data/teams/drafts/<YYYY-MM-DD>_<regulation_id>_tr_team.md
```

### Data Provenance

The processed stats file tracks its source in metadata fields (`source_file`, `source_metagame`, `source_battles`). When the source regulation doesn't match the target (e.g., Reg I stats filtered to Reg M-A legality), Meta Scout must prominently disclose this at the top of the report with a caveat. This is not an edge case — it's the default for new regulations. (See origin: resolved question on R4)

### Meta Report Contract

The meta report is markdown for human reading, but TR Architect also parses it. To prevent silent breakage, the report template defines required section headings as a contract:

```markdown
## Data Provenance
## Top Threats
## Dominant Archetypes
## Speed Tier Breakdown
## Exploitable Weaknesses
## Item & Move Trends
## Unknown Pokemon
```

Both agent prompts reference this template. If Meta Scout's output format changes, the template is the single source of truth.

### Team Draft Format: Showdown Paste

Team drafts use **Showdown paste format** — the success criteria say "paste into Pokemon Showdown," so the format should be directly pasteable. Each draft file contains:

1. A markdown header with metadata (date, regulation, strategy summary)
2. The Showdown paste block (6 Pokemon with moves, items, EVs, natures, abilities)
3. Strategic reasoning for each pick

Example:

```
# TR Team Draft — Reg M-A — 2026-04-10

## Strategy
[Why this team, what it beats, win conditions]

## Team (Showdown Paste)
Porygon2 @ Eviolite
Ability: Download
Level: 50
EVs: 252 HP / 4 Def / 252 SpA
Quiet Nature
IVs: 0 Spe
- Trick Room
- Tri Attack
- Ice Beam
- Recover

[... 5 more Pokemon ...]

## Reasoning
### Porygon2
[Why this Pokemon, what role it fills, what it beats]
```

### "Most Recent Report" Resolution

TR Architect must filter by the current regulation ID when picking the most recent report (not just by date). The naming convention `<date>_<regulation_id>_report.md` makes this straightforward — glob for `*_<current_regulation_id>_report.md` and sort by date prefix.

### Directory Creation

Both agents create output directories (`data/meta/`, `data/teams/drafts/`) on first run if they don't exist. No setup prerequisite.

### Web Search Failure

Both agents search the web. For new regulations with no community discussion yet, web search may return nothing useful. Agents proceed with data-only analysis and note the gap in their output (e.g., "No community discussion found for Reg M-A — analysis based on stats only"). They never block on empty search results.

### Unknown Pokemon (Additive — not in original requirements)

Meta Scout should flag regulation-legal Pokemon with no usage data (currently 104 of 259) in a dedicated section. These are potential surprise picks that the TR Architect should be aware of. This was not in the original requirements but is a low-cost addition that makes both agents more useful.

## Acceptance Criteria

- [ ] `agents/coaching/meta-scout.md` exists with correct frontmatter and system prompt
- [ ] `agents/coaching/tr-architect.md` exists with correct frontmatter and system prompt
- [ ] `skills/vgc:meta-analysis-guide/SKILL.md` exists with meta analysis methodology and report template
- [ ] `skills/vgc:tr-theory/SKILL.md` exists with TR theory framework and team draft template
- [ ] Meta Scout reads `data/config.json` to discover current regulation and meta file
- [ ] Meta Scout reads processed stats and regulation JSON, searches the web, writes dated report to `data/meta/`
- [ ] Meta Scout report includes all 7 required sections (Data Provenance, Top Threats, Dominant Archetypes, Speed Tier Breakdown, Exploitable Weaknesses, Item & Move Trends, Unknown Pokemon)
- [ ] Meta Scout discloses data provenance when source regulation doesn't match target
- [ ] TR Architect accepts optional file path argument for a specific meta report
- [ ] TR Architect defaults to most recent report matching the current regulation ID
- [ ] TR Architect searches the web for TR-specific builds/tech
- [ ] TR Architect writes team drafts in Showdown paste format to `data/teams/drafts/`
- [ ] TR Architect includes strategic reasoning for each Pokemon pick
- [ ] Both agents create output directories if missing
- [ ] Both agents handle empty web search results gracefully (proceed with data-only analysis)
- [ ] CLI installer (`bin/cli.mjs`) already copies `agents/` — verify it works with new `coaching/` subdirectory
- [ ] New skills are not user-invocable (`user-invocable: false`)

## Success Metrics

- Meta Scout report is genuinely useful to a competitive player — not a restatement of usage percentages
- TR Architect team drafts are detailed enough to paste into Showdown and start testing
- A new regulation drop requires only re-running the data pipeline + Meta Scout — no agent changes

## Dependencies & Risks

- **Web search quality**: Both agents depend on web search returning relevant results. For brand-new regulations, this will often return nothing — agents must degrade gracefully.
- **Data provenance**: Current stats are proxy data (Reg I filtered to M-A). Agents must be transparent about this.
- **TR theory content**: The exact framework content will be collaboratively authored during implementation. The structure is defined but the substance needs domain input from the user.
- **Meta analysis guide content**: Same — structure defined, substance needs collaborative authoring.

## Implementation Phases

### Phase 1: Agent + Skill Scaffolding

Create the file structure and frontmatter for both agents and both companion skills. Bodies can be placeholder prompts.

**Files:**
- `agents/coaching/meta-scout.md`
- `agents/coaching/tr-architect.md`
- `skills/vgc:meta-analysis-guide/SKILL.md`
- `skills/vgc:meta-analysis-guide/report-template.md`
- `skills/vgc:tr-theory/SKILL.md`
- `skills/vgc:tr-theory/team-template.md`

**Also:**
- Verify CLI installer handles `agents/coaching/` subdirectory correctly
- No need to pre-create `data/meta/` or `data/teams/drafts/` — agents create them on first run

### Phase 2: Meta Scout — Full Implementation

Write the complete Meta Scout agent prompt and meta analysis guide skill content.

1. **Meta analysis guide** (`skills/vgc:meta-analysis-guide/SKILL.md`): Define methodology for identifying archetypes, ranking threats, analyzing speed tiers, spotting weaknesses. Include the report template with required section headings.
2. **Meta Scout prompt** (`agents/coaching/meta-scout.md`): Full system prompt covering data loading, web search strategy, report writing, provenance disclosure, unknown Pokemon flagging.
3. **Test run**: Invoke Meta Scout against current Reg M-A data and review the output.

### Phase 3: TR Architect — Full Implementation

Write the complete TR Architect agent prompt and TR theory skill content. This phase requires collaborative authoring of the TR framework.

1. **TR theory** (`skills/vgc:tr-theory/SKILL.md`): Define setter criteria, speed tier rules, core roles, team composition checks, win condition planning. This will be authored collaboratively with the user.
2. **TR Architect prompt** (`agents/coaching/tr-architect.md`): Full system prompt covering report parsing, web search for TR builds, team construction, Showdown paste output, reasoning.
3. **Test run**: Invoke TR Architect against a Meta Scout report and review the team draft.

## Sources & References

### Origin

- **Origin document:** [docs/brainstorms/2026-04-10-vgc-coaching-agents-requirements.md](docs/brainstorms/2026-04-10-vgc-coaching-agents-requirements.md) — Key decisions carried forward: markdown over JSON for reports, dated files over overwriting, drafts folder for teams, both agents search the web with different lenses, independent invocation.

### Internal References

- Agent conventions from cc-forge: `agents/<category>/agent-name.md` with YAML frontmatter (`name`, `description`, `model`)
- Existing skill pattern: `skills/vgc:parse-regulation/SKILL.md`
- CLI installer: `bin/cli.mjs:43-57` (already handles agent directory copying)
- Data config: `data/config.json`
- Processed stats: `data/stats/processed/reg_m-a_meta.json`
- Regulation data: `data/regulations/reg_m-a.json`

### External References

- [Claude Code subagents docs](https://code.claude.com/docs/en/sub-agents) — agent frontmatter fields, `skills` preload, `tools` allowlist
- [Claude Code skills docs](https://code.claude.com/docs/en/skills) — `user-invocable: false`, supporting files in skill directories
- [Showdown paste format](https://pokepast.es/) — standard team export format for Pokemon Showdown
