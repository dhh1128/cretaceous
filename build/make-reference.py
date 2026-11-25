#!/usr/bin/env python3
"""Build build/reference.docx: pandoc's default reference doc, restyled for a novel.

Pandoc's stock reference.docx styles body text like a blog post — no first-line
indent, a blank line between paragraphs, teal headings. Kindle Create carries the
imported paragraph shape into its themes, so the source docx should already look
like a book. This rewrites the handful of styles that matter and adds the custom
"Scene Break" style the filter references.

Run:  python3 build/make-reference.py
"""

import re
import shutil
import subprocess
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "reference.docx"

# w:pPr / w:rPr bodies keyed by styleId. Each replaces whatever the default had.
STYLES = {
    # 11pt serif, single-spaced, no widows/orphans surprises.
    "Normal": (
        "",
        '<w:rFonts w:ascii="Georgia" w:hAnsi="Georgia" w:cs="Georgia"/>'
        '<w:sz w:val="22"/><w:szCs w:val="22"/>',
    ),
    # Novel body: 0.25" first-line indent, no space between paragraphs.
    "BodyText": (
        '<w:spacing w:before="0" w:after="0" w:line="276" w:lineRule="auto"/>'
        '<w:ind w:firstLine="360"/>',
        "",
    ),
    # First paragraph of a chapter or after a scene break: flush left.
    "FirstParagraph": (
        '<w:spacing w:before="0" w:after="0" w:line="276" w:lineRule="auto"/>'
        '<w:ind w:firstLine="0"/>',
        "",
    ),
    # Chapter number. Centered, black, space above, own page.
    "Heading1": (
        '<w:keepNext/><w:keepLines/><w:pageBreakBefore/>'
        '<w:spacing w:before="0" w:after="480"/><w:jc w:val="center"/>'
        '<w:outlineLvl w:val="0"/>',
        '<w:rFonts w:ascii="Georgia" w:hAnsi="Georgia" w:cs="Georgia"/>'
        '<w:b/><w:color w:val="000000"/><w:sz w:val="36"/><w:szCs w:val="36"/>',
    ),
    # Epigraphs: an archival document, so monospace and ragged right.
    "BlockText": (
        '<w:spacing w:before="0" w:after="120"/><w:jc w:val="left"/>'
        '<w:ind w:left="567" w:right="567" w:firstLine="0"/>',
        '<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New"/>'
        '<w:sz w:val="19"/><w:szCs w:val="19"/>',
    ),
    "Title": (
        '<w:spacing w:before="2400" w:after="240"/><w:jc w:val="center"/>'
        '<w:ind w:firstLine="0"/>',
        '<w:rFonts w:ascii="Georgia" w:hAnsi="Georgia" w:cs="Georgia"/>'
        '<w:b/><w:color w:val="000000"/><w:sz w:val="72"/><w:szCs w:val="72"/>',
    ),
    "Author": (
        '<w:spacing w:before="0" w:after="240"/><w:jc w:val="center"/>'
        '<w:ind w:firstLine="0"/>',
        '<w:rFonts w:ascii="Georgia" w:hAnsi="Georgia" w:cs="Georgia"/>'
        '<w:color w:val="000000"/><w:sz w:val="28"/><w:szCs w:val="28"/>',
    ),
}

CHAPTER_LABEL = (
    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="ChapterLabel">'
    '<w:name w:val="Chapter Label"/><w:basedOn w:val="Normal"/>'
    '<w:next w:val="FirstParagraph"/><w:qFormat/>'
    '<w:pPr><w:spacing w:before="360" w:after="360"/>'
    '<w:jc w:val="center"/><w:ind w:firstLine="0"/></w:pPr>'
    "</w:style>"
)

SERIES = (
    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Series">'
    '<w:name w:val="Series"/><w:basedOn w:val="Normal"/>'
    '<w:next w:val="Title"/><w:qFormat/>'
    '<w:pPr><w:spacing w:before="1800" w:after="0"/>'
    '<w:jc w:val="center"/><w:ind w:firstLine="0"/></w:pPr>'
    '<w:rPr><w:smallCaps/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>'
    "</w:style>"
)

DEDICATION = (
    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Dedication">'
    '<w:name w:val="Dedication"/><w:basedOn w:val="Normal"/><w:qFormat/>'
    '<w:pPr><w:spacing w:before="2880" w:after="0"/>'
    '<w:jc w:val="center"/><w:ind w:firstLine="0"/></w:pPr>'
    '<w:rPr><w:i/></w:rPr>'
    "</w:style>"
)

SCENE_BREAK = (
    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="SceneBreak">'
    '<w:name w:val="Scene Break"/><w:basedOn w:val="Normal"/>'
    '<w:next w:val="FirstParagraph"/><w:qFormat/>'
    '<w:pPr><w:spacing w:before="360" w:after="360"/>'
    '<w:jc w:val="center"/><w:ind w:firstLine="0"/></w:pPr>'
    '<w:rPr><w:sz w:val="22"/></w:rPr>'
    "</w:style>"
)


def patch_style(xml: str, style_id: str, ppr: str, rpr: str) -> str:
    pat = re.compile(
        r'(<w:style [^>]*w:styleId="%s"[^>]*>)(.*?)(</w:style>)' % re.escape(style_id),
        re.S,
    )
    m = pat.search(xml)
    if not m:
        raise SystemExit(f"style {style_id} not found in reference styles.xml")
    body = re.sub(r"<w:pPr>.*?</w:pPr>", "", m.group(2), flags=re.S)
    body = re.sub(r"<w:rPr>.*?</w:rPr>", "", body, flags=re.S)
    if ppr:
        body += f"<w:pPr>{ppr}</w:pPr>"
    if rpr:
        body += f"<w:rPr>{rpr}</w:rPr>"
    return xml[: m.start()] + m.group(1) + body + m.group(3) + xml[m.end() :]


def main() -> None:
    base = HERE / ".reference-default.docx"
    with base.open("wb") as fh:
        subprocess.run(
            ["pandoc", "--print-default-data-file", "reference.docx"],
            check=True,
            stdout=fh,
        )

    with zipfile.ZipFile(base) as zin:
        names = zin.namelist()
        blobs = {n: zin.read(n) for n in names}

    styles = blobs["word/styles.xml"].decode("utf-8")
    for sid, (ppr, rpr) in STYLES.items():
        styles = patch_style(styles, sid, ppr, rpr)
    styles = styles.replace("</w:styles>", SCENE_BREAK + CHAPTER_LABEL + SERIES + DEDICATION + "</w:styles>")
    blobs["word/styles.xml"] = styles.encode("utf-8")

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            zout.writestr(n, blobs[n])
    base.unlink()
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
