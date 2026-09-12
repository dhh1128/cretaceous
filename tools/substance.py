"""Separate real edits from pure renumbering in a diff.

    python3 tools/substance.py <sha> <file>    # one file
    python3 tools/substance.py --stale         # every file with a stale marker

Most of what changed in the day-indexed files is the day numbers moving and
nothing else. That is not worth reading. This applies the old-to-new renumbering
to the minus side of each changed line and asks whether the result is *identical*
to the plus side. If it is, the line changed in no other way and is dropped.

It fails safe in one direction only. Identical-after-renumbering is a strong test:
any real edit changes something the map cannot account for, so it survives. A line
this tool calls substantive may still be trivial; a line it drops cannot be.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from checks import DASHES, ROOT, _marker_set_at, check_approval_not_stale  # noqa: E402
from gloss import RENUMBER  # noqa: E402


def renumber(line: str) -> str:
    """Apply the old-to-new day map wherever a day number can appear."""
    def sub_run(m: re.Match) -> str:
        return m.group(1) + re.sub(r"\d+", lambda d: str(RENUMBER.get(int(d.group(0)), d.group(0))), m.group(2))

    out = re.sub(rf"(\bDays?\s+)(\d+(?:\s*(?:[{DASHES}]|,|\band\b|\bto\b|\bor\b)\s*\d+)*)",
                 sub_run, line, flags=re.I)
    # a leading table cell is a day in the day-indexed tables
    out = re.sub(rf"^([+\- ]?\|\s*\**)(\d+(?:\s*[{DASHES}]\s*\d+)?)(\**)",
                 lambda m: m.group(1) + re.sub(r"\d+", lambda d: str(RENUMBER.get(int(d.group(0)), d.group(0))),
                                               m.group(2)) + m.group(3), out)
    # bare parentheticals -- milieu-allocation section 5 writes days as "(7)"
    out = re.sub(r"\((\d{1,2})\)", lambda m: f"({RENUMBER.get(int(m.group(1)), m.group(1))})", out)
    return out


DAY_TOKEN = re.compile(rf"\bDays?\s+\d+(?:\s*[{DASHES}]\s*\d+)?", re.I)
LEAD_CELL = re.compile(rf"^(\|\s*\**)(\d+(?:\s*[{DASHES}]\s*\d+)?)(\**\s*\|)")


# A day number can sit anywhere: "Day 7", a leading table cell, a bare parenthetical
# "(7)", or -- the case that defeated the first version -- the SECOND cell of a table,
# as in "| *Ornithomimus* | 7 | fast, harmless". So blank every standalone one- or
# two-digit integer that is not part of a decimal, which is what a scene number looks
# like. Blanking too much is safe: the numbers are reported and checked against the
# map, so anything the map does not explain surfaces as a line to eyeball rather than
# passing silently.
BARE_NUMBER = re.compile(r"(?<![\d.])(\d{1,2})(?![\d.])")


def skeleton(line: str) -> str:
    """The line with every day-shaped number blanked, so two versions of a row match."""
    return BARE_NUMBER.sub("<D>", line[1:])


def day_numbers(line: str) -> list[int]:
    return [int(x) for x in BARE_NUMBER.findall(line[1:])]


def hunks(sha: str, path: str) -> list[tuple[str, list[str], int]]:
    """(hunk header, changed lines, first line number on the new side)."""
    diff = subprocess.run(["git", "-C", str(ROOT), "diff", "-U0", sha, "--", path],
                          capture_output=True, text=True).stdout
    out, head, body, start = [], None, [], 0
    for line in diff.splitlines():
        if line.startswith("@@"):
            if head:
                out.append((head, body, start))
            m = re.search(r"\+(\d+)", line)
            head, body, start = line, [], int(m.group(1)) if m else 0
        elif head is not None and line[:1] in "+-" and not line.startswith(("---", "+++")):
            body.append(line)
    if head:
        out.append((head, body, start))
    return out


def authored_since(path: str, since: str) -> set[int]:
    """Current line numbers whose content was last written by a commit after `since`.

    Used to drop lines whose present text came out of a change set Daniel read and
    approved. Blame answers that exactly, and it answers it about the file as it
    stands -- which is the only state worth showing him. An earlier version of this
    tool diffed to an intermediate commit and put a half-swept line in front of him
    as though it were current.
    """
    keep = set(subprocess.run(["git", "-C", str(ROOT), "log", "--format=%H", f"{since}..HEAD"],
                              capture_output=True, text=True).stdout.split())
    out, n = set(), 0
    for line in subprocess.run(["git", "-C", str(ROOT), "blame", "--line-porcelain", "--", path],
                               capture_output=True, text=True).stdout.splitlines():
        if len(line) >= 40 and line[:40].isalnum() and " " in line:
            sha_, _, rest = line.partition(" ")
            parts = rest.split()
            if len(parts) >= 2 and parts[1].isdigit():
                n = int(parts[1])
                if sha_ in keep:
                    out.add(n)
    return out


def classify(sha: str, path: str, approved_since: str | None = "17dbee1"):
    """(renumbered, approved, off-map day moves, substantive lines).

    Lines are paired by their text with every day number blanked, across the whole
    file rather than within a hunk. Pairing within a hunk by position was wrong: a
    moved or inserted row makes the plus and minus counts differ, and the whole hunk
    then read as substantive. body-and-resources.md reported twenty-one lines to
    read that way, and every one of them was a day number moving.

    A matched pair whose days all follow the old-to-new map changed in no other way.
    A pair whose days moved some other way is reported as one short line, because the
    only question it raises is whether that move was intended. Only genuinely
    unmatched lines are text somebody has to read.
    """
    approved = authored_since(path, approved_since) if approved_since else set()
    minus, plus, plus_line, n_hunk_appr = [], [], {}, 0
    from_hunk: dict[int, tuple] = {}
    for head, body, start in hunks(sha, path):
        adds, i = [], 0
        for l in body:
            if l.startswith("+"):
                adds.append((l, start + i))
                i += 1
        # A hunk whose new text was entirely written by an approved change set is his,
        # deletions included -- the old lines it replaced are not worth reading. Without
        # this, removing the km column left fifteen orphaned minus lines looking like
        # content he had never seen.
        if adds and all(n in approved for _, n in adds):
            n_hunk_appr += len(body)
            continue
        for l in body:
            from_hunk[id(l)] = (head, tuple(body))
            if l.startswith("-"):
                minus.append(l)
        for l, n in adds:
            plus.append(l)
            plus_line[id(l)] = n

    drop = lambda l: re.match(r"^[+-]approval: ", l)
    minus = [l for l in minus if not drop(l)]
    plus = [l for l in plus if not drop(l)]

    # Pair FIRST, then attribute what is left. Filtering approved lines out before
    # pairing orphans their partners and inflates the residual -- it took
    # body-and-resources from twenty-one lines to twenty-six by "improving" it.
    pool, pairs, orphan_minus = list(plus), [], []
    for a in minus:
        hit = next((b for b in pool if skeleton(b) == skeleton(a)), None)
        if hit:
            pool.remove(hit)
            pairs.append((a, hit))
        else:
            orphan_minus.append(a)

    renumbered, offmap = 0, []
    for a, b in pairs:
        da, db = day_numbers(a), day_numbers(b)
        # Only positions that actually moved are day moves. Blanking every day-shaped
        # integer also catches things that are not days -- dyad temperatures, ladder
        # rungs -- and those sit unchanged on both sides. Checking them against the
        # renumbering map flagged seven false moves in character-arcs.md alone.
        moved = [(x, y) for x, y in zip(da, db) if x != y] if len(da) == len(db) else None
        if moved is not None and all(RENUMBER.get(x, x) == y for x, y in moved):
            renumbered += 2
        else:
            shown = moved if moved else f"{da} → {db}"
            offmap.append(f"  {shown}   {skeleton(a)[:86]}")

    # Whatever did not pair: a plus line whose present text came out of a change set
    # he read is his; a minus line is his if nothing survives of it there.
    n_appr = n_hunk_appr + sum(1 for l in pool if plus_line[id(l)] in approved)
    pool = [l for l in pool if plus_line[id(l)] not in approved]

    # Emit WHOLE hunks. Showing one side of a change without the other makes a
    # modification read as a deletion, which is the most alarming way to render a
    # diff wrong -- four replaced lines in milieu-allocation.md looked like content
    # being removed. The reduction decides which hunks are worth showing; it does not
    # get to decide which half of one you see.
    seen, real = set(), []
    for l in orphan_minus + pool:
        head, body = from_hunk[id(l)]
        if head in seen:
            continue
        seen.add(head)
        real.append(head)
        real += list(body)
    return renumbered, n_appr, offmap, real


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--stale":
        targets = [(v.file, _marker_set_at(v.file)[1]) for v in check_approval_not_stale()]
    elif len(argv) == 2:
        targets = [(argv[1], argv[0])]
    else:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    for path, sha in sorted(targets):
        renum, appr, offmap, real = classify(sha, path)
        total = renum + appr + len(offmap) * 2 + len(real)
        verdict = "nothing for you" if not real and not offmap else \
                  f"{len(real)} line(s) to read, {len(offmap)} day move(s) to eyeball"
        print(f"\n## {path} — {total} changed: {renum} renumbering, {appr} from approved "
              f"change sets — {verdict}")
        if offmap:
            print("\nDays moved in a way the renumbering does not explain. Text otherwise identical:\n")
            print("\n".join(offmap))
        if real:
            print("\n```diff"); print("\n".join(real)); print("```")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
