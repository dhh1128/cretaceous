---
approval: unapproved
---

# Handoff pointer

The handoff a new session loads is the newest dated directory `.ignored/handoff-<date>/`, and its file HANDOFF.md. At this writing that is `.ignored/handoff-2026-11-08/`. Handoffs themselves stay in `.ignored/` because they quote working material and change at every break; this tracked file is what lets a session find them, as novel-method edition 1 asks (`~/code/me/novel-method/runbook.md` D9, Q-RXPW).

**At every handoff**, which is every natural break (a day's maps approved, a day drafted) rather than a guess at how much context is left:

1. Write the handoff to `.ignored/handoff-<date>/`, and change the directory named above to it in the same commit as the work it hands off.
2. Run the flywheel capture, which writes Daniel's turns from this session (including those typed while it was busy) and his hand-edit commits to `.ignored/captures/`:

   ```
   python3 ~/code/me/novel-method/tools/capture.py /home/daniel/code/me/cretaceous
   ```

   The transcript defaults to the newest one Claude Code keeps for this directory, which is the running session; `--session <id-prefix>` picks another.
3. At the retro, classify each correction, delight and hand edit in the capture as canon, method, craft, tool or friction, and file each non-canon item as a tick in `~/code/me/novel-method` with his exact words, the session id and the timestamp (`~/code/me/novel-method/adopt.md`, "The flywheel", steps 2 and 3).
