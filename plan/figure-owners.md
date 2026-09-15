---
approval: unapproved
---

# Shared figures — one owner each

**The problem this solves, in one number: `206 years` appears in twelve files and twenty-four places, and until this table existed no file owned it.** `milieu-brief.md` §2 says it is negotiable by about fifty years in either direction — so it is explicitly a figure somebody might move, and moving it meant finding twenty-four sites by hand with nothing to say when you had missed one. That is the 67-Mya failure waiting to happen again in a larger version.

**The rule, which `milieu-brief.md` already states and nothing enforced: one fact, one place.** A figure is stated by its owner and cited by everybody else. This table is the register of owners, and `shared_figures_owned` fails the suite when a figure appears in two or more files without a row here.

**So the table is not maintained by remembering to add things.** The second mention is what fails. A figure stated once needs no row; the moment it is stated twice, the check stops you and this is where it lands. That is the only structural guarantee available over prose, and its strength is exactly the detector's recall — good for numbers, moderate for named entities, poor for propositions carried entirely in words. **The blind spot shrinks as facts move into tables**, because the prose surface is what is being measured.

**`owner` takes three kinds of value.** A file path, meaning that file states the figure and everyone else cites it. **`distinct`**, meaning the occurrences are different propositions that happen to share a number — a real answer, not an exemption, and the `what` column has to say which propositions. And **`spelling`**, meaning the same proposition written two ways, with the row pointing at the owner of the canonical form.

---

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

## What is not here, and why

**Craft measurements** — the sentence-length distributions, the hook rates, the purpose mixtures — live in `prompts/` and `process/` and are deliberately out of scope. They are facts about Daniel's two published novels rather than about this world, `process/` is where method history belongs, and `pacing-and-stakes.md` §8 already owns the ones that matter with a check over them.

**Named entities and their attributes are the obvious next table and are not this one.** Today's father contradiction — `minor-characters.md` naming him Daven and killing him while `milieu-brief.md` §9 calls him undefined and §11 lists him as open — is the same shape as `206 years` and is not reachable from a numeric detector. It needs a row per *attribute*, not per name, and it needs a placement decision first, because the cast is currently split across two approved files with the three protagonists in one and everybody else in the other.
