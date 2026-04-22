---
title: Scout-Meta Synthesis Balance & Community Integration
type: feat
status: active
date: 2026-04-21
origin: docs/brainstorms/2026-04-21-scout-meta-synthesis-improvements-requirements.md
---

# Scout-Meta Synthesis Balance & Community Integration

## Overview

Rework the `/scout-meta` skill's synthesis step so the final report draws in balance from all four analyst agents (usage, archetype, community, exploit) — not primarily from usage. A real run on 2026-04-21 produced a draft that under-used community findings (named tournament winners, ladder WRs, the "no Covert Cloak" narrative, rising-tech picks like Talonflame and Rapid Strike Urshifu) and had to be manually revised. This plan introduces a structured **claims-list contract** between agents and the orchestrator, a **balance check** gate before writing, and three new report blocks (Meta Narrative, Signal Divergence callouts, What Would Change My Mind) that specifically surface community signal.

## Problem Statement

The skill has a structural bias toward stats. In the SKILL.md source-mapping table, community-scout is listed as a **secondary** source on 3 of 8 report sections and **primary** on only 1, with no mechanism to detect when synthesis is unbalanced. Agents return free-form markdown; the synthesizer reads them and writes a report in one pass, with no accounting of which claims were used. Soft guidance ("resolve contradictions with judgment") did not prevent the 2026-04-21 regression.

Concrete failures from that run (see origin doc Problem Frame):
- Named 4/19 tournament winners (TheMoistPleb, HyogaVGC) absent from first draft.
- Sun archetype prevalence estimate was 8–10% by usage with **no** signal that it won both major tournaments that weekend.
- "No Covert Cloak is format-defining" — community-scout's best framing — was buried in the Item Trends section instead of anchoring the report.
- Hard TR's 62.3% ladder WR (community) and 5–7% usage (stats) divergence was unannotated.
- Rising tech picks (Rapid Strike Urshifu vs Incin, Hippowdon vs Sneasler, Primarina as Intimidate-ignoring attacker) were dropped.

The user had to prompt a second pass to fold community findings in. That's a synthesis defect, not a gathering defect — all four agents returned quality output.

## Proposed Solution

Three structural changes, landed as one atomic skill update (see phasing rationale in Technical Approach → Implementation Phases):

1. **Rebalance the source-mapping table** in SKILL.md so community-scout is primary or co-primary on archetype prevalence, meta narrative, rising tech, and anti-meta strategies (see origin: `docs/brainstorms/2026-04-21-scout-meta-synthesis-improvements-requirements.md` → R1).
2. **Change the agent-to-orchestrator contract** — each agent appends a structured `Claims` list (5–10 numbered, one-line key findings) to its markdown output. Community-scout additionally appends a **Headline Insight** field (R9).
3. **Add a balance-check gate** in the skill methodology — the synthesizer must tick through every agent's `Claims` list (used or dropped-with-reason) before writing the report. The ticked list becomes the **coverage self-audit** (R7) held in orchestrator context.

Add three report blocks driven by those changes: **Meta Narrative** after Data Provenance (R4), **Signal Divergence** callouts in Dominant Archetypes and Top Threats when stats and community disagree (R3, R6), and **What Would Change My Mind** near the end (R10).

## Technical Approach

### Architecture

Touch points (all markdown, no code):

- `skills/scout-meta/SKILL.md` — rebalanced source-mapping table, new balance-check step, new Meta Narrative / Signal Divergence / What-Would-Change-My-Mind rules, confirmation output updated to cite the audit.
- `skills/scout-meta/report-template.md` — three new section templates; `## Data Provenance` follows current convention; new sections inserted in the order: Data Provenance → Meta Narrative → Top Threats → … → What Would Change My Mind.
- `agents/coaching/community-scout.md` — output contract adds `### Headline Insight` and `## Claims` sections, plus a named-entities rule (tournament winners, event size, date — no paraphrasing) to solve R5.
- `agents/coaching/usage-analyst.md` — output contract adds `## Claims` list.
- `agents/coaching/archetype-analyst.md` — output contract adds `## Claims` list.
- `agents/coaching/exploit-finder.md` — output contract adds `## Claims` list.

No new agents, no code changes, no data-pipeline changes. This is prompt engineering plus report-template evolution.

### The Claims Contract (load-bearing design)

Every agent appends, as the final section of its return message:

```markdown
## Claims
1. [one-line claim with inline numbers when relevant]
2. …
(5–10 claims, each testable against the agent's own body text)
```

Community-scout additionally prepends:

```markdown
### Headline Insight
[One sentence — the single framing line that should anchor the report. If no clear narrative emerged from research, return: "No clear narrative — community coverage is thin."]
```

The synthesizer in SKILL.md Step 5 (renumbered to Step 5a/5b):

- **5a. Collect Claims.** Concatenate all four agents' `Claims` lists into a single numbered roster (e.g., U1–U8, A1–A7, C1–C9, E1–E6 prefixed by agent).
- **5b. Tick-through.** For each claim, decide: **Used** (cite where in the report body), **Dropped** (one-line reason, e.g., "redundant with U3", "low-confidence per Gaps & Caveats"), or **Deferred** (list in Outstanding Questions). No fourth option. The ticked table is the audit (R7).
- **5c. Balance gate.** If any agent has <60% of its claims Used + Dropped-with-reason (i.e., any Deferred-without-reason OR unaddressed), the synthesizer must revise before writing. If any agent has 0 Used claims, hard-fail and revise regardless.
- **5d. Divergence detection.** During tick-through, when a Used claim from one agent contradicts a Used claim from another (numeric disagreement, archetype prevalence gap, contradictory narrative), flag it and require a **Signal Divergence** callout in the relevant report section.

**Why claims-list over alternatives** (origin deferred question, resolved here):

- **Word-count heuristic.** Rejected — provenance is unidentifiable once the synthesizer paraphrases.
- **LLM review pass.** Rejected as first choice — higher carrying cost, and the claims-list solves the same problem *plus* gives us the audit for free (one mechanism, two requirements).
- **Claims list with manual tick-through.** Selected. Cheap, observable, auditable, and the structure itself forces balance.

### Report Structure Changes

Current template order → new template order (see `skills/scout-meta/report-template.md`):

```
1. Data Provenance
2. Meta Narrative                    ← NEW (community-scout Headline Insight + expansion)
3. Top Threats
4. Core Combinations
5. Dominant Archetypes               ← Signal Divergence callouts added where applicable
6. Speed Tier Breakdown
7. Exploitable Weaknesses
8. Item, Move & Mechanic Trends
9. Unknown Pokemon                   ← restructured per R8: grouped by role, community-scout
                                       rising-tech picks promoted here instead of buried
10. What Would Change My Mind        ← NEW (community-scout-sourced; upcoming events to watch)
```

**Meta Narrative block** — 2–4 sentences max, anchored by community-scout's Headline Insight. Hard rule: if Headline Insight returned "No clear narrative — community coverage is thin.", the block is **omitted entirely** rather than fabricated. Synthesis must not manufacture narrative.

**Signal Divergence callout** — inline blockquote format:

```markdown
> **Signal Divergence:** Stats list Sun at ~8–10% usage; community-scout reports both major 4/19 events were won by Sun+Tailwind (TheMoistPleb 9-2, HyogaVGC 8-1). Treat stats prevalence as a floor, not a ceiling.
```

Required in Dominant Archetypes entries when prevalence estimates differ from raw usage due to community evidence; required in Top Threats entries when ladder WRs diverge from usage-share rank.

**What Would Change My Mind** — bullet list of 2–3 upcoming events / data drops community-scout named. If community-scout surfaces none, fall back to "Next ladder stats refresh" as a single default bullet.

### Revised Source-Mapping Table

New table for SKILL.md Step 5 (was Step 5):

| Report Section | Primary | Co-primary | Secondary |
|---|---|---|---|
| 1. Data Provenance | orchestrator provenance note | — | usage-analyst Data Snapshot |
| 2. Meta Narrative **(NEW)** | community-scout Headline Insight | — | exploit-finder structural gaps |
| 3. Top Threats | usage-analyst Top Threats | community-scout tier list consensus | — |
| 4. Core Combinations | archetype-analyst Dominant Cores | usage-analyst teammate data | — |
| 5. Dominant Archetypes | archetype-analyst + **community-scout tournament results** | — | community-scout Meta Shifts |
| 6. Speed Tier Breakdown | usage-analyst Speed Tier Distribution | archetype-analyst Speed Control Landscape | — |
| 7. Exploitable Weaknesses | exploit-finder | community-scout Anti-Meta Strategies | — |
| 8. Item, Move & Mechanic Trends | usage-analyst + **community-scout Rising Tech** | — | — |
| 9. Unknown Pokemon | orchestrator catalog + **community-scout rising-tech picks** | — | — |
| 10. What Would Change My Mind **(NEW)** | community-scout Gaps & Caveats / upcoming events | — | — |

Community-scout promoted from "secondary on 3 of 8" to "primary or co-primary on 6 of 10."

### Implementation Phases

One atomic update (single commit or PR) because each change is independently pointless — the balance check assumes claims lists exist; the Meta Narrative block assumes Headline Insight exists; the rebalanced table assumes the new sections exist. However, development can proceed in three internal steps for clarity:

#### Phase 1: Report template + source-mapping table

Files: `skills/scout-meta/report-template.md`, `skills/scout-meta/SKILL.md` (Step 5 table + Rules section additions).

Deliverables:
- New report-template.md with Meta Narrative, Signal Divergence guidance, What Would Change My Mind, restructured Unknown Pokemon.
- Rebalanced source-mapping table in SKILL.md.
- New rule in SKILL.md Rules section: "Omit Meta Narrative block if community-scout's Headline Insight returned the thin-coverage sentinel."

Success criteria: Template renders correctly (markdown valid); SKILL.md still flows as a coherent skill doc.

#### Phase 2: Agent contract changes

Files: `agents/coaching/{usage-analyst,archetype-analyst,community-scout,exploit-finder}.md`.

Deliverables:
- All four agents append `## Claims` section spec (5–10 terse claims, agent-prefixed IDs).
- community-scout prepends `### Headline Insight` spec with thin-coverage fallback.
- community-scout adds "Named Entities" rule: tournament winners, event sizes, dates returned verbatim, not paraphrased (R5).
- community-scout "Gaps & Caveats" section renamed/augmented to explicitly include **Upcoming Events to Watch** list.

Success criteria: Each agent's output contract is unambiguous and terse (no structural bloat).

#### Phase 3: Skill orchestration — balance gate

Files: `skills/scout-meta/SKILL.md` (Step 5 replaced with 5a/5b/5c/5d, new task in Progress Tracking).

Deliverables:
- Progress Tracking task list adds "Collect and tick-through claims" between "Run parallel analyst agents" and "Synthesize scouting report."
- Step 5a/5b/5c/5d methodology as specified above.
- Confirmation output (Step 6) updated to cite the audit numbers: "Written to …; audit: U 8/8 used, A 6/7 used (1 dropped), C 9/9 used, E 6/6 used."

Success criteria: Skill reads top-to-bottom as a clear procedure; balance gate is a hard step, not a suggestion.

## Alternative Approaches Considered

- **Prompt-only coaching without structural changes** (e.g., add "use all four agents equally" to the Rules section). Rejected — origin doc notes this is the class of soft guidance that already failed. The current Rules section already says "resolve contradictions with judgment" and it did not prevent the 2026-04-21 failure.
- **Merge community-scout into archetype-analyst.** Rejected in origin — different tools (web vs. stats), different failure modes, loses parallelism.
- **Fifth synthesizer agent.** Rejected in origin — orchestrator *is* the synthesizer and should stay so; extracting synthesis loses orchestrator context.
- **LLM review pass before writing.** Deferred — claims-list tick-through achieves the same balance goal with lower carrying cost and doubles as the audit trail. Reintroduce only if balance gate fails in practice.
- **Automated divergence detection** (compare usage% vs. tournament-winner-archetype-count). Rejected — structuring community-scout's output enough to enable automation would bloat the agent contract. Manual divergence flagging gated by the claims-tick step is the correct trade-off.

## System-Wide Impact

### Interaction Graph

```
/scout-meta (orchestrator)
  ├─ loads config.json, stats, regulation, Pokemon DB
  ├─ parallel-fires:
  │    ├─ usage-analyst ──→ markdown + Claims
  │    ├─ archetype-analyst ──→ markdown + Claims
  │    ├─ community-scout ──→ Headline Insight + markdown + Claims
  │    └─ exploit-finder ──→ markdown + Claims
  ├─ collects Claims roster (NEW)
  ├─ ticks through Claims (NEW — hard gate)
  ├─ detects divergence across ticked claims (NEW)
  ├─ writes report to data/meta/<date>_<reg>_report.md
  └─ reports audit counts to user
                │
                ↓ downstream consumer
        /build-tr-team reads data/meta/<latest>.md
                │
                ↓ specifically via agents/coaching/tr-architect.md
        which greps/reads the report for Top Threats, Archetypes, Speed Tiers
```

### Error Propagation

- **Agent returns no `Claims` section.** Balance gate should hard-fail that agent (0 Used) and trigger revision — but the synthesizer needs a fallback: re-prompt the agent once for a Claims list, then downgrade gracefully to "agent returned no Claims — synthesizer must infer claims from body." Add as a defensive rule.
- **Community-scout returns thin-coverage sentinel.** Expected path — Meta Narrative block omitted, What Would Change My Mind falls back to default bullet. No hard fail.
- **Claims-list contradicts body text.** Synthesizer must trust body text and flag in audit as a claim to verify. Rare but possible.

### State Lifecycle Risks

- **Partial audit on synthesizer error.** If the synthesizer dies mid-tick-through, no report is written and no audit is persisted. Acceptable — the skill is idempotent (re-run produces fresh agents and fresh claims). No orphaned state.
- **Report file overwrite.** Report filename is dated (`YYYY-MM-DD_<reg>_report.md`), so two runs in one day clobber. Not new, not this plan's concern — side-quest if it matters.

### API Surface Parity

Downstream consumers of the report:

- `agents/coaching/tr-architect.md` reads `data/meta/<latest>.md`. Today it consumes Top Threats, Dominant Archetypes, and Speed Tier Breakdown by section heading. New sections (Meta Narrative, What Would Change My Mind) are additive — will not break the consumer. Signal Divergence callouts are blockquotes inside existing sections — invisible to a heading-based reader.
- `skills/build-tr-team/SKILL.md` — same story.
- No API changes needed downstream.

**Verification step in Phase 1:** grep `agents/coaching/tr-architect.md` and `skills/build-tr-team/SKILL.md` for hard-coded section names before finalizing template order. If any consumer does heading-sensitive parsing of sections beyond Data Provenance / Top Threats / Dominant Archetypes, adjust.

### Integration Test Scenarios

No unit test framework for skills — "testing" is running the skill end-to-end and eyeballing output. Three scenarios to run against:

1. **Replay 2026-04-21 inputs.** Same regulation, same stats, same community window. Confirm:
   - TheMoistPleb and HyogaVGC tournament wins appear in Meta Narrative and/or Dominant Archetypes on first write.
   - "No Covert Cloak" framing anchors the Meta Narrative block.
   - Sun archetype entry has a Signal Divergence callout.
   - Hard TR's 62.3% ladder WR vs ~5–7% usage is flagged.
   - Audit shows ≥80% of community-scout claims Used.

2. **Deliberately starve one agent.** Mock community-scout to return empty output (or a stub). Confirm:
   - Balance gate catches it — synthesis does not proceed to writing.
   - If mock returns the thin-coverage sentinel for Headline Insight, Meta Narrative block is omitted cleanly without fabrication.

3. **Synthetic contradiction.** Mock stats saying archetype X is 30% usage + community saying archetype X lost every event. Confirm Signal Divergence callout fires.

## Acceptance Criteria

### Functional Requirements

- [ ] `skills/scout-meta/SKILL.md` source-mapping table rebalanced per the revised table above (R1).
- [ ] `skills/scout-meta/SKILL.md` Methodology Step 5 replaced with 5a/5b/5c/5d — claims collection, tick-through, balance gate, divergence detection (R2, R3, R7).
- [ ] `skills/scout-meta/SKILL.md` Rules section includes: (a) "Meta Narrative omitted if community-scout returned thin-coverage sentinel"; (b) "Tournament winners, event sizes, dates are copied verbatim from community-scout, never paraphrased" (R5); (c) "Balance gate is a hard stop — revise before writing, do not ship an unbalanced report."
- [ ] `skills/scout-meta/report-template.md` includes section templates for Meta Narrative (R4), Signal Divergence callouts (R3), What Would Change My Mind (R10), and restructured Unknown Pokemon that promotes community-scout rising-tech picks (R8).
- [ ] All four agents (`usage-analyst.md`, `archetype-analyst.md`, `community-scout.md`, `exploit-finder.md`) append a `## Claims` output spec (R2, R7 precondition).
- [ ] `community-scout.md` prepends `### Headline Insight` spec with thin-coverage sentinel (R9).
- [ ] `community-scout.md` adds "Named Entities" rule forbidding paraphrase of tournament winners / sizes / dates (R5).
- [ ] SKILL.md Progress Tracking task list adds "Collect and tick-through claims" task.
- [ ] SKILL.md confirmation output (Step 6) includes audit counts per agent.

### Non-Functional Requirements

- [ ] Agent output additions (Claims list, Headline Insight) stay terse — ≤10 claims per agent, one line each. No section bloat.
- [ ] Report template remains human-readable; new sections do not fragment the flow.
- [ ] No regressions in downstream consumers (tr-architect, build-tr-team) — verified by running `/build-tr-team` against a post-change report.

### Quality Gates

- [ ] Integration test scenario 1 (2026-04-21 replay) produces community findings in the report on first write.
- [ ] Integration test scenario 2 (starved community-scout) confirms balance gate fires.
- [ ] Integration test scenario 3 (synthetic contradiction) confirms Signal Divergence callout fires.
- [ ] Downstream check: `/build-tr-team` consumes the new report shape without error.

## Success Metrics

- **Primary:** A clean re-run of `/scout-meta` on the 2026-04-21 inputs produces a report that names tournament winners, includes the "no Covert Cloak" framing, flags Sun prevalence divergence, and lists rising-tech picks — all on first write, without user prompting for a second pass.
- **Secondary:** Audit output shows each agent with ≥80% claims Used, zero agents with 0 Used claims.
- **Tertiary:** User reading the top 3 report sections gets the format's defining story in ≤2 minutes (judgment call, not quantitative).

## Dependencies & Prerequisites

- No external dependencies.
- Assumes the current four analyst agents remain in scope (per origin). If any agent is split or retired, the source-mapping table must be revisited.
- Assumes the downstream consumer pattern (tr-architect / build-tr-team reading by section heading) holds — verified in Phase 1.

## Risk Analysis & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Balance gate becomes noisy — forces ceremony without improving output | Medium | Medium | Threshold is "every agent's claims addressed (Used or Dropped-with-reason)," not "every claim Used." Low-signal claims can be dropped with a one-line reason. Revisit threshold after 3 real runs. |
| Claims list inflates token cost per agent call | Low | Low | Cap at 10 claims, one line each. Rough budget: ~200 extra tokens per agent per run. Negligible. |
| Meta Narrative block encourages synthesizer to fabricate narrative when community signal is thin | Medium | High | Hard rule: if Headline Insight returns the thin-coverage sentinel, block is **omitted entirely**. Rule called out in SKILL.md Rules section explicitly. Belt-and-suspenders: Headline Insight sentinel string is fixed ("No clear narrative — community coverage is thin.") so the synthesizer can string-match it. |
| Agent omits `Claims` section entirely | Low | Medium | Defensive rule: synthesizer re-prompts agent once for Claims; if still absent, infers from body text and flags in audit. |
| Signal Divergence callouts proliferate and become noise | Low | Medium | Rule: only callout when the divergence is **actionable** (changes a build decision). Minor numeric wobble doesn't qualify. Spot-check after first real run. |
| Downstream consumer breaks on reordered sections | Low | High | Phase 1 verification grep before finalizing template. If tr-architect parses by heading, verify all referenced headings still exist and in a reasonable position. |

## Future Considerations

- **Automated divergence detection.** If manual callouts prove unreliable in practice, revisit structuring community-scout's output enough to enable programmatic comparison (e.g., machine-readable "events won by archetype" list). Deferred per origin doc rationale.
- **LLM review pass.** If balance gate fails to catch real regressions after 3 runs, add a lightweight LLM review as a second gate. Deferred.
- **Audit persistence.** Currently orchestrator-only; consider writing the audit to a sibling `.audit.md` file for historical tracking. Deferred per origin (kept internal by default).
- **Meta Narrative in downstream consumers.** If `tr-architect` starts keying off the narrative framing ("format has no Covert Cloak → Taunt is higher-leverage"), that's a real feature, not scope creep. Track as a follow-up.

## Documentation Plan

- Update `CLAUDE.md` only if the new report structure changes how TR-architect consumes meta reports. Likely not — new sections are additive.
- Update `skills/scout-meta/SKILL.md` comments at the top of Step 5a/5b to explain the claims-contract rationale briefly.
- No separate docs/ files needed — SKILL.md is authoritative.

## Sources & References

### Origin

- **Origin document:** [docs/brainstorms/2026-04-21-scout-meta-synthesis-improvements-requirements.md](../brainstorms/2026-04-21-scout-meta-synthesis-improvements-requirements.md)
  - Key decisions carried forward:
    1. Structural rebalance of source-mapping table over prompt-only coaching (Key Decisions).
    2. Balance check as hard gate, not soft suggestion (Key Decisions).
    3. Keep community-scout's output structure but add Headline Insight field (Key Decisions).
    4. Coverage self-audit internal to orchestrator, not in public report (Key Decisions).
  - All 10 requirements (R1–R10) mapped into Acceptance Criteria.
  - 6 Deferred-to-Planning questions from origin all resolved inline (balance-check implementation → claims list; Meta Narrative placement → after Data Provenance; audit location → orchestrator context; What-Would-Change-My-Mind sources → community-scout Gaps & Caveats + upcoming events; divergence detection → manual via claims tick-through; phasing → one atomic update, three internal development steps).

### Internal References

- Current skill: [skills/scout-meta/SKILL.md](../../skills/scout-meta/SKILL.md)
- Current template: [skills/scout-meta/report-template.md](../../skills/scout-meta/report-template.md)
- Agent files: [agents/coaching/community-scout.md](../../agents/coaching/community-scout.md), [usage-analyst.md](../../agents/coaching/usage-analyst.md), [archetype-analyst.md](../../agents/coaching/archetype-analyst.md), [exploit-finder.md](../../agents/coaching/exploit-finder.md)
- Real-world failure artifact: [data/meta/2026-04-21_reg_m-a_report.md](../../data/meta/2026-04-21_reg_m-a_report.md) (both before and after manual revision — compare versions to see exactly what the balance gate is supposed to catch)
- Prior skill plan (context for this repo's planning style): [docs/plans/2026-04-10-001-feat-meta-scout-tr-architect-agents-plan.md](2026-04-10-001-feat-meta-scout-tr-architect-agents-plan.md)

### Related Work

- Downstream consumer: [agents/coaching/tr-architect.md](../../agents/coaching/tr-architect.md) and [skills/build-tr-team/SKILL.md](../../skills/build-tr-team/SKILL.md) — must be verified non-breaking in Phase 1.
