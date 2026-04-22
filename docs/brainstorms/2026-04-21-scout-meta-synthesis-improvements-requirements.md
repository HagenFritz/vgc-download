---
date: 2026-04-21
topic: scout-meta-synthesis-improvements
---

# Scout-Meta Skill — Synthesis Quality Improvements

## Problem Frame

The `/scout-meta` skill spawns four analyst agents in parallel (usage, archetype, community, exploit) and synthesizes their outputs into a dated report. Observation from a real run on 2026-04-21: the synthesis over-weighted the usage-analyst output and underused the community-scout output, even though community findings contained the highest-signal material (named tournament winners, 62.3% Hard TR ladder WR, the "no Covert Cloak is format-defining" narrative, specific rising tech like Talonflame and Rapid Strike Urshifu).

The user had to manually prompt a second pass to fold community material in. The skill's source-mapping table (Section 5 of SKILL.md) lists community-scout only as a *secondary* source on 3 of 8 report sections — a structural bias toward stats. The skill also has no synthesis-quality checks before writing: a report that leans 80/20 on one agent produces the same "confirm with 3-line summary" output as one that balances all four.

This affects report usefulness directly. A team builder reading the original draft would miss that Sun + Tailwind won the first tournament weekend despite being only ~8–10% of usage — which is a team-selection-level decision.

## Requirements

- **R1.** The skill must treat each of the four analyst outputs as a first-class input to synthesis. No section should be "usage-only" where community signal is available. The source-mapping table must be rebalanced so community-scout is a primary or co-primary source for at least archetype prevalence, meta narrative, rising tech, and anti-meta strategies.
- **R2.** The skill must include an explicit **synthesis-balance check** before writing the report: count references to each agent's findings across the draft, and flag any agent whose contribution is below a floor (e.g., fewer than 3 distinct references). If flagged, the synthesizer must revise before writing.
- **R3.** When stats and community signal disagree on archetype prevalence (e.g., usage 8% vs. "won both tournaments this weekend"), the report must surface the divergence explicitly — not silently prefer one. The current rule ("present both with the data-side first and note the divergence") is too weak; requires a named **Signal Divergence** callout in the relevant section.
- **R4.** The report must include a **Meta Narrative** block near the top that names the format's defining story (from community-scout) — e.g., "no Covert Cloak is a format-defining item absence." This is the single most actionable framing piece and was buried in Item Trends in the original draft.
- **R5.** The skill must record named tournament winners, event sizes, and dates when community-scout returns them — not paraphrase. A team builder uses specific names to find team lists later.
- **R6.** Prevalence estimates in the Dominant Archetypes section must be allowed to deviate from raw usage when tournament results justify it, with the reasoning shown inline (e.g., "~8–10% by stats, but won both 4/19 events — overperforming").
- **R7.** The synthesis step must produce a **coverage self-audit** appended to the report (or held in orchestrator context) listing which agent claims were used, which were dropped, and why. This makes the synthesis auditable instead of a black box.
- **R8.** The skill must handle thin / sparse data cases more honestly. When only 53 of 259 Pokemon have usage data (observed), the report's Unknown Pokemon section should be structurally richer — grouped by role, with community-scout's rising-tech picks *promoted* into it rather than buried.
- **R9.** Agent prompts should be updated so community-scout explicitly returns a **"Headline insight" field** — the one framing the synthesizer should anchor the report around. Currently community-scout returns six sections with no prioritization.
- **R10.** The skill should add a lightweight **"what would change my mind"** section to the report: list the 2–3 upcoming events or data sources (e.g., Indianapolis Regional) whose results would invalidate the current read. This forces the synthesizer to state confidence explicitly.

## Success Criteria

- A test run against the same 2026-04-21 inputs produces a report where community findings (tournament winners, ladder WRs, narrative framing, rising tech picks) appear in the report body on first write — not only after manual prompting.
- Synthesis-balance check correctly flags drafts that over-rely on one agent (verified by deliberately under-weighting one agent's input and confirming the check catches it).
- Signal Divergence callouts appear when stats and community disagree (verified against the Sun and Hard TR archetypes in the test run).
- A reader can skim the top 3 sections of the report and get the format's defining story, not just a stats readout.
- Coverage self-audit shows ≥80% of each agent's section-level claims either used or explicitly dropped-with-reason.

## Scope Boundaries

- **Not in scope:** Changing the four analyst agents' roles or adding new agents. The issue is synthesis, not gathering.
- **Not in scope:** Automating the `/scout-meta` run on a schedule, or ingesting more raw data sources. Input quality is a separate concern.
- **Not in scope:** Tooling to validate stats (e.g., checking Pokemon DB stat fields are populated — noticed as empty during the run). Worth a separate side-quest.
- **Not in scope:** Rewriting the report template itself beyond adding the Meta Narrative, Signal Divergence, and "What would change my mind" blocks.
- **Not in scope:** Changing how `build-tr-team` consumes the report (downstream concern).

## Key Decisions

- **Rebalance the source-mapping table in SKILL.md Step 5**, rather than relying on synthesizer judgment. Structural bias is easier to fix than prompt-level coaching.
  - *Rationale:* The current table lists community-scout as "Secondary" for 3 of 8 sections and primary for only 1. Flipping the defaults forces balance.
- **Synthesis-balance check is a hard gate, not a soft suggestion.** Skill must revise before writing if an agent is underrepresented.
  - *Rationale:* Soft suggestions in the current "Rules" block (e.g., "Resolve contradictions with judgment") didn't prevent the failure mode on first run.
- **Keep community-scout's output structure as-is but add a required "Headline insight" field.** Less invasive than refactoring the whole agent.
- **Coverage self-audit goes in orchestrator context, not the public report by default.** Default: internal; optional: expose with a flag. Keeps the public report readable.

## Dependencies / Assumptions

- Assumes the four analyst agents remain roughly as-scoped today. If one is removed or split, the source-mapping table changes.
- Assumes `AskUserQuestion` + TaskCreate tooling stays available for the skill.
- Assumes the current report template consumers (`build-tr-team` primarily) can tolerate one new top-level section (Meta Narrative) without changes. Needs verification during planning.

## Alternatives Considered

- **Just update the prompt with "use all four agents equally."** Rejected — same class of soft guidance that failed on the 2026-04-21 run.
- **Merge community-scout into archetype-analyst.** Rejected — they have different tools (web vs. stats) and different failure modes; merging loses parallelism.
- **Have the synthesizer call an LLM review step before writing.** Deferred — the balance check + self-audit should be enough. Adding a review-agent layer is higher carrying cost and can be added later if the simpler checks fail.
- **Add a 5th "synthesizer" agent that does only synthesis.** Rejected — the orchestrator *is* the synthesizer and should stay that way; extracting synthesis loses the benefit of orchestrator context.

## Outstanding Questions

### Resolve Before Planning

- *(none — scope is bounded and decisions are made)*

### Deferred to Planning

- **[Affects R2][Technical]** What's the right implementation for the synthesis-balance check? A word-count heuristic per agent section? An LLM call? A structured "each agent's claims list" that the synthesizer must tick through? Planning should pick the lowest-cost approach that actually catches the failure.
- **[Affects R4][Technical]** Where exactly in the report does the Meta Narrative block go — before Top Threats, between Data Provenance and Top Threats, or as part of Data Provenance? Needs a pass on the report-template.md consumers.
- **[Affects R7][Technical]** Is the coverage self-audit appended to the report (as a collapsible section), kept in the orchestrator's response message, or written to a sibling `.audit.md` file? Output location affects downstream readers.
- **[Affects R10][Needs research]** What signal sources does community-scout already check that could populate "what would change my mind" cheaply? (Likely Victory Road's event calendar and Smogon's tournament thread.)
- **[Affects R1, R3][Technical]** Should divergence detection be automated (compare usage% to tournament-winner-archetype-count) or left to the synthesizer? Automated is more reliable; manual is cheaper to build.
- **[Affects all]** Should these improvements land as one skill update or phased (e.g., rebalance table first, then add checks, then add new sections)? Planning should decide based on whether each requirement can be tested independently.

## Next Steps

→ `/ce:plan` for structured implementation planning
