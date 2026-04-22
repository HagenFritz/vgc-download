---
date: 2026-04-22
topic: build-tr-team-item-legality-sidequest
tied-to: docs/plans/2026-04-21-001-feat-scout-meta-synthesis-balance-plan.md (parallel skill-hardening work)
---

# Build-TR-Team — Item Legality Enforcement (Side-Quest)

## Problem Frame

The `/build-tr-team` pipeline produced a team on 2026-04-22 with **three illegal items** (Life Orb on Hatterene, Assault Vest on Rhyperior, Flame Orb on Conkeldurr). Pokemon Champions has a restricted 117-item legal list stored at `data/stats/items/champions_items.json` (sourced from serebii.net). None of the three team-building agents — `tr-architect`, `tr-viability-checker`, `speed-math-auditor` — load or cross-check this file.

The user caught the error; the pipeline did not. The `speed-math-auditor` explicitly validated "No illegal combos detected" while three of six slots carried illegal items. That's a false-pass, which is worse than a missed check — it signals confidence in wrong data.

`CLAUDE.md` references `data/stats/items/champions_items.json` as authoritative ("Legal items for the current game") but that reference lives in the data-pipeline section, not in agent definitions. The agents' training prior carries standard VGC items (Life Orb, Assault Vest, Choice Band, Flame Orb, Rocky Helmet) and will suggest them by default unless constrained.

## Requirements

- **S1.** `tr-architect` must load `data/stats/items/champions_items.json` before producing a draft and cross-check every item assignment against the list. Items not in the list are rejected before output.
- **S2.** `tr-viability-checker` must include a new check: **Item Legality** (each of the 6 items appears in `champions_items.json`). Fails loud if any item is illegal.
- **S3.** `speed-math-auditor` must stop asserting "No illegal combos detected" unless it has actually checked item legality — silent fallbacks to training prior knowledge are a false-pass.
- **S4.** Minimal viable fix: add the item-legality check to **one** agent (viability-checker is the natural home) and require `tr-architect` to read the file on load. Scoping down to one enforcement point is cheaper than three.

## Success Criteria

- Re-run `/build-tr-team` against the 2026-04-21 scouting report. Confirm the output team has zero illegal items on first write.
- Deliberately inject an illegal item into a mock draft. Confirm `tr-viability-checker` flags it as a CRITICAL failure, not a POLISH note.

## Scope Boundaries

- **Not in scope:** Building a move-legality checker (does this Pokemon learn this move in Champions). Separate problem.
- **Not in scope:** Ability legality. The Champions ability list is also restricted but would need its own data file; no such file exists in repo today.
- **Not in scope:** Tera type legality. Not relevant to Champions (no Tera).
- **Not in scope:** Changes to `/scout-meta`. The scout-meta synthesis improvements plan is parallel and independent — that's about *reading* stats; this is about *writing* teams.

## Key Decisions

- **Enforce in `tr-viability-checker`, not in `tr-architect`.** Rationale: `tr-architect` is a creative agent with a wide output surface — enforcing hard rules there fights its nature. The checker is already a validation pass, so adding a check there is clean. If the architect drafts illegal items, the checker catches it and revision fixes it.
- **Still require `tr-architect` to load the item file for reference.** Even if the final enforcement is downstream, giving the architect the legal list up-front reduces the chance of illegal drafts in the first place and avoids burning a revision cycle on something mechanical.
- **Define a "preferred legal substitutes" mapping** in the architect's prompt for the most commonly-wanted illegal items (Life Orb → Twisted Spoon / Fairy Feather / type-booster; Assault Vest → type-resist berry or Leftovers; Flame Orb → Black Belt + Iron Fist or similar). Prevents the architect from fumbling substitution the way the 2026-04-22 pipeline did (user had to fix it manually).

## Dependencies / Assumptions

- Assumes `data/stats/items/champions_items.json` stays authoritative. If Champions adds items via game updates, the file must be refreshed (`scripts/parse_items.py` already exists for this).
- Assumes the three coaching agents can read repo files via their existing tool set (checked: they all have `Read`).

## Alternatives Considered

- **Just add "check items are legal" to the agent prompts without loading the file.** Rejected — agents will fall back to training priors and hallucinate a legal item list. The whole point of the data file is to be authoritative.
- **Filter items at the skill level (orchestrator reads and rejects illegal).** Rejected — the orchestrator doesn't understand the strategic role of items, so filtering there produces garbage substitutions. Fix belongs in the agents.
- **Add a fourth "item-legality-checker" agent.** Rejected — single-purpose agents are expensive; this fits cleanly inside the existing viability checker.

## Outstanding Questions

### Resolve Before Planning

- *(none)*

### Deferred to Planning

- **[Affects S1][Technical]** Does `tr-architect` load the item file on every invocation, or does the orchestrator pass the item list in the prompt? Passing it is more reliable (agent definitely sees it) but costs tokens per run.
- **[Affects S4][Technical]** Should the illegal-item catch be a hard revision trigger (like the existing CRITICAL findings) or a soft inline fix (checker suggests substitute, architect applies)? Hard revision is safer but slower.
- **[Affects all]** Should the same pattern extend to ability legality later? If yes, the enforcement mechanism should be generic enough to handle multiple legality checks, not hard-coded to items.

## Next Steps

→ `/ce:plan` when ready. Scope is small and bounded.
