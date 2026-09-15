---
approval: unapproved
---

# Working on Cretaceous

**Read `README.md` first** — what the novel is, what is in each folder, and which files have been approved. This file is the part that is only about how to work here.

Daniel is the author. You are not. Everything below follows from that.

---

## 1. The rule that governs everything

**Nothing enters this novel that Daniel did not approve.** When a scene needs something the world does not supply, put it to him as a proposal. Do not reach for what the genre supplies by default. His words, 2026-09-10: *"Not now, not ever, can you just pull old and tired tropes from trashy sci fi and use them to fill in gaps in my novel. What goes in is what I say goes in, not what you make up."*

**What counts as approval is narrow, and it is not what you would guess:** *"Commits aren't evidence of my work, because commits have been made by AI. What is evidence of me is a question that you directly ask me, that I directly approve."*

So:

- **A citation to a canon file proves nothing.** For most of 2026-09-10 the milieu brief asserted the colony shared a village-wide telepathic web. It had a heading, three numbered consequences, and citations in five files. It had grown out of one atmospheric sentence a drafting model wrote in a scene, which a later pass promoted to a rule. Daniel had never heard of it.
- **`git log -S '<phrase>'` runs one way only.** If a thing first appears in `content/*.md` it is generated scene prose, which is strong evidence it was invented rather than decided. It can never prove the converse — he reviewed the first few scenes line by line in November, so plenty of material that originated there is genuinely his.
- **The only test that works is whether he recognizes it.** Archaeology builds the list to show him. It does not clear or condemn anything by itself.
- **The approval state is in the files themselves.** See §2. Nothing outside the repo is needed to read it.

## 2. How approval is recorded

**Every markdown file carries one line of frontmatter:**

```
---
approval: approved 3f9c1a2b
---
```

Three values, and nothing else. `approved <hash>` — Daniel said yes to exactly these contents. `provisional <hash>` — he accepted them weakly, live enough to build on and cheap to revisit. `unapproved` — nobody asked, or he has not answered. **`unapproved` is the default and carries no hash.**

**The hash is eight hex characters over the file's body, ignoring the frontmatter, and no human writes it.** `python3 tools/approve.py <file>` stamps it. A file whose body no longer hashes to its marker has changed since he read it, and that is a comparison rather than an argument:

```
python3 tools/approve.py --list                  # every marker, and what is stale
uv run --with pytest pytest tools/ -k approved   # the same thing, as a test
```

**Why not a date.** A date has day granularity, and this project works in bursts inside a day: the corpus was written, approved and committed between one morning and one midnight, so a date-based check reported perfectly clean while eleven approved files had been edited after the commit that approved them. A date also has to be typed and bumped by hand, which is work that buys nothing. And a bare `approved` with no date at all cannot express re-approval, because approved-to-approved is a no-op that git cannot see. A hash fixes all three: exact, machine-written, and it notices uncommitted edits, which nothing based on commit history can.

**Sub-file granularity is one token: `[?]`.** It goes at the front of whatever it marks — a paragraph, a bullet, a table cell — and means *this specific thing is not covered by the file's approval*. `[~]` for provisional-within-approved. Anything unmarked inherits the frontmatter, so an approved file reads clean and only the exceptions carry ink.

**The invariant you maintain, and it is the whole point:**

> **Every assertion in the corpus is either covered by an approved file marker or carries `[?]`.**

So when you add something to an approved file, you mark it `[?]` — unless you are enacting a ruling Daniel just made, in which case it is his and needs no mark. A reader can then tell at every line whether they are standing on his ground or an AI's, and anything a session invents is visible instead of silent.

**Approval history does not go in knowledge files.** No dates, no "Daniel said", no "struck on". Those files carry *what is true*, in whatever state it is in; git carries how it got there. The one exception is where a constraint exists specifically to stop a known error being re-made — then state it as a standing prohibition (*"this is not a culture of telepaths; do not extend the proximity sense"*), never as a dated event. `process/methodology-theory.md` keeps its post-mortems, because history is that file's subject.

## 3. How to ask him things

**His attention is the scarce resource in this project**, and the process is measured on it — see `process/methodology-theory.md` §11. Three numbers per scene: invention-ledger items put to him, words he had to read, words he had to write. The baseline is deliberately terrible: scene D2.3, zero ledger items, ~8,600 words read, thousands written, and the output unusable.

- **Propose, don't ask.** An open question makes him do the work. A proposal lets him scan and object, which is an order of magnitude cheaper. Every proposal should be answerable in a few words.
- **One or two questions at a time, in dependency order** — the one whose answer implies the most about the others first. A list of twenty questions makes him answer ones that later answers would have settled.
- **Deciding *not* to specify something is not a question.** It needs his approval only when the omission has a consequence somebody could get wrong. Everything else you decide and record.
- **Never be elliptical.** If you write "the paralysis is spatial," say what paralysis and what you mean by spatial. Compression that costs him a round-trip is not economy.
- **Say what you need from him at the top**, before the reasoning that led there.

## 4. How to deliver prose

The procedure is `process/scene-build-runbook.md`. Two things in it are load-bearing and both have been violated:

**The map is approved before any prose exists.** Phase 4 is a hard stop — the forward map plus the invention ledger go to him together, and you wait. Objecting to a move costs him a sentence; objecting to the drafted version of the same move costs him a paragraph and you a rewrite. *(This has been skipped once, and the prose written out of order was discarded — which is the cheapest possible outcome and not one to rely on.)*

**Nothing reaches him that has not passed the mechanical checks.** The blacklist, the logic checker, the repetition hawk, the four invariants, and the invention audit. Spending his attention on defects a checklist catches is the most expensive mistake available here.

**Measure the sentence distribution every time, and measure it separately for dialogue and for narration.** `prompts/ai-tells-blacklist.md` used to say rhythm was not the problem and not to spend effort there. That was true of four particular drafts and false in general: the first draft of scene D1.1 came out at 42.4% sentences of five words or fewer, from a session that had read the exemption and believed it. Targets are in `prompts/style-canon.md` §0.

**The comparison that finding was made against was wrong, and the corrected version is worth more.** 42.4% was read as fifteen points above a book-level norm of 25.7%, which sounds like a vague rhythm problem. It is not one. Daniel's dialogue runs about 41% short sentences and his narration about 19–22% once speech-attribution fragments are set aside, so the book-level figure is mostly a fact about his dialogue-to-narration ratio. That draft was writing **narration at his dialogue rate**, which is a specific defect with a specific fix.

**The general lesson, and it applies past sentence length: a blended statistic can be hit exactly by prose that is wrong in both halves.** The two novels appeared to agree on mean sentence length to two decimal places, which looked like a fingerprint and was an accident — cordimancy attributes speech three and a half times as often as viking, and those fragments manufacture enough two-word narration sentences to drag its blend onto viking's. Segmented, the books differ. Any measurement that mixes dialogue with narration, or one scene's job with another's, should be assumed to be hiding its own opposite until it has been split.

## 5. House conventions

- **US English, everywhere** — prose, notes, ledgers, commit messages, chat. This has been corrected more than once and it keeps coming back, because a literary register pulls toward British spellings. The list is `tools/british-english.txt`, 1,818 British→American pairs, and `uv run --with pytest pytest tools/ -k english` checks prose and filenames against it. A word that only looks British — *tonne* as a unit, *dialogue*, *monologue*, *archaeology* — goes in that file as an exception with its reason. The `-logue` family is not uniform: *dialogue* and *monologue* are US-standard, *catalog* and *analog* are not. Verbatim quotations are exempt: correcting one would falsify the source.
- **Never hard-wrap markdown.** One line per paragraph, however long.
- **Where things go.** Scene maps and invention ledgers in `plan/scene-maps/` (created when the first one is built; the directory is empty). Drafted prose in `content/`. Working analyses that outlive a session but are not canon in `.ignored/`, which is gitignored. Do not leave loose untracked files in the repo root.
- **Do not invent organizing schemes.** Ask before adding a folder or a naming convention. *(A `process/` directory was created on 2026-09-10 without being asked for.)*
- **`kb/worldbuilding/lingo.md` is a closed list, and it is closed.** <!-- @WF-lingo.closed: true --> Coining colony vocabulary during drafting is a defect, not a flourish. If a scene seems to need a word that is not there, that is a note for Daniel.

## 7. Retired claims — things the corpus said and no longer may

**When Daniel rules something out, the ruling has to outlive the session that got it.** This is the one place §2's no-history rule is deliberately inverted, under the exception §2 already carves: a constraint that exists to stop a known error being re-made is stated as a standing prohibition. The suite reads this table and fails on any of these phrases appearing in a tracked file.

**Why it exists.** On 2026-09-12 five rulings made that same day were still contradicted in live plan files hours later, two of them in files the session believed it had already fixed. Applying a ruling by hand means finding every instance by memory, and memory is exactly what fails across a corpus of twenty-five files. **A prohibition is checkable; an intention is not.**

| phrase | what is true instead |
|---|---|
| `noble lie` | The corruption was **drift, not deceit**. The duty is a genuine founder instruction and the Traditionalists are right about it; what drifted is the belief that the *apparatus* enforcing it came from the founders. Teva reads it as a lie and that reading is the emotional truth and is wrong — the distance her arc travels. `kb/worldbuilding/the-second-jump.md` |
| `no stable shelter` | Genesis is a **built research station** and much of it still stands. The mission's purpose was laboratory work, so they arrived with structures good enough to culture in. They left over water, food and the disorientation. `plan/milieu-brief.md` §3 |
| `colony invention, not a founder` | The **duty** is a founder instruction; the **apparatus** is the colony's extension of it into a situation nobody wrote rules for. `plan/milieu-brief.md` §6 |
| `four micrometer` | The croc reads **disturbance on the water's surface**, not vibration through the ground. Leitch and Catania measured a probe indenting *modern* crocodilian skin — a local touch threshold, not ground displacement, not an extinct animal. `plan/tech-rules.md` |
| `Deinosuchus` | **Campanian, and extinct some seven million years before this story opens.** The animal stays, at six meters, and is deliberately not placed to genus. `kb/research/geo-flora-fauna.md` §4.4 |
| `67mya jump` | The second jump is **a thousand years**. 67 Mya is where the Enclave emigrates at the end of book 3 — a different jump. `plan/sequels.md` |
| `telepath` | **This is not a culture of telepaths.** The proximity sense is not to be extended. |

**Retired scene addresses.** Scene ids are **`D<day>.<n>`** and always have been since the renumber. The outline-unit form is dead, and the suite fails on any of these appearing in a tracked file: `1.1`, `1.2`, `2.1`, `2.2`, `2.3`, `2.4`, `2.5`, `3.1`, `3.2`, `3.3`, `3.4`, `4.1`, `4.2`, `4.3`, `5.1`, `6.1`, `6.2`, `6.3`, `6.4`, `6.5`, `6.6`, `7.1`, `7.2`, `7.3`, `8.1`, `8.2`, `8.3`, `8.4`, `9.1`, `9.2`, `9.3`, `9.4`, `10.1`, `11.1`, `12.1`, `13.1`, `14.1`, `15.1`. `no_legacy_addresses` reads that list from this sentence. **It is listed rather than described because a range would be wrong** — `11.2` and `2.8` look like addresses and are a sentence-length mean and a percentage, and a check that flagged them would be crying wolf about the two most common kinds of number in this corpus. Four of these kept their digits across the move, so `2.3` became `D2.3`: a stale one does not read as broken, it reads as almost right, which is why the prohibition is permanent rather than a one-off sweep.

**Three exemptions, and they are narrow.** `AGENTS.md` itself, since the table has to name what it forbids. `content/superseded/` and `content/rejected/`, because those are the record of what was actually drafted and editing them destroys the evidence they are kept for. And **any single line carrying the token `[retired]`**, which is how a file cites a retired claim in order to correct it — the escape is per line and visible in a grep, so nobody can quietly exempt a paragraph.

**Adding to this table is part of applying a ruling, not a follow-up to it.** A ruling that retires a phrase and does not land here will be re-made.

## 6. Standing hazards, learned the expensive way

**Preferences inflate into laws.** Something he said once in passing comes back as *never*, *not one, not ever*, *one per act*. The content is usually fine and the modality is invented — and a model obeys grammar, so a quota gets spent against like a budget. The test: does the rule cite something? His critique, a measurement against his own novels, a physical fact? If yes it keeps its force. If not it is a guideline, and should read like one.

**Summary files generate contradictions and nothing else.** Six have been deleted. The clearest case opened by conceding that it loses every disagreement with the file it summarized. A file that restates another file will drift from it, and then a drafter picks whichever it read last. Point at the authority instead.

**The corpus is full of decisions nobody made.** Yesterday's rewrites bundled real decisions of his with large numbers of unrequested changes, and the real decisions made the commits look legitimate. Examples found in one day: an exact population replacing a deliberate vagueness, accents stripped from every name in the name file, a calendar arguing against a season pivot and then scheduling one three times, a character's dead sibling changing cause of death.

**The novel is strict third-person limited, and that constrains what a scene can pay.** The reader receives exactly what the POV character receives. Irony works by the POV character *misreading shared information*, never by the reader getting extra information. A planning layer that assigns the reader a payment a POV cannot deliver is a defect — one did, at scene D1.1, and it took Daniel to notice.

**Read the whole file before matching a neighbor.** Two artifacts can share a naming pattern and be different kinds of thing, and most of what looks like convention here is a previous session's arbitrary choice.
