---
approval: approved 2026-09-12
---

# Foreshadow, Chekhov, and motif

Planning layers B8 and B9, book-wide. Every plant paired with its payoff in both directions, each carrying a **signal level**; and every motif on a count and a spacing budget.

---

## 1. Signal levels

**Default is NONE.** The lesson from viking: the book's best foreshadow is a beat tag in which the villain reaches for hand lotion mid-conversation. Never revisited, no emphasis, and it is the tell that he framed the protagonist. Models plant foreshadowing with a paragraph break and an "oddly."

| level | means | budget |
|---|---|---|
| **none** | the reader can only see it on a second reading | most of the list |
| **faint** | a character notices and moves on | perhaps six |
| **overt** | the text asks the reader to remember | **two**, and both are Chekhov's guns in the strict sense — a physical object the reader must know exists |

## 2. The ledger

| # | plant | where | payoff | where | signal |
|---|---|---|---|---|---|
| 1 | Noli's total dependence on Keo's projection | 2.1 | she cannot be saved by it | 7.2 | none |
| 2 | **The third suit, left on the rack** | 4.2 | Keo's injury; and the reader knows the real reason | 8.2 / 10.1 | **overt** |
| 3 | Benal's mathematics dismissed as dead symbols | 2.2 | the only knowledge that matters | 12.1 | faint |
| 4 | Keo leaves the machete on the taboo shelf | 4.2 | he pilots the wig | 13.1 | faint |
| 5 | **Joram's face holding only fear** | 3.1 | the fear was for him, and it was about Yara | 14.1 | none |
| 6 | Sila: "one lost lightcell" | 3.1 | they come home in a machine | 14.1 | none |
| 7 | **The archaea failsafe dissolves unmaintained old-tech** | 4.2 | **at Genesis, nothing has dissolved — the failsafe is a colony invention, not a founder instruction** | 12.1 | none |
| 8 | The First Walk: 200 out, 94 arrived | 3.1 | their own journey costs them Noli and nearly Keo | 7–9 | none |
| 9 | Omya taught Teva to read the stars | 1.1 | **Teva was being trained for the Watch.** She has a Keeper's memory and not a Keeper's senses, so she was meant to inherit the sky and got part of the way | 2.4, Day 3 | none |
| 9b | **Omya recites the sky perfectly and cannot hold a protein fold** | 2.4 | the star lore survived because it is checked nightly; the mission drifted because nothing tested it. And Benal recognizes a 206-year positional dataset in a dying woman's head | Nights 6 and 10, 12.1 | none |
| 9c | Nobody counts the Watch as a loss | 2.4 | **the impactor could already be findable and nobody is left who would know** | book 2 | none |
| 10 | Teva's mother died of what kills Alira | 1.1 | the confession | 10.1 | faint |
| 11 | **Four water gourds, filled for three people** | 2.3 | Yara | later in 2.3 | **none — never remarked on** |
| 12 | "We'll be fine" | 2.1 | after the midpoint nobody can say it, and someone tries | 8.3 | faint |
| 13 | Liaso's story: a T. rex watched him for an hour | 3.4 | the single distant sighting | Day 13 | none |
| 13b | **The founders lost two wigs and their drones to the sky** | Genesis records, 12.1 | the Day 19 chase is a repetition of a founder-era disaster, not a novel threat | 13.x | faint |
| 14 | The temporal flash symbol | 8.4 | the signal the heretics received | 12.1 | **overt** |
| 15 | Marek dismissive at home / fighting in the chamber | 2.2 / 3.1 | Benal understands his father | 14.1 | none |
| 16 | **The river crossed easily in low water** | Day 8 | **not in flood — spread.** The channel becomes kilometers of shallow water and stops being a crossing at all; the way home is not the way out | Days 16–18 | faint |
| 17 | Benal's shoulder capacitor red-lined at the theft | 4.2 | it dies, and he hides it | Day 11 | none |
| 18 | A yazhi corrected about stone-cycad poison | Act 1 | **Teva overrules Keo, leaches the mash short, and it poisons her** | Day 12 decision, Day 13 collapse | none |
| 19 | Grounders are Noli's catch | Days 3–10 | **after Day 11 nobody catches them, and the food changes** | Day 12 | none |
| 20 | The suits are fed sugar | 4.3 | the honey is split between four mouths and two suits | Day 6 | none |
| 21 | **The river gratings pass anything small, which grows up inside** | 2.5, as the reason for the drill | **how Yara died, inside the perimeter, in water she had crossed a hundred times** | 2.3 / 10.1 | none |
| 22 | The gratings must be raised to open the river | 2.5 or 4.x | **flying the wig means opening the croc barrier, every time** | 15.1, book 2 | none |

**Validator:** no plant without a payoff, no payoff without a plant, and the ledger is checked in both directions.

### The reverse index — `[requires]`, written on the dependent move

**Every pointer in the table above is written at the plant end, and that is the wrong end for the way plants actually break.**

A plant is rarely destroyed by someone editing the plant. It is destroyed by someone cutting, moving or rewriting it while working on something else entirely — and the payoff then fails **silently, in a scene nobody was looking at.** A forward-only pointer is invisible from where the damage shows up.

So every payoff move also carries **`[requires <scene>.<move>]`**, and the check becomes symmetric and mechanical:

1. Every `requires` resolves to a move that still exists.
2. Every `plants →` has a matching `requires` at the far end.
3. An unmatched pair on either side is a broken chain, **found by walking the maps rather than by rereading the novel.**

**And `requires` carries a payload, not just an address.** A pointer can stay valid while the thing it points at stops doing its job — the move survives at 2.3.17 but gets rewritten so Riel fills three gourds and mentions a fourth, and the address still resolves. So the form is:

> `[requires 2.2 — Benal's mathematics shown as dismissable]`
> `[requires 2.3.17 — four gourds filled for three people, unremarked]`

That converts a link check into a **contract**: the dependent move states what it needs, and anyone editing the source can see what they would break. Pointer integrity is not semantic integrity, and every serious continuity failure this project has found — the helmet, Alira's age, the season pivot — was semantic with the addresses intact.

**An unresolved `requires` is a work queue.** A dependent move naming a scene that does not exist yet is telling you what must be written before this scene can be, which is the build order falling out of the annotation for free.

**This generalizes past foreshadowing.** The same mechanism carries the reader-payment chains in `knowledge-ledger.md` — fact O's payment at 3.1 carries `[requires 2.2]`, and fact N's completion scene carries `[requires 2.3, 3.1, 4.1]`, naming the contributions it completes. Retroactive plants are allowed and encouraged — cordimancy tells the legend of the seedling *after* the reader has already seen the impossible oak, so it lands as recognition rather than setup.

## 3. Motifs

Each carries a count and a spacing. **A motif that appears in every chapter is wallpaper.**

### Counting — around 8 to 10 appearances, evenly spread. The numbers in this section are targets for spacing, not caps.

The strongest available and it is already everywhere without having been noticed. Riel gives a number where anyone else would give an impression. Hesh does the First Walk arithmetic. Twelve suits, ten that work, eleven if Sarel's is repairable. Eighty kilometers. Eighty percent of a protocol, which is worth nothing. Position one-oh-seven.

**Counting is how this society holds itself together — and the one number nobody can produce is the impact date.** That is the motif's payoff and it needs no comment: the culture that counts everything cannot count the only thing that matters.

### Erasure — 6, widely spaced. **The strongest motif in the book.**

The Council chamber's bare walls, "a monument to erasure." The archaea that dissolve old-tech to sterile sludge. Clay vessels shaped to look like random clumps so nothing appears made. **The returning — a people who dissolve their own dead within the hour and keep no graves.** **A suit that eats its wearer if the wearer dies in it.** And all of it inside the blast radius of the thing that will erase every trace of them anyway.

They are a civilization organized entirely around leaving no evidence that it existed — and its whole purpose is to be remembered by the future it is trying to save. That is the book's grimmest joke and it should never be stated.

**Better if no character articulates this.** It is available to the reader from the accumulation, and a line of commentary would probably kill it.

### Water is death — not a motif, a physical law, and it should never be argued for

The mantra is stated early and then **never defended**, because the book proves it five separate ways and the reader assembles the proof themselves:

1. **Crocs.** The primary threat, and mental projection barely touches a hungry one.
2. **Teva.** The sea is where her own judgment comes due — the short-leached mash leaves her with a headache she cannot think through at the one moment navigation matters. *(Not her magnetic sense, which is worth more offshore than on land — a heading matters most where there are no landmarks. Not her thermal failure either; the lethal half of that is heat, and there is no cold water in this world.)*
3. **The weapons.** Archaea in the shafts wake on sustained wetting. Water eats the things you defend yourself with.
4. **Genesis.** The one place they must reach sits in the sea, and the sea takes the raft, the fieldpack, and Benal's mathematics.
5. **Yara.** Eleven meters of open water she had crossed a hundred times.

Nobody in the novel enumerates this. The mantra is a children's rule that turns out to be an understatement, and the reader should get there alone.

### Light as diagnostic — 6, mostly Act 1 and Act 3

In this world light is *information*, not beauty. The cultures glow by protocol — rust-red for T-cell, blue for lysine. Lightmold is calibrated. The suits' forearm displays. Chromatophores reading the environment. Then Genesis: a powered section, and the first light in the book that means something is *working*.

### Things that survive because they are checked — 3, and one of them is the thesis

Star lore, checked nightly, intact after 206 years. The mission instructions, checked by nothing, corrupted beyond use. The synthesis protocol, checked constantly, and dying anyway because the checkers are dying. Give the articulation to Benal, once.

### The thesis — spoken twice in the whole novel

Per the cordimancy standard, where the title concept is said aloud exactly twice across 124,000 words. Here:

1. **Teva at 14.1** — *they're not liars, they're believers.*
2. **One earlier statement, in a different key**, that the reader will not recognize as the thesis until 14.1 recontextualises it. Best candidate: Riel or Joram in 2.3, about the founders or about the Council, said in passing, about something small.

Nothing else in the novel states it. Not the narration, not the epigraphs, not Benal.

## 4. Rules

```rule
id:       plant-payoff-bijection
shape:    bijection
every:    plant in the ledger of §2
has:      payoff
evidence: §2's own validator — "no plant without a payoff, no payoff without a plant, and the ledger is checked in both directions"
check:    plant_payoff_bijection
status:   ratified 2026-09-12
```

1. **Signal level defaults to none.** If a plant needs a paragraph break to be noticed, it is the wrong plant.
2. **Revisiting a plant to remind the reader usually kills it.** One placement, one payoff, unless there is a reason.
3. **A motif appearance that does no other work is decoration.** Every instance of counting must also be characterization, plot, or tension.
4. **Two overt guns, and both are objects** — the third suit on the rack, and the symbol in the flash. Everything else is buried.
5. **Check `plan/knowledge-ledger.md` before planting.** A plant is only foreshadowing if the reader is in a position to hold it; if the fact is already ironic, the plant is doing something else and should be labeled as such.
