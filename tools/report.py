"""The second front end: the same checks, emitted as a markdown change set.

    python3 tools/report.py              # everything, grouped by check
    python3 tools/report.py day_tokens   # one check

pytest answers "is the corpus consistent." This answers "what would I have to
change," in the shape Daniel reads and strikes.
"""

from __future__ import annotations

import sys

from checks import CHECKS, ROOT, calendar, corpus as _corpus, run_all

CORPUS = _corpus()


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

    from checks import check_approval_not_stale, rules
    if rules():
        print("## rules\n")
        print("Ratified rules are enforced by the suite. Proposed rules are listed with what they "
              "would catch today, so a rule can be judged against its violations rather than its "
              "sentence. Only Daniel ratifies -- see `tools/RULES.md`.\n")
        for r in sorted(rules(), key=lambda r: r.id):
            fn = CHECKS.get(r.fields.get("check", ""))
            caught = "no checker written yet" if fn is None else f"catches {len(fn())} today"
            print(f"- {r.render()} — {caught} — `{r.file}:{r.line}`")
        print()

    stale = {v.file for v in check_approval_not_stale()}
    marked = [p for p in sorted(CORPUS)
              if len(CORPUS[p]) > 1 and CORPUS[p][1].startswith("approval: ")
              and CORPUS[p][1] != "approval: unapproved"]
    if marked:
        print("## approval\n")
        print("Markers carry a hash of the body, not a date — see `AGENTS.md` §2. A file whose "
              "body no longer hashes to its marker has changed since he read it. "
              "`python3 tools/approve.py --list` is the same table; `approve.py <file>` re-stamps one.\n")
        print("| file | marker | changed since approval |")
        print("|---|---|---|")
        for path in marked:
            print(f"| `{path}` | {CORPUS[path][1].removeprefix('approval: ')} | "
                  f"{'**yes**' if path in stale else 'no'} |")
        print()

    return 1 if total else 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "tools"))
    raise SystemExit(main(sys.argv))
