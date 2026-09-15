---
approval: unapproved
---

# Shared figures — one owner each

**The problem this solves, in one number: `206 years` appears in twelve files and twenty-four places, and until this table existed no file owned it.** `milieu-brief.md` §2 says it is negotiable by about fifty years in either direction — so it is explicitly a figure somebody might move, and moving it meant finding twenty-four sites by hand with nothing to say when you had missed one. That is the 67-Mya failure waiting to happen again in a larger version.

**The rule, which `milieu-brief.md` already states and nothing enforced: one fact, one place.** A figure is stated by its owner and cited by everybody else. This table is the register of owners, and `shared_figures_owned` fails the suite when a figure appears in two or more files without a row here.

**So the table is not maintained by remembering to add things.** The second mention is what fails. A figure stated once needs no row; the moment it is stated twice, the check stops you and this is where it lands. That is the only structural guarantee available over prose, and its strength is exactly the detector's recall — good for numbers, moderate for named entities, poor for propositions carried entirely in words. **The blind spot shrinks as facts move into tables**, because the prose surface is what is being measured.

**`owner` takes three kinds of value.** A file path, meaning that file states the figure and everyone else cites it. **`distinct`**, meaning the occurrences are different propositions that happen to share a number — a real answer, not an exemption, and the `what` column has to say which propositions. And **`spelling`**, meaning the same proposition written two ways, with the row pointing at the owner of the canonical form.

---

## The owners

| figure | what it is | owner |
|---|---|---|
| 206 years | how long since the transit, at the novel's opening | `plan/milieu-brief.md` §1 |
| 66 Mya | when the story happens | `plan/milieu-brief.md` §1 |
| 66 million | the same figure spelled out | `spelling` — see 66 Mya |
| 67 Mya | where the Enclave emigrates at the end of book 3. **Not the second jump, which is a thousand years** | `plan/sequels.md` |
| 80 km | the Enclave to the coast, overland | `plan/journey-calendar.md` §1 |
| 8 km | Day 3's distance | `plan/journey-calendar.md` §1 |
| 40 km | **`distinct`** — the river's distance along the route in the calendar, and the transit's spatial targeting accuracy in EP7. Two propositions, one number | `distinct` |
| 22 °C | what rain lands near | `plan/journey-calendar.md` §2 |
| 32 °C | the top of the shelf-sea range, 28–32 | `plan/journey-calendar.md` §2 |
| 24 °C | the top of the mean-annual-air range, 20–24 | `kb/research/geo-flora-fauna.md` §2.2 |
| 190 cm | Benal's height | `plan/milieu-brief.md` §9 |
| 65 kg | Benal's mass | `plan/milieu-brief.md` §9 |
| 3 days | **`distinct`** — the founders' three years at Genesis, biome day-ranges, and leaching time all use the token. Not one proposition | `distinct` |
| 2 days | **`distinct`** — suit feeding interval, forage day-ranges, days of food. Not one proposition | `distinct` |

---

## Word-form figures, and the ones that are not figures at all

**`shared_figures_owned` requires a leading digit, so it sees `6 m` and is blind to *six meters*.** That is how the croc's length came to sit in seven files unnoticed — more than half the spread of the `206 years` above, and nothing looked. `word_figures` closes it, and the fix is not a bigger regex: a figure written in words **carries the numeric form in an inline `@WF-` claim on the same line**, so the prose declares itself instead of a pattern trying to read English. The claim buys more than a row does — a row says an owner exists, a claim says every restatement agrees.

**But a word-number is not always a figure, and this table is where that is said out loud.** *Two days* occurs twenty-nine times across ten files and is twenty-nine different statements: two days of food, two days past the poisoning, two days without sleep, a speech she has had for two days. Annotating those under one key would assert they are one fact, which is the annotation-that-lies failure in its purest form. So a phrase listed here is exempt from `word_figures`, and the `why` column is the whole justification.

**Three verdicts, and they are the same three the owners table uses.** `idiom` — the words recur but the proposition does not, so there is nothing to bind. `distinct` — genuinely two or more propositions sharing a number, named in the `why`. `spelling` — one proposition written loosely, with the row pointing at the exact figure that owns it.

| phrase | verdict | why |
|---|---|---|
| two days | `idiom` | rations, elapsed time, sleep debt, suit feeding, a prepared speech. Twenty-nine statements, no shared proposition |
| three people | `idiom` | the trio as a count, and portions divided three ways |
| two people · one day · two years · six days · nine days · three weeks · four years · sixteen years | `idiom` | ordinary durations and ages in prose; no proposition recurs |
| three days · four days · four hours · six hours · three hours · two hours · one hour · twelve hours | `idiom` | leaching stages, lay-ups, watches and marches. The corpus measures in these constantly |
| two kilometers · three kilometers · four kilometers · eight kilometers · twelve kilometers | `idiom` | per-day distances, owned day by day by `plan/journey-calendar.md` §1 and not a single figure |
| two suits · three meters · one meter | `idiom` | the stolen pair against the twelve in store; sightlines; a juvenile croc against an adult |
| three generations | `idiom` | the name-reuse horizon and the drift span are different spans |
| five weeks | `idiom` | Marisol's silence, and a separate interval in the ladder |
| three years | `distinct` | **the founders' three years *at Genesis* against the three years the First Walk *took*.** `plan/minor-characters.md:65` and `plan/milieu-brief.md:64` are not the same span and the corpus has never said so |
| fifteen meters | `distinct` | the border-tangle's height, which the wig's ceiling deliberately matches; nests at twelve to fifteen; the kiva's collapse hole at ten to fifteen |
| ten meters | `distinct` | the flybeak's wingspan, and the radius Noli will not enter around the barrier |
| thirty meters | `distinct` | conifer emergent height; canopy depth above the nests; the proximity sense's reach into the ground; and the retired nest height |
| a million years · one-million years | `distinct` | the depth of book 3's emigration relative to 66 Mya, the galactic-year figure, and fragment 8's artifact |
| two hundred years | `spelling` | a deliberate round of `206 years` — the prose rounds and the register owns the exact figure. See the owners table above |

```rule
id:       word-figures-carry-digits
shape:    membership
every:    figure written in words, repeated across two or more files
has:      an inline `@WF-` claim on the same line whose value carries the number
evidence: `shared_figures_owned` requires a leading digit, so the croc's length sat in seven files with no owner and nothing looked — more than half the spread of the `206 years` this register was built for. The exemptions below are the measurement: run as a worklist first, the detector found 52 groups, of which 17 were one proposition, 14 were idiom or genuinely distinct, and the rest resolved once the numeral was parsed whole
check:    word_figures
status:   ratified
```

---

## What is not here, and why

**Craft measurements** — the sentence-length distributions, the hook rates, the purpose mixtures — live in `prompts/` and `process/` and are deliberately out of scope. They are facts about Daniel's two published novels rather than about this world, `process/` is where method history belongs, and `pacing-and-stakes.md` §8 already owns the ones that matter with a check over them.

**Named entities and their attributes are the obvious next table and are not this one.** Today's father contradiction — `minor-characters.md` naming him Daven and killing him while `milieu-brief.md` §9 calls him undefined and §11 lists him as open — is the same shape as `206 years` and is not reachable from a numeric detector. It needs a row per *attribute*, not per name, and it needs a placement decision first, because the cast is currently split across two approved files with the three protagonists in one and everybody else in the other.
