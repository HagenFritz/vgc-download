---
name: vgc:tr-theory
description: "Reference documentation for Trick Room team-building theory. Not a user command — loaded into the TR Architect agent as domain knowledge."
user-invocable: false
---

# Trick Room Team-Building Theory

This document defines the framework for building competitive Trick Room teams in VGC Doubles. It is loaded into the TR Architect agent as reference knowledge.

## Progress Tracking

Before starting, use `TaskList` to find any lingering tasks and delete them all with `TaskUpdate` (status: `deleted`). Then create fresh tasks upfront using `TaskCreate` so the user can see the full checklist. Mark each task `in_progress` when you start it and `completed` when done. Create these tasks:

1. "Load meta report and regulation data" (activeForm: "Reading data files...")
2. "Analyze meta for TR opportunities" (activeForm: "Identifying TR openings...")
3. "Search for current TR builds" (activeForm: "Searching web for TR tech...")
4. "Select team and fill roles" (activeForm: "Building team roster...")
5. "Design sets (EVs, moves, items)" (activeForm: "Designing competitive sets...")
6. "Run composition checks" (activeForm: "Verifying team composition...")
7. "Write team draft" (activeForm: "Writing Showdown paste draft...")

## Methodology

### Step 1: Load Data

Read the meta scouting report (from the user's file path argument, or auto-detect):
1. Read `data/config.json` to get `current_regulation`
2. Glob for `data/meta/*_<current_regulation>_report.md` and pick the most recent by date prefix
3. If no report exists, tell the user to run Meta Scout first

Also read:
- `data/regulations/<current_regulation>.json` — allowed Pokemon list
- `data/pokemon_db/<current_regulation>_pokemon.json` — base stats, types, and abilities for all regulation-legal Pokemon. Use this for speed tier math, type coverage analysis, and ability selection.

### Step 2: Analyze the Meta for TR Opportunities

From the scouting report, identify:
- **Top threats to prepare for**: The Pokemon you'll face most often
- **Speed distribution**: Is the meta fast? That makes TR stronger.
- **Exploitable weaknesses**: Shared vulnerabilities across top archetypes
- **Common strategies to counter**: Tailwind, weather, Psyspam, etc.
- **Anti-TR tech in the meta**: Taunt users, Imprison users, fast Fake Out

### Step 3: Search for Current TR Builds

Search the web specifically for Trick Room strategies in the current format:
- `"Pokemon Champions" VGC <regulation> Trick Room team`
- `"Pokemon Champions" VGC Trick Room tournament results`
- `"Pokemon Champions" VGC TR core <regulation>`

**CRITICAL**: Always include `"Pokemon Champions"` in search queries to avoid pulling data from older games.

Look for: what TR setters and abusers are people using, innovative tech, community consensus on TR viability.

If web results are sparse, note the gap and build from stats + theory alone.

### Step 4: Select the Team

Follow the Building Process (see below) to fill all 6 team slots. Every pick must be from the regulation's `allowed_pokemon` list — cross-reference before finalizing.

### Step 5: Design Sets

For each Pokemon, determine:
- **Item**: Based on role and what's available
- **Ability**: The competitive choice
- **Nature**: Brave/Quiet for abusers, bulky natures for setters
- **EVs**: Optimize for the role. TR abusers get max HP + offensive stat. Setters get bulk.
- **IVs**: 0 Speed for all TR abusers. 0 Attack for special attackers.
- **Moves**: 4 moves per Pokemon. Protect is almost mandatory on non-setters in VGC.

### Step 6: Run Composition Checks

Run through all 8 Team Composition Checks (see below). If any check fails, adjust the team before proceeding.

### Step 7: Write the Draft

Follow the [team template](team-template.md) exactly. Create `data/teams/drafts/` if it doesn't exist:
```bash
mkdir -p data/teams/drafts
```

Write to: `data/teams/drafts/<YYYY-MM-DD>_<regulation_id>_tr_team.md`

---

## Reference Material

For detailed competitive knowledge (setter analysis, abuser archetypes, EV math, counterplay, bring-4 strategy), see [competitive-reference.md](competitive-reference.md). Consult it when making specific Pokemon selections, designing EV spreads, or planning counterplay.

---

## Theory Framework

### Core Roles

Every TR team fills these roles across 6 Pokemon (some Pokemon fill multiple):

1. **TR Setter (1-2)** — Bulky, reliable, survives a turn to set TR. Items: Mental Herb, Eviolite, Safety Goggles, Focus Sash.
2. **TR Abuser (2-3)** — Low speed (base <50 ideal, <70 max), high offense, 0 Spe IVs, Brave/Quiet nature.
3. **Redirector (0-1)** — Follow Me or Rage Powder to protect setter turn 1. Expendable after TR is set.
4. **Speed Control Backup (0-1)** — Works OUTSIDE TR. Tailwind, Icy Wind, or naturally fast. This is Plan B.
5. **Anti-Meta Pick (1-2)** — Counters the top meta threats. Chosen based on the scouting report.

For detailed setter/abuser analysis, items, and specific Pokemon, see [competitive-reference.md](competitive-reference.md).

### Speed Tier Rules

- **Abusers:** Base 0-50 speed preferred. 0 Spe IVs, speed-hindering nature.
- **Setters:** Bulk > speed. Mid-speed is fine.
- **At least one Pokemon that works outside TR.** If all 6 are slow, you auto-lose when TR expires.

Speed benchmarks: base 30 or below moves first under TR against almost everything; base 31-50 is solid; base 51-70 is borderline; base 71+ is not a TR abuser. See [competitive-reference.md](competitive-reference.md) for calculated minimum speeds at Level 50.

## Team Composition Checks

Before finalizing a team, verify:

1. **Can you set TR reliably?** Do you have Mental Herb or redirection to beat Taunt? Can your setter survive common attacks?
2. **Can you win without TR?** What's your Plan B when the opponent prevents or stalls out TR?
3. **Do you have a Taunt answer?** Mental Herb, Magic Bounce, or a fast Taunt of your own.
4. **Do you have an Imprison answer?** Some opponents carry Imprison + Trick Room to block your setup. Can you KO the Imprisoner or play around it?
5. **Type coverage across the 6?** Don't stack weaknesses. If you have 3 Ground-weaks, one Earthquake wipes your team.
6. **Fake Out answer?** Fake Out flinches your setter turn 1. Inner Focus, redirection, or your own Fake Out to pressure back.
7. **Spread move coverage?** In Doubles, spread moves (Earthquake, Rock Slide, Heat Wave) are efficient. Have at least 2-3 Pokemon with good spread options.
8. **Item diversity?** Don't double up on items. Each Pokemon needs a distinct held item.

## Win Condition Planning

Every team needs 2-3 distinct win conditions:

1. **Primary:** The ideal game plan. Usually "set TR, sweep with [abuser]."
2. **Secondary:** When primary is disrupted. "Switch to [backup attacker] or play without TR."
3. **Anti-meta:** Specific to the current format. "Exploit the shared weakness of [top threats]."

Each win condition should suggest a different **bring-4** combination. A good TR team has 2-3 viable bring-4 options depending on the matchup.

## Anti-Meta Selection Process

When choosing Pokemon to counter the meta:

1. Read the meta scouting report's **Top Threats** and **Dominant Archetypes** sections
2. Identify the top 3-5 Pokemon/archetypes you'll face most often
3. Find Pokemon that:
   - Resist or are immune to their main STAB moves
   - Hit them super-effectively
   - Are slow enough for TR (or fast enough for your Plan B)
   - Don't overlap with weaknesses already on your team
4. Cross-reference against the **Exploitable Weaknesses** section for format-wide vulnerabilities

## Building Process

1. **Start with the setter.** Pick based on the meta — what threats does it need to survive? Does it need Magic Bounce for heavy Taunt metas?
2. **Pick 2-3 abusers.** Cover different types. At least one physical and one special to avoid Intimidate being a complete shutdown.
3. **Add support.** Redirector, speed control backup, or anti-meta picks depending on what the team needs.
4. **Check composition.** Run through all 8 team composition checks above.
5. **Plan bring-4s.** Map out at least 3 bring-4 combinations for common matchups.
6. **Refine EVs.** Optimize spreads based on specific damage calcs against top meta threats.
