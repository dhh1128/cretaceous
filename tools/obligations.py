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


# A line can be a whole table row, and what it owes this scene is often one clause
# deep in it. Printing the first 200 characters hid `D3.2 the grounder decoy` at the
# end of the projection row in `tech-rules.md`, and the first D3.2 map contradicted
# that approved clause without anyone seeing it. So print the clause that names the
# scene or the day, and the start of the line only when nothing names it.
SPLIT = re.compile(r"\s+\|\s+|\s+·\s+|(?<=[.;])\s+(?=[*A-Z`(])")


def clause(line: str, pat: re.Pattern[str], width: int = 320) -> str:
    """The cell or sentence of `line` that matches `pat`, else its opening."""
    flat = re.sub(r"\s*<!--.*?-->", "", line.strip())
    segs = [s.strip() for s in SPLIT.split(flat) if s.strip()]
    hits = [s for s in segs if pat.search(s)]
    if not hits:
        return flat[:width]
    if flat.startswith("|"):
        # In a table row the leading cells say what the row is about: an id is
        # not enough on its own, so take the next cell too when the first is short.
        lead = segs[:2] if len(segs[0].strip("| *")) < 12 else segs[:1]
        if all(h in lead for h in hits):
            return flat[:width]
        hits = lead + [h for h in hits if h not in lead]
        hits = [h.strip("| ") for h in hits]
    out = " … ".join(hits)
    return out if len(out) <= width else out[:width] + "…"


def scene_pattern(sid: str) -> re.Pattern[str]:
    """The scene's id where it is named in prose, not only as an `@` tag."""
    return re.compile(rf"(?<![\w@]){re.escape(sid)}(?![\d.])")


def day_pattern(day: int) -> re.Pattern[str]:
    return re.compile(rf"(?<![\w])(?:Days?|Nights?)\s+(?:\d{{1,2}}\s*[–—-]\s*)?{day}(?![\d])"
                      rf"|(?<![\w])(?:Days?|Nights?)\s+{day}\s*[–—-]\s*\d{{1,2}}(?![\d])")


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
        print(f"  {p}:{n}\n      {clause(line, scene_pattern(sid))}")
    if not t:
        print("  none. This scene is addressed by day rather than by name in every layer.")

    if "--day-only" not in argv:
        d = day_lines(day)
        print(f"\n--- owed by Day {day}: {len(d)} lines. "
              f"Which of {', '.join(siblings)} carries each is a drafting decision ---\n")
        for p, n, line in d:
            print(f"  {p}:{n}\n      {clause(line, day_pattern(day))}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
