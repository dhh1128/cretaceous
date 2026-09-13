# tools — the consistency suite

Answers one question: **does anything in the corpus disagree with anything else in the corpus?** It is blind to the other question — whether any of it is Daniel's — and a green run must never be read as approval. See `AGENTS.md` §1.

```
uv run --with pytest pytest tools/          # the fast suite, ~0.5s
uv run --with pytest pytest tools/ -k day   # one category
python3 tools/report.py                     # the same checks as a markdown change set
python3 tools/report.py day_tokens          # one check
```

`pytest` is not installed on this box and no `pyproject.toml` or venv is wanted in a novel repo, so `uv run --with pytest` supplies it per invocation. `report.py` needs nothing but the standard library.

Five files. `checks.py` holds the logic as plain functions returning violations; `test_consistency.py` is a thin pytest front end; `report.py` is a second front end for the document Daniel reads and strikes; `ratify.py` is how a proposed rule becomes an enforced one and `approve.py` is how a file's contents get Daniel's marker, and both need a TTY so an agent cannot run them. Logic never goes in the test methods — a suite that can say something is wrong but not what to change is half a tool.

**One test per invariant, not per violation, and the test name states the claim.** `test_every_file_reference_resolves` fails once, listing all thirteen dangling pointers, rather than thirteen times. Two reasons. The failing line reads as a sentence and needs no docstring to decode it. And the failure count then means what it looks like it means: an earlier version parametrized per violation and reported thirteen pointers plus seven stray dates as *"20 failed"*, which reads as twenty problems and is two. The instances go in the message as `file:line — what`, which is the change-set row.

## The two rules that govern what may be written here

**A check asserts a relationship, never a value.** *"Every day named anywhere exists in the calendar"* is a check. *"The savanna is 6 km"* is a second copy of the calendar wearing a test costume: it freezes a number into a new location, and if that number was never approved the suite now enforces an invention. This is the failure the corpus has already suffered and it is the one thing that would make the suite worse than nothing.

**Anything the corpus declares about itself is read from the corpus at runtime.** The day range comes from parsing the calendar's own table. The US-English word list comes from the grep command in `AGENTS.md` §5. A check that hardcodes one of those is the seventh copy of a fact and it will drift.

### The one place `checks.py` cheats

`british_words()` reads `AGENTS.md` §5 and then adds ten words found in the corpus that the blacklist does not carry — `armoured`, `synthesised`, `energised`, `micrometres`, `cruellest`, and five more. Those belong in `AGENTS.md` §5, which is the owner. When they are moved there, delete the extension list.

## The checks, and why each exists

| check | asserts | why it exists |
|---|---|---|
| `day_tokens` | every day named anywhere is a day the calendar has, and no range runs backward | A scripted day sweep in `2e9f355` double-mapped the first number of nine ranges, producing `Days 14–13`. This catches eight of those nine. **The ninth is `voice-sheets.md:39`, `Days 15–19`, which ascends and looks sane** — proof that the check is a net, not a proof. |
| `calendar_owns_distances` | no file but the calendar carries a per-day distance column | `body-and-resources.md` §3 kept its own `km` column and the two drifted apart unnoticed. Deleting the duplicate is better than checking it, and this check retires when that happens. |
| `file_refs` | every `` `file.md` `` the corpus points at exists | Thirteen pointers survive into files deleted in the 2026-09-10 restructure, and each still reads as authority. |
| `section_refs` | every `` `file.md` `` §N citation resolves to a heading numbered N | Renumbering the calendar's sections silently broke four citations. Nobody noticed for a day. |
| `frontmatter` | every file carries exactly one of the three approval values | `AGENTS.md` §2. The scheme is worthless if a file can quietly carry no marker. |
| `approval_not_stale` | every approved file's body still hashes to what its marker records | Markers carry an eight-character body hash, not a date. **Three designs, and the first two both asked chronological questions and got the wrong answer.** A hand-written date has day granularity, and this corpus was written, approved and committed inside one day. Commit ordering then counted a formatting migration — stripping those dates off every marker — as an edit to all 24 approved files at once. A hash is a comparison: immune to reformats, immune to commit churn, and it sees uncommitted edits, which neither chronological version could. |
| `approval_stated_once` | a file's approval state appears in its own frontmatter and nowhere else | README carried a second copy and it was wrong about five files. The column is now deleted rather than generated, and this check keeps it deleted. It matches claim phrases — *is approved*, *are recent and unapproved* — not the bare word, so *"No approved prose exists yet"* and *"four [provisional] names"* do not fire. It will also miss a trailing *"Both are unapproved"* whose files were named a sentence earlier. |
| `us_english` | no British spellings | `AGENTS.md` §5. A literary register pulls toward them and it keeps coming back. |
| `closed_list_uncounted` | nobody states how many terms the closed vocabulary holds | The terms are canon and the count is incidental. Four files carried a number that had been wrong since the file was created — `git show` returns sixteen at every commit that ever touched it. A fact nothing depends on is a fact that only drifts, so the number is deleted rather than corrected. |
| `reserved_species_unspent` | species held in reserve are not spent in an active allocation | *Alphadon* and *Meniscoessus* are on the reserve list and are also the grounders Noli catches. |
| `dated_provenance` | knowledge files carry what is true, not how it got approved | `AGENTS.md` §2: no dates, no "Daniel said", no "struck on". The pattern deliberately does not match the bare name, because *"that is a note for Daniel, not a license"* is instruction, not history. It exempts only the frontmatter fence. The markers used to need an exemption of their own; now that they carry no dates, they need none. |
| `rules_wellformed` | every ``` ```rule ``` block parses, carries its fields, and has evidence | The rule formalism, checked by the suite it feeds. See `tools/RULES.md` |
| `species_showcase_count` | every species row names at most two days | Rule `species-one-showcase`. Currently a regression guard — nothing violates it |
| `allocation_day_agreement` | a species carries the same day in §3 and §5 | Rule `allocation-day-agreement`. Catches three violations against the pre-repair corpus and none now |
| `biome_covers_every_day` | every day falls inside at least one biome band | Rule `biome-covers-every-day`. Catches five against the pre-repair corpus — Days 7, 8, 9, 17 and 18 had no band at all |
| `plant_payoff_bijection` | every ledger row has a plant, a payoff, and an address at each end | Rule `plant-payoff-bijection`, ratified. The ledger's own validator asks for this in both directions and nothing had ever run it |
| `overt_plant_budget` | the foreshadow ledger carries the number of overt plants it budgets | The budget and the table agree today. It is here as a regression guard, and as the template for the other declared budgets. |
| `scene_day_tags` | every scene carries a day tag, and it is a day the calendar has | The safety net for the renumber. Green today and expected to stay green — a scene that loses its day during the sweep stops being placeable in the world, and nothing else would notice. |
| `act_composition` | every act holds the number of scenes its own heading claims | Green today. An act that says fourteen and holds nine is what a rebuild produces silently. |
| `scenes_per_day` | each day holds the number of scenes `pacing-and-stakes.md` §5 proposes | **The rescene's progress bar**, and red by design. One line clears per day rebuilt. |
| `eliminated_unit_word` | the eliminated unit word appears nowhere outside the README item that explains it | Red by design. Reports locations only: each instance needs its own replacement word — *worth a beat* and *the last beat of his arc* do not take the same one — so a check that proposed substitutions would be proposing prose. Blockquotes are exempt, because those are verbatim passages from Daniel's novels and rewording one would falsify the source. |
| `epigraph_count` | the epigraph suite's declared size equals the fragments that exist | Three numbering systems are live in a channel the species ladder runs through. |
| `allocation_covered` | every species or small-life item allocated to a day appears in a scene on that day | **The first check that looks inside a scene.** Catches twelve today, including *Anzu*, which has a full species showcase on Day 4 and appears in no Day 4 scene, and *Ornithomimus* on Day 10, which the allocation calls the one animal that is simply a pleasure to watch. |
| `every_scene_moves_a_ladder` | no two consecutive scenes carry identical ladder values | `pacing-and-stakes.md` §6 — a scene that moves none is cut. Catches one today and grows teeth as the rescene fills the values in. |
| `scene_entry_complete` | every scene entry carries a size band, a day, a POV, a place, a `**Ladders:**` line and an `**Ends on:**` line | A field an entry does not carry is a field no other check can read, and the failure is silent — `scenes_per_day` read the day-keyed entries as absent for a whole rescene because nothing had widened the pattern that finds them. **Catches 24 today, in two distinct groups:** twelve Act 2 entries still in the older single-line form, which carry no size band, no ladders and no ending and are being converted now; and **twelve Act 1 entries — 1.1, 2.1, 2.2, 2.4, 2.5, 3.1 through 3.4, 4.1 through 4.3 — that carry everything else and no `**Ends on:**`**, which is not the conversion and is nobody's known work item. `**Hazard:**` is deliberately not required: it arrived after the format did, and the 26 entries that predate it are not defective for lacking it. |
| `pov_run_length` | no more scenes run consecutively in one POV than the corpus says may | Three POVs that take turns are a promise, and a stretch that forgets to rotate reads as a different book for as long as it lasts. **Catches one today, and it is the absence of the rule rather than a breach of it:** no file declares the ceiling, so the check reports the missing declaration. See "The POV run ceiling has no owner yet" below. |
| `payment_order` | no ledger row pays before the scene that plants it | A plant only works forward, and the ledger is what a drafting pass reads to decide what has to exist first, so a reversed row sends the writing at it backwards. **Catches one today:** row 21 of `foreshadow-and-motif.md` §2 plants the river gratings at 2.5 and pays them at 2.3, both on Day 2. Four cells resolve to no scene at all — `Act 1`, `book 2`, `13.x`, `7–9` — and those are reported by `unresolved_payment_addresses()` rather than guessed at, because whether every cited address resolves is its own invariant and it is blocked on the renumber. |
| `allocation_off_day` | an allocated item does not appear on a day it was not allocated to | **Written and deliberately not registered.** The inverse of `allocation_covered` and the instrument `milieu-allocation.md` says it exists to be. It cannot be made honest against the scene list; the measurements are below. |

### The POV run ceiling has no owner yet

`pov_run_length` reads its ceiling from `plan/pacing-and-stakes.md` and finds nothing, because nothing in the corpus states one. It reports the missing declaration rather than falling back on a default, because a number chosen in this directory would be the suite enforcing a decision nobody made — rule one, in its most tempting form, since three is such an obvious answer that it barely feels like an invention.

**Where it belongs: `plan/pacing-and-stakes.md` §3.** That is where the rotation is asserted — *"This is a rotating three-POV novel, so the reader learns whose head they are in before the first sentence rather than four lines down"* — and a ceiling on the run is the same fact stated as a constraint. §4 already carries the sibling rule for size, *"Never two consecutive scenes of the same shape."*

**In these words**, as its own line after that paragraph:

> **No more than N consecutive scenes in one POV.**

`N` spelled as a word or a numeral; the check reads either, and reads nothing else, so a paraphrase will not register. What the number has to be decided against, all of it measurement rather than opinion:

- **The scene list today** runs 70 scenes in 50 runs — 38 of one scene, nine of two, one of three, **one of five** (KEO, 3.3 through 4.3, which is the theft) and **one of six** (BENAL, D13.1 through D15.1, which is the drag-frame, the coast, the raft and the coral bank).
- **In Daniel's own novels:** `viking.md` never runs three consecutive chapters in one head across fifty-five, and `cordimancy.md` has a single run of five.
- So a ceiling of three flags both long runs, and a ceiling of five flags only the six. Neither is a number this directory may pick.

### Why `allocation_off_day` is written and not registered

It is the inverse of `allocation_covered` and it is the instrument `milieu-allocation.md` says it exists to be — *the world is a finite set of striking things, and each one is assigned to one or two days and is off-limits elsewhere.* It is in `checks.py`, out of `CHECKS`, and this is the argument.

**The corpus does not assert what the check would enforce.** §3 of the allocation, one line under that premise: *"Each species gets one showcase. After its day it may be referenced but not re-described."* The croc row spells out what a permitted reference looks like — *after Day 8 it is a shape, a wake, an absence of birds.* So the invariant is not *appears nowhere else*; it is *is not re-described elsewhere*, and re-description is a property of prose that no key match can see. Registering the stronger claim would enforce a rule that was never made.

**And the scene list is a plan, not prose.** This directory's own "Not yet built" list already has this check under **Blocked on prose**, and that judgment was right. Most of what fires is the plan discussing its own allocations: the saropo-riding plan proposed and rejected on Days 7 and 8, *"the honey on Day 6, the turtle corridor on Day 14"* in a Day 16 hazard note, *"four days after a mosasaur destroyed their raft"* on Day 19.

**The measurements**, all against the scene list, all counting one (day, item) pair as one finding:

| what is filtered | fires | genuine |
|---|---|---|
| nothing — `_alloc_keys` and substring matching, exactly as `allocation_covered` uses them | 29 | 2 |
| word-boundary matching, and keys of fewer than six characters dropped | 11 | 2 |
| the above, plus lines that name a day other than the scene's own | 10 | 2 |
| **word boundary, six-character floor, and keys that prefix a closed-list term exempted — what is implemented** | **3** | **1** |
| all four together | 2 | 1 |

**The noise has three sources and the first is worth keeping as a warning.** Substring matching collides: `achero`, from *Acheroraptor*, matches **treacherous**; `ants`, from hell ants, matches *wants* and *plants*; `hell` matches *unshelled*. Then `_alloc_keys` takes the first three words of the whole cell rather than the colony name, so *"the large river crocodylian — croc"* yields `large`, `river` and `crocod`, and `river` fires on seven days. Then the permitted references above.

**The trade that decides it.** The closed-list exemption is what buys the precision in that table, and it is bought by refusing to look at *croc*, *saropo*, *razortail*, *flybeak*, *grounder* and *stonefruit* — the five animals and the one food the colony has words for, which are the most repeated nouns in the book and precisely where a repetition instrument is needed. A version that sees them cries wolf four times in five; a version that does not is blind in the middle of its own subject. **Neither is worth a human's attention, so neither is registered.**

**Two genuine findings it did surface, recorded here because the check cannot be trusted to keep finding them.** Scene 7.1 on Day 10 serves *"sweet, mealy 'dinosaur-fruit' (Annonaceae)"* while the stonefruit is allocated to Days 4, 6 and 13. Scene 8.2 on Day 11 has Keo climbing *"(e.g., against a pack of Razortails)"* while the razortail's one showcase is Day 3. Both sit in the older Act 2 entries.

**What would make it registrable**, in order of cost: a declared key column in the allocation table, which is already this directory's stated fix for `allocation_covered`'s false-positive class and is a change to an approved file; a way for a scene entry to mark a mention as the permitted kind of reference; or drafted prose in `content/` to run it against instead of a planning document, which is what it was always meant for.

## The rescene baseline, recorded before the rebuild started

**The suite is deliberately red, and this is the record that green was reached by doing the work.** The checks were written first, against the un-rebuilt corpus, so "watch it go red, rebuild, watch it go green" means something. The person who writes the checks is also the person who could quietly relax one, and a number written down beforehand is the only guard against that.

At the commit that introduced the rescene tier:

| check | violations at baseline |
|---|---|
| `scenes_per_day` | **14** — Days 3, 4, 5, 6, 7, 8, 9, 12, 13, 15, 16, 17, 18, 19 |
| `eliminated_unit_word` | **98** |
| `epigraph_count` | **1** |
| `scene_day_tags` | 0 — green, and must stay green through the renumber |
| `act_composition` | 0 — green, and must stay green through the renumber |

**If a number here goes down without the corresponding work being done, the check was weakened.** Any change to one of these five checks that reduces its baseline count belongs in a commit that says so in its message and explains why the old assertion was wrong.

### Why the shape of the list is not the content of a scene

Every check above `allocation_covered` asserts something about the *list* — how many scenes a day holds, whether an act's count matches its heading, whether a day tag resolves. **All of them pass on empty stubs.** The rescene's first three days went in and the progress bar moved from 14 to 11, and a pass that had written three scenes carrying nothing would have moved it exactly as far.

The demonstration, from the session that built these: a drafting pass produced three Day 6 scenes and silently dropped six things the allocation assigns to Day 6 — the amber, the armored indifferent animal, the oaks and walnuts, the stonefruit, the face-height spiderwebs, and the harmless croc in clear water, which had been argued for in conversation minutes earlier. Nothing in the suite noticed. **A counting check can be satisfied by doing the wrong thing**, which is the same defect as a statistic averaged over two populations, and the answer is the same: look inside.

### The known false-positive class in `allocation_covered`

The search key is derived from the allocation row's own label, and the page and the table rarely agree on wording. Matching is on a six-character prefix, which handles *Grounders* against *a grounder* and *Mosasaurus* against *the Mosasaur* — the first attempt stripped a trailing `s`, which fixed the first pair and broke the second. It will still miss a scene that names an animal by the colony's word while the row names it by binomial. **When that starts costing more than the check catches, the fix is a declared key column in the allocation table**, which is a change to an approved file.

### The log against that baseline

| when | check | count | why it moved |
|---|---|---|---|
| baseline | — | 14 / 98 / 1 | the checks written, nothing rebuilt |
| Days 7–9 rescened | `scenes_per_day` | 14 → **11** | eight scenes written for Days 7, 8 and 9. **`SCENE_ENTRY` was widened in the same commit** to accept the provisional day-keyed ids, and that alone does not account for the drop: with the old pattern the new scenes were invisible and those days read as 0, and with the new pattern but no new scenes they would read 1, 1, 0 against 3, 3, 2 and still fail. Both were needed. |
| Days 7–9 rescened | `epigraph_count` | 1 → **0** | `knowledge-ledger.md` now declares the suite at the size `content/epigraphs.md` actually holds, and says plainly that its own seven-row table is the superseded design, kept only for the job column until the rescene reassigns it. |
| Days 7–9 rescened | `eliminated_unit_word` | 98 → **97** | incidental, from rewriting the two river entries. The sweep has not started. |
| Day 6 written in | `scenes_per_day` | 11 → **10** | three scenes for Day 6. |
| Genesis rescened | `scenes_per_day` | 10 → **7** | Days 15, 16 and 17 built out, twelve scenes where there were four. **Day 18's target was raised from 2 to 3 in the same commit and that is a moved goalpost, so here is the argument:** the §5 row always named three separate things for that day, and the capsule makes a fourth. Two scenes was under-specified from the start. Day 19 went from 3 to 5 and still fails at 5 against 8, which is correct — the chase and everything after it is unbuilt. |
| Genesis rescened | `allocation_covered` | 12 → **13** | went **up**, correctly. Replacing the old combined Day 19 entry with three Genesis scenes removed the only mention of the flybeak on its allocated day. The check noticed that the chase had been deleted before I got round to saying so. |
| Days 3–5 rescened | `scenes_per_day` | 6 → **3** | seven scenes across three days. Only Days 12, 13 and the back half of 19 are left. |
| Days 3–5 rescened | `allocation_covered` | 13 → **5** | the largest single drop the check has produced, and it was not aimed at: writing three days properly picked up frogs, fish, snails, mushrooms, stonefruit and *Anzu*, all of which had been allocated and unspent for months. **This is the check working as an instrument rather than a guard** — the misses were a to-do list for what the scenes had to contain. |
| Days 12–13 rescened | `scenes_per_day` | 3 → **1** | four scenes across the two days. **Only Day 19 is left**, at 5 against 8. |
| Days 12–13 rescened | `allocation_covered` | 5 → 4 → **1** | went up before it went down, which is the expected shape: a day with no scenes is skipped, so building one *exposes* its allocations. *Thescelosaurus*, *Palaeosaniwa* and the *T. rex* all surfaced the moment those days had entries, and all three earned their place — the burrow holes are a hazard on the day the ground is worst, and the apex predator that ignores them pairs against the mid-tier one that does not. |
| Day 19 rescened | `scenes_per_day` | 1 → **0** | **the rescene is done.** 69 scenes against the 69 §5 proposes, and every day holds its number. |
| Day 19 rescened | `allocation_covered` | 1 → **0** | the flybeak's second and last appearance is the chase, so writing the chase cleared it. It stayed red for four commits because the honest fix was always to write the scene. |

**Where the baseline ended up.** `scenes_per_day` 14 → 0, `allocation_covered` 12 → 0, `epigraph_count` 1 → 0. `eliminated_unit_word` is still at 97 and the sweep has not started. `every_scene_moves_a_ladder` sits at 1, on a pair in Act 1 that predates the rescene.

**Two targets moved during the rescene and both are argued rather than quiet.** Day 18, two to three, because the §5 row always named three things and the capsule made a fourth. Day 19, eight to nine, because the row listed nine separate jobs and its last entry was two of them — the chamber settles nothing by design, and Teva's turn cannot happen in a cave. **`act_composition` caught the second one within a minute**, because the Act 3 heading still claimed seventeen: a count stated in two places is a count that can be checked.

## Not yet built

**Blocked on the rescene.** Every scene id cited anywhere resolves to a scene in `scene-list.md`; every `[requires]` pointer resolves. Scene numbers are about to be reassigned, so building these now buys a suite that goes red for the right reason at the wrong time.

**A check nobody has written, and it would have caught a real error.** `plan/` may not contradict `kb/research/`. `milieu-brief.md` already states the precedence — *if this file and one of those disagree, the specialist file wins and the discrepancy is a defect* — and nothing enforces it. The scene list had a *Quetzalcoatlus* snatching prey on the wing while `kb/research/geo-flora-fauna.md` said, on its own line, that the animal was a terrestrial stalker hunting on the ground. The research was right and the plan ignored it for months.

**Blocked on prose.** The blacklist and word-choice rules, the sentence-distribution targets in `prompts/style-canon.md` §0, and the repetition window. The allocation-against-prose check — one search key per allocated item, flagging any use outside its day — is now written as `allocation_off_day` and is not registered; it needs prose to run against and a way to tell a permitted reference from a re-description, and "Why `allocation_off_day` is written and not registered" above has the measurements.

**Blocked on nothing but time.** `milieu-allocation.md` §3 and §5 must agree on every day number; every day is covered by exactly one biome band; the motif budgets against their own tables; every character's physical attributes stated in one place only.

## The lens tier

Not built. When it is: `@pytest.mark.llm`, deselected by default, because if the fast loop stops being instant it stops being run. Results cached by a hash of the input so a typical pass re-checks only what changed. Cheap seats do extraction, frontier does judgment, and every finding gets one short refutation call to a **different model family** before it reaches Daniel — agreement inside one family is weak evidence, and four agents on 2026-09-11 returned roughly fifteen findings of which several were already known and one was wrong.

Prefer the `panel` wrapper over bare `llm` for OpenRouter seats: the seats are reasoning models, several stall past the default timeout on multi-kilobyte prompts, and `panel.conf` already pins the per-seat timeouts that fix it. Pass low reasoning effort for extraction work, and check `finish_reason` before trusting any sweep — a seat that runs out of output tokens exits zero with a body truncated mid-thought.
