# tools — the consistency suite

Answers one question: **does anything in the corpus disagree with anything else in the corpus?** It is blind to the other question — whether any of it is Daniel's — and a green run must never be read as approval. See `AGENTS.md` §1.

```
uv run --with pytest pytest tools/          # the fast suite, ~0.5s
uv run --with pytest pytest tools/ -k day   # one category
python3 tools/report.py                     # the same checks as a markdown change set
python3 tools/report.py day_tokens          # one check
```

`pytest` is not installed on this box and no `pyproject.toml` or venv is wanted in a novel repo, so `uv run --with pytest` supplies it per invocation. `report.py` needs nothing but the standard library.

Three files. `checks.py` holds the logic as plain functions returning violations; `test_consistency.py` is a thin pytest front end, one parametrized case per violation so a failure reads `test_day_tokens[plan/tech-rules.md:21]` and the test id is the change-set row; `report.py` is a second front end for the document Daniel reads and strikes. Logic never goes in the test methods — a suite that can say something is wrong but not what to change is half a tool.

## The two rules that govern what may be written here

**A check asserts a relationship, never a value.** *"Every day named anywhere exists in the calendar"* is a check. *"The savanna is 6 km"* is a second copy of the calendar wearing a test costume: it freezes a number into a new location, and if that number was never approved the suite now enforces an invention. This is the failure the corpus has already suffered and it is the one thing that would make the suite worse than nothing.

**Anything the corpus declares about itself is read from the corpus at runtime.** The day range comes from parsing the calendar's own table. The US-English word list comes from the grep command in `AGENTS.md` §5. The closed-vocabulary count comes from counting `lingo.md`'s rows. A check that hardcodes one of those is the seventh copy of a fact and it will drift.

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
| `approval_not_stale` | no file's last commit postdates its approval date | `AGENTS.md` §2 gives this as a shell one-liner. It currently fires on nothing, because the whole corpus was written, approved and committed on one day — which is itself worth knowing. |
| `approval_stated_once` | a file's approval state appears in its own frontmatter and nowhere else | README carried a second copy and it was wrong about five files. The column is now deleted rather than generated, and this check keeps it deleted. It matches claim phrases — *is approved*, *are recent and unapproved* — not the bare word, so *"No approved prose exists yet"* and *"four [provisional] names"* do not fire. It will also miss a trailing *"Both are unapproved"* whose files were named a sentence earlier. |
| `us_english` | no British spellings | `AGENTS.md` §5. A literary register pulls toward them and it keeps coming back. |
| `closed_list_uncounted` | nobody states how many terms the closed vocabulary holds | The terms are canon and the count is incidental. Four files carried a number that had been wrong since the file was created — `git show` returns sixteen at every commit that ever touched it. A fact nothing depends on is a fact that only drifts, so the number is deleted rather than corrected. |
| `reserved_species_unspent` | species held in reserve are not spent in an active allocation | *Alphadon* and *Meniscoessus* are on the reserve list and are also the grounders Noli catches. |
| `dated_provenance` | knowledge files carry what is true, not how it got approved | `AGENTS.md` §2: no dates, no "Daniel said", no "struck on". The pattern deliberately does not match the bare name, because *"that is a note for Daniel, not a license"* is instruction, not history. |
| `overt_plant_budget` | the foreshadow ledger carries the number of overt plants it budgets | The budget and the table agree today. It is here as a regression guard, and as the template for the other declared budgets. |

## Not yet built

**Blocked on the rescene.** Every scene id cited anywhere resolves to a scene in `scene-list.md`; every scene's day tag matches the calendar row for its content; every `[requires]` pointer resolves. Scene numbers are about to be reassigned, so building these now buys a suite that goes red for the right reason at the wrong time.

**Blocked on prose.** The blacklist and word-choice rules, the sentence-distribution targets in `prompts/style-canon.md` §0, the repetition window, and the allocation-against-prose check — one search key per allocated item, flagging any use outside its day. That last one is the repetition instrument `milieu-allocation.md` exists to be, and it stays deterministic.

**Blocked on nothing but time.** `milieu-allocation.md` §3 and §5 must agree on every day number; every day is covered by exactly one biome band; the motif budgets against their own tables; every character's physical attributes stated in one place only.

## The lens tier

Not built. When it is: `@pytest.mark.llm`, deselected by default, because if the fast loop stops being instant it stops being run. Results cached by a hash of the input so a typical pass re-checks only what changed. Cheap seats do extraction, frontier does judgment, and every finding gets one short refutation call to a **different model family** before it reaches Daniel — agreement inside one family is weak evidence, and four agents on 2026-09-11 returned roughly fifteen findings of which several were already known and one was wrong.

Prefer the `panel` wrapper over bare `llm` for OpenRouter seats: the seats are reasoning models, several stall past the default timeout on multi-kilobyte prompts, and `panel.conf` already pins the per-seat timeouts that fix it. Pass low reasoning effort for extraction work, and check `finish_reason` before trusting any sweep — a seat that runs out of output tokens exits zero with a body truncated mid-thought.
