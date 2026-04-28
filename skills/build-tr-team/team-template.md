# Team Draft Template

This template defines the format for TR Architect team drafts. Teams use Showdown paste format so they can be directly imported into Pokemon Showdown for testing.

Output path and filename sequencing are managed by SKILL.md Step 6.

## Required Format

Every team draft must include these sections:

```markdown
# TR Team Draft — <Regulation Name> — <YYYY-MM-DD-NNN>

## Strategy Summary

<2-3 sentences: What is this team's game plan? What archetypes does it beat?
What are its win conditions? When do you set TR and when do you play without it?>

## User Constraints

> Omit this section entirely if no archetype argument was provided.

- **Preference string:** "<exact text the user provided>"
- **User-specified picks:** <Pokemon name — Role> / <Pokemon name — Role> (list each pinned pick)
- **Architect choices:** <remaining slots, filled to complete the team>

## Win Conditions

1. **Primary:** <The main way this team wins — e.g., "Set TR and sweep with Torkoal Eruption">
2. **Secondary:** <Backup plan — e.g., "Mega Charizard Y sun offense without TR">
3. **Anti-Meta:** <How this team handles the top threats from the meta report>

## Team (Showdown Paste)

<Pokemon 1> @ <Item>
Ability: <Ability>
Level: 50
EVs: <EV Spread>
<Nature> Nature
IVs: 0 Spe
- <Move 1>
- <Move 2>
- <Move 3>
- <Move 4>

<Pokemon 2> @ <Item>
...

<Repeat for all 6 Pokemon>

## Roster Breakdown

### <Pokemon 1>
- **Role:** <TR setter / TR abuser / redirector / speed control / anti-meta>
- **Why this pick:** <What it does for the team, what meta threats it answers>
- **Key interactions:** <Important Doubles synergies with teammates>
- **EV rationale:** <Why this spread — what does it survive, what does it KO>

### <Pokemon 2>
...

<Repeat for all 6 Pokemon>

## Bring-4 Guidelines

Suggested bring-4 combinations for common matchups:

- **vs. Tailwind Offense:** <4 Pokemon to bring and why>
- **vs. Trick Room Mirror:** <4 Pokemon>
- **vs. Weather Teams:** <4 Pokemon>
- **vs. Goodstuffs/Balance:** <4 Pokemon>

## Threats and Weaknesses

- **Hard counters:** <What this team struggles against>
- **Soft checks:** <Manageable but uncomfortable matchups>
- **Tech options:** <Alternative moves/items to consider for specific metas>
```

## Notes on Showdown Paste Format

- Level is always 50 for VGC
- IVs default to 31 and are only listed when non-standard (e.g., `IVs: 0 Atk` for special attackers, `IVs: 0 Spe` for TR abusers)
- EVs must total 508 or less (510 including rounding)
- Natures that reduce Speed (Brave, Quiet, Relaxed, Sassy) are preferred for TR abusers
- Mega Stones go in the item slot (e.g., `Charizard @ Charizardite Y`)
