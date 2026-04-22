# Pokémon Champions Meta Scouting Report — Regulation M-A — 2026-04-21

## Data Provenance

Source: `championstournaments` (100,000 battles)
Raw file: `reg_m-a_chaos.json`
Regulation: `reg_m-a` (53 of 259 Pokemon matched)

> **Note:** Stats are from the current-game Pokémon Champions tournament ladder, filtered locally to Reg M-A legal Pokemon and Champions legal items. This is **real data, not proxy** — but only ~20% of the legal dex appears in usage, meaning the long tail is dark. Trust the top-20 rankings; assume anything below ~2% usage is invisible.
>
> **Community context:** Format is 13 days old (started 2026-04-08). Only one real tournament weekend has happened (2026-04-19): Sun + Tailwind won both major online events — **TheMoistPleb** 9-2 at VGC Trainers School (86 players) and **HyogaVGC** 8-1 at Ewokpadawan (83 players). No Regional (Indianapolis, May) and no Global Challenge cutoff yet. Ladder win rates (Mega Froslass 63.8%, Hard TR 62.3%) are reported but tournament-sample data is thin. TheGamer has already published a "meta lacks variety" piece pointing at the narrow Mega + Incineroar skeleton. Smogon's Reg M-A thread (3780373) and Pokemon Zone are the primary community hubs; ChampionsMeta and Limitless have raw data but top-cut team lists from 4/19 are not yet published. Treat everything below as preliminary — adaptation cycle hasn't happened.

## Top Threats

1. **Incineroar** — 51.18% usage
   - **Sets:** Fake Out (99%) / Parting Shot (96%) / Flare Blitz (87%) / Throat Chop (43%) or Darkest Lariat (39%). Sitrus Berry 55% / Choople Berry 17% / Shuca Berry 12%. Intimidate 98%.
   - **Strengths:** The format's glue. Fake Out + Intimidate + Parting Shot controls turn 1 on roughly half of teams. Momentum piece, not a wincon.
   - **Weaknesses:** 4x Fighting (Sneasler CC), neutral Ground/Water/Rock. Competitive/Defiant punishes the Intimidate chain.
   - **Common partners:** Sneasler 40%, Sinistcha 37%, Garchomp 36%, Floette-E 23%, Basculegion 23%.

2. **Sneasler** — 48.35%
   - **Sets:** Close Combat (99.6%) / Dire Claw (97.9%) / Fake Out (89.4%) / Protect (77.4%). White Herb 74.7% / Focus Sash 21%. Unburden 89.8%.
   - **Strengths:** White Herb + Close Combat is a free speed reset — effective Spe 240 after one trigger. Dire Claw status roulette, Fake Out on top.
   - **Weaknesses:** 4x Psychic and 4x Fairy. Floette-Mega and Mega Gardevoir erase it. Intimidate chip off a clean read does real damage.
   - **Common partners:** Incineroar 42.5%, Garchomp 40.9%, Kingambit 38%, Basculegion 29.6%.

3. **Garchomp** — 38.65%
   - **Sets:** Earthquake (90%) / Dragon Claw (86%) / Rock Slide (77%) / Protect (71%). Choice Scarf 26.5% / White Herb 16.4% / Soft Sand 15.6%. Rough Skin 91%.
   - **Strengths:** Spread EQ + spread Rock Slide from a fast physical base. Scarf variant is the revenge-kill speed-control piece; non-Scarf sets abuse Rock Slide flinch math.
   - **Weaknesses:** **4x Ice** — the single biggest exploit on the board. Any Icy Wind user cripples it.
   - **Common partners:** Sneasler 51.2%, Incineroar 48%, Charizard 33%, Rotom-W 29%, Kingambit 28%.

4. **Sinistcha** — 31.11%
   - **Sets:** Matcha Gotcha (99%) / Rage Powder (98%) / Trick Room (68%) / Life Dew (56%) / Strength Sap (26%). Sitrus 56% / Leftovers 14%. Hospitality 99%.
   - **Strengths:** The format's only meaningful Rage Powder user AND the meta's primary TR button. Semi-room flex on balance teams.
   - **Weaknesses:** 4x Dark, Ghost. Taunt erases it. No Safety Goggles counterplay item exists in Champions — so redirection is unchecked, which also means Fire/Flying spread damage through Focus Sash reads on the field one-shot it.
   - **Common partners:** Incineroar 61.2%, Sneasler 43.6%, Floette-E 26.3%, Tyranitar 25.5%.

5. **Kingambit** — 28.74%
   - **Sets:** Sucker Punch (99%) / Protect (92%) / Kowtow Cleave (89%) / Iron Head (59%) / Swords Dance (32%) / Low Kick (24%). Black Glasses 61% / Choople 30%. Defiant 98%.
   - **Strengths:** Priority nuke under every turn in. Defiant punishes the Intimidate spam it shares a team with. Sucker Punch respects no speed tier.
   - **Weaknesses:** 4x Fighting. Sneasler CC through it. Slow (base 50) without support.
   - **Common partners:** Sneasler 64%, Garchomp 37.4%, Incineroar 35%, Basculegion 30%.

6. **Basculegion** — 25.28%
   - **Sets:** Last Respects (98%) / Wave Crash (93%) / Aqua Jet (87%) / Flip Turn (74%). Choice Scarf 68.3% / Mystic Water 21%. Adaptability 75.6%, Swift Swim 24.2%.
   - **Strengths:** Scarf Last Respects snowballs endgames. Swift Swim under Pelipper is the rain wincon. Aqua Jet priority covers the one speed tier it can't beat under Tailwind.
   - **Weaknesses:** Grass spread, Electric. Perish Trap hard-counters the 1-mon wincon game.
   - **Common partners:** Sneasler 57%, Incineroar 47%, Pelipper 38%, Kingambit 34%, Archaludon 28%.

7. **Floette-Eternal** — 19.16%
   - **Sets:** Calm Mind (84%) / Moonblast (82%) / Dazzling Gleam (88%) / Protect (99%). Floettite 99%. Flower Veil 72% / Fairy Aura 27%.
   - **Strengths:** Mega Fairy wincon. Spread Gleam + CM = late-game snowball. Hits Sneasler 4x.
   - **Weaknesses:** Steel-types shut it down. Kingambit Sucker Punch ends setup lines.
   - **Common partners:** Incineroar 62%, Sneasler 53%, Garchomp 48%, Sinistcha 43%, Aerodactyl 36%.

8. **Charizard** — 18.06%
   - **Sets:** Heat Wave (90%) / Solar Beam (75%) / Weather Ball (49%) / Protect (97%). Charizardite Y 92%. Drought (from Mega Y) — Solar Power 38% / Blaze 44%.
   - **Strengths:** Mega Y sun nuker. Solar Beam 1-turn under Drought. Spread Heat Wave threatens everything but water.
   - **Weaknesses:** **4x Rock.** Aerodactyl/Tyranitar Rock Slide ends it. Loses the weather war to Rain.
   - **Common partners:** Garchomp 70%, Incineroar 61%, Sneasler 58%, Venusaur 46%, Whimsicott 42%.

9. **Rotom-Wash** — 17.96%
   - **Sets:** Hydro Pump (98%) / Thunderbolt (73%) / Will-O-Wisp (56%) / Volt Switch (55%) / Electroweb (28%). Three-way item split — Sitrus 37% / Scarf 28% / Leftovers 26%.
   - **Strengths:** Levitate walls Ground spam for its partner. Multiple viable builds — utility pivot, Scarf revenge, Lefties stall.
   - **Weaknesses:** Grass/Electric/Ghost. Sinistcha Matcha Gotcha hits hard.
   - **Common partners:** Garchomp 62%, Incineroar 49%, Sneasler 49%, Floette-E 25%.

10. **Whimsicott** — 17.34%
    - **Sets:** Tailwind (99%) / Moonblast (94%) / Encore (73%) / Protect (48%) / Sunny Day (31%). Focus Sash 75.5%. Prankster 99.4%.
    - **Strengths:** The #1 Tailwind setter. Prankster Encore shuts down setup turns. Sunny Day 31% indicates Charizard sun partner.
    - **Weaknesses:** Dark-type attackers ignore Prankster. Steel/Poison resist Fairy. Prankster Taunt/Encore usage is criminally low — free tech slot if you copy it.
    - **Common partners:** Incineroar 52%, Garchomp 50%, Sneasler 48%, Charizard 44%.

11. **Aerodactyl** — 15.81%
    - **Sets:** Rock Slide (99%) / Dual Wingbeat (95%) / Tailwind (94%) / Protect (94%). Focus Sash 79.4% / Aerodactylite 14.8%. Unnerve 89%.
    - **Strengths:** Sash Tailwind lead that doesn't give up flinch pressure. Rock Slide 99% one-shots Charizard and 2HKOs Whimsicott through Sash.
    - **Weaknesses:** Water/Electric/Ice/Steel. Status moves kill its Sash-safe plan.
    - **Common partners:** Sneasler 59%, Garchomp 49%, Incineroar 48%, Floette-E 44%, Kingambit 35%.

12. **Pelipper** — 14.95%
    - **Sets:** Hurricane (97%) / Weather Ball (87%) / Tailwind (79%) / Wide Guard (34%). Focus Sash 74.5%. Drizzle 98%.
    - **Strengths:** Drizzle + Tailwind on one slot. Immune to Intimidate-chip-via-Incineroar (it pivots in on rain damage, not attack). Wide Guard 34% is meaningful Rock Slide tech.
    - **Weaknesses:** 4x Electric. Electro Shot (Archaludon) OHKOs under rain.
    - **Common partners:** Basculegion 65%, Archaludon 59%, Incineroar 48%, Sinistcha 44%, Dragonite 35%.

13. **Tyranitar** — 13.94%
    - **Sets:** Rock Slide (97%) / Protect (82%) / Knock Off (72%) / Low Kick (57%) / Dragon Dance (16%). Tyranitarite 68% / Scarf 13%. Sand Stream 100%.
    - **Strengths:** Mega TTar Rock Slide cannon. Sand setter unlocks Excadrill (47.6% teammate rate).
    - **Weaknesses:** **4x Fighting.** Sneasler Close Combat is a free switch-in punish.
    - **Common partners:** Sinistcha 57%, Incineroar 52%, Excadrill 48%, Sneasler 31%.

14. **Archaludon** — 12.21%
    - **Sets:** Electro Shot (91%) / Flash Cannon (90%) / Draco Meteor (57%) / Protect (77%). Leftovers 53% / Magnet 11%. Stamina 72%, Sturdy 22%.
    - **Strengths:** Rain's special nuke. Electro Shot is instant-charge under rain — the scariest unresisted move in the format. Stamina stacks on every Knock Off.
    - **Weaknesses:** 4x Fighting. Mud-slinging Ground moves bypass its defense.
    - **Common partners:** Pelipper 72%, Basculegion 58%, Incineroar 46%, Sneasler 37%.

15. **Dragonite** — 11.64%
    - **Sets:** Protect (80%) / Hurricane (52%) / Draco Meteor (44%) / Extreme Speed (40%) / Tailwind (32%). Dragoninite-Mega 65% / Lum 15%. Multiscale 73%.
    - **Strengths:** Mega mixed attacker with ESpeed priority. Tailwind variant doubles as speed control.
    - **Weaknesses:** **4x Ice.** Icy Wind rips it in half. Rock coverage is also punishing.
    - **Common partners:** Sneasler 54%, Basculegion 51%, Pelipper 45%, Incineroar 38%.

16. **Farigiraf** — 11.40%
    - **Sets:** Trick Room (97%) / Hyper Voice (72%) / Psychic (68%) / Helping Hand (48%) / Imprison (15%). Sitrus 50% / Colbur 18% / Mental Herb 15%. Armor Tail 99%.
    - **Strengths:** Dedicated TR setter with Armor Tail blocking priority (including Sucker Punch). Imprison tech for mirror TR.
    - **Weaknesses:** Dark/Bug. Taunt kills the plan — Mental Herb only helps once.
    - **Common partners:** Incineroar 50%, Sneasler 37%, Kingambit 30%, Torkoal 30%, Charizard 24%.

17. **Venusaur** — 11.37%
    - **Sets:** Sludge Bomb (95%) / Sleep Powder (75%) / Protect (81%) / Leaf Storm (35%) / Earth Power (31%). Focus Sash 57% / Venusaurite 19.5%. Chlorophyll 93%.
    - **Strengths:** Chlorophyll doubles Speed under sun → effective 160. Sleep Powder + Sludge Bomb is a hard lock-out combo.
    - **Weaknesses:** 4x Ice. Dies to Charizard mirrors without Zard support.
    - **Common partners:** Charizard 73.5%, Incineroar 73%, Garchomp 63%, Sneasler 48%.

18. **Gengar** — 10.49%
    - **Sets:** Shadow Ball (95%) / Protect (94%) / Sludge Bomb (58%) / Perish Song (50%) / Disable (28%). Gengarite 93%. Shadow Tag 24% (Mega) / Cursed Body 76%.
    - **Strengths:** Shadow Tag + Perish Song traps single-wincon teams. Disable tech lines are real.
    - **Weaknesses:** Dark/Ghost coverage. Whimsicott Encore shuts it down.
    - **Common partners:** Incineroar 71%, Sinistcha 33%, Kingambit 29%.

19. **Froslass** — 9.96%
    - **Sets:** Blizzard (98%) / Shadow Ball (96%) / Aurora Veil (74%) / Protect (97%). Froslassite 98.5%. Snow Warning (Mega) 17% / Cursed Body 55% / Snow Cloak 27%.
    - **Strengths:** Mega Froslass is a rising pick — sets snow on Mega Evolve, veils up, Blizzard spams. Ladder WR reported at 63.8%.
    - **Weaknesses:** Kingambit and Incineroar wall it cleanly — and both sit above 28% usage. Organic check.
    - **Common partners:** Sneasler 70%, Kingambit 61%, Garchomp 46%, Incineroar 31%.

20. **Milotic** — 9.12%
    - **Sets:** Scald (90%) / Protect (85%) / Icy Wind (58%) / Ice Beam (53%) / Recover (43%). Leftovers 77%. Competitive 97%.
    - **Strengths:** Competitive snags +2 SpA off every Incineroar switch-in. Icy Wind is the meta's anti-Tailwind / anti-Dragonite button.
    - **Weaknesses:** Grass/Electric. Slow without its own speed control.
    - **Common partners:** Garchomp 50%, Incineroar 49%, Sneasler 39%, Charizard 35%.

## Core Combinations

- **The Big Three — Incineroar + Sneasler + Garchomp.** Not an archetype, the *default glue*. Sneasler on 42.5% of Incineroar teams; Garchomp on 48% of Sneasler teams. Sits on ~40–50% of teams in some permutation. Fake Out pressure → Unburden reset → spread physical cleanup.
- **Kingambit + Sneasler.** Sneasler on 64% of Kingambit teams. Priority + sweeper bully core. Nightmare coverage: CC + Sucker Punch + Kowtow.
- **Rain HO — Pelipper + Basculegion + Archaludon.** Tightest correlation on the board: Archaludon→Pelipper 71.9%, Pelipper→Basculegion 65%. The rain package is Drizzle → Scarf Last Respects / rain-boosted Wave Crash / instant Electro Shot.
- **Sun — Charizard-Y + Venusaur.** Venusaur→Charizard 73.5%. Drought + Chlorophyll + Sleep Powder. The winning archetype of the first tournament weekend.
- **Sand — Tyranitar-Mega + Excadrill.** Tyranitar on 92.7% of Excadrill teams. Sand Rush Exca doubles Speed → 176 effective. Sinistcha (TTar teammate 57%) adds semi-room backup.
- **Hard TR — Farigiraf + Sinistcha + Torkoal.** Farigiraf→Torkoal 30%. Armor Tail blocks priority, Imprison (15%) locks mirror setters, Torkoal Eruption under sun+TR deletes.

## Dominant Archetypes

- **Semi-Room Balance (Incineroar + Sinistcha core)** (~30–35%)
  - Core: Incineroar / Sinistcha / Sneasler / Garchomp or Kingambit.
  - Win condition: Fake Out + Parting Shot to control turn 1, then flex — if opponent is fast, flip TR; if opponent is slow, pressure under neutral speed.
  - Strengths: Beats pure Tailwind (TR inverts speed), crushes slow balance.
  - Weaknesses: Rain (Pelipper ignores Intimidate-chip on the field-mon, Bascu's Aqua Jet beats TR speed), Taunt leads into Sinistcha.

- **Dual-Setter Tailwind Offense** (~18–22%)
  - Core: Whimsicott + Aerodactyl + Sneasler + Garchomp.
  - Win condition: Turn 1 Tailwind (two Focus Sash setters), Sneasler CC + spread Rock Slide under doubled Speed.
  - Strengths: Beats hard TR (Taunt/Encore the setter), beats sun (outspeeds Chari).
  - Weaknesses: Rain parity speed control, Intimidate chains, Competitive Milotic.

- **Rain HO** (~12–15%)
  - Core: Pelipper / Basculegion-Scarf / Archaludon / Incineroar or Sneasler.
  - Win condition: Drizzle → Scarf Last Respects snowball + instant Electro Shot + rain-boosted Wave Crash. Pelipper Tailwind on top = two speed modes.
  - Strengths: Auto-wins weather war vs Sun, breaks fat balance, punishes TR through raw damage.
  - Weaknesses: Grass spread coverage, Gengar Perish trap, dedicated Electric tech.

- **Chlorophyll Sun + Tailwind** (~8–10% by stats, but **won both major 4/19 events** — overperforming its usage)
  - Core: Charizard-Y / Venusaur / Incineroar / Whimsicott (Sunny Day 31% on her set confirms the pairing) / Garchomp.
  - Win condition: Drought → Sleep Powder disable + Sludge Bomb / Heat Wave spread. Solar Beam/Weather Ball as 1-turn moves. Whimsicott Tailwind layers *on top* of Chlorophyll for double-speed math.
  - Strengths: Beats hard TR (speeds through setters), beats bulky water walls through Grass+Fire. The speed-stacking (Drought Chlorophyll × Tailwind) is currently the fastest damage output in the format.
  - Weaknesses: Rain (weather war loss — Pelipper overwrites Drought), Rock Slide flinch spam (Zard 4x weak), Aerodactyl Sash leads.
  - **Real teams:** TheMoistPleb (VGC Trainers School, 86-player winner) and HyogaVGC (Ewokpadawan, 83-player winner) both ran variants of this on 2026-04-19.

- **Hard Trick Room** (~5–7% by stats, **62.3% ladder WR** per community trackers but no tournament wins yet)
  - Core: Farigiraf / Sinistcha / Torkoal / Incineroar or Kingambit.
  - Win condition: Double setter into TR, Torkoal Eruption under sun+TR, Sucker Punch cleanup.
  - Strengths: Speed-inverts Tailwind offense, turns Scarfers into liabilities. Ladder WR says the archetype *works* — tournament drop-off suggests it's either underrepresented or over-performing vs ladder noise.
  - Weaknesses: Taunt leads, Imprison wars, fast setters themselves. Small event sample — regression likely once experienced players adapt.

- **Sand Offense** (~6–8%)
  - Core: Tyranitar-Mega / Excadrill / Sinistcha / Rotom-Wash.
  - Win condition: Sand up, Excadrill Sand Rush cleans, Rock Slide flinch pressure.
  - Strengths: Favorable weather war vs Sun, Sp.Def boost tanks special attackers.
  - Weaknesses: Rain, Fighting spam (TTar 4x), fast Fairy.

- **Perish Trap Cheese** (~3–5%)
  - Core: Mega Gengar / Politoed / Incineroar.
  - Win condition: Shadow Tag → Perish Song → protect out the Perish count. Disable cheese tech.
  - Strengths: Destroys 1-mon wincons (Scarf Bascu, Mega DD sweepers).
  - Weaknesses: Whimsicott Encore, Taunt Incineroar, healthy pivots.

### Archetype Matchup Notes

- **Rain > Sun** (hard). Drizzle overwrites Drought, Bascu-Scarf outruns +Spe Venusaur, Water walls Heat Wave.
- **Rain > Semi-Room** (slight). Pelipper dodges Intimidate-chip, Aqua Jet beats TR tiers, Archaludon walls most breakers.
- **Hard TR > Tailwind Offense** (if TR sets). Armor Tail blocks Sucker, Torkoal Eruption deletes setters.
- **Sun > Hard TR** (outspeeds setters under Drought).
- **Semi-Room ≈ Tailwind** (Sinistcha's TR+Rage Powder toolbox is the equalizer).

## Speed Tier Breakdown

### Fast (base 100+)
- Aerodactyl — 130 (Sash + Tailwind, doesn't always need raw speed)
- Sneasler — 120 (effective 240 under Unburden)
- Whimsicott — 116 (Prankster makes raw Speed mostly irrelevant)
- Gengar — 110 / Froslass — 110
- Garchomp — 102 (Scarf tier = 153)
- Charizard — 100

### Mid (base 60–99)
- Floette-Eternal — 92
- Excadrill — 88 (Sand Rush doubles to 176)
- Rotom-Wash — 86
- Milotic — 81
- Venusaur — 80 (Chlorophyll sun = 160)
- Dragonite — 80
- Basculegion — 78 (Scarf = 117; Swift Swim rain = 156)
- Sinistcha — 70
- Pelipper — 65

### Slow (base 1–59) — TR candidates
- Tyranitar — 61
- Incineroar — 60 / Farigiraf — 60
- Kingambit — 50

### Speed Control Summary
- **Tailwind dominates.** Whimsicott (98.8%), Aerodactyl (93.6%), Pelipper (78.7%), Dragonite (32.4%). Four of the meta's main speed-control pieces run Tailwind.
- **Trick Room is the counter.** Sinistcha 67.9% / Farigiraf 96.9%. Only two real TR setters at scale, but Sinistcha's 31% total usage means ~1 in 3 games the opponent can flip speed.
- **Choice Scarf distribution:** Basculegion 68% is the scariest unaided speed tier. Garchomp 26.5%, Rotom-W 28%, Tyranitar 13%.
- **Icy Wind is underused.** Only Milotic (57.6%), Rotom-W (27.7%), Gengar (16.2%), Pelipper (7.4%). Given Garchomp 4x and Dragonite 4x Ice, this is a structural exploit.

## Exploitable Weaknesses

### 1. Ground is free money (7 top-20, 183% summed usage)
Incineroar / Sneasler / Kingambit / Rotom-W* / Tyranitar / Archaludon / Gengar** (*neutral; **Levitate-aware). Spread Earthquake with a Flying/Levitate partner is the single best blanket answer to the default Big Three team. **Mega Excadrill is the hammer.**

### 2. Ice cripples the Tailwind skeleton (Garchomp/Dragonite both 4x)
Icy Wind does speed control AND ~OHKO-range damage. Milotic already runs it 57.6%; nobody runs it often enough. Weavile, Froslass, Ninetales-A are immediate upgrades.

### 3. Redirection is a monoculture
Sinistcha is the only Rage Powder user at scale (97.7%). **There is no Safety Goggles or Covert Cloak in the Champions legal item list** — so Sinistcha control = Taunt her or KO her. Overheat Charizard, Air Slash Aerodactyl, or Dazzling Gleam Floette all erase her through Sash reads.

### 4. Fake Out is two-mon-concentrated
Incineroar (99%) and Sneasler (89%) — that's it in the top 20. An Inner Focus or Ghost-type lead invalidates opponent turn 1.

### 5. Intimidate is single-sourced
Only Incineroar runs it in the top 20. **Competitive Milotic and Defiant Kingambit convert the meta's glue into free stat boosts.** Copy harder.

### 6. Tailwind setter decapitation
Whimsicott/Aerodactyl/Pelipper are all Focus Sash. Status chip + Rocky Helmet + flinch math is enough to punch through Sash. Kill the setter turn 1 and Tailwind offense has no backup.

### 7. Speed ceiling is soft
Top 20 has nothing over base 130 unboosted. Weavile (125), Hawlucha (118), Mega Lucario (112) under Tailwind outrun everything the meta can revenge.

### 8. Prankster Taunt / Encore is criminally underused
Whimsicott is on 17% of teams but runs Taunt/Encore tech on a small fraction of sets. One Prankster Encore on a Trick Room or Swords Dance ends games.

## Item, Move & Mechanic Trends

- **Mega Evolution is structural.** 10+ of the top 20 carry a Mega Stone. Mega Y Charizard (92%), Mega Floette (99%), Mega Froslass (98%), Mega Gengar (93%), Mega Dragonite (65%), Mega Tyranitar (68%), Mega Gardevoir (71%), Mega Venusaur (19.5%), Mega Aerodactyl (14.8%). A team without a Mega is behind on power budget.
- **Focus Sash is endemic.** Whimsicott 75.5%, Aerodactyl 79.4%, Pelipper 74.5%, Excadrill 82.6%, Venusaur 57%. Knock Off and Rocky Helmet are underrated answers.
- **White Herb** is the anti-Incineroar item — Sneasler 74.7%, Garchomp 16.4%, Dragonite 4%. Instant Intimidate reset, free neutral-attack swing.
- **Choople Berry** shows up on the Fighting-weak side (Kingambit 30.3%, Maushold, Incineroar 17%) — specifically as Sneasler CC tech.
- **Rising tech (community-cited):**
  - **Mega Froslass snow leads** — Snow Warning triggers on Mega, Blizzard / Shadow Ball / Taunt / Protect. 63.8% ladder WR (Pokemon Zone). Capped at the top because Kingambit and Incineroar both wall it cleanly — so the meta's ubiquity is its own Froslass check.
  - **Mega Excadrill setup** — active Smogon team report thread (3781020). The paper anti-meta choice against the Ground-weak skeleton.
  - **Talonflame** — Gale Wings priority Tailwind, specifically cited as the Whimsicott-replacement that ignores Fake Out disruption.
  - **Defiant Kingambit / Competitive Milotic** — picked up specifically to punish Incineroar ubiquity.
  - **Rapid Strike Urshifu** (if in the legal pool) — Water STAB bypasses Intimidate attack math; community-cited as the cleanest Incineroar punish.
  - **Hippowdon** — bulky Ground + Sand Stream; cited as the Sneasler wall.
  - **Primarina** — Liquid Voice Hyper Voice ignores Intimidate (special), bypasses Substitute lines.
- **Anti-meta mechanics / format narrative:** **No Covert Cloak in Champions** is *the* structural story of the format — Rage Powder + Fake Out have zero item counter, which is why Sinistcha's 97.7% Rage Powder rate is so load-bearing. This also means **Prankster Tailwind took a hit vs SV formats** — no Covert Cloak to stop Fake Out disruption on the setter — which is why Talonflame is gaining share and why the winning 4/19 teams paired Whimsicott with redundant setters. TheGamer's meta write-up on 2026-04-21 frames the format as low-variety: a narrow Mega pool plus Incineroar glue, with power budget shifted out of restricted legendaries (not present in M-A) and into Megas.
- **Most-used moves:** Protect (near-universal), Fake Out (Incin + Sneas), Rock Slide (Garchomp/Aero/TTar/Exca), Tailwind (4+ setters), Moonblast (Fairy spam), Icy Wind (underspread speed control), Sucker Punch (Kingambit), Dazzling Gleam (spread Fairy).

## Unknown Pokemon

**211 of 259 Reg M-A legal Pokemon have zero usage data.** That's 81% of the dex dark. The list is long; notable subsets:

### Unused Megas (59 total) — Surprise-pick potential
Most power-budget-relevant:
- **Mega Excadrill** (Ground/Steel) — the #1 anti-meta pick on the board. Spread EQ threatens 7 top-20 Pokemon.
- **Mega Gardevoir** (Psychic/Fairy) — 165 SpA tier. Dazzling Gleam spread hits Garchomp/Dragonite/TTar, Psychic 4x Sneasler.
- **Mega Lucario** (Fighting/Steel) — CC hits 4 of the top 6. Inner Focus blocks Fake Out on the base form.
- **Mega Gallade** — Inner Focus + Fighting/Psychic coverage against Incineroar + Sneasler.
- **Mega Hatterene** (Psychic/Fairy) — Magic Bounce blocks Taunt, TR-native speed, Dazzling Gleam spread. Perfect Farigiraf partner that *doesn't* share a Ghost/Psychic stack.
- **Mega Gyarados** (Water/Dark) — Intimidate + Dark STAB for the Ghost pile.
- **Mega Scizor** (Bug/Steel) — Bullet Punch priority, Steel resists Fairy.
- **Mega Kangaskhan** — Parental Bond Fake Out slot that doesn't overlap Incineroar.
- **Mega Pidgeot / Mega Altaria / Mega Pinsir / Mega Heracross / Mega Manectric / Mega Sharpedo / Mega Glalie / Mega Lopunny / Mega Medicham** — all plausible offensive alternatives. Some (Lopunny, Medicham, Pinsir) have real Fighting/Normal offensive profiles that deserve testing.

### Unused non-Megas worth highlighting
- **Weavile** (Dark/Ice, 125 Spe) — Ice coverage + Dark STAB + Knock Off. Speed ceiling threat.
- **Mudsdale** (Ground, Stamina/Inner Focus) — Slow EQ abuser under TR, Inner Focus blocks Fake Out.
- **Hatterene** (base form, Magic Bounce) — TR-native, blocks status, Dazzling Gleam.
- **Rhyperior** (Ground/Rock, Solid Rock) — TR-speed, Rock+Ground spread.
- **Conkeldurr / Crabominable / Pangoro** — TR Fighting breakers for the Ghost+Dark pile.
- **Tinkaton** (Fairy/Steel) — Gigaton Hammer OHKOs Garchomp/Dragonite/TTar. Steel resists Floette/Whimsicott.
- **Hawlucha** (Fighting/Flying, 118 Spe, Unburden) — fastest Fighting in the pool. Ground immune, punishes Incineroar/Kingambit/TTar.
- **Empoleon** (Water/Steel, Competitive) — walls the Intimidate cycle like Milotic with harder Steel resists.
- **Oranguru** — Imprison + TR lockout setter. Anti-mirror tech.
- **Primarina** (Water/Fairy) — Liquid Voice Hyper Voice bypasses Substitute, ignores Intimidate as a special attacker.
- **Talonflame** — Gale Wings priority Tailwind setter (community-cited as the anti-Whimsicott option).
- **Excadrill (base form)** — Sand Rush pairs with Mega TTar, Iron Head + EQ coverage.
- **Rapid Strike Urshifu** — if legal to Paldea — Water STAB bypasses Intimidate math.

Everything else is a long tail — Absol, Banette, Castform, Flareon, Furfrou, etc. — either outclassed or specialty picks. Treat anything on the unused list as a *real* possibility until an opponent shows it.

---

**Bottom line for team builders:**

1. The meta has a 5-Pokemon skeleton (Incineroar / Sneasler / Garchomp / Sinistcha / Kingambit). Your team plan should either join it or exploit it.
2. Tailwind > TR right now, but Sinistcha means a third of games flip.
3. The single biggest unpunished weakness is **Ground coverage against the Big Three + Steel/Dark walls.** Mega Excadrill is the top anti-meta pick on paper.
4. No Covert Cloak means Rage Powder redirection has no item counter — Taunt and KO pressure on Sinistcha are the only answers.
5. Sun won the first tournament weekend; Rain beats Sun; Perish Trap beats Rain. Play the rock-paper-scissors honestly.
