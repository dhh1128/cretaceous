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


def classify(sha: str, path: str, approved_since: str | None = "17dbee1"
             ) -> tuple[int, int, int, list[str]]:
    """(pure-renumbering lines, approved-change-set lines, lines left, those lines).

    Always diffs the marker commit against HEAD. Anything else shows a state that
    no longer exists. Three buckets:

    1. the old line, renumbered, is character-for-character the new line;
    2. the current text there was written by a commit implementing a change set
       Daniel read and approved;
    3. everything else, which is his to read.
    """
    approved_lines = authored_since(path, approved_since) if approved_since else set()
    pure = appr = 0
    real: list[str] = []
    for head, body, new_start in hunks(sha, path):
        minus = [l for l in body if l.startswith("-")]
        plus = [l for l in body if l.startswith("+")]
        plus_at = {id(l): new_start + i for i, l in enumerate(plus)}

        if plus and all(plus_at[id(l)] in approved_lines for l in plus):
            appr += len(minus) + len(plus)       # the current text here is his
            continue

        if len(minus) == len(plus) and minus:
            leftover = []
            for a, b in zip(minus, plus):
                if renumber(a)[1:] == b[1:]:
                    pure += 2
                elif plus_at[id(b)] in approved_lines:
                    appr += 2
                else:
                    leftover += [a, b]
            if leftover:
                real.append(head)
                real += leftover
        else:
            real.append(head)
            real += body

    real = [l for l in real if not re.match(r"^[+-]approval: ", l)]
    return pure, appr, len([l for l in real if l[:1] in "+-"]), real


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--stale":
        targets = [(v.file, _marker_set_at(v.file)[1]) for v in check_approval_not_stale()]
    elif len(argv) == 2:
        targets = [(argv[1], argv[0])]
    else:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    for path, sha in sorted(targets):
        pure, appr, n, real = classify(sha, path)
        total = pure + appr + n
        verdict = "nothing for you" if n == 0 else f"{n} line(s) to read"
        print(f"\n## {path} — {total} changed: {pure} renumbering, {appr} from approved "
              f"change sets, {n} left — {verdict}")
        if real:
            print("\n```diff")
            print("\n".join(real))
            print("```")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
