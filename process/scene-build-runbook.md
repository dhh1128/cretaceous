---
approval: unapproved
---

# Scene build runbook

*The procedure for building one scene of Cretaceous with the whole process active. Reusable for every scene — substitute the scene number. Version 1, 2026-09-10.*

**This file is part of a flywheel.** Phase 0 loads it, phases 1–8 run it, phase 9 improves it. A session that skips phase 9 has taken from the process without paying back into it. See `methodology-theory.md` §11.

---

## Phase 0 — LOAD

Read, in this order, before doing anything else:

1. `methodology-theory.md` — the claims, their status, the tests, and the standing hazards. **Read the Withdrawn claims and the hazards especially.** They record things already tried that did not work; re-deriving them costs a session.
2. This runbook.
3. `prompts/ai-tells-blacklist.md` — the defects Daniel has actually found in generated prose.

**What went wrong before, so you do not repeat it.** On 2026-09-10 a draft of scene D2.3 was produced from a structure map alone, with every other layer deliberately switched off to isolate a variable. Daniel read 8,600 words and wrote thousands in critique to correct 2,000 words of unusable prose. The dominant failure was **unsubstantiated invention** — the drafter invented sleeping arrangements, a set of twins, a character's age, where suits are stored, the temperature at dawn, and then built further material on each invention, so each correction meant unwinding a structure rather than replacing a word. The second failure was **characters with no wants**, which was a defect in the brief and not in the writing. Phases 3 and 4 exist because of these two.

---

## Phase 1 — Gather

Read every layer that allocates anything to this scene. Read the files; do not grep them. Grepping is how allocations get missed, and a missed allocation is a scene that fails its job silently.

| file | what it gives this scene |
|---|---|
| `scene-list.md` | the scene's entry: size, day, POV, location, ladders, what it must carry, what it ends on |
| `outline.md` | which step of the fifteen-step structure this sits in |
| `body-and-resources.md` | the loadout at departure, and the physical state this scene inherits |
| `pacing-and-stakes.md` | the four ladders and this scene's rung on each |
| `character-arcs.md` | what each character wants, believes, fears and hides at this point |
| `voice-sheets.md` | per-character speech shape, and **what each never says** |
| `knowledge-ledger.md` | which facts are known to whom here; which rows this scene pays |
| `foreshadow-and-motif.md` | plants and payoffs landing here |
| `humor-plan.md` | comic allocation |
| `milieu-allocation.md` | which sensory material is budgeted here, and which is spent elsewhere |
| `milieu-brief.md` | world facts the scene touches |
| `kb/worldbuilding/*` | everything else about the world |
| `minor-characters.md` | cast, names, ages, established facts |
| `tech-rules.md` | how the technology behaves — **and check its audit table for a gap assigned to this scene.** A capability taught here for the first time, cost-free, is an obligation, not a suggestion: D2.3 owes accelerated healing and its price, D2.5 owes croc vibration sensing, D3.1 owes suit thermal management and suit feeding. A scene that skips its teaching leaves a later scene exploiting a capability the reader has never seen |
| `body-and-resources.md`, `journey-calendar.md` | physical state, food, water, weather, time of day |
| `style-canon.md` | verbatim Hardman passages — the voice target |
| `writing-style.md`, `word-choice-expert.md` | prose rules |

If a layer's allocation refers to a scene by number, check which scene list it was written against — the layers were written against three different ones and never fully reconciled.

---

## Phase 2 — Forward map

Build the scene structure map per `methodology-theory.md` §4. Roughly one move per 100 words of intended prose. This is the join table: every allocation from phase 1 gets bound to a **position**, not just to the scene.

Requirements that exist because they were violated:

- **Every character present gets a `wants` line.** Not just the POV. A character with no want is furniture, and Daniel will hate them.
- **A world-facts block in IN** — the physical facts of the location the scene will touch, stated so the drafter never has to invent them. Where things are kept. Where animals sleep. Heights, distances, temperature, light.
- **Moves state what a move *does*, not what it looks like.** "Riel describes a stretch of ground: distances, terrain, one hazard" produced non-sequitur drivel because the move had a shape and no function.
- **Voice traits carry a scope.** "Riel counts" without bounds metastasized into a whole family obsessed with precision measurement.
- **Every `[requires]` carries a payload** — what it needs to still be true, not just where it lives.

## Phase 3 — Check the map, before anything else

Run the four invariants from `methodology-theory.md` §5 **against the map itself.** The D2.3 map promised a reader payment that no move delivered, sat in the open for a day, and neither of two AI sessions noticed.

1. State closure against the neighboring scenes.
2. Every ledger row named in `OUT — READER` is paid by a move.
3. Every `[turn — READER ONLY]` corresponds to a ledger row.
4. Every `[requires]` resolves, and its payload is still true at the far end.

Then re-read the scene-list entry and confirm every "must carry" item has a move.

**`git add` the map before you run anything against it.** The suite reads `git ls-files`, so an untracked map is invisible to every check and the run comes back clean because **it never looked.** That happened on the first map written after the checks existed: `scene_map_in_complete` and `scene_map_backward_closure` both passed, and both had examined two files rather than four. A green run on a file the corpus cannot see is worse than a red one.

**And run the mechanical checks here, not only at phase 7.** `uv run --with pytest pytest tools/ -q` against the map itself. On the first two maps this caught a citation to a section that does not exist and an instance of the eliminated unit word, three phases before the runbook had been putting the gate. It costs five seconds and it is defects Daniel would otherwise have read.

### The outside read, before the ledger goes to him

**Hand the map to models from other lineages and ask them to break it.** `methodology-theory.md` C11 has the evidence and the two cautions; this is the procedure.

The packet is self-contained or it is worthless — a reviewer who cannot see the canon invents objections out of the gaps. It carries the framing, the standard it is judging against, **the canon the map rests on, the entries for the state-closure neighbors**, and the map. `.ignored/redteam/build-packet.py` assembles it from the corpus at build time so it cannot drift from what the map actually cites.

Three things that decide whether it is worth the call:

- **Ask for refutation against the stated standard, not for an opinion.** "What do you think of this" returns polite endorsement from every provider.
- **The highest-value section is the undeclared inventions**, because that is the ledger's own measure: what the pass failed to ask about. Say so in the prompt and ask for it exhaustively.
- **Verify before adopting.** One seat's headline finding in the first run was confidently wrong and would have broken a working scene. Agreement across lineages is weak evidence and a single confident dissent is not evidence at all until you have chased it.

**Its output is ledger items**, which is why it sits before phase 4 rather than after it. Two of the first run's findings reshaped the scenes and neither was reachable from the four invariants.

## Phase 4 — Invention ledger — **STOP HERE**

List everything the scene will have to invent that no canon file substantiates. For each:

- a **proposed answer**, not a question — Daniel scans and objects; he does not do the work
- a **provenance mark** — *grounded* (cite the file) or *invented* (nothing says)
- an answer that fits in **a few words**

Only *invented* lines need his attention. Include the *grounded* ones so he can catch a bad citation.

**Give him the list and wait.** Do not draft. The pass is judged on what it failed to ask about: if the draft later contains an invention that was not on the ledger, the ledger pass was incomplete, and that is the defect to record in phase 9.

## Phase 5 — Write answers back to canon, and annotate them on the way in

Every answer goes into the appropriate canon file immediately. **This is what makes the ledger shrink.** An answer left only in a chat transcript will be invented again, differently, in the next scene.

**Not with a date and an attribution**, which an earlier version of this line asked for and `AGENTS.md` §2 forbids: knowledge files carry what is true, and git carries how it got there. Where a ruling exists specifically to stop a known error being re-made, state it as a standing prohibition instead.

**One file is not enough, and this is the step that keeps being underestimated.** A fact minted in conversation lands wherever the session happened to be working, and every *other* file that touches it goes on saying the old thing — which is how a single figure came to mean the years at Genesis in one approved file and the duration of the walk in another, with nothing in the suite able to see it. **So a write-back is not done when the fact is written down. It is done when every file that states the fact states the same thing.** Grep for the fact before you write, not after.

**Then annotate it, in the same edit.** `claims_agree` is the only instrument that can catch two well-formed assertions that are jointly false, and it is inert until somebody declares the claim — so the annotation goes on at mint time, on every site, not in a later sweep:

```
**a week to a month, and not three years.** <!-- @WF-firstwalk.duration: weeks -->
```

`WF-` for world fact, then `<subject>.<attribute>: <value>`, lowercase and dotted. **The check fires when one key carries two values anywhere in the corpus**, so the value is worth nothing on a single site and worth a great deal on the third one. **Annotate what a later session would plausibly re-invent**: figures, colors, durations, who is alive, which room has which property. Not prose judgments and not scene decisions, which belong in the map.

**An annotation that lies is worse than none**, because it reads as authoritative and the check will agree with it. Only annotate what you have just verified against the file you are editing.

*(There is a separate standing sweep for facts that predate the convention, and its handoff lives under `.ignored/`, which is gitignored and cannot be cited from a tracked file. Phase 5 is for the facts this scene created. **The backlog does not shrink if new ones keep arriving unannotated.**)*

## Phase 6 — Draft

One pass. One mind holding the scene at once. Do not factor the writing into layers — plan in layers, draft in one pass, revise in layers.

Inputs: the map, plus **everything**. Style canon, voice sheets, world bible, milieu brief, cast list, tech rules, blacklist, the answered invention ledger. Never strip inputs to isolate a variable in a run that is meant to produce usable prose; that was the D2.3 mistake.

## Phase 7 — Mechanical checks, before Daniel sees anything

Iterate until clean. Do not send him a draft that has not passed all of these.

- `prompts/ai-tells-blacklist.md`, every section
- `prompts/logic-checker.md`
- `prompts/repetition-hawk.md`
- the four invariants, now against the prose
- **the invention audit**: every concrete fact in the draft is in canon or on the answered ledger. Anything else is an unauthorized invention and comes out.

His attention is the scarcest thing in this project. Spending it on defects a checklist catches is the most expensive mistake available.

## Phase 8 — Daniel reads

**Tell him what to evaluate.** An unscoped "is this better?" gets scoped to whatever was last discussed — that has already produced one false finding. If you want a verdict on structure, ask for structure.

## Phase 9 — RETRO — mandatory

Not optional, and not long. Budget it before you start so the session does not end without it.

1. **Update `methodology-theory.md`**: the §10 log, any claim whose status changed, anything withdrawn. A withdrawn claim keeps its post-mortem.
2. **Update this runbook**: whatever you had to work out that was not written down.
3. **Update `ai-tells-blacklist.md`**: new tells from Daniel's critique; and check whether the old ones recurred.
4. **Record the three flywheel numbers** (`methodology-theory.md` §11): invention-ledger items asked, author words read, author words written. They should fall from scene to scene. If they do not, the flywheel is not turning and something in this procedure is wrong.

---

## Open question for the first run

`Q-8HNV`, unanswered as of 2026-09-10: for scene D1.1, is `content/superseded/01.1.md` an **input** — map the existing scene and rebuild from that map, inheriting the architecture Daniel designed — or is it **set aside**, mapping D1.1 from the scene list and the layers alone and writing fresh? The first inherits a structure he liked along with whatever is wrong with it; the second is a cleaner test of the process. Ask him before phase 2.
