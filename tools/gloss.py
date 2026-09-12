"""Annotate day numbers with what the calendar says they are.

    python3 tools/gloss.py <file>          # gloss a file
    cat something | python3 tools/gloss.py # gloss stdin
    python3 tools/gloss.py --diff <sha> <file>   # gloss a diff, old numbering on the
                                                 # minus side and new on the plus side

A day number is an address and carries no meaning. `Day 11` is unreadable without
the calendar open beside it, and the numbering has now moved twice, so anything
written before the move reads in a scheme nobody holds in their head any more.
This makes a line say `Day 11 → Noli at dawn, then the fall`.

The minus side of a diff is glossed against the fourteen-day calendar as it stood
before `2e9f355`, because that is the scheme those lines were written in.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from checks import CALENDAR, DASHES, ROOT, calendar, plain  # noqa: E402

OLD_REV = "2e9f355^"
WIDTH = 44


def _parse(text: str) -> dict[int, str]:
    """day -> what happens, from the FIRST day-indexed table in the text.

    First, not any: these files also carry a night-sky table and a weather table
    keyed by day, and a naive scan lets the last one win — which glossed Day 8 as
    "nothing. Five nights of overcast" instead of the crossing."""
    days: dict[int, str] = {}
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            if days:
                break                     # the calendar table has ended
            continue
        cells = [plain(c) for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        m = re.fullmatch(rf"(\d+)(?:\s*[{DASHES}]\s*(\d+))?", cells[0])
        if not m:
            continue
        what = re.sub(r"\s+", " ", cells[1]).strip()
        for d in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1):
            days[d] = what
    return days


def old_calendar() -> dict[int, str]:
    text = subprocess.run(["git", "-C", str(ROOT), "show", f"{OLD_REV}:{CALENDAR}"],
                          capture_output=True, text=True).stdout
    return _parse(text)


def new_calendar() -> dict[int, str]:
    return {d: v["where"] for d, v in calendar().items()}


def short(s: str) -> str:
    s = re.sub(r"\s*[—–-]\s*.*$", "", s) if len(s) > WIDTH else s
    return s if len(s) <= WIDTH else s[: WIDTH - 1].rstrip() + "…"


DAY_REF = re.compile(rf"\bDays?\s+\d+(?:\s*[{DASHES}]\s*\d+)?", re.I)
ROW_DAY = re.compile(rf"^([+\- ]?\|\s*\**)(\d+(?:\s*[{DASHES}]\s*\d+)?)(\**\s*\|)")


def gloss_line(line: str, days: dict[int, str]) -> str:
    """Append what each day named on this line actually is."""
    found: list[int] = []
    for m in DAY_REF.finditer(line):
        found += [int(x) for x in re.findall(r"\d+", m.group(0))]
    row = ROW_DAY.match(line)
    if row:
        found += [int(x) for x in re.findall(r"\d+", row.group(2))]
    seen, notes = set(), []
    for d in found:
        if d in seen or d not in days:
            continue
        seen.add(d)
        notes.append(f"{d}={short(days[d])}")
    return f"{line}    « {' · '.join(notes)} »" if notes else line


# The one renumbering this corpus has been through, as a record rather than an
# authority: the fourteen-day calendar became nineteen days in 2e9f355. Nothing
# computes from this -- it exists so a human reading old text can place it. Days
# 7, 8, 9, 17 and 18 are new and have no old counterpart.
RENUMBER = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 10, 8: 11, 9: 12,
            10: 13, 11: 14, 12: 15, 13: 16, 14: 19}


def print_map() -> None:
    old, new = old_calendar(), new_calendar()
    print("| old day | what it was | → | new day | what it is |")
    print("|---|---|---|---|---|")
    for o in sorted(RENUMBER):
        n = RENUMBER[o]
        print(f"| {o} | {short(old.get(o, '—'))} | → | **{n}** | {short(new.get(n, '—'))} |")
    print()
    for n in sorted(set(new) - set(RENUMBER.values())):
        print(f"| — | *(new day)* | → | **{n}** | {short(new[n])} |")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--map":
        print_map()
        return 0
    if argv and argv[0] == "--diff":
        sha, path = argv[1], argv[2]
        old, new = old_calendar(), new_calendar()
        diff = subprocess.run(["git", "-C", str(ROOT), "diff", "-U1", sha, "--", path],
                              capture_output=True, text=True).stdout
        for line in diff.splitlines():
            if line.startswith("-") and not line.startswith("---"):
                print(gloss_line(line, old))
            elif line.startswith("+") and not line.startswith("+++"):
                print(gloss_line(line, new))
            else:
                print(line)
        return 0

    text = Path(argv[0]).read_text(encoding="utf-8") if argv else sys.stdin.read()
    days = new_calendar()
    for line in text.splitlines():
        print(gloss_line(line, days))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
