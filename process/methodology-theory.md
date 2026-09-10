---
approval: unapproved
---

# Methodology: getting from a plan to prose

*Started 2026-09-10. A living document — updated as evidence arrives, and intended to outlive this novel.*

## 0. What this is, and what it is not

This is a **theory with tests**. It states what we believe about producing long-form fiction from a planned foundation, what evidence supports each belief, and what result would falsify it. It is written to be portable: the second reader is whoever runs this on *The Clanless* or on a Cretaceous sequel, and the claims are stated so that they can fail there.

It is **not** a production plan for Cretaceous. That is `scene-build-runbook.md`, which has phases and a procedure. The relationship is that this file holds the claims and that file is one instantiation of them for one book. Where they disagree, this file records the disagreement and the evidence; it does not silently overrule.

Every claim below carries a status:

- **Supported** — tested, replicated, and I would act on it.
- **Provisional** — tested once, plausible, not replicated.
- **Untested** — believed, with reasons, no evidence.
- **Withdrawn** — was believed, now falsified. Kept, because the corpse is the most useful part of a methodology and the easiest to lose.

## 1. The problem

A novel of this kind gets planned in layers: plot, scene list, character arcs, milieu, humour, foreshadowing, knowledge, pacing, voice. Cretaceous has fourteen such files against roughly 10,000 words of prose.

Each layer allocates something *per scene*. None of them can say **where inside the scene** it goes, and the ordering is often the whole difference between a plant and an infodump. So at drafting time the writer opens eight files and hopes.

**The missing artifact is a join: a per-scene structure where every layer's allocation gets bound to a position in time.** Everything else here follows from that.

Independent support: an adversarial review of the fourteen layers by a non-Claude model, run without sight of any of this work, returned as its headline absence — *"No file says which file wins… The scene brief is the missing layer where the thirty dimensions were supposed to be assembled."* Constructive support: the first forward map ever written (scene 2.3) immediately showed that two layers were specifying the same move and neither knew — `foreshadow-and-motif.md`'s four water gourds filled for three people, and `scene-list.md`'s "one small thing Riel does that is about her."

## 2. The claims

**C1. Planning layers need a join artifact. — Supported.**
Two independent routes, one destructive and one constructive, above.

**C2. Continuity is checkable from structure alone, without reading prose. — Provisional.**
If each scene map states an entry state and an exit delta, then *exit state of scene N must equal entry state of scene N+1* is mechanical. Blind maps did surface real defects this way: one flagged that ~20% of a scene is description that is never used, and that a scene's stated emotional target has "no move that alters it." Not yet run as a full-novel sweep.

**C3. If state is explicit, drafting need not be sequential. — Untested.**
Shingled drafting exists to carry continuity across chunk boundaries by dragging prose context forward. The only thing the overlap transmits is state. Make state explicit and any scene can be drafted from its own map plus its neighbors' state blocks — in any order, in parallel, and re-draftable in isolation. This is the live disagreement with `process-design-v2.md` §7 and the most valuable untested claim here.

**C4. Description and generation are separate properties of a schema field. — Supported.**
`[refused]` — a character declining to answer something on the page — is useless as a descriptive discriminator: its density measures the mapper, not the scene, and it reverses between model lineages. As an *instruction* it is the strongest field tested. Three writers from three model families, given a move reading `Neither man answers. [refused]`, all produced the refusal, none explained it, and all closed on the same wordless action. **Evaluate every field twice and cut only what fails both.**

**C5. A structure map does not carry duration. — Supported.**
Three writers put a scene's turn on the right move, belonging to the right person, and all three spent a paragraph where the author spent one sentence. Duration is missing at move scale. It is also missing at scene scale: Daniel's account of why a major character's death runs 295 words is that the reader has carried the anticipation for half a novel, and dwelling would dampen it. The map's own format hides this — a move taking one sentence looks identical to a move taking a paragraph — which is why all three expanded and none noticed.

**C6. The reader is a party to the scene and must be tracked like one. — Supported.**
Two independent findings landed here. A forward map produced a scene whose hinge changes no character at all: the reader learns something the POV misses and the parents already knew. And C5's duration finding is unstatable without recording what the reader arrives carrying. `knowledge-ledger.md` has eleven ironic rows — facts the reader holds and the characters do not — and until now recorded acquisition for characters and nothing for the reader.

**C7. A rich brief does not produce mechanical prose. — Provisional.**
This was the main risk against the whole approach: that a map detailed enough to write from degrades drafting into inflating each line into a paragraph. Four drafts, three model families, two scenes: none reproduced the staccato that made the existing Cretaceous drafts unusable, and several landed within noise of the author's own sentence profile. Whatever causes that failure, it is not having a plan.

**C8. Brief grain drives sentence rhythm. — WITHDRAWN.**
Reported 2026-09-09 on a single controlled pair: a coarser map produced 34.0% short sentences against a finer map's 24.2%. **The control was confounded** — the two maps came from different mappers, so grain and map authorship varied together. A larger manipulation (1 move per 100 words against 1 per 24, same scene, same model, same target) produced 21.5% against 19.5%, both on target. Four times the manipulation, one tenth the effect.
*What replaced it:* nothing yet. The staccato remains unexplained. A live successor claim — that **total specification** matters rather than its division into moves — is compatible with all the data and untested. See §7.

**C9. Forward grain and derived grain are different quantities. — Supported.**
Maps derived from finished prose cluster at one move per 27–38 words. A forward map of an unwritten scene came in at one per 100, and not through laziness: a derived map records every move that *happened*, a forward map records every move an author can *decide* before writing. Most of a derived map's content is discovered in the writing. Any rule that sets a move target for briefs from measurements of finished prose is asking briefs to invent structure they have no basis for choosing.

## 3. The pipeline

Four stages. Each answers a different question, and the point of the split is that no stage does two jobs.

```
scene list        intent      why this scene exists; what it must carry
     ↓
forward map       decisions   ~1 move / 100 words · the join table · IN, SPINE, moves, OUT
     ↓
invention ledger  authorize   everything the scene must invent, proposed for a
                              yes/no before any prose exists  ← author checkpoint
     ↓
move sheet        expansion   ~1 move / 25-30 words · invents the undecided moves · structure only
     ↓
prose             voice       one pass, one mind holding the scene at once
```

### The invention ledger (Daniel's design, 2026-09-10)

**The problem it solves is the economics of correction.** Drafting 2.3 cost him 8,600 words of reading and thousands of words of critique to produce 2,000 words of unusable prose — and that ratio is the failure mode this whole project exists to escape. The largest single cause was **unsubstantiated invention**: a drafter with gaps in its brief invented sleeping arrangements, a set of twins, a character's age, where a suit is stored, and the temperature at dawn — and then built further material on top of each invention, so every correction required unwinding a small structure rather than replacing a word.

**Inverting it is cheap.** Before drafting, enumerate everything the scene will have to invent that no canon file substantiates, and put it to the author as a list. Design rules, all learned from what went wrong:

1. **Propose, don't ask.** An open question makes the author do the work. A proposal makes him scan and object, which is an order of magnitude cheaper and is what he asked for.
2. **Mark provenance on every line** — *grounded* (a canon file says it, cite the file) or *invented* (nothing says). Only the invented lines need his attention; the grounded ones are there so he can catch a bad citation.
3. **A few words is the whole budget for an answer.** If a line needs a paragraph to settle, it is a design question and belongs in the scene list, not here.
4. **Write every answer back to canon.** Otherwise the same question is invented again in the next scene, differently. This is the property that makes the ledger shrink: by scene 40 most of what scene 1 had to invent is established, and the pass gets cheaper as the book proceeds.
5. **Unlisted invention is the failure.** The pass is judged on what it failed to *ask about*, not on the quality of its proposals. A drafter that invents something absent from the ledger means the ledger pass was incomplete.

**Claim C10 — a pre-draft invention ledger reduces total author cost per scene. Untested.** Falsifier: run it on one scene and count the author's words in and read in, against the 2.3 baseline of ~8,600 read and thousands written. If the total is not dramatically lower, the stage does not earn its checkpoint.

**The expansion stage is the newest and least established.** Its rationale: somebody must invent the moves that lie between the decided ones — the specific deflection, the gesture, the interruption. Currently that is the drafter, inventing structure and producing sentences simultaneously under a word target. The expansion stage moves that invention somewhere with no obligation to produce a sentence, and makes it reviewable before any prose exists.

Its case does not rest on rhythm (see C8). It rests on what it produced: given a forward map move reading *"Riel fills the gourds, counting aloud. There are four,"* the expansion returned *"Riel stops one gourd at the same marked line as the others"* and, later, *"Riel holds the dipper above the fourth gourd until it empties"* and *"the water line trembles in all four gourds as the nest sways."* Three moves that deepen a plant the plan says must never be remarked on, none decidable at forward-map altitude.

**Drafting stays one pass.** Factoring the *decisions* into layers is the whole method; factoring the *writing* into layers gives committee prose. This is not in dispute.

## 4. The artifact

```
### <id> — <name> — <POV> (<distance>)                  <word budget>

IN     place · time · weather and light
       per character: body, resources, what they know, what they want
       relationship temperatures this scene will touch
       READER: what the reader arrives carrying — promises made, dread
         accumulated, facts held that no character holds
         (COMPUTED from the ledger once scenes are ordered; never authored,
          because an authored one drifts and a drifted one asserts the
          reader knows something they were never told)

SPINE  the one continuous thing the scene hangs on — a hand-task, an
       argument, an approaching threat, a list of objects. May be handed
       off mid-scene; say so if it is. Some scenes have none.

1..n   moves: one move by one party, in order. The world is a party.
       A feeling is not a move.
       types:  [image] [ledger] [spine] [body] [refused] [turn] [opens] [closes]
       turn:   name who it happens to. Often not the speaker. May be a
               silent listener, or READER ONLY.
       links:  [answers N] · [pays <scene>.<move>] · [plants → <scene>]
               [requires <scene>.<move> — what it needs to still be true]
                 written on the DEPENDENT move, and carrying a payload:
                 `[requires 2.3.17 — four gourds filled for three, unremarked]`
                 not `[requires 2.3.17]`. See §5.4.
       duration: mark moves that run long (`~15% of scene`) AND moves that
               must land in a single sentence. Both directions.

OUT    deltas only, against IN
       what changed · what was worked on and did not · what is left open
       what the scene refused to answer
       READER: which ledger rows were paid or contributed to here
```

Cut from an earlier version: `[withheld]`, meaning the narration declines to tell the reader something. It fired once in sixteen blind maps because it asks a mapper to infer intention from an absence. Its work is done by OUT's "left open" and "refused outright" lines, which fired in every map in both lineages.

## 5. Mechanical invariants

Checkable by walking the maps. No prose is read.

1. **State closure.** Exit state of scene N equals entry state of scene N+1. Catches time, weather, injury, inventory, and location drift.
2. **Ledger payment.** Every ironic row in the knowledge ledger is either *delivered* — named in exactly one scene's `OUT — READER` — or *accumulated*, contributed to by several scenes and completed in exactly one named completion scene. Named nowhere means the reader never gets it. Named twice as delivered means the narrative is telling them what they already know.
3. **Scheduled arrivals.** Every `[turn — READER ONLY]` corresponds to a ledger row. Catches a map inventing a payment the ledger does not know it owes.
4. **Dependency symmetry.** Every `[requires]` resolves to a move that still exists, and every `[pays]`/`[plants]` has a matching `[requires]` at the far end. Plants are rarely broken by editing the plant; they are broken by moving or cutting it while working on something else, and a forward-only pointer is invisible from where the damage appears.

   **And every `requires` states what it needs, not just where it lives.** Address resolution catches deletion and movement. It does not catch the failure this corpus has actually suffered: someone edits the source move, it survives at the same address, and now reads *"Riel fills three gourds and mentions a fourth."* The pointer resolves, the check passes, the plant is dead. Every serious continuity failure here has been of that kind with addresses intact throughout — a suit with no faceplate in one file and a visor, regulator and filter in three others; a child two and a half years old in one scene and three weeks in the next; a calendar declaring no season pivot beside its own table naming the last day of the dry season. **Pointer integrity is not semantic integrity.** The payload converts a link check into a contract: the dependent move states what it needs, and anyone editing the source can see what they would break without knowing who depends on them.

   **Corollary — an unresolved `requires` is a work queue.** A move naming a scene that does not exist yet is telling you what has to be written first. Walk the maps, collect the unresolved pointers, and build order falls out of the annotation rather than being chosen. That matters most for a book drafted out of order: a sequence that depends on something unwritten announces itself before anyone drafts it.

## 6. Tests

Each states its question, its method, and what result kills the claim.

**T1 — Falsification by matched pairs.** *Does the artifact discriminate?* Map pairs of scenes matched on function and mismatched on quality, blind. **Run 2026-09-09**, eight scenes, two lineages. Result: it does not discriminate by annotation density, and that measure is withdrawn. It does produce per-scene defect reports regardless of provenance, which is the value that survived.

**T2 — Generative.** *Can a scene be written from a map, and what does the map fail to determine?* Give the same map to writers from different model families; whatever they disagree on is what the map does not carry. **Run 2026-09-09.** Yielded C4, C5 and C7.

**T3 — Expansion stage.** *Does the move sheet earn its existence?* Same scene, same model, same target: draft from the forward map, and draft from an expanded move sheet. **Run 2026-09-10**, partially. Rhythm: indistinguishable, both on target. Content: the expansion invented material the forward map could not specify. **Not yet judged blind by Daniel, which is the judgment that decides the stage.** If the expansion earns nothing, the stage does not exist.

**T4 — State closure sweep.** *Does the continuity invariant catch real defects at novel scale?* Derive maps for every written scene, walk §5.1 across the sequence, compare the defect list against what a human reader or the logic-checker prompt finds independently. **Not run.** Kills C2 if the sweep finds only what a careful read already finds.

**T5 — Parallel drafting.** *Is shingling necessary once state is explicit?* Draft a contiguous run of scenes shingled, and the same run independently from maps plus neighboring state blocks, and grade the seams blind. **Not run.** This is the decisive test for C3 and the one that most changes the production plan.

**T6 — Prospectivity.** *Is a schema field a plan or a review?* For each line of a map, ask whether an author could have decided it before the scene existed. Lines that fail move to an `OBSERVED` block; they belong to the review layer, not the brief. Standing check, applied at every schema change. It has already caught one violation: a note that a paragraph "runs long and unadorned" is an observation about output, and became a word-share budget instead.

## 7. What we do not know

- **What causes the staccato.** 41.6% short sentences in the existing drafts against ~26% in the target. Not underspecification (C8). The live hypothesis is total specification rather than move count, untested.
- **Whether the expansion stage survives blind judgment** (T3).
- **Whether shingling is necessary** (T5, C3).
- **Whether move density has any regularity at all.** It is not measurable in absolute terms — two mappers under identical instructions on identical text differ by ~30%. It may be measurable as a within-author ratio; the one measurement showed an author varying density across scenes by ~2.85× and generated prose by 1.2–1.7×, carried almost entirely by a single pair.
- **How to verify an accumulated ledger payment.** A delivered row is checkable — one move, one scene. "The reader now has enough to have revised" is a judgment, and the completion-scene mechanism makes it *locatable* without making it *verifiable*.

## 8. Standing hazards

Failure modes this project has actually hit. Each cost real work.

**Same-producer rule.** When a test varies one property of an artifact, both conditions must come from the same producer. Violated 2026-09-09: a grain control drew its two maps from different mappers, so grain and authorship varied together, and a false causal claim reached a collaborator who acted on it. The blind round had been built specifically to defeat this class of error, in the same session.

**Unblinded evaluation.** Whoever knows which artifact is which will write a richer analysis of the one they expect to be better, without intending to and without being able to detect it. Blind, or do not run the test.

**Deriving method from the thing you are replacing.** The first version of this schema was built from the planning stack that produced the drafts being demoted. It inherited their assumptions. The second was built by mapping a scene from the author's own prose *before* writing any spec, and five of its six fields differ.

**Prior AI output is not a convention.** An artifact left by an earlier session is not evidence of anyone's preference. Check provenance — `git log --diff-filter=A` — before matching a neighbor's formatting, structure, or naming.

**Layer drift across baselines.** Cretaceous's layers were written against three different scene lists and never reconciled, so allocations point at scene numbers that have since moved. Any renumbering must sweep every layer, and a layer that references scenes by number should say which list it was written against.

**Pointer integrity is not semantic integrity.** A cross-reference check that only resolves addresses reports a green corpus while the thing being pointed at has been rewritten into uselessness. Every cross-reference states what it needs, not just where it lives. See §5.4.

**Preferences inflate into laws.** A thing the author said once, in passing, comes back as *never*, *not one, not ever*, *must not*, *one per act*. The content is usually fine and the **modality** is invented — and a drafting model obeys grammar, so a quota gets spent against like a budget. Caught 2026-09-10, when `character-arcs.md`'s "one touch per act" caused a scene ledger to record that a character touched nobody because the act's touch was "spent elsewhere." Nobody decided that; the sentence shape did.

*The test is the provenance test aimed at force rather than content: does the rule cite something?* "Complete sentences in narration" cites a line-by-line critique. "Cold is not a hazard" cites 28–32 °C water. Those keep their force. A rule citing nothing becomes a guideline with its reasoning visible, so a drafter can tell when breaking it is right.

**Measurements become targets.** A number stated as a finding gets read as an instruction. A per-scene word target, a move-count target, a sentence-length target: all three appeared here, and all three were wrong, because the right value is set by the job and the context and not by an average.

## 9. Applying this to a new novel

Order matters; each step depends on the last.

1. **Build the style reference from the author's own prose, verbatim**, before writing any specification. Do not derive it from previous generated output, however much of it exists.
2. **Map three or four scenes from that prose by hand**, at different scene types, and let them dictate the schema fields. Do not carry this file's schema over unexamined — it was forced into shape by one author's work.
3. **Run T1 blind, with matched pairs and at least two model lineages.** Expect it to falsify something.
4. **Write one forward map**, and run T6 on it. If most lines fail prospectivity, the schema is a review format and not a brief format.
5. **Run T2 and T3** before writing briefs at volume.
6. Only then plan the layers, and pin every allocation to a scene *and a position*.

## 11. The flywheel

**The process is not a pipeline that gets run. It is a flywheel that gets loaded, run, and improved, once per scene, sixty times.** Daniel's framing, 2026-09-10, and the reason this document exists at all rather than living in someone's context window.

Each cycle: **LOAD** (`process/scene-build-runbook.md` phase 0 — read this file and the blacklist before touching the scene) → **RUN** (phases 1–8) → **IMPROVE** (phase 9 — update this file, the runbook, and the blacklist). A session that skips the improve step has taken from the process without paying back into it, and the next session pays for that.

**Three loops turn, and each converts a one-time cost into a permanent asset.**

| loop | input | asset | what falls |
|---|---|---|---|
| **canon** | invention-ledger answers written back to the world files | a world that answers its own questions | ledger items per scene |
| **method** | the retro after each scene | this document and the runbook | rediscovery; repeated mistakes |
| **craft** | Daniel's critique of each draft | `ai-tells-blacklist.md` | repeat defects per draft |

The canon loop is the one with the steepest curve. Scene 1 must invent almost everything about its location; scene 40 inherits nearly all of it. If the ledger is not shrinking by the tenth scene, the write-back step in phase 5 is not happening.

**The ratchet.** A flywheel without one spins backwards. Here it is the status labels in §2 and the corpses kept in §7 and §8: a claim that was tested and withdrawn stays visible with its post-mortem, so no later session re-derives it, re-believes it, and re-acts on it. **Deleting a withdrawn claim is the single most damaging edit anyone can make to this file.** Two false findings have already been produced and retracted inside one session; the cost of a retraction is small and the cost of a silent re-adoption is not.

**Measurement.** Three numbers, recorded in the §10 log at every retro, all of them proxies for the only thing that matters — how much of Daniel's attention a usable scene costs:

1. **invention-ledger items** put to him before drafting
2. **author words read** — how much prose he had to read
3. **author words written** — how much critique he had to write

The baseline, and it is deliberately a bad one: **scene 2.3, 2026-09-10 — 0 ledger items, ~8,600 words read, thousands written, and the output was unusable.** Every subsequent scene is measured against that. If the numbers do not fall, the flywheel is not turning, and the right response is to fix the procedure rather than to try harder at the scene.

## 10. Log

- **2026-09-09** — Schema v1 built from the planning stack; discarded on provenance grounds. Schema v2 derived from `viking.md:3036` (the campfire). T1 run: eight blind scenes, two lineages, sixteen maps. Annotation-density discriminator withdrawn. `[withheld]` cut. T2 run: three writers, three lineages. C4, C5, C7. C8 reported.
- **2026-09-10** — `READER` added to IN and OUT; `[turn — READER ONLY]`; `[requires]`; two-way duration markers. Ledger payment invariant refined into delivered/accumulated with a named completion scene. T3 run. **C8 withdrawn** — control confounded by mapper identity. Same-producer rule recorded as a standing hazard. `[requires]` given a semantic payload after three real continuity failures were shown to have kept their addresses intact throughout; unresolved-`requires`-as-work-queue noted. This file created.
