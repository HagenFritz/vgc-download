# Team Review Template

This template defines the format for team review reports produced by the `/vgc:review-team` skill. Reviews are matchup-first: understand where the team stands before deciding what to change.

## Output Path

```
data/teams/reviews/<YYYY-MM-DD>-<NNN>_<regulation_id>_review.md
```

Example: `data/teams/reviews/2026-04-28-001_reg_m-a_review.md`

Sequence numbering follows the same pattern as team drafts: daily counter, zero-padded to 3 digits, restarting each day.

## Required Format

Every review report must include all sections in this order:

```markdown
# Team Review — <Regulation Name> — <YYYY-MM-DD-NNN>

**Reviewed:** <input file path>
**Regulation:** <regulation_id>
**Mode:** Full team (6 Pokemon) / Partial team (<N> Pokemon)
**Meta report:** <report path>

## Team

<Paste the full Showdown paste of the reviewed team here exactly as provided.
If the input was a draft .md file, extract just the Showdown paste block.>

---

## Meta Coverage Analysis

*From team-coverage-analyst*

### Threat Grid

| Threat | Usage | Coverage | Answer | Severity if missing |
|--------|-------|----------|--------|---------------------|
| ... | ...% | ✅ / 🟡 / 🔴 | ... | — / IMPORTANT / CRITICAL |

### Archetype Matchup Table

**[Archetype Name]** (~X%): **[Favored / Even / Unfavored]**
- **Why:** ...
- **Bring-4:** ...

*(repeat for each dominant archetype in the meta report)*

### Type Vulnerability Audit

- **[Type]** — hits [Pokemon A], [Pokemon B], [Pokemon C] (SE). [Exploitation note.]

### Structural Gaps

**Over-covered:**
- ...

**Under-covered:**
- ...

### Overall Verdict

[One paragraph: best matchup, worst matchup, tournament viability assessment.]

---

## Improvement Suggestions

*From team-improvement-advisor*

### Change List

**🔴 CRITICAL ...**
- **Specific change:** ...
- **Why:** ...
- **Verification:** ...

**🟡 IMPORTANT ...**
...

**🔵 POLISH ...**
...

### Suggested Leads by Matchup

**vs. [Archetype]:** Lead [Pokemon A] + [Pokemon B] — ...

*(repeat for 2-3 key archetypes)*

---

## Revised Paste (Advisory)

> Apply selectively. The Change List above is the canonical recommendation. This paste applies all suggested changes — review each before importing.

[Full 6-Pokemon Showdown paste with suggestions applied]
```

## Notes on Format

- The `## Team` section reproduces the input as-is — no edits, no improvements. This is the baseline being reviewed.
- The `## Revised Paste` section is clearly labeled advisory. The Change List is canonical.
- For partial team reviews (mode=partial), the Revised Paste completes the roster to 6 using suggested additions.
- If a section from an agent is unusually long, the orchestrator may truncate at natural section boundaries to keep the report readable in under 5 minutes.
