"""The second front end: the same checks, emitted as a markdown change set.

    python3 tools/report.py              # everything, grouped by check
    python3 tools/report.py day_tokens   # one check

pytest answers "is the corpus consistent." This answers "what would I have to
change," in the shape Daniel reads and strikes.
"""

from __future__ import annotations

import sys

from checks import CHECKS, ROOT, calendar, run_all


def main(argv: list[str]) -> int:
    wanted = argv[1:] or list(CHECKS)
    unknown = [w for w in wanted if w not in CHECKS]
    if unknown:
        print(f"unknown check(s): {', '.join(unknown)}", file=sys.stderr)
        print(f"available: {', '.join(CHECKS)}", file=sys.stderr)
        return 2

    results = {name: CHECKS[name]() for name in wanted} if argv[1:] else run_all()
    total = sum(len(v) for v in results.values())
    days = calendar()

    print(f"# Consistency report\n")
    print(f"{total} violations across {sum(1 for v in results.values() if v)} of "
          f"{len(results)} checks. Calendar: {min(days)}-{max(days)} days, "
          f"parsed from `plan/journey-calendar.md`.\n")

    for name, violations in results.items():
        doc = (CHECKS[name].__doc__ or "").strip().splitlines()[0]
        if not violations:
            print(f"## {name} — clean\n\n{doc}\n")
            continue
        print(f"## {name} — {len(violations)}\n\n{doc}\n")
        print("| file:line | what |")
        print("|---|---|")
        for v in violations:
            print(f"| `{v.file}:{v.line}` | {v.message} |")
        print()

    return 1 if total else 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "tools"))
    raise SystemExit(main(sys.argv))
