# Trick Room Competitive Reference

Deep reference material for building Trick Room teams in VGC Doubles. This supplements the core theory in SKILL.md with detailed competitive knowledge sourced from VGCGuide (Wolfe Glick), Smogon, Nugget Bridge, and Pikalytics.

## Why Trick Room Is Strong

- TR has won 7 of 12 VGC World Championships — historically the most successful macro-strategy in the format.
- In Doubles, two Pokemon benefit from reversed speed each turn. That's 8 "moves under TR" across 4 usable turns (the setting turn counts as turn 1).
- Slow Pokemon typically have higher base stats in HP, Attack, Special Attack, and defenses because their low Speed frees the stat budget.
- TR abusers invest 0 EVs in Speed, gaining ~252 extra EVs compared to speed-invested Pokemon — a massive efficiency advantage that compounds across the team.
- TR does NOT affect move priority. Fake Out (+3), Protect (+4), Extreme Speed (+2) still resolve in their normal brackets.

## Hard TR vs Semi-TR

### Hard Trick Room
All 6 Pokemon built around TR. Multiple setters, multiple abusers, dedicated support. The entire game plan revolves around getting TR up and sweeping.

- **Pros:** Maximum TR consistency. All 4 brought Pokemon benefit from TR. Opponents face a unified strategy.
- **Cons:** Predictable in team preview. If TR is denied repeatedly, no fallback. Vulnerable to Imprison and heavy Taunt.

### Semi-Trick Room
1-2 slow abusers + 1 setter + 3-4 fast/mid-speed Pokemon. TR is one mode, not the only mode.

- **Pros:** Flexible and unpredictable at team preview. Better tournament consistency.
- **Cons:** Fewer Pokemon benefit from TR. The TR mode is less powerful than a dedicated TR team's.

Community consensus: Semi-TR generally has superior tournament viability because of flexibility. However, full TR excels in metas where the top threats are fast and frail.

## Detailed Setter Analysis

### Bulky Setters

**Cresselia** — Called "the absolute ruler of Trick Room" by Smogon. 120/120/130 defenses, Levitate immunity to Earthquake, huge movepool (Helping Hand, Icy Wind, Psyshock, Lunar Dance). Can set TR 2-3 times per game. Weakness: low offensive pressure, vulnerable to Taunt.

**Dusclops** — Eviolite creates absurd bulk. Ghost typing is immune to Fake Out and Normal-type attacks. Will-O-Wisp cripples physical attackers. Weakness: dead weight if Taunted; Knock Off removes Eviolite.

**Porygon2** — Eviolite bulk + Download boosts Attack or SpA based on opponent's lower defense. Recover enables late-game re-setting. Tri Attack provides neutral coverage with 20% status chance. The GOAT if legal.

### Offensive Setters

**Hatterene** — Magic Bounce is the strongest anti-Taunt ability — reflects Taunt back. High Special Attack. Pairs extremely well with Indeedee-F (Psychic Terrain blocks Fake Out on both sides).

**Reuniclus** — 125 Special Attack + Magic Guard (no Life Orb recoil, no weather/status chip). Base 30 Speed is ideal for TR.

**Chandelure** — High SpA, Ghost-typing (Fake Out immune), access to Imprison + Trick Room to block opposing TR. Use Focus Sash.

### Surprise Setters

**Mimikyu** — Disguise guarantees it survives one hit. Can set TR through almost anything turn 1. Falls off after Disguise breaks.

**Farigiraf** — Armor Tail blocks priority moves entirely, meaning opponents cannot Fake Out to flinch it.

### Setter Items

| Item | Use Case |
|------|----------|
| Mental Herb | Cures Taunt on first use. The premier anti-Taunt tech. |
| Eviolite | +50% Def/SpD for NFE Pokemon (Porygon2, Dusclops). Best bulk item. |
| Safety Goggles | Blocks Rage Powder redirection and Spore. |
| Focus Sash | Guarantees survival from full HP. Best on offensive/frail setters. |
| Kasib/Colbur Berry | Halves super-effective Dark or Ghost damage once. |

## Detailed Abuser Archetypes

### Physical Abusers

**Rhyperior** — 140 Atk, 40 Speed, dual STAB Earthquake + Rock Slide (both spread). Solid Rock reduces super-effective damage by 25%.

**Conkeldurr** — Drain Punch recovery, Mach Punch priority for out-of-TR play, Iron Fist or Guts. Fire Punch coverage.

**Hariyama** — Fake Out for early game + Guts with Flame Orb for massive Close Combat. Doubles as support AND abuser.

**Escavalier** — 135 Atk, 20 Speed. Overcoat blocks Spore and Rage Powder.

**Marowak-Alola** — Thick Club doubles Attack. Lightning Rod redirects Electric moves from allies.

### Special Abusers

**Torkoal** — Drought + Eruption at full HP is devastating spread damage. Slowest weather setter, perfectly suited to TR.

**Armarouge** — 66.3% TR usage in 2026 Pikalytics data. Weak Armor or Flash Fire depending on team needs.

### Critical Note on Eruption/Water Spout
These moves have 150 base power at full HP but scale down with damage taken. TR teams using them must protect the user's HP or pair with Helping Hand for guaranteed KOs even at reduced HP.

## Redirection Deep Dive

### Follow Me vs Rage Powder
- Follow Me has NO immunities — strictly more reliable.
- Rage Powder is blocked by Grass-types, Safety Goggles holders, and Overcoat ability Pokemon.
- Stalwart ability (Duraludon) ignores both entirely.

### Best Redirectors for TR
- **Amoonguss**: Rage Powder + Spore + Regenerator + naturally slow. The premier TR redirector.
- **Indeedee-F**: Follow Me + Psychic Surge (blocks Fake Out on both sides) + Healing Wish.
- **Clefable**: Follow Me + Friend Guard (reduces damage to allies by 25%).

### The Expendable Redirector Principle
From VGCGuide: "One of the best outcomes of Turn 1 is that a redirector is knocked out, which allows a free switch under Trick Room to a more offensive Pokemon." Redirectors are expendable — their job is to eat hits so the setter sets TR, then get out of the way.

## Helping Hand Amplification
Helping Hand boosts the target's move power by 50% for that turn. On a TR team, pairing Helping Hand support (Cresselia, Indeedee-F, Togekiss) with a high-power abuser creates devastating one-shots. Helping Hand + Eruption or Helping Hand + Earthquake can OHKO Pokemon that would otherwise survive.

## Speed Tier Math

### The Speed Stat Formula at Level 50

```
Min Speed = floor((Base + 0 + 0 + 5) * 0.9)
```
(0 Speed IV, 0 Speed EV, Speed-hindering nature)

### Calculated Minimum Speeds

| Base Speed | Min Speed at Lv50 | Pokemon Examples |
|-----------|-------------------|------------------|
| 20 | 22 | Shuckle |
| 30 | 31 | Reuniclus, Torkoal (base 20, so 22) |
| 35 | 36 | Torkoal |
| 40 | 40 | Rhyperior |
| 45 | 45 | Hariyama |
| 50 | 49 | Iron Hands |
| 65 | 63 | Hatterene |
| 75 | 72 | Porygon2 |

### Underspeeding
Under TR, you want to be SLOWER than your opponent. 0 Speed IVs + Speed-hindering nature guarantees you underspeed opposing TR abusers who might have neutral natures or non-zero Speed IVs.

### Speed Creep in Mirrors
In TR mirrors, the standard is 0 Speed IV + hindering nature. Speed "creeping" means running neutral nature or 1 Speed IV to move AFTER the opponent under TR (so you move first when TR ends). Risky and only for specific mirror matchups.

## EV Spreading for TR Teams

### The Core TR Advantage
TR Pokemon don't invest in Speed, giving them ~252 extra EVs compared to speed-invested Pokemon. A typical fast Pokemon: 252 Spe / 252 Atk / 4 HP. A TR abuser: 0 Spe / 252 Atk / 252 HP / 4 Def.

### Standard TR Abuser Spread
252 HP / 252 Atk (or SpA) / 4 Def. Nature: Brave (+Atk -Spe) or Quiet (+SpA -Spe).

### Benchmark-Driven Spreading (Advanced)
Top players don't use generic 252/252 spreads. They:
1. Identify the top 3-5 attacks the Pokemon must survive
2. Use a damage calculator to find exact EV thresholds
3. Allocate remaining EVs to offensive benchmarks (what must you OHKO/2HKO?)
4. Cross-reference with Nature boost

### EV Math at Level 50
- First 4 EVs in a stat = 1 stat point (if IV is odd). Every 8 EVs after = 1 more point.
- Clean EV values: 4, 12, 20, 28, 36, 44, 52 ... 244, 252.
- Invest in an odd number of stats (1, 3, or 5) for maximum efficiency.
- Diminishing returns: 20 EVs in a low base stat has proportionally larger impact than in a high base stat.

### HP Optimization
- **Life Orb**: Recoil is 10% max HP rounded down. HP ending in 9 takes 1 less recoil.
- **Sitrus Berry**: Heals 25% max HP. HP divisible by 4 gives clean recovery.
- **Leftovers**: Heals 1/16 max HP. HP divisible by 16 is optimal.

### Setter EV Philosophy
Maximize bulk to guarantee TR setup. Typical: 252 HP / split Def-SpD based on meta threats. Offensive stat is tertiary. Exception: offensive setters like Hatterene who max SpA and rely on Focus Sash or Magic Bounce.

## Counters and Counterplay

### Taunt
Prevents status moves (including TR) for 3 turns. Prankster Taunt (+1 priority) is the most common TR denial.

**Answers:**
- Mental Herb (auto-cures first Taunt)
- Magic Bounce (Hatterene — reflects Taunt back)
- Redirection (Follow Me forces Taunt onto redirector)
- Lead second setter from the back
- Dark-type Pokemon are immune to Prankster moves

### Fake Out
+3 priority flinch on the setter, preventing TR turn 1.

**Answers:**
- Ghost-type setters (immune to Fake Out)
- Psychic Terrain via Indeedee-F (blocks all priority moves)
- Redirection (Follow Me absorbs Fake Out)
- Your own Fake Out (flinch their Fake Out user first)
- Inner Focus / Armor Tail abilities

### Imprison
A Pokemon with Imprison + Trick Room uses Imprison to prevent ALL opponents from using TR. Cannot be redirected.

**Answers:**
- KO the Imprison user (effect ends when they leave)
- Force them out (Roar, Whirlwind, Dragon Tail, Red Card)
- Run two setters (they can only Imprison one)
- Don't set TR — go Plan B. They wasted a slot on Imprison.

### Stalling / Protect
Opponent Protects both Pokemon on alternating turns, wasting TR turns. Or defensive Intimidate cycling.

**Answers:**
- Predict Protects and set up (Swords Dance, switch in fresh abuser)
- Spread moves (can't Protect both Pokemon every turn)
- Plan to re-set TR with a bulky setter + Recover
- Count turns and position for the endgame

### KO Pressure (Doubling Into Setter)
Opponent targets setter with both Pokemon to KO before TR goes up (TR has -7 priority).

**Answers:**
- Redirection (forces both attacks onto redirector)
- Bulk investment (Eviolite, defensive EVs survive the double-up)
- Focus Sash (guarantees survival from full HP)

### Opposing Trick Room
Opponent uses TR when yours is active, inverting back to normal speed.

**Answers:**
- KO their setter before they can reverse
- Taunt the opposing setter
- Don't re-set if they also have slow Pokemon — play neutral speed

## When NOT to Set Trick Room

- **Against opposing TR teams**: Setting TR gives them the speed advantage too. Consider playing neutral or using your fast mode.
- **When your setter is revealed and they have hard counters**: If they show Imprison + TR user and you have one setter, go Plan B.
- **When you're winning without it**: If fast Pokemon are already taking KOs, TR might slow you down.
- **When your abusers are all KO'd**: Setting TR with no one to abuse it wastes a turn.
- **Turn count math**: If only 2 Pokemon remain on each side, TR may not provide enough turns to matter.

## Bring-4 Decision Making

### Standard TR Bring-4 Lines

1. **Set-and-sweep**: Redirector/Fake Out + Setter lead, 2 abusers in back. Set TR turn 1, switch in abusers.
2. **Pressure lead**: Abuser + Fake Out lead. Abuser Protects, Fake Out flinches. Turn 2: set TR with a back-row switch.
3. **Plan B (no TR)**: Fast Pokemon + fast attacker. Offense without TR against opposing TR or Taunt-heavy teams.

### Team Preview Process

1. **Identify opponent synergies** — what pairs and strategies does their team support?
2. **Work backwards by exclusion** — which of your 6 contribute least against their specific team?
3. **Ensure coverage** — your 4 must collectively answer every major threat on their side.
4. **Choose leads deliberately** — the lead pair should establish tempo.
5. **Plan for turn 1** — mentally simulate their likely leads vs your intended leads.

## Protect in VGC Doubles

Protect is the most-used move in VGC. In Doubles, your partner still attacks while you Protect — creating asymmetric advantage.

**Five core uses:**
1. **Pace control**: Stall out Tailwind, TR, weather, or stat boosts.
2. **Positioning**: Shield a threat while switching its partner.
3. **Mind games**: Forces suboptimal opponent decisions.
4. **Threat preservation**: Keep a key attacker alive one more turn.
5. **Turn stalling**: Wait out temporary effects.

**Guideline:** 4 of 6 team members should run Protect. Exceptions: Choice item holders, Assault Vest users, extremely bulky setters with recovery.

## Intimidate Awareness

Intimidate is the most format-warping ability in VGC. It drops the Attack of both opponents on switch-in.

**Why it matters for TR teams:**
- A single Intimidate drop reduces physical damage by ~33%.
- Incineroar (Intimidate + Fake Out + Parting Shot) appears on nearly every team.
- TR teams with only physical abusers get shut down by Intimidate cycling.

**Mandatory answer:** Include at least one special attacker on the team. Also consider: Defiant/Competitive (reverse drops into +2), Clear Body, Clear Amulet, or simply having enough physical power to push through drops.

## Sources

- VGCGuide.com (Wolfe Glick) — Team Building, Trick Room, Speed Control, EV Spreading, Team Preview, Protect
- Smogon — Trick Tactics: A Guide to Trick Room in VGC, A Beginner's Guide to Trick Room, Speed Control Guide
- Nugget Bridge — Bulking Up: Defensive EV Spreads, Speed Kills: Controlling Speed in VGC
- Pikalytics — VGC 2026 usage data and TR setter distribution
