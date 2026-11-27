"""Assemble the book from the chapter files.

    python3 tools/build_book.py [out.md]      # default: .ignored/book.md
    python3 tools/build_book.py --ids [out.md]  # reading copy: each scene headed by its id
    python3 tools/build_book.py --art [out.md]  # with the interior illustrations (build.sh)

Each `content/chN.md` holds a chapter's label, its epigraph if it has one, and one
`<!-- scene: D<day>.<n> -->` line per scene, with `§` between scenes. The prose lives
only in the scene files, so a chapter file can never drift from the scene it shows.

The epigraph text is copied into the chapter file so it can be read there, which makes
it a second copy of `content/epigraphs.md`. **The build refuses to run if the two
differ**, so a fragment edited in one place and not the other fails loudly instead of
shipping two versions. A scene not yet drafted is shown as a bracketed placeholder.

With `--art`, each piece listed in `build/illustrations.txt` is placed just before its
scene, as a paragraph holding one image with the class `illustration`, which the pandoc
filters in `build/` turn into a page of its own. The image is a grayscale JPEG of the
master, written to `.ignored/art/`, because the masters are color-mode PNGs with an
alpha channel and several megabytes each, which KDP's print checker and e-readers
both handle badly.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
FRONT = re.compile(r"\A---\n.*?\n---\n", re.S)
COMMENT = re.compile(r"<!--.*?-->", re.S)
MANIFEST = ROOT / "build" / "illustrations.txt"
ART_OUT = ROOT / ".ignored" / "art"


def illustrations() -> dict[str, str]:
    """Scene id -> the markdown paragraph that shows its illustration."""
    from PIL import Image  # only the --art build needs Pillow

    ART_OUT.mkdir(parents=True, exist_ok=True)
    out = {}
    for n, line in enumerate(MANIFEST.read_text().splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        fields = [f.strip() for f in line.split(" | ")]
        if len(fields) != 3 or not all(fields):
            sys.exit(f"{MANIFEST.name}:{n}: want 'scene | image | alt text'")
        sid, src, alt = fields
        if sid in out:
            sys.exit(f"{MANIFEST.name}:{n}: {sid} is listed twice")
        master = (ROOT / src).resolve()
        if not master.is_relative_to((ROOT / "art").resolve()):
            sys.exit(f"{MANIFEST.name}:{n}: {src} is not in art/")
        if not master.is_file():
            sys.exit(f"{MANIFEST.name}:{n}: {src} does not exist")
        if not (CONTENT / f"{sid}.md").exists():
            sys.exit(f"{MANIFEST.name}:{n}: no scene {sid}")
        # Rebuilt every time, which is about a second a piece: a cache keyed on mtime
        # can miss a changed master, and writing through a stale symlink is avoided by
        # unlinking first.
        dest = ART_OUT / f"{master.stem}.jpg"
        dest.unlink(missing_ok=True)
        im = Image.open(master)
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            flat = Image.new("RGBA", im.size, "white")
            flat.alpha_composite(im)
            im = flat
        im.convert("L").save(dest, "JPEG", quality=92, dpi=(300, 300))
        alt = alt.replace("[", "\\[").replace("]", "\\]")
        out[sid] = f"![{alt}]({dest.relative_to(ROOT)}){{.illustration}}"
    return out


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


def build(ids: bool = False, art: bool = False) -> str:
    source = (CONTENT / "epigraphs.md").read_text()
    pieces = illustrations() if art else {}
    placed = set()
    out = []
    for n, path in enumerate(chapters(), 1):
        text = body(path)
        for m in re.finditer(r"<!-- epigraph: (EP\d+) -->\n((?:>.*\n?)+)", text):
            if m.group(2).rstrip() != epigraph(m.group(1), source):
                sys.exit(f"{path.name}: {m.group(1)} differs from content/epigraphs.md")

        def scene(m: re.Match) -> str:
            f = CONTENT / f"{m.group(1)}.md"
            if not f.exists():
                return f"[{m.group(1)} not yet drafted]"
            head = f"<!-- -->\n\n*[{m.group(1)}]*\n\n" if ids else ""
            return head + COMMENT.sub("", body(f)).strip()

        # The epigraph comes first, then the label (day, POV, place), then the prose (Daniel, 2026-11-11).
        text = re.sub(r"\A(\*[^*\n]+\*)\n\n(<!-- epigraph: EP\d+ -->\n(?:>.*\n?)+)", r"\2\n\1\n", text)
        # An illustration goes before the § that opens its scene, so the paragraph after
        # the break still follows the break. A chapter's first scene has no §, and no
        # placement there is right yet: before the heading lands it in the previous
        # chapter's epub file, and after the label breaks the flush-left first
        # paragraph. So it is refused until a piece needs it.
        for sid, para in pieces.items():
            marker = f"<!-- scene: {sid} -->"
            if marker not in text:
                continue
            placed.add(sid)
            new = re.sub(rf"§(\s*){re.escape(marker)}", lambda m: f"{para}\n\n§{m.group(1)}{marker}", text)
            if new == text:
                sys.exit(f"{MANIFEST.name}: {sid} opens {path.name}; a chapter's first scene "
                         "cannot carry an illustration yet")
            text = new
        text = re.sub(r"<!-- scene: (D\d+\.\d+) -->", scene, text)
        out.append(f"## {n}\n\n" + COMMENT.sub("", text).strip())
    for sid in pieces.keys() - placed:
        sys.exit(f"{MANIFEST.name}: {sid} is in no chapter")
    return "\n\n".join(out) + "\n"


def main(argv: list[str]) -> int:
    ids = "--ids" in argv
    art = "--art" in argv
    argv = [a for a in argv if a not in ("--ids", "--art")]
    dest = Path(argv[0]) if argv else ROOT / ".ignored" / "book.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    text = build(ids, art)
    dest.write_text(text)
    print(f"{dest}: {len(chapters())} chapters, {len(text.split()):,} words")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
