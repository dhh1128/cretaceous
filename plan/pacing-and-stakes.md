---
approval: unapproved
---

# Pacing and the four stake ladders

Sets scene count, scene sizing, chapters, and the four stakes curves — which are one problem, because the ladders are what tell you where scenes are needed.

**Indexed by day.** Scene numbers are being reassigned and the fifteen-unit outline structure is retiring as an address system; the nineteen days in `journey-calendar.md` are stable and are what everything here hangs on.

---

## 1. Where we are

**The rescene is in progress and this section is the record of where it has got to.** Days 6, 7, 8, 9, 15, 16, 17, 18 and the Genesis half of 19 are rebuilt, in the Act 1 format, with ladders and hazards. `python3 tools/report.py scenes_per_day` prints what is left at any moment and is more current than this paragraph.

**Nothing is short.** Every day holds the number §5 asks for, and `uv run --with pytest pytest tools/ -k scenes_per_day` is the live answer rather than this sentence.

**Days 12 and 13 are the ones that need a conversation rather than a pass.** They are the mash and the hinge of Teva's arc, and the canon for them is unusually rich: `plan/outline.md`, `plan/character-arcs.md` and `plan/body-and-resources.md` between them already fix the decision, the physiology, the sleep debt and the reversal where Keo carries the person who carried him.

## 2. Why Act 1 went from ten scenes to fourteen

Two organs were missing, and both are now scened. Recorded because the reasoning generalizes.

**Keo's parents never spoke to him on the page.** He was with Noli, then he saw Joram across a crowded chamber, then he robbed them while they slept. The parent-nuance arc — the novel's stated subject — rested on two adults who never had a conversation with their son, so there was nothing to plant the misjudgment with. Scene D2.3 exists for this. @D2.3

**Omya never spoke to Teva.** The grandmother was already failing when we met her, so the reader never met the woman whose disappearance drives the protagonist, and the Day 15 confession — *"I left her while she's disappearing"* — had nothing behind it. Scene D2.4 exists for this. @D2.4

**The generalization: a relationship the book asks the reader to revise must be dramatized before the revision.** Wherever an arc turns on someone being misjudged, check that they have been *present* first.

## 3. Chapters, scenes, and moves

**A chapter is the reader-facing unit — what they finish before putting the book down. A scene is the writing unit.** One chapter holds one or two scenes; a chapter is rarely three.

At the count §5 proposes that implies **roughly 40 to 50 chapters**, which for a YA thriller of this length puts a chapter at about 2,000 words. That is the right size for the form and it is what the reader is actually pacing themselves against.

**Both novels break scenes inside a chapter**, by different marks. **viking** uses `§` — 39 across 55 chapters. **cordimancy** uses an extra blank line. *(Do not try to verify the second by counting: a blank-line convention does not survive export, and `cordimancy.md` retains three whitespace-only lines in the whole book. An earlier version of this section counted that and concluded the novel had no internal breaks, which is wrong.)*

**cordimancy also labels every chapter**, in an italic line of the form `*subject ~ POV*` — *the antechild ~ Malena, a decade later*. The subject phrase is always a concrete object or event, never a theme, and the time element rides in the same line, so the label absorbs the transition instead of a bridging paragraph doing it.

### Decided: take both

**Chapters carry a cordimancy-style label naming the POV and the day. Scenes inside a chapter are separated by viking's `§`.**

```
*the Vitarium ~ Teva, Day 1*
```

The label earns its place twice over here. This is a **rotating three-POV novel**, so the reader learns whose head they are in before the first sentence rather than four lines down.

**No more than five consecutive scenes in one POV.**

**Five rather than three, and the difference is a measurement.** Across Daniel's two novels the rotation is not mechanical: `viking` never stays in one head for three consecutive chapters in fifty-five, while `cordimancy` runs strict alternation for eleven chapters, brings a third POV in at twelve, and then holds one head for five. Three would be `viking`'s practice imposed on a book that is structurally closer to neither. Five is the wider of the two and it still binds — the list currently runs 38 single scenes, nine pairs, one triple and one run of five, and that five is Act 1's theft sequence, which sits exactly at the line and is the kind of deliberate long hold the ceiling exists to permit rather than punish.

**The ceiling is not a target and the mean is not the measurement.** A book that alternated perfectly would satisfy any ceiling and read like a metronome; what the number is for is catching the run nobody chose. The one it caught on its first pass was six — Benal from the drag-frame through the mosasaur to the coral bank — assembled from two decisions that were each right on their own and never looked at together. And it is a **nineteen-day journey with days that will be skipped**, so a label reading *Day 13* does the work a paragraph of *two days on* would otherwise have to.

**And the `§` carries the transition, which means the first clause after it does the time-skip inside itself.** No "meanwhile." No standalone "later that day." That rule is the one that makes the mark worth having, and `prompts/style-canon.md` §3 has the passages.

The cost, accepted: this is a visible formal device and not a YA-thriller convention.

## 4. Scene sizing

Page-turning is not a function of short scenes. It comes from three things.

**Scene endings are governed by §8, not by a rule stated here.** <!-- @WF-hook.rule: distribution --> This section used to say *every scene ends on a hook — a question, a turn, or a threat; no scene closes on summary or on a settled feeling*, and called it the largest lever available at no cost. It is not free and it is not what the two novels do: a quarter of their chapters close with no forward pull at all, and which ones do is predicted by what the chapter was for. §8 has the conditional form and the distribution that replaces the absolute.

**Length runs inversely to tension.** Short scenes at crisis points, because the white space between them is where dread does its work; longer scenes for consolidation and world, where the reader wants to stay. Never two consecutive scenes of the same shape.

**Richness is a function of scene count, not scene length.** A world feels deep when each scene shows one new true thing — a different hour, weather, biome, ritual — not when one scene shows twenty. More scenes means more distinct places to *be*. Long scenes make a world feel thorough; many scenes make it feel large.

| size | words | use |
|---|---|---|
| **short** | 400–900 | a hard cut, a single image, a scene that exists to land one blow |
| **medium** | 1,000–1,600 | the workhorse |
| **long** | 1,800–2,500 | consolidation, revelation, the emotional set-pieces |

**The arithmetic, and it is what ties the scene count to the word count.** A mix of a quarter short, half medium, a quarter long, at the midpoint of each band:

> 17 × 650 + 35 × 1,300 + 17 × 2,150 = **93,000 words**

at the sixty-nine scenes §5 now proposes. **Going long is fine.** Ninety or ninety-five thousand is an acceptable draft, and trimming happens in the post-edit, where it is cheaper and far better informed than planning the book short would be. **So this figure is not a ceiling to design against, and no scene is cut to protect it.** *(At sixty scenes the same mix gave 81,000, and the three river days are most of what moved it. Shifting the mix short — a third short, half medium, the rest long — would put sixty-nine scenes back at 84,000, which is available if a draft runs away rather than a plan. And no estimate here is based on the drafted scenes in `content/superseded/`: they average about 1,058 words, but they are not the book, and their length is a symptom of what they left out rather than a rate to plan against.)*

## 5. Proposed shape — about 70 scenes

`[?]` **Every number in this section and the next is tentative — the scene counts and the ladder values alike, not only the rows added for the new days.** They are an interpolation of a coarser curve that was never put to Daniel. **The rescene is where they get argued**, and arguing them before it would be settling the answer before the question. Read them as a shape, not a specification.

**These tables carry the proposal only.** What the scene list holds today is in §1, and it is not repeated here — there are no approved scene drafts, so a "now" count only names scenes that are themselves about to be questioned, and the column would come out at the end of the rescene anyway.

| act | proposed |
|---|---|
| **1** | 14 — done |
| **2** | ~39 |
| **3** | ~16 |
| | **~69** |

**Act 2, by day.** This is where the template-indexed version of this document was actively misleading: it asked for nine scenes in *Fun and Games*, which spans Days 3 to 10 — a stretch containing the crossing, the constrictor, the only happy day in the novel, and the day the sun nearly kills Teva. Those need different treatment and the old granularity could not say so.

| day | scenes | what it is |
|---|---|---|
| 3 | 4 | out through the tangle, the razortails, the first day outside. The biggest day in the book |
| 4 | 2 | the rain arrives; the walking begins in earnest |
| 5 | 2 | the constrictor |
| **6** | **3** | **the gift.** Fed, dry, laughing. The deposit every later day draws on |
| **7** | **3** | **they come to the water and stop.** Arriving · the plans proposed and discarded on the bank — raft, riding a saropo across, upstream, go home · the night nobody sleeps |
| **8** | **3** | **the crossing.** Driving the hadrosaur while they wait for the afternoon · the water · the far bank, with nobody able to walk |
| **9** | **2** | what it cost and what it bought. Across, and still walking |
| 10 | 3 | the savanna; hubris at its peak; Teva cooking inside her own protection |
| 11 | 6 | Noli, then the fall |
| **12** | **2** | **the mash.** She overrules him and is wrong, which is the hinge of her arc |
| **13** | **2** | it comes due; he carries her; one distant sighting of the thing that never touches them |
| 14 | 3 | the mudflats, the raft, the mosasaur |
| 15 | 4 | the eye, the failing to get in, the tail, and the confessions |

**Act 3, by day.** Genesis is three distinct days and Day 19 is everything else.

| day | scenes | what it is |
|---|---|---|
| 16 | ~3 | getting in · the dry powered section · the protocols found · the first food since the raft |
| 17 | ~3 | the logs of the arrival · the epiphany and FG · the second jump |
| 18 | **3** | no boat, and no route home · Keo finds something to talk to, and two hulls · **the flash that shows a man burying something where Benal was lying yesterday**. Raised from two: the row always named three things, and the capsule is a fourth |
| 19 | **9** | salvaging one wig from two · the capsule · the launch · the chase · the landing on the river · the handover · the confrontation with FB failing · the final image · **and one scene after it, outside, under the sky.** Raised from eight: the row listed nine separate jobs, and the last of them is two — the chamber settles nothing by design, and Teva's turn cannot happen in a cave |

**Discovery and comprehension are different scenes**, and so are the handover and the confrontation. That is the principled reason to split rather than a feeling about length: see the three-ladder rule in §6.

---

## 6. The four ladders

Emotional, Physical, Social, Species — written `EM`, `P`, `S`, `SP`, because `E` collided with the epigraph prefix and `X` with the surprise prefix, and when two things collide on a letter both go to two letters rather than one. Rough 0–10, by day.

*(The per-day values are an interpolation of a coarser curve. Days 4, 5, 6, 12 and 13 previously had no rating of their own, which is how a novel came to have an unscened rest day sitting inside a rising stretch.)*

| day | EM | P | S | SP | what moves |
|---|---|---|---|---|---|
| **1** | 4 | 1 | 2 | 3 | rage ignites; the community fails in public |
| **2** am | 3 | 1 | 3 | 3 | *rest — the deposit* |
| **2** eve | 5 | 2 | 5 | 4 | paralysis made official |
| **2** night | 6 | 4 | **8** | 4 | the theft destroys two families' standing |
| **3** | 6 | 7 | 8 | 4 | out through the tangle, and the razortails. Terrified and elated |
| **4** | 5 | 6 | 6 | 5 | the arithmetic arrives; first open doubt |
| **5** | 6 | 8 | 6 | 5 | the constrictor. Shattered, then welded |
| **6** | **3** | **3** | 5 | 5 | ***the gift.*** *Every ladder drops. This is what makes Day 7 onward cost something* |
| **7** | 7 | **4** | 6 | 5 | they reach the water and cannot enter it. Three kilometers walked and the day spent standing still |
| **8** | 8 | 9 | 7 | 5 | the crossing |
| **9** | **5** | 6 | 6 | 5 | the drop after it. Across, and nothing to feel yet |
| **10** | 6 | 8 | 5 | 5 | hubris at its peak, and she is dying of heat beside him |
| **11** | **9** | 9 | 6 | 5 | Noli, then the fall |
| **12** | 7 | 8 | 7 | 5 | she decides, and is wrong |
| **13** | 7 | 9 | 7 | 6 | it comes due; he carries her |
| **14** | 8 | **10** | 7 | 6 | drowning, the mosasaur, the fieldpack lost |
| **15** | **10** | 5 | 7 | 6 | the confessions; chosen family forged |
| **16** | 7 | 4 | 6 | 7 | out of the water, fed, and still alive. The exhale |
| **17** | 8 | 4 | 8 | **10** | the protocols are real, and then FG |
| **18** | 9 | 5 | 8 | 9 | no way home — and then the machine |
| **19** am | 8 | **10** | 9 | 8 | the chase |
| **19** eve | 9 | 5 | **10** | 9 | the confrontation |
| **19** night | **10** | 3 | 10 | 9 | the parents |

**Act 3 gives each ladder its own summit, in sequence: species on Day 17, physical on Day 19 afternoon, social that evening, emotional that night.** That is the answer to "ratchet and converge," and it is the justification for sixteen scenes — each has a distinct job rather than sharing one.

**Day 6 is a trough on every ladder and that is deliberate.** A curve that only rises exhausts a reader. The one day where nothing is wrong is what makes everything after it land, and it is currently unwritten.

### The diagnosis

**Two ladders are flat through the middle of the book.**

**Social** goes dormant once they leave and does not move again until the confrontation, because the trio walks away from everyone who could raise it. Act 2 then runs on physical stakes almost alone, which is how an eleven-day walk reads as walking with monsters attached.

**Species barely moves anywhere** — 3, 3, 4, 4, 4, then nine consecutive rows at 5, then 6, 6, 6, 7, then 10 at the revelation. Nine rows without a move, and adding the river days made that stretch longer rather than shorter. It is the ladder Daniel most wants the reader to feel, and it is abstract, and abstractions do not climb on their own.

### The fixes

**Social, in Act 2: the ladder is intra-trio standing.** Who leads, who is trusted, who is carried, who is a liability. It is already in the plan as "skills clash" and needs only to be tracked as a stake rather than a theme — `character-arcs.md` §3 has the dyad temperatures by day and they are the instrument. Plus two pressures they can feel without being present for: **compounding guilt**, since what they have done to their families is getting worse while they cannot see it, and the fact that they do not know whether their parents are confined, punished or dead.

**Species, in Act 2: the ladder lives in the epigraph channel.** This is the fix that makes the rest work. **Marisol is dying across the fragments.** Cecilia's messages escalate — her sister is well, then tired in a way she would not have written if she were only tired, then five weeks of nothing, then a message marked UNDELIVERED. The species stakes climb in one channel while the physical stakes climb in the other, and they braid. The reader feels the future dying on a schedule, in a voice they have come to love, while three children walk through a swamp.

**Thirteen fragments now exist** in `content/epigraphs.md`, five of them Cecilia's, with the queue times in the headers doing the escalation wordlessly — *queued 2d, 6d, 14d, 31d, UNDELIVERED, NO ROUTE*. The channel is built; what it needs is placement against the new scene list.

### The rule that governs scene count

**Every scene moves at least one ladder.** A scene that moves none is cut.

**A scene that moves three is probably two scenes.** This is the principled reason to split Day 17 and Day 19 rather than a feeling about length.

**The ladders must not all move together.** If all four climb in every scene the book is monotonous and exhausting. Day 2 morning is a rest on three of four, and Day 6 is a rest on all four, and those two troughs are what make the theft and the midpoint land.

---

## 7. What to do next

**Rescene Acts 2 and 3.** Act 1 is done. Act 2 needs the four missing days most of all — Day 6 because it is the deposit, Day 9 because it is what the river cost, and Days 12 and 13 because they are the hinge of Teva's arc. It also needs the river built out: Days 7 and 8 carry one scene each and the crossing is the courage the book is built on. Act 3 needs roughly to triple.

The rescene is done. What remains of it is the numbering: scenes become **`D<day>.<n>`**, chapters get drawn over them, and the fifteen-unit outline structure stops being an address system. See `README.md`, open work item 5.

---

## 8. Scene purpose, and the ending distribution that follows from it

**Every scene carries one purpose, and the purpose implies a distribution of endings rather than an ending.** The entry names it on one line beside the ladders — `**Purpose:** TRAVERSE · **Ending:** THREAT`. The purpose is what the scene is for; the ending is what the scene map chose. A check then verifies the shape across the book, and never argues with any one scene.

**This exists because the rule it replaces was a preference that had inflated into a law.** <!-- @WF-hook.rule: distribution --> §4 used to require a hook at the end of every scene. Measured against Daniel's two novels, a quarter of chapters close with no forward pull and another eighth hold an emotion open — 37.8% do not hook — and the ones that do not are not scattered. They concentrate in two jobs. A relationship chapter settles 57% of the time. A chapter whose job is a commitment hooks 83% of the time. **The flat rule is a fact about a thriller's mixture of chapter jobs, mistaken for a fact about how he ends chapters**, and obeying it would write the relationship scenes wrong in a specific and predictable direction.

### 8a. The eight purposes

Derived from the two novels rather than imported from a craft manual, and assigned here from what a scene's entry says it is for — its premise line, its must-carry list, and which ladder its own note says moves.

- **PRESSURE** — advance a threat. In a novel whose antagonist is a world, this is the scene where the world's threat is established, measured, or waited on rather than met: the river counted, the night before the crossing, the door closing behind them.
- **CLASH** — a confrontation, attack, escape or rescue executed on the page.
- **DISCOVER** — deliver information or a revelation.
- **TRAVERSE** — move them through space or through a physical ordeal; the journey or the survival *is* the job.
- **BOND** — two characters negotiate their standing with each other.
- **DECIDE** — a character commits to a course, or is forced to choose.
- **CONSOLIDATE** — regroup after a crisis. Count the cost, treat the wounded, grieve, rest.
- **OPEN** and **CLOSE** — establish the premise at the start of the book, or resolve at the end. One scene each.

**Where two jobs compete, take the one that occupies the most words and explains why the scene exists in the plot.** The boundaries that move under a second reader are CLASH against TRAVERSE, and DISCOVER against BOND — the same two the measurement named. Confidence in any single assignment is medium; confidence in the distribution over seventy of them is much higher, which is the whole reason the check is written over the aggregate.

### 8b. The ending taxonomy

Eight kinds, of which the first six pull the reader forward, the seventh holds an emotion open, and the eighth closes without pull.

**QUESTION** — the last sentence is an interrogative. **THREAT** — a declared future action, condition or consequence. **REVEAL** — a fact lands that changes what the reader knows. **RESOLVE** — the POV decides or begins to act; a threshold is crossed. **BLACKOUT** — consciousness, contact or presence is cut. **OMINOUS** — a closing image charged with dread, carrying no new fact. **HELD** — grief, fear, tenderness or exhaustion held open, neither resolved nor advanced. **SETTLED** — a small gesture, a wry note or a summary that closes with no forward pull.

### 8c. The measured table

Pooled across `viking` and `cordimancy`, 111 chapters. **This table is the owner of these figures** — the working file they were measured in is untracked and does not survive a clone, so the numbers live here and the check reads them from here.

| purpose | chapters | hook | held | settled |
|---|---|---|---|---|
| **DECIDE** | 12 | 83.3% | 8.3% | 8.3% |
| **TRAVERSE** | 15 | 80.0% | 13.3% | 6.7% |
| **PRESSURE** | 19 | 78.9% | 0.0% | 21.1% |
| **CLASH** | 17 | 58.8% | 11.8% | 29.4% |
| **DISCOVER** | 22 | 50.0% | 22.7% | 27.3% |
| **BOND** | 14 | 28.6% | 14.3% | 57.1% |
| **CONSOLIDATE** | 6 | 66.7% | 16.7% | 16.7% |
| **OPEN** | 4 | 75.0% | 25.0% | 0.0% |
| **CLOSE** | 2 | 0.0% | 0.0% | 100.0% |

**The single strongest regularity in either novel: eight of twelve DECIDE chapters end on RESOLVE**, and RESOLVE appears in no other purpose more than four times. When the job is a commitment, the commitment is what the last sentence contains.

**And the one that is counterintuitive: CLASH hooks least of the action purposes, at 58.8%.** The violence is not where the hooks are. The plotting and the traveling are.

**The tier claim is more robust than any single row.** DECIDE, TRAVERSE and PRESSURE together hook 80.4% of the time across 46 chapters; BOND and DISCOVER together hook 41.7% across 36. That 39-point gap is four times its own standard error, while the gaps between neighboring rows mostly are not. Where a row and the tier disagree about a scene, the tier is the better guide.

### 8d. How the band is built, and why it is one standard error

A class of *n* scenes at a baseline rate *p* is checked against a band, and **the band has to absorb two independent uncertainties**: the baseline rate is itself an estimate off twelve to twenty-two chapters, and our own *n* scenes are a draw at that rate. They compound as `SE = sqrt(p(1-p) × (1/N + 1/n))`, where `N` is the chapter count in the table above. A band that used only the second term would be pretending the measurement is exact, and its own source says no per-book cell should be quoted as a rate.

**The multiplier is one standard error, and the argument for it is that two standard errors produces bands that cannot fail.** At two, three of the five policed classes have a degenerate edge — TRAVERSE runs to 17.0 of 17, PRESSURE to 10.0 of 10 and CLASH to 8.0 of 8, so none of them can catch the failure this layer exists to prevent, which is a drafting pass reading the old §4 rule and hooking everything. BOND's lower edge falls to 0.0 of 13, so it cannot catch the opposite drift either. At one standard error all five bands are two-sided and all five classes pass on the list as it stands, which is the evidence that the threshold is demanding without being unfair: the check had a real chance of failing and did not.

**The cost, stated rather than hidden:** a one-sigma band admits roughly a one-in-three false alarm per class on a book that genuinely matches the measurement. A class that drifts outside is worth reading, not an automatic error, and the check says which class and by how much rather than only that something is wrong.

**Two floors, for two different reasons.** A class is not policed when the table's own chapter count is too small for the rate to be one its source would defend, and it is not policed when this book gives it so few scenes that almost any assignment satisfies almost any band. The first is a fact about the measurement, the second about this list, and they disqualify different classes: DECIDE fails on scenes at three, while CONSOLIDATE and OPEN and CLOSE fail on chapters. Those four carry a purpose and an ending and are not checked, and the check names them rather than passing them silently.

**The three numbers, in these words**, because a check that chose them in `tools/` would be the suite enforcing a decision nobody made:

> **The band is one standard error. A class is policed at twelve or more chapters and at five or more scenes.**

Spelled as words or as numerals; the check reads either, and reads nothing else, so a paraphrase will not register.

### 8e. The scene against the chapter, which is a real gap and not a rounding error

**The measurement counts chapter endings and this layer applies it to scenes.** A chapter here will hold one or two scenes, so a scene that sits inside a chapter ends at a `§` where the reader does not stop, and the pressure to hook there is genuinely lower than at a chapter break. The two quantities are not the same and no correction between them is available yet, because the chapters have not been drawn.

**What makes the application defensible anyway is that the table conditions on purpose.** The book-level 62.2% is mostly a fact about the mixture of jobs in those two novels and transports badly to any other book; a statement about what a *relationship* unit does at its end is a statement about the craft of relationship units, and transports much better. That is the whole reason the conditional form replaced the flat one.

**When chapters are drawn, re-run the check over chapter-final scenes only.** That is the comparison that actually matches what was measured, and the interior `§` endings become a separate population with no baseline behind them.

### 8f. What the list holds

Seventy scenes: TRAVERSE 17, DISCOVER 14, BOND 13, PRESSURE 10, CLASH 8, DECIDE 3, CONSOLIDATE 3, and one each of OPEN and CLOSE. **Sixty-two of those are policed and eight are not** — DECIDE under the scene floor, CONSOLIDATE and OPEN and CLOSE under the chapter floor. Forty-five hook, twelve hold and thirteen settle — **64.3% against a measured 62.2%**, with every policed class inside its band.

**That is a finding about the scene list rather than about this layer.** Those endings were written under the flat rule in §4, by passes that believed every scene had to hook, and they came out at the conditional shape anyway: BOND at 30.8% against a measured 28.6%, PRESSURE at 80.0% against 78.9%. The two classes that run high are DISCOVER at 64.3% against 50.0% and CLASH at 75.0% against 58.8%, both inside the band and both in the direction the old rule would push. **The instinct in the entries was better than the rule they were written under, and that is the argument for deleting the rule rather than for correcting the entries.**
