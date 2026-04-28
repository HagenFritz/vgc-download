---
date: 2026-04-27
topic: tr-builder-archetype-input
---

# TR Builder: User-Guided Archetype Input

## Problem Frame

The `/build-tr-team` skill currently produces a fully automated team draft with no way for the user to steer it toward a particular strategy or pinned picks. Users who have a specific core in mind (e.g., "Oranguru as TR setter + Mega Golurk No Guard Dynamic Punch as abuser") are forced to accept whatever the architect picks and manually evaluate fit afterward. Giving users an optional archetype argument lets experienced players get a team built *around* their ideas rather than despite them, while still benefiting from meta analysis and critic review.

## Requirements

- R1. The `/build-tr-team` skill accepts an optional free-text archetype argument (e.g., `"Oranguru setter + Mega Golurk abuser"`). When omitted, behavior is identical to today.
- R2. When an archetype argument is provided, it is passed to the tr-architect as a soft preference constraint — the architect strongly prefers the requested picks and roles but may deviate if a critic flags a critical viability failure (e.g., a pinned Pokemon is illegal in the regulation).
- R3. Critics (meta-coverage-checker, tr-viability-checker, speed-math-auditor) evaluate pinned picks on the same criteria as any other slot. If a pinned Pokemon fails a critical check, the critic flags it — but the revision pass works *around* the pick (adjusts teammates, items, EV spreads) rather than replacing it. Known weaknesses from pinned picks surface explicitly in the final report's "Known Weaknesses" section.
- R4. The final team draft file and the user confirmation message both note which picks (if any) were user-specified and which were architect choices.

## Success Criteria

- A user can invoke `/build-tr-team "Oranguru setter + Mega Golurk abuser"` and receive a 6-Pokemon draft where Oranguru is the TR setter and Mega Golurk is the primary abuser.
- If the user omits the archetype argument, the skill behaves exactly as before (no regressions).
- If a pinned Pokemon has a critical weakness, it appears in the final report's "Known Weaknesses" section with a clear note that it was user-specified and retained intentionally.

## Scope Boundaries

- The archetype argument is free-text; no structured schema or validation UI needed.
- The skill does not re-run critics after the revision pass to verify pinned-pick weaknesses are resolved — that's already the one-revision-max rule.
- This feature does not change how the scout-meta pipeline works.
- Move-level pinning ("must use Dynamic Punch") is in scope for the archetype string but the architect interprets it as a preference, not a hard contract — no enforcement mechanism needed beyond passing the text.

## Key Decisions

- **Soft preference, not hard pin**: Architect treats the archetype string as a strong preference. If a pick is regulation-illegal, the architect can deviate. This keeps the pipeline from silently producing illegal teams. (see conversation: 2026-04-27)
- **Skill argument, not interactive prompt**: Input is provided as a quoted string at invocation time. No runtime prompting. Keeps the flow identical to today when no argument is given.
- **Flag but don't replace**: Critics evaluate pinned picks normally. Revision pass works around them. Known weaknesses are documented rather than auto-fixed. This respects user intent and avoids the architect overriding explicit user choices.

## Dependencies / Assumptions

- `skills/build-tr-team/SKILL.md` is the only file that needs updating for the orchestration change (argument parsing + passing constraint to tr-architect Task call).
- `agents/coaching/tr-architect.md` needs a new instruction block explaining how to handle a user archetype constraint.
- The `argument-hint` frontmatter field in the skill already exists and just needs updating.

## Outstanding Questions

### Deferred to Planning

- [Affects R2][Technical] How should the SKILL.md parse and forward the argument? The skill is markdown-driven (not code), so "argument parsing" means reading `$ARGUMENTS` or equivalent and interpolating into the Task prompt string.
- [Affects R4][Technical] What's the best format for surfacing user-specified picks in the output file? Options: a header note, a tag in the roster section, a dedicated "User Constraints" section.

## Next Steps

→ `/ce:plan` for structured implementation planning
