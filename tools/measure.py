"""Measure a drafted scene before Daniel reads it.

    python3 tools/measure.py content/D3.2.md [more files...]

Prints, per file: words; narration sentences of five words or fewer, as a share of
narration (target 19-22%, `prompts/style-canon.md` §0 and `AGENTS.md` §4); narration
sentences with two or more `, and` joints (budget two or three a scene,
`prompts/ai-tells-blacklist.md` §30); and the count of `nobody` (§29).

**Narration only.** Quoted speech is removed before sentences are split, because
Daniel's dialogue runs about twice his narration's short-sentence rate and a
blended figure hides both (`AGENTS.md` §4). Attribution fragments left behind by
the removal — `said Teva.`, `he whispered.` — are not counted as short narration.

It lived in /tmp until 2026-10-09, which is reaped on this box, and the scene
procedure depends on it, so it is tracked here.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SPEECH = re.compile(r'"[^"]*"')
COMMENT = re.compile(r"<!--.*?-->", re.S)
SENT = re.compile(r"(?<=[.!?])\s+")
ATTRIB = re.compile(r"^(?:\w+\s+)?(?:said|asked|whispered|breathed|called|shouted|answered)\b[^.!?]*[.!?]?$", re.I)


def measure(path: Path) -> dict:
    text = path.read_text()
    body = text.split("---", 2)[2] if text.startswith("---") else text
    body = COMMENT.sub("", body)
    words = len(body.split())
    narr = []
    for para in body.strip().split("\n\n"):
        for s in SENT.split(SPEECH.sub(" ", para).strip()):
            s = s.strip(" ,—-")
            if not s or ATTRIB.match(s):
                continue
            narr.append(s)
    short = [s for s in narr if len(s.split()) <= 5]
    chains = [s for s in narr if s.count(", and") >= 2]
    return {
        "words": words,
        "narration": len(narr),
        "short": short,
        "chains": chains,
        "nobody": len(re.findall(r"\bnobody\b", body, re.I)),
    }


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__.strip().splitlines()[0])
        return 2
    for name in argv:
        m = measure(Path(name))
        pct = 100 * len(m["short"]) / max(1, m["narration"])
        print(f"{name}: {m['words']} words; narration ≤5 words {pct:.1f}% "
              f"({len(m['short'])}/{m['narration']}); comma-and chains {len(m['chains'])}; nobody {m['nobody']}")
        for c in m["chains"]:
            print(f"    chain: {c[:110]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
