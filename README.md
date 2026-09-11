---
approval: unapproved
---

# Cretaceous

**Cretaceous** is a YA survival thriller, 70–100k words, aimed at a tenth-grade reading level and planned as the first book of a trilogy. Near-future humanity discovers time travel and an unstoppable pandemic at almost the same moment, and sends two hundred scientists, soldiers and specialists sixty-six million years back to the Yucatán — to the exact spot the Chicxulub impactor will land, on the logic that whatever they build there will be erased, so nothing they do can leave a trace. Their charge is to solve the disease, learn to travel forward, and carry the answer home. The transit went wrong. Two hundred and six years later their descendants are a colony of nine hundred-odd people living in tree platforms and a limestone cave, holding a mission they have half forgotten, and the two things they no longer know are that **the genetic upgrades they give their children are the cure**, and that the asteroid is about two decades out rather than centuries.

The story runs nineteen days. A child dies in the Vitarium because the last Master Keeper has dementia and the synthesis protocol is dying inside her head; the Council debates and does nothing; and three teenagers — Keo, Teva and Benal, with a small feathered predator named Noli — steal two environmental suits and walk eighty kilometers to the original arrival site to find the complete protocols. They get there. It costs them Noli, most of their gear, and nearly Teva. What they find is the truth about their own society, which is not the lie they expect: the corruption was drift rather than deceit, and only the original colonists could ever have gone home. The book is told in rotating third-person limited across the three of them, with an epigraph channel of twenty-first-century documents the characters cannot see — which is where most of the dramatic irony lives, and where the future dies on a schedule while three children walk through a swamp.

**The project is mid-reconstruction and that governs how to work in it.** There are roughly 10,600 words of drafted prose in `content/superseded/`, and they are **not canon and not a style exemplar** — they are edited AI output that measures nothing like Daniel's own novels, and their worldbuilding has been harvested into the planning layers. Most of those layers were written in a single day, 2026-09-10, by an AI session, and are being approved one file at a time. The governing rule, in Daniel's words: *"Commits aren't evidence of my work, because commits have been made by AI. What is evidence of me is a question that you directly ask me, that I directly approve."* Every commit here is authored by Daniel and most of the content in them is not his. **A citation to a canon file therefore proves nothing about whether something was ever decided** — one file spent a day asserting the colony was telepathic because a drafting model wrote an atmospheric sentence in a scene and a later pass promoted it to a rule. Check the approval table below before building on anything, and when the world does not supply something a scene needs, ask rather than invent.

---

## Where to start

**A new session should read `process/scene-build-runbook.md` first.** It is the procedure for building one scene with the whole apparatus running, and `process/methodology-theory.md` is the reasoning behind it — the claims, their evidence, and the failures that cost real work. Both are recent and unapproved.

## The files

### `plan/` — the novel's design

| file | what it is | approved? |
|---|---|---|
| `outline.md` | the fifteen-beat structure, with rationale, and the sequel arcs | **yes** |
| `milieu-brief.md` | the world: premise, mission status, the Enclave, technology, upgrades, the crisis, the cast's facts | **reviewed and corrected 2026-09-10** |
| `journey-calendar.md` | nineteen days, distances, and the weather score | **yes** |
| `body-and-resources.md` | food, water, injury, fatigue, pace — the physical continuity chain | **yes** |
| `milieu-allocation.md` | biome, species and sensory budget, one showcase per thing | **yes** |
| `humour-plan.md` | comic registers, placement, and the charm deficit | **yes** |
| `scene-list.md` | the scenes | **no — and it needs rewriting.** 38 scenes against a 60-scene proposal; Acts 2 and 3 still in the old format; Days 6, 7, 8, 9, 12, 13, 17 and 18 unscened; its own header says 40 |
| `pacing-and-stakes.md` | scene count, the three size bands, the four stake ladders | **no — this is the gate.** The scene list cannot be rebuilt until it is settled |
| `knowledge-ledger.md` | who knows what when, in three columns; the irony allocation; the epigraph suite | **no.** Its rows can be approved now; its payment assignments name scene numbers and must wait for the new list |
| `character-arcs.md` | the three arcs, the losses, the dyads | **no.** Read, not formally approved. The arcs are Daniel's; the machinery under them was extrapolated |
| `voice-sheets.md` | per-character idiolect, and what each never says | **no** |
| `foreshadow-and-motif.md` | plants paired with payoffs, signal levels, motif budgets | **no** |
| `tech-rules.md` | every capability audited for where its rule is taught and where it is exploited | **no** |
| `minor-characters.md` | everyone but the three; four `[provisional]` names | **no** |

### `prompts/` — what you hand a model

`style-canon.md` (verbatim passages from Daniel's two novels — the voice target, and the primary instrument), `writing-style.md` (the prose rules), `ai-tells-blacklist.md` (defects found in real generated drafts, in Daniel's own words — run as a gate before he sees anything), plus three role prompts: `logic-checker.md`, `repetition-hawk.md`, `word-choice-expert.md`.

### `kb/` — reference

`worldbuilding/` holds invented canon that needed its own file: `safety-suits.md`, `the-wig.md`, `lingo.md` (a **closed** list of fifteen drifted words — coining new ones is a defect), `names.md`, `benals-equation.md`. **All approved.** `research/` holds real-world reference: `geo-flora-fauna.md`, `predator-vision.md`, and an image. Approved.

### `content/` — prose

`epigraphs.md` holds the thirteen archival fragments. `superseded/` is the ten drafted Act 1 scenes, retained for reference only. `rejected/` is labeled failures, kept because they are useful negatives, each carrying a line saying why it was rejected. **No approved prose exists yet** — the novel has not been written.

### `.ignored/` — working documents, untracked

Analyses that outlive a session but are not canon: the authorization audit, the milieu-brief and character-arcs comparisons against the versions Daniel approved, and the register of open questions.

## Open work, in order

1. **Approve `pacing-and-stakes.md`.** Everything downstream waits on it.
2. **Approve the rows of `knowledge-ledger.md`.**
3. **Rewrite the scene list** to the approved count. Much of the open-question backlog gets worked off here rather than in the abstract.
4. **Thirty-five open questions**, in `plan/open-questions.md` — twelve carried over, twelve restored after being removed without answers, five reopened, and the rest raised during the 2026-09-10 review.
5. **Renumber, and retire "beat" as an organizing term.** Approved 2026-09-10, deferred until the rescene because the scene count goes from 38 to roughly 60 and every number moves then anyway. Four units, and nothing else:

   - **Act** — three.
   - **Chapter** — the reader-facing unit, the thing you finish before putting the book down. Holds one or more scenes. This has never existed and was asked for at the start of the project.
   - **Scene** — the writing unit: one POV, one place, one continuous stretch of time. Numbered **sequentially, 1 to 60**, so a scene number is an address and carries no other claim.
   - **Move** — one action by one party inside a scene. What the scene maps enumerate.

   The present numbering is beat-major, so `4.3` means the third scene of beat 4, which sits inside Act 1 — the first digit is not an act and reads as though it were. **The fifteen "beats" are Blake Snyder's *Save the Cat!* template**, applied on 2025-11-02 without being asked for. Several of its labels actively misdescribe this book: there is no *Fun and Games* in eleven days of mudwalk and no *Bad Guys Close In* in a novel whose antagonist is a world. The structure is demoted to **an analysis note** — a check that the story would also work as a film, which is a fair test — and stops being the organizing principle or the address system.

   **Scope: 392 scene references across 25 files, and 40 Snyder labels.** `methodology-theory.md` §8 records that this corpus has already suffered layer drift from a renumber that did not sweep everything, so this is a scripted sweep with a verification pass, not hand-editing.

6. **Tag scene obligations `@2.3` across the layers**, once the rewrite has settled the numbering. Every line in any layer that assigns work to a scene gets the tag, so `grep -rn '@2\.3' plan/` returns that scene's complete obligation set. The scene map's layers-joined table is then generated rather than hand-assembled, and phase 3 gains an invariant: every tagged obligation has a move. Deferred until after the rewrite because half the numbers will move.
7. The remaining unapproved layers, in any order.
