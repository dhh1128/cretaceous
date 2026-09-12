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

### The log against that baseline

| when | check | count | why it moved |
|---|---|---|---|
| baseline | — | 14 / 98 / 1 | the checks written, nothing rebuilt |
| Days 7–9 rescened | `scenes_per_day` | 14 → **11** | eight scenes written for Days 7, 8 and 9. **`SCENE_ENTRY` was widened in the same commit** to accept the provisional day-keyed ids, and that alone does not account for the drop: with the old pattern the new scenes were invisible and those days read as 0, and with the new pattern but no new scenes they would read 1, 1, 0 against 3, 3, 2 and still fail. Both were needed. |
| Days 7–9 rescened | `epigraph_count` | 1 → **0** | `knowledge-ledger.md` now declares the suite at the size `content/epigraphs.md` actually holds, and says plainly that its own seven-row table is the superseded design, kept only for the job column until the rescene reassigns it. |
| Days 7–9 rescened | `eliminated_unit_word` | 98 → **97** | incidental, from rewriting the two river entries. The sweep has not started. |

## Not yet built

**Blocked on the rescene.** Every scene id cited anywhere resolves to a scene in `scene-list.md`; every `[requires]` pointer resolves. Scene numbers are about to be reassigned, so building these now buys a suite that goes red for the right reason at the wrong time.

**A check nobody has written, and it would have caught a real error.** `plan/` may not contradict `kb/research/`. `milieu-brief.md` already states the precedence — *if this file and one of those disagree, the specialist file wins and the discrepancy is a defect* — and nothing enforces it. The scene list had a *Quetzalcoatlus* snatching prey on the wing while `kb/research/geo-flora-fauna.md` said, on its own line, that the animal was a terrestrial stalker hunting on the ground. The research was right and the plan ignored it for months.

**Blocked on prose.** The blacklist and word-choice rules, the sentence-distribution targets in `prompts/style-canon.md` §0, the repetition window, and the allocation-against-prose check — one search key per allocated item, flagging any use outside its day. That last one is the repetition instrument `milieu-allocation.md` exists to be, and it stays deterministic.

**Blocked on nothing but time.** `milieu-allocation.md` §3 and §5 must agree on every day number; every day is covered by exactly one biome band; the motif budgets against their own tables; every character's physical attributes stated in one place only.

## The lens tier

Not built. When it is: `@pytest.mark.llm`, deselected by default, because if the fast loop stops being instant it stops being run. Results cached by a hash of the input so a typical pass re-checks only what changed. Cheap seats do extraction, frontier does judgment, and every finding gets one short refutation call to a **different model family** before it reaches Daniel — agreement inside one family is weak evidence, and four agents on 2026-09-11 returned roughly fifteen findings of which several were already known and one was wrong.

Prefer the `panel` wrapper over bare `llm` for OpenRouter seats: the seats are reasoning models, several stall past the default timeout on multi-kilobyte prompts, and `panel.conf` already pins the per-seat timeouts that fix it. Pass low reasoning effort for extraction work, and check `finish_reason` before trusting any sweep — a seat that runs out of output tokens exits zero with a body truncated mid-thought.
