---
approval: unapproved
---

# Script-first drafting, one scene (SCENE)

You are drafting scene SCENE of *Cretaceous*, a YA survival novel by Daniel Hardman, in strict third-person limited. Repo: `/home/daniel/code/me/cretaceous`. You write ONLY *SCENE-script.md*, *SCENE-raw.md* and *SCENE-notes.md* in `/home/daniel/code/me/cretaceous/.ignored/draft/`. Do not modify the repo, commit, or run `tools/approve.py`.

**Do not read the existing draft of this scene** (`process/scene-build-runbook.md` Phase 6) (*content/SCENE.md*) or its git history; a fresh draft that has not anchored on the old one's wording is the point. Read the other scenes of the same day freely for continuity.

## Inputs

The approved map *plan/scene-maps/SCENE.md*, in full; every move is owed. Then, per `process/scene-build-runbook.md` Phase 0 and Phase 6: `README.md`, `AGENTS.md` (§4, §7 retired phrases), `prompts/style-canon.md`, `prompts/writing-style.md`, `prompts/ai-tells-blacklist.md` (all; §33, §34 and §35 especially), `plan/voice-sheets.md`, `plan/character-arcs.md` rows for the day, `plan/milieu-brief.md`, `plan/body-and-resources.md` (note §1: Keo's fever is his healing running hot, never infection; his cut stops bleeding within the hour), `kb/worldbuilding/safety-suits.md`, `plan/humor-plan.md`, `plan/backstory.md` as the map cites. The scenes on either side in `content/`. The target register is `content/D11.1.md`, `content/D11.2.md` (both edited by the author) and `content/D11.5.md` (drafted this way, and preferred by him): plain, grounded, nothing the reader already has.

The map's band is a floor for the map's material, never for the prose. Do not pad (`process/scene-build-runbook.md` Phase 6).

**The opening sentence after a time jump** (Q-NP03): when time has passed since the previous scene, the first sentence carries the jump through something the POV perceives (light, heat, a meal, a task finished), never a clock or "hours later", and never opens on an action that echoes the previous scene's last one; Daniel read D13.2's opening as the next second of D13.1 because it did both.

## Method

**Stage 1, the script.** The scene as dialogue only, every spoken line in order as `NAME: …`, with bare `[move N]` header lines and nothing else. The characters carry the scene through talk where the map gives them talk: each line answers the one before, friends answer rather than dodge, nobody hedges what they know exactly, a joke must be true in the world, every evaluation's referent is plain, and each line is checked against what that speaker knows then. If the scene is mostly wordless, the script is short; do not invent talk the map's situation would not produce. Save as *SCENE-script.md*.

**Stage 2, the narration.** Write the scene around the fixed script, adding only what talk cannot carry: bodies, hands, the world, what the POV perceives and remembers. Do not narrate what a line already makes plain (`prompts/ai-tells-blacklist.md` §33) or explain a line after it. You may cut a script line or replace it with a gesture; log each. Save with frontmatter `---\napproval: unapproved\n---` and a blank line as *SCENE-raw.md*.

*SCENE-notes.md*: body word counts of script and scene (state method), script lines cut or replaced, and anything invented that neither map nor canon supplies (keep near zero; each is a defect).

Run heavy shell work under `nice -n 19`. Report back briefly: counts and invented items.
