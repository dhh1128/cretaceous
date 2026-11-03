---
approval: unapproved
---

# Trim and truth pass, one scene (SCENE)

You are revising one drafted scene of *Cretaceous*, a YA survival novel in strict third-person limited. Repo: `/home/daniel/code/me/cretaceous`. Read-only on the repo: you write only the two output files named below.

## Read first

- The scene's approved map: */home/daniel/code/me/cretaceous/plan/scene-maps/SCENE.md*. It says what must happen. Every move, and every line the map quotes, must survive.
- `/home/daniel/code/me/cretaceous/prompts/ai-tells-blacklist.md` §33, §34 and §35 in full, and skim the rest.
- `/home/daniel/code/me/cretaceous/plan/voice-sheets.md` for Teva, Keo and Benal.
- the scene before this one in `/home/daniel/code/me/cretaceous/content/` (so you know what the reader already has) and `/home/daniel/code/me/cretaceous/content/D11.1.md` and `D11.2.md` (both edited by the author; they are the target register).

## The pass

Go sentence by sentence and line by line. Apply every change as an edit, not a suggestion. Do not add material (`prompts/ai-tells-blacklist.md` §33) except the minimum words to repair a sentence a cut broke, or to replace a false line with a true one.

**Trim (§33, §34):** cut the sentence the reader already has (the scene shows it, another sentence in the paragraph says it, an earlier scene said it, or it is a non-event); cut action slowed by explanation (explained perception, the announcing paragraph, saying it twice louder, decoration inside action, stock aftermath, location tails). There is no word floor: a scene may end well under its band.

**Truth, the lessons of the author's edit to D11.2:**
- A voice tic that makes a false claim goes. A hedge ("roughly", "possibly", "I think") is cut when it hedges something the speaker knows exactly; a joke-shaped line is cut when what it says is not true in the world.
- Every evaluation needs its referent on the page. "That was funny" needs the thing that was funny to be plain.
- A claim needs a source. If a character asserts something, they must be able to know it. They carry a pedometer and suit sensors; "you can't trust distances out here" would be false.
- Friends answer rather than dodge. A line that deflects where a friend in this situation would simply answer is changed to the answer, or cut.
- Dialogue is checked against what each speaker knows at this moment (canon, and the scenes before) and what they would say aloud in this state (their state in the map's BODY and RELATIONS lines).
- An action needs its purpose on the page. If a character stops to do something (gather, build, pick up, take apart), the reader must know why from the POV before or as it happens. Daniel, of D13.2's beetles: "why would Benal stop to pick up beetles? For his collection? Makes no sense at all." They were food, and nothing said so.
- The last line (`prompts/ai-tells-blacklist.md` §36): if the scene ends on danger, a question or a loss, cut any closing line that reassures, answers, or lets the reader stop comfortably.
- Watch word echoes: the same noticeable word twice within a few lines, unless the repetition is deliberate.
- Protect repeated images that pay off. Before cutting a second mention of something, check whether the scene or a later one builds on it. The author restored "empty hands" after an earlier pass cut it.

**Settled premises are not reopened.** If something seems physically wrong, check `plan/milieu-brief.md` for a `settled: true` premise before flagging it; a settled premise is never a finding.

## Output

1. The revised scene, with the frontmatter unchanged, to *OUT_SCENE*.
2. A log to `OUT_LOG`: first a line `words before: N, after: M, removed: R (P%)`; then a table with one row per change: the original text, the new text (or "cut"), the category (§33, §34, truth, echo, repair), and a few words of reason. Last, a count of changes per category.

Count words on the body only (exclude frontmatter), with `sed '1,/^---$/{/^---$/!d};1,3d' FILE | wc -w` or equivalent; state which method you used.
