---
title: "feat: TR Builder user-guided archetype input"
type: feat
status: completed
date: 2026-04-27
origin: docs/brainstorms/2026-04-27-tr-builder-archetype-input-requirements.md
---

# feat: TR Builder User-Guided Archetype Input

## Overview

Add an optional archetype preference argument to the `/build-tr-team` skill so users can steer the team draft toward specific picks and strategies (e.g., `"Oranguru setter + Mega Golurk No Guard Dynamic Punch abuser"`). The argument is forwarded to the tr-architect as a soft preference constraint — the architect strongly prefers the requested picks but may deviate only if a pick is regulation-illegal. Critics evaluate pinned picks normally; the revision pass works *around* user-specified picks rather than replacing them. Known weaknesses from pinned picks surface explicitly in the final report.

When no argument is provided, the skill behaves identically to today. Zero regressions.

## Problem Statement / Motivation

The current skill produces a fully automated draft with no user steering. Experienced players who have a specific core in mind (e.g., a setter/abuser pair from a recent tournament) have no way to get a team built *around* their ideas — they must accept the architect's choices and manually evaluate fit. This is the remaining scope from issue #8.

## Proposed Solution

Three file changes, in dependency order:

1. **`skills/build-tr-team/team-template.md`** — Add an optional `## User Constraints` section after `## Strategy Summary`. The architect fills this in when an archetype argument was provided; otherwise it is omitted.

2. **`skills/build-tr-team/SKILL.md`** — Two changes:
   - Update `argument-hint` frontmatter from `[meta report path]` to `[archetype preference]`
   - In Step 1, add instructions to capture the user's archetype argument as `<user_archetype_preference>`. In Step 2, conditionally include a `User Archetype Preference:` field in the tr-architect Task prompt when a preference was provided. In Step 5 (revision), instruct the architect to preserve user-pinned picks when working around critic findings.

3. **`agents/coaching/tr-architect.md`** — Add a `User Archetype Preference` instruction block explaining how to handle the new field: treat as strong preference, deviate only for regulation illegality, surface any known weaknesses from pinned picks in "Threats and Weaknesses".

## Technical Considerations

### Argument Passing Convention

This repo has no runtime argument-parsing mechanism — `argument-hint` is UI metadata only; `$ARGUMENTS` is not implemented anywhere. The established pattern is that the skill body instructs Claude (the orchestrator) to manually interpolate values into Task prompt strings using angle-bracket placeholders.

The convention for this feature:
- In Step 1 of SKILL.md, add: "If the user provided an archetype argument, capture it as `<user_archetype_preference>`. If not, treat this as absent — do not add the User Archetype Preference field to any Task prompt."
- In the Step 2 Task prompt block, add a conditional line: `User Archetype Preference: <user_archetype_preference>  ← include only when provided`
- This is consistent with how every other placeholder is handled in the skill (the orchestrator reads and substitutes values, not a template engine).

### Soft Preference Semantics

The `User Archetype Preference:` field instructs the architect to:
1. Include the specified Pokemon in the draft
2. Assign them the specified roles
3. Deviate **only** if the Pokemon is absent from the regulation's `allowed_pokemon` list
4. Document any meta-unfriendly aspects of the user-specified picks in "Threats and Weaknesses" (not remove them)

This is explicitly *not* a hard pin — the revision pass can adjust teammates, items, and EV spreads around a pinned pick, but cannot replace it.

### Output Labeling (R4)

Two changes needed for R4:
- **Team template**: Add `## User Constraints` section after `## Strategy Summary`, containing the raw archetype preference string and a note on which Pokemon were user-specified. Architect fills this only when a preference was given.
- **SKILL.md Step 6 confirmation**: When writing the final draft, include a line in the user confirmation: "User-specified picks: [list] / Architect picks: [list]" when an archetype preference was provided.

### Critic Behavior (R3)

No changes to any critic agent files. The SKILL.md revision-pass Task prompt needs one addition: "User-specified picks below are soft preferences — work around them (adjust teammates, items, spreads), do not replace them. Surface their weaknesses in Known Weaknesses."

The critics already return findings without making substitutions — this is an instruction to the architect during the revision pass, not to the critics themselves.

## Implementation Units

### Unit 1: Update team-template.md

**Goal:** Add optional `## User Constraints` section to the required format.

**Files:** `skills/build-tr-team/team-template.md`

**Approach:** Insert the section immediately after `## Strategy Summary` in the Required Format block. Mark it as conditional ("omit if no archetype preference was provided").

```markdown
## User Constraints  ← omit this section if no archetype argument was provided

- **User-specified picks:** <list of Pokemon and roles from the archetype argument>
- **Architect choices:** <remaining slots>
- **Preference string:** "<exact text the user provided>"
```

**Patterns to follow:** Existing template sections (discrete named headings, bullet sub-fields).

**Verification:** Template file renders correctly. The section heading is unique so grep for downstream consumers won't find false positives.

---

### Unit 2: Update SKILL.md — argument capture and forwarding

**Goal:** SKILL.md instructs the orchestrator to capture the archetype argument in Step 1 and forward it conditionally to the tr-architect Task prompt in Step 2 and the revision Task prompt in Step 5.

**Files:** `skills/build-tr-team/SKILL.md`

**Approach (three sub-changes):**

**2a. Frontmatter `argument-hint`:**
```yaml
argument-hint: "[archetype preference]"
```

**2b. Step 1 addition** — after existing data-loading instructions, add:
```
If the user provided an archetype argument, capture it:
- <user_archetype_preference> = the raw argument string (e.g., "Oranguru setter + Mega Golurk abuser")
- If no argument was given, <user_archetype_preference> is absent — omit the User Archetype Preference field from all Task prompts below.
```

**2c. Step 2 Task prompt** — add one conditional line to the tr-architect Task call, after `Legal items:`:
```
User Archetype Preference: <user_archetype_preference>  ← include only when provided; omit the line entirely if absent
```

**2d. Step 5 revision Task prompt** — add to the `Constraints:` block:
```
- User-specified picks (from archetype preference) are soft preferences — work around them (adjust teammates, items, spreads, bring-4 guidelines) rather than replacing them. Surface known weaknesses in the Known Weaknesses / Threats and Weaknesses section explicitly.
```

**Patterns to follow:** Existing angle-bracket placeholder convention (lines 49–68 of current SKILL.md). The revision Constraints block (lines 149–155).

**Verification:** No existing functionality changes when `<user_archetype_preference>` is absent. When present, the Task prompt includes the field. The argument-hint reflects the actual argument type.

---

### Unit 3: Update tr-architect.md — handle archetype preference

**Goal:** Architect knows what to do when it receives a `User Archetype Preference:` field in its Task prompt.

**Files:** `agents/coaching/tr-architect.md`

**Approach:** Add a new `## User Archetype Preference` section after the existing `## Rules` block:

```markdown
## User Archetype Preference

When the Task prompt includes a `User Archetype Preference:` field:

- **Treat it as a strong preference.** Build the team around the specified Pokemon and roles. The user wants these picks — don't second-guess the strategic choice.
- **Verify legality first.** Before committing to any pinned pick, confirm it appears in the regulation's `allowed_pokemon`. If it does not appear, note the conflict in your draft and choose the closest legal alternative.
- **Fill the remaining slots** to complement the pinned picks — cover their type weaknesses, provide their missing support (redirection, speed control, spread damage), and complete the TR core.
- **Document pinned picks** in the `## User Constraints` section of the team draft (before `## Win Conditions`). List which Pokemon were user-specified vs. architect-chosen.
- **Surface weaknesses honestly.** If a pinned pick has a meta-unfriendly matchup or structural weakness, note it in `## Threats and Weaknesses`. Do not hide it. The user chose the pick deliberately — they deserve to know the tradeoff.
- **During revision pass:** Work *around* pinned picks. Adjust teammates, items, EV spreads, and bring-4 guidelines to compensate for flagged weaknesses. Do not replace pinned picks — that's not your call.
```

**Patterns to follow:** Existing `## Rules` block style (bold lead term + prose explanation).

**Verification:** Agent instructions are unambiguous about when and how to use the preference. The soft-preference semantics (deviate only for regulation illegality) are explicit.

---

### Unit 4: Update SKILL.md — Step 6 user confirmation

**Goal:** The confirmation message to the user identifies which picks were user-specified vs. architect-chosen (R4 second half).

**Files:** `skills/build-tr-team/SKILL.md`

**Approach:** In Step 6, update the "Confirm to the user with:" list to add:
```
- User-specified picks (if any): [list from <user_archetype_preference>] vs. Architect picks: [remaining slots]
```
Only include this line when `<user_archetype_preference>` was provided.

**Patterns to follow:** Existing Step 6 confirmation bullet list (lines 183–186 of current SKILL.md).

**Verification:** When no argument, confirmation message is identical to today. When argument present, picks are clearly labeled.

## Acceptance Criteria

- [ ] `/build-tr-team "Oranguru setter + Mega Golurk abuser"` produces a 6-Pokemon draft where Oranguru is the TR setter and Mega Golurk is the primary abuser
- [ ] `/build-tr-team` with no argument produces output identical to the current behavior (no regression)
- [ ] The final team draft file contains a `## User Constraints` section when an archetype argument was provided, omitted when not
- [ ] If a pinned Pokemon fails a critic check, the revision pass adjusts teammates/items/spreads rather than replacing the pinned pick
- [ ] Known weaknesses of pinned picks appear in `## Threats and Weaknesses` with an explicit note that the pick was user-specified
- [ ] The user confirmation message identifies user-specified vs. architect picks when an archetype argument was provided
- [ ] The `argument-hint` frontmatter reflects the new argument type (`[archetype preference]`)
- [ ] tr-architect.md contains unambiguous instructions for handling the `User Archetype Preference:` field

## Dependencies & Risks

- **No `$ARGUMENTS` runtime mechanism exists.** The feature relies on Claude-as-orchestrator reading the user's argument from context and manually interpolating it. This is the existing pattern — but it means the "parsing" is implicit, not enforced. Risk: orchestrator might not pick up the argument if instructions aren't explicit enough. Mitigation: SKILL.md Step 1 instructions must be directive, not suggestive.
- **Regulation illegality edge case.** If a user pins a Pokemon that doesn't exist in the current regulation, the architect deviates. This is the intended soft-preference behavior, but the user may be surprised. Mitigation: tr-architect.md instructions say to note the conflict explicitly in the draft.
- **Team template section ordering.** Adding `## User Constraints` between `## Strategy Summary` and `## Win Conditions` could break any downstream consumer that does heading-sensitive parsing. Mitigation: grep `agents/` and `skills/` for hard-coded heading references before writing the template change.

## Sources & References

### Origin

- **Origin document:** [docs/brainstorms/2026-04-27-tr-builder-archetype-input-requirements.md](docs/brainstorms/2026-04-27-tr-builder-archetype-input-requirements.md)
  Key decisions carried forward:
  - Soft preference (not hard pin) — architect deviates only for regulation illegality
  - Skill argument at invocation time (not interactive prompt)
  - Flag but don't replace — critics evaluate pinned picks; revision pass works around them

### Internal References

- `skills/build-tr-team/SKILL.md` — orchestrator (argument-hint L4, Step 1 L33–42, Step 2 Task prompt L49–68, Step 5 revision Constraints L149–155, Step 6 confirmation L183–186)
- `skills/build-tr-team/team-template.md` — output format (Strategy Summary L22–24, Threats and Weaknesses L72–76)
- `agents/coaching/tr-architect.md` — architect agent (Rules L26–33)
- Related issue: #8 (remaining scope — user-guided archetype input)
