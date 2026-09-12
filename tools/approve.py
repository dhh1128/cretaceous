"""Record that Daniel has approved a file's current contents. See AGENTS.md §2.

    python3 tools/approve.py --list                 # every marker, and what is stale
    python3 tools/approve.py <file> [<file>...]     # stamp the current body hash
    python3 tools/approve.py --provisional <file>   # the weaker marker

The marker carries a hash of the body rather than a date. Nothing is typed by hand
and nothing is bumped; this writes it. A date had day granularity, which this corpus
defeats routinely, and a bare `approved` could not express re-approval at all,
because approved-to-approved is a no-op git cannot see.

**It requires a terminal**, for the same reason `ratify.py` does: an agent's shell
has no TTY, so a session cannot approve its own output by running the script.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from checks import ROOT, body_hash, check_approval_not_stale, corpus  # noqa: E402


def marker(path: str) -> str | None:
    lines = corpus().get(path, [])
    return lines[1] if len(lines) > 1 and lines[1].startswith("approval:") else None


def stamp(path: str, state: str) -> str:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    h = body_hash(text)
    lines[1] = f"approval: {state} {h}\n" if state != "unapproved" else "approval: unapproved\n"
    p.write_text("".join(lines), encoding="utf-8")
    return h


def main(argv: list[str]) -> int:
    state = "approved"
    if argv and argv[0] == "--provisional":
        state, argv = "provisional", argv[1:]

    stale = {v.file: v.message for v in check_approval_not_stale()}

    if not argv or argv[0] in {"--list", "-l"}:
        for path in sorted(corpus()):
            m = marker(path)
            if not m:
                continue
            flag = "  ⚠ CHANGED SINCE APPROVAL" if path in stale else ""
            print(f"{m.removeprefix('approval: '):<28} {path}{flag}")
        print(f"\n{len(stale)} file(s) changed since approval.")
        return 0

    if not sys.stdin.isatty():
        print("approve.py needs a terminal. Run it in a shell of your own — an agent's\n"
              "shell has no TTY, and that is the point. See AGENTS.md §2.", file=sys.stderr)
        return 2

    unknown = [a for a in argv if a not in corpus()]
    if unknown:
        print(f"not tracked markdown in this repo: {', '.join(unknown)}", file=sys.stderr)
        return 2

    done = 0
    for path in argv:
        print(f"\n{path}")
        print(f"  now: {marker(path)}")
        if path in stale:
            print(f"  {stale[path]}")
        print(f"  git diff will show what changed: git diff -- {path}")
        if input(f"  mark {state}? [y/N] ").strip().lower() in {"y", "yes"}:
            print(f"  {state} {stamp(path, state)}")
            done += 1
        else:
            print("  unchanged")

    print(f"\n{done} marked. Run the suite: uv run --with pytest pytest tools/ -q")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
