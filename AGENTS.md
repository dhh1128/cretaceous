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
approval: approved 2026-09-10
---
```

Three values, and nothing else. `approved <date>` — Daniel said yes to these contents on that date. `provisional <date>` — he accepted it weakly, live enough to build on and cheap to revisit. `unapproved` — nobody asked, or he has not answered. **`unapproved` is the default and needs no date.**

**The date is load-bearing.** Approval is a property of contents at a moment, not of a filename. A file whose last commit postdates its approval date has changed since he looked at it, and that is one command to detect:

```
for f in $(git ls-files '*.md'); do
  a=$(sed -n '2s/approval: [a-z]* //p' "$f")
  [ -n "$a" ] && [ "$(git log -1 --format=%ad --date=short -- "$f")" \> "$a" ] && echo "STALE: $f"
done
grep -L 'approval:' $(git ls-files '*.md')   # unmarked files
```

**Sub-file granularity is one token: `[?]`.** It goes at the front of whatever it marks — a paragraph, a bullet, a table cell — and means *this specific thing is not covered by the file's approval*. `[~]` for provisional-within-approved. Anything unmarked inherits the frontmatter, so an approved file reads clean and only the exceptions carry ink.

**The invariant you maintain, and it is the whole point:**

> **Every assertion in the corpus is either covered by an approved file marker or carries `[?]`.**

So when you add something to an approved file, you mark it `[?]` — unless you are enacting a ruling Daniel just made, in which case it is his and needs no mark. A reader can then tell at every line whether they are standing on his ground or an AI's, and anything a session invents is visible instead of silent.

**Approval history does not go in knowledge files.** No dates, no "Daniel said", no "struck on". Those files carry *what is true*, in whatever state it is in; git carries how it got there. The one exception is where a constraint exists specifically to stop a known error being re-made — then state it as a standing prohibition (*"this is not a culture of telepaths; do not extend the proximity sense"*), never as a dated event. `process/methodology-theory.md` keeps its post-mortems, because history is that file's subject.

## 3. How to ask him things

**His attention is the scarce resource in this project**, and the process is measured on it — see `process/methodology-theory.md` §11. Three numbers per scene: invention-ledger items put to him, words he had to read, words he had to write. The baseline is deliberately terrible: scene 2.3, zero ledger items, ~8,600 words read, thousands written, and the output unusable.

- **Propose, don't ask.** An open question makes him do the work. A proposal lets him scan and object, which is an order of magnitude cheaper. Every proposal should be answerable in a few words.
- **One or two questions at a time, in dependency order** — the one whose answer implies the most about the others first. A list of twenty questions makes him answer ones that later answers would have settled.
- **Deciding *not* to specify something is not a question.** It needs his approval only when the omission has a consequence somebody could get wrong. Everything else you decide and record.
- **Never be elliptical.** If you write "the paralysis is spatial," say what paralysis and what you mean by spatial. Compression that costs him a round-trip is not economy.
- **Say what you need from him at the top**, before the reasoning that led there.

## 4. How to deliver prose

The procedure is `process/scene-build-runbook.md`. Two things in it are load-bearing and both have been violated:

**The map is approved before any prose exists.** Phase 4 is a hard stop — the forward map plus the invention ledger go to him together, and you wait. Objecting to a beat costs him a sentence; objecting to the drafted version of the same beat costs him a paragraph and you a rewrite. *(Skipped on 2026-09-10, which is why `content/01.1.md` exists ahead of an unapproved map.)*

**Nothing reaches him that has not passed the mechanical checks.** The blacklist, the logic checker, the repetition hawk, the four invariants, and the invention audit. Spending his attention on defects a checklist catches is the most expensive mistake available here.

**Measure the sentence distribution every time.** `prompts/ai-tells-blacklist.md` used to say rhythm was not the problem and not to spend effort there. That was true of four particular drafts and false in general: the first draft of scene 1.1 came out at 42.4% sentences of five words or fewer against Daniel's 25.7%, from a session that had read the exemption and believed it. Targets are in `prompts/style-canon.md` §0.

## 5. House conventions

- **US English, everywhere** — prose, notes, ledgers, commit messages, chat. This has been corrected more than once and it keeps coming back, because a literary register pulls toward British spellings. Grep before delivering: `grep -InE '\b(colour|centre|realise|organise|recognise|behaviour|favour|defence|grey|whilst|analyse|metre|artefact|fibre|offence|practise|learnt|travelled|modelling|labelled|summarise|kilometre|neighbour|labour|travelled|towards)\b'`
- **Never hard-wrap markdown.** One line per paragraph, however long.
- **Where things go.** Scene maps and invention ledgers in `plan/scene-maps/`. Drafted prose in `content/`. Working analyses that outlive a session but are not canon in `.ignored/`, which is gitignored. Do not leave loose untracked files in the repo root.
- **Do not invent organizing schemes.** Ask before adding a folder or a naming convention. *(A `process/` directory was created on 2026-09-10 without being asked for.)*
- **`kb/worldbuilding/lingo.md` is a closed list of fifteen words.** Coining colony vocabulary during drafting is a defect, not a flourish. If a scene seems to need a word that is not there, that is a note for Daniel.

## 6. Standing hazards, learned the expensive way

**Preferences inflate into laws.** Something he said once in passing comes back as *never*, *not one, not ever*, *one per act*. The content is usually fine and the modality is invented — and a model obeys grammar, so a quota gets spent against like a budget. The test: does the rule cite something? His critique, a measurement against his own novels, a physical fact? If yes it keeps its force. If not it is a guideline, and should read like one.

**Summary files generate contradictions and nothing else.** Six have been deleted. The clearest case opened by conceding that it loses every disagreement with the file it summarized. A file that restates another file will drift from it, and then a drafter picks whichever it read last. Point at the authority instead.

**The corpus is full of decisions nobody made.** Yesterday's rewrites bundled real decisions of his with large numbers of unrequested changes, and the real decisions made the commits look legitimate. Examples found in one day: an exact population replacing a deliberate vagueness, accents stripped from every name in the name file, a calendar arguing against a season pivot and then scheduling one three times, a character's dead sibling changing cause of death.

**The novel is strict third-person limited, and that constrains what a scene can pay.** The reader receives exactly what the POV character receives. Irony works by the POV character *misreading shared information*, never by the reader getting extra information. A planning layer that assigns the reader a payment a POV cannot deliver is a defect — one did, at scene 1.1, and it took Daniel to notice.

**Read the whole file before matching a neighbor.** Two artifacts can share a naming pattern and be different kinds of thing, and most of what looks like convention here is a previous session's arbitrary choice.
