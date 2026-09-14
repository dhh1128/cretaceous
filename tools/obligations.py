"""Everything the planning layers owe one scene, at both precisions.

    python3 tools/obligations.py D12.1
    python3 tools/obligations.py D12.1 --day-only

**The problem this solves.** `README.md` item 6 promised that one grep returns a
scene's complete obligation set, and `@D12.1` tags deliver that for Act 1 and
almost nowhere else — because **Act 1 is addressed by scene and Acts 2 and 3 are
addressed by day.** The foreshadow ledger pays at "Day 12"; the species allocation
is a day column by design; `body-and-resources.md` is a day table. 107 lines carry
a scene tag and 262 name a day and no scene.

**The wrong fix is to tag those onto scenes.** A statement made about a day is
true of the day, and pushing it onto one of its scenes would assert a precision
nobody chose — which is the failure mode this whole corpus exists to avoid. So the
layers keep the precision they actually have, and the *query* unions the levels.

**What that means for the reader of the output.** Scene-precise lines are owed by
this scene. Day-precise lines are owed by this day, and **which of its scenes
carries each one is a drafting decision, not a lookup.** The tool says so rather
than pretending otherwise, and it names the sibling scenes so the choice is
visible.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from checks import SCENE_DAY, iter_lines, lines_of, scenes  # noqa: E402

SCENES = "plan/scene-list.md"
DAY_NAMED = re.compile(r"(?<![\w])Days?\s+(\d{1,2})(?:\s*[–—-]\s*(\d{1,2}))?(?![\w])")


def scene_day(sid: str) -> int | None:
    for _, s, line in scenes():
        if s == sid:
            m = SCENE_DAY.search(line)
            return int(m.group(1)) if m else None
    return None


def entry(sid: str) -> list[str]:
    """The scene's own entry, header to the next heading or rule."""
    lines, out, inside = lines_of(SCENES), [], False
    for line in lines:
        if re.match(rf"^#{{2,4}}\s*{re.escape(sid)}\s*[—–-]", line):
            inside = True
        elif inside and (line.startswith("#") or line.strip() == "---"):
            break
        if inside:
            out.append(line)
    return out


# README and AGENTS describe the tagging and use a tag as their example, which is
# methodology rather than an obligation on any scene.
TAG_EXEMPT = ("README.md", "AGENTS.md")


def tagged(sid: str) -> list[tuple[str, int, str]]:
    tag = re.compile(rf"@{re.escape(sid)}(?![\d.])")
    return [(p, n, line) for p, n, line in iter_lines()
            if p not in TAG_EXEMPT and tag.search(line)]


def day_lines(day: int) -> list[tuple[str, int, str]]:
    """Lines in the layers that speak about this day.

    `scene-list.md` is excluded: its day mentions are other scenes' entries, which
    are siblings rather than obligations, and they are listed separately."""
    out = []
    for p, n, line in iter_lines():
        if not p.startswith(("plan/", "kb/")) or p == SCENES:
            continue
        if "@D" in line or "[retired]" in line:
            continue
        for a, b in DAY_NAMED.findall(line):
            lo, hi = int(a), int(b or a)
            if lo <= day <= hi:
                out.append((p, n, line.strip()))
                break
    return out


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__.strip().splitlines()[0])
        print("\n    python3 tools/obligations.py D12.1\n")
        return 2
    sid = argv[0]
    day = scene_day(sid)
    if day is None:
        print(f"{sid} is not a scene in {SCENES}", file=sys.stderr)
        return 2

    siblings = [s for _, s, line in scenes()
                if (m := SCENE_DAY.search(line)) and int(m.group(1)) == day]

    print(f"\n=== {sid} — Day {day} ===\n")
    for line in entry(sid):
        print("  " + line)

    t = tagged(sid)
    print(f"\n--- owed by this scene: {len(t)} tagged ---\n")
    for p, n, line in t:
        print(f"  {p}:{n}\n      {line.strip()[:200]}")
    if not t:
        print("  none. This scene is addressed by day rather than by name in every layer.")

    if "--day-only" not in argv:
        d = day_lines(day)
        print(f"\n--- owed by Day {day}: {len(d)} lines. "
              f"Which of {', '.join(siblings)} carries each is a drafting decision ---\n")
        for p, n, line in d:
            print(f"  {p}:{n}\n      {line[:200]}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
