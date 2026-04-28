# Competitive Truths

User-maintained facts about Pokemon Champions VGC that override AI priors during team analysis.

The `/vgc:review-team` skill reads this file before analysis and treats every entry as authoritative ground truth. Add facts here when the AI gets something wrong or makes a suggestion that contradicts established competitive knowledge.

**Format:** Plain bullet lists under labeled sections. No special syntax required.

> **Note on move verification:** The Pokemon DB (`data/pokemon_db/`) does not store move pools — `moves` arrays are empty for all Pokemon. Move legality cannot be mechanically verified from the DB. Facts in this file are the primary override mechanism for move-related analysis.

---

## Mega Abilities (Pokemon Champions)

Facts about Mega Evolution abilities for Pokemon Champions Megas whose data is missing from PokeAPI (and therefore the local Pokemon DB).

- **Meganium-Mega** — Ability is **Mega Sol**, a Drought-equivalent that sets harsh sunlight on switch-in. This makes Weather Ball a Fire-type 90 BP move and lets Solar Beam fire without a charge turn. Meganium-Mega is Grass/Fairy type. Do not flag Weather Ball or Solar Beam as illegal or questionable on Meganium-Mega.

---

## Move Restrictions

Moves a Pokemon can legally learn but should never run in VGC for competitive reasons.

- **Incineroar — do not run Protect.** Protect is legal on Incineroar but wastes its most valuable turns. Incineroar's turns are worth far more on Fake Out (turn 1 flinch to enable a teammate's KO), Parting Shot (pivot + Intimidate reset), Knock Off, and Flare Blitz. A turn spent on Protect is a turn Incineroar is not cycling Intimidate or enabling its partner. Never suggest Protect on Incineroar.

---

## Item Restrictions

Items that are legal but widely considered anti-competitive for specific Pokemon. (Add entries here as needed.)

---

## Playstyle Rules

Broader strategic truths about specific Pokemon's role. (Add entries here as needed.)
