# C08 raw trajectory schema

All records are little-endian, packed without padding, with no headers. Reader dtypes are in audit.py. design.csv names every world path and settings. Regime codes 0, 1 and 2 denote stable, periodic reversal and unpredictable. Energy is in sixteenth-units. Genotype code is 3L + 2S.

| File | Record | Meaning |
|---|---|---|
| founders.bin | uint8 genotype | 60 values in ID order, founder IDs 0–59, birth period −1, energy 384 ticks, belief 0.5 |
| mapping.bin | uint8 mapping | One per period, 0–239 |
| actions.bin | uint16 period, uint16 ID, int16 energy before and after foraging, int8 hidden state / site / reading / patch, uint8 reward acquired / return steps, float64 prior / belief | Row for each alive at period start, including terminal actions. Negative action values are absent. Post-foraging energy precedes reproduction. Motion and energy transfers are reconstructible from the action fields and protocol. Reward is event credit, even if the individual later dies on return. |
| events.bin | uint16 period / ID / parent, uint8 genotype | Parent 65535 denotes death. Birth rows imply parent −208 and child +192 energy ticks, newborn blank belief. Child IDs increase from 60 and their ancestry traces to a founder. Differences from the parental genotype record the mutated loci. Blocked births are recoverable from eligibility and available slots. |
| passive0.bin through passive7.bin | uint16 ID / parent, uint8 genotype | One row per active event in corresponding order, with time and type inherited from that event. Parent 65535 denotes death. No energetic actions. |

The independent audit constructs end-of-period living genotype counts, including newborns, and continuous roster histories from the raw ledgers. curves.npy stores columns 0–5 active genotype counts, column 6 active number of founder lineages present, and columns 7–12 genotype counts summed across eight passive replays. Its first axis follows design.csv and the second is global period.
