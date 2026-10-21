"""Assemble the book from the chapter files.

    python3 tools/build_book.py [out.md]      # default: .ignored/book.md

Each `content/chN.md` holds a chapter's label, its epigraph if it has one, and one
`<!-- scene: D<day>.<n> -->` line per scene, with `§` between scenes. The prose lives
only in the scene files, so a chapter file can never drift from the scene it shows.

The epigraph text is copied into the chapter file so it can be read there, which makes
it a second copy of `content/epigraphs.md`. **The build refuses to run if the two
differ**, so a fragment edited in one place and not the other fails loudly instead of
shipping two versions. A scene not yet drafted is shown as a bracketed placeholder.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
FRONT = re.compile(r"\A---\n.*?\n---\n", re.S)
COMMENT = re.compile(r"<!--.*?-->", re.S)


def body(path: Path) -> str:
    return FRONT.sub("", path.read_text()).strip()


def epigraph(fragment: str, source: str) -> str:
    m = re.search(rf"^### {fragment} —.*?\n\n((?:>.*\n?)+)", source, re.M)
    if not m:
        sys.exit(f"{fragment} is not in content/epigraphs.md")
    return m.group(1).rstrip()


def chapters() -> list[Path]:
    found = sorted(CONTENT.glob("ch*.md"), key=lambda p: int(re.sub(r"\D", "", p.stem)))
    return [p for p in found if re.fullmatch(r"ch\d+", p.stem)]


def build() -> str:
    source = (CONTENT / "epigraphs.md").read_text()
    out = []
    for n, path in enumerate(chapters(), 1):
        text = body(path)
        for m in re.finditer(r"<!-- epigraph: (EP\d+) -->\n((?:>.*\n?)+)", text):
            if m.group(2).rstrip() != epigraph(m.group(1), source):
                sys.exit(f"{path.name}: {m.group(1)} differs from content/epigraphs.md")

        def scene(m: re.Match) -> str:
            f = CONTENT / f"{m.group(1)}.md"
            return COMMENT.sub("", body(f)).strip() if f.exists() else f"[{m.group(1)} not yet drafted]"

        text = re.sub(r"<!-- scene: (D\d+\.\d+) -->", scene, text)
        out.append(f"## {n}\n\n" + COMMENT.sub("", text).strip())
    return "\n\n".join(out) + "\n"


def main(argv: list[str]) -> int:
    dest = Path(argv[0]) if argv else ROOT / ".ignored" / "book.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    text = build()
    dest.write_text(text)
    print(f"{dest}: {len(chapters())} chapters, {len(text.split()):,} words")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
