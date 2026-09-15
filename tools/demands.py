"""What the written scene maps demand of the scenes nobody has written yet.

    python3 tools/demands.py          # every scene with demands on it
    python3 tools/demands.py D2.6     # one scene's brief

**This is the payoff of mapping late-to-early and it is the whole reason for
that order.** A scene map tests every scene upstream of it, so its yield is
proportional to the state it inherits — and each `[requires X — payload]` it
writes is a demand on a scene that may not exist yet. Collected, those demands
are a *brief*: by the time the earliest scenes are mapped they arrive carrying
a list of everything the rest of the book needs them to deliver, each with its
payload stated.

That inverts the usual job. Instead of writing D2.6 and hoping it plants
enough, you write it against a list of what three later scenes have already
committed to needing from it.

`methodology-theory.md` §5.4 calls an unresolved `requires` a work queue. This
is the queue, sorted so the most-demanded scene is the one to write next."""

from __future__ import annotations

import re
import sys
from collections import defaultdict

from checks import MAPS_DIR, corpus, scene_days_by_address

REQ = re.compile(r"\[requires\s+(D\d+\.\d+)(?:\.(\d+))?\s*(?:—|--)\s*([^\]]+)\]")


def day_order(sid: str) -> tuple[int, int]:
    day, n = sid[1:].split(".")
    return int(day), int(n)


def collect() -> tuple[dict[str, list[tuple[str, str | None, str]]], set[str]]:
    mapped = {p[len(MAPS_DIR):-3] for p in corpus() if p.startswith(MAPS_DIR)}
    demands: dict[str, list[tuple[str, str | None, str]]] = defaultdict(list)
    for path, lines in corpus().items():
        if not path.startswith(MAPS_DIR):
            continue
        source = path[len(MAPS_DIR):-3]
        for line in lines:
            for m in REQ.finditer(line):
                target, move, payload = m.groups()
                demands[target].append((source, move, payload.strip()))
    return demands, mapped


def main(argv: list[str]) -> int:
    demands, mapped = collect()
    known = set(scene_days_by_address())
    wanted = argv[1:]
    if wanted:
        missing = [w for w in wanted if w not in demands]
        for w in missing:
            where = "exists and nothing demands anything of it" if w in known else "is not a scene"
            print(f"{w} {where}")
        wanted = [w for w in wanted if w in demands]
    else:
        wanted = sorted(demands, key=day_order)

    unwritten = [s for s in demands if s not in mapped]
    if not argv[1:]:
        print(f"{sum(len(v) for v in demands.values())} demands, from {len(mapped)} maps, "
              f"on {len(demands)} scenes — {len(unwritten)} of them unmapped.\n")
        hottest = sorted(unwritten, key=lambda s: (-len(demands[s]), day_order(s)))[:3]
        if hottest:
            print("Most demanded and unwritten, which is the order to map them in:")
            for s in hottest:
                print(f"  {s} — {len(demands[s])}")
            print()

    for target in wanted:
        state = "mapped" if target in mapped else "NOT YET MAPPED"
        print(f"{target}  ({state})")
        for source, move, payload in sorted(demands[target]):
            # The move number belongs to the TARGET, not the source: the pointer
            # reads `requires <target>.<move>`. Printing it beside the source is
            # the obvious misreading and it was made once already.
            at = f" move {move}" if move else ""
            print(f"    {target}{at} must deliver: {payload}")
            print(f"        demanded by {source}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
