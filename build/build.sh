#!/usr/bin/env bash
# The chapter files -> .ignored/drift{,-beta}.{docx,epub,pdf}
#
#   bash build/build.sh          # the KDP set: drift.docx, drift.epub, drift.pdf
#   bash build/build.sh --beta   # the beta reader's set: drift-beta.{docx,epub,pdf}
#
# Adapted from ~/code/me/viking/build (on kelun), 2026-11-25. Both sets come from
# tools/build_book.py without --ids, so no scene id reaches a reader. They differ
# only in the front matter, build/front-matter.md (title, copyright, dedication)
# or build/front-matter-beta.md (a not-for-distribution note naming the draft
# tag in place of the copyright page), and in build/back-matter.md (About the
# Author), which only the published set carries.
#
# The docx is the thing to open in Kindle Create. The epub is what KDP accepts
# directly for Kindle if you skip Kindle Create, and a cross-check of the reflow.
# The pdf is a 6x9in trade paperback interior, twoside, for KDP print. PDFs are
# built with tectonic (brew install tectonic) where viking used xelatex.
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p .ignored

beta=0
for arg in "$@"; do
  case "$arg" in
    --beta) beta=1 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

# The front-matter files carry the corpus's approval frontmatter; the book does not.
strip_fm() { awk 'NR==1 && /^---$/ {fm=1; next} fm && /^---$/ {fm=0; skip=1; next} fm {next} skip && /^$/ {skip=0; next} {skip=0; print}' "$1"; }

[[ -f build/reference.docx ]] || python3 build/make-reference.py

python3 tools/build_book.py .ignored/book.md >/dev/null

if (( beta )); then
  name=drift-beta
  # The newest draft tag, plus a warning if the prose has moved since it.
  tag="$(git describe --tags --abbrev=0 --match '*-draft')"
  if ! git diff --quiet "$tag" -- content; then
    tag="$tag plus later edits"
  fi
  strip_fm build/front-matter-beta.md | sed "s/DRAFT_TAG/$tag/" > .ignored/front.md
else
  name=drift
  strip_fm build/front-matter.md > .ignored/front.md
fi
src=".ignored/$name.md"
cat .ignored/front.md .ignored/book.md > "$src"
# About the Author goes in the published book only, not the beta copy.
(( beta )) || { printf '\n'; strip_fm build/back-matter.md; } >> "$src"

pandoc "$src" \
  --from=markdown+smart \
  --lua-filter=build/kdp.lua \
  --reference-doc=build/reference.docx \
  --metadata title="Drift" \
  --standalone \
  --output=".ignored/$name.docx"
echo "wrote .ignored/$name.docx"

pandoc "$src" \
  --from=markdown+smart \
  --lua-filter=build/kdp.lua \
  --split-level=1 \
  --css=build/epub.css \
  --epub-title-page=false \
  --metadata title="Drift" \
  --metadata author="Daniel Hardman" \
  --metadata lang=en-US \
  --standalone \
  --output=".ignored/$name.epub"
echo "wrote .ignored/$name.epub"

# 6x9in is the common trade-paperback trim. twoside so the gutter alternates
# with the binding, openany so a chapter is not forced onto a recto (no blank
# pages). 0.875in inside clears KDP's minimum gutter for up to 700 pages.
pandoc "$src" \
  --from=markdown+smart \
  --lua-filter=build/pdf.lua \
  --top-level-division=chapter \
  --pdf-engine=tectonic \
  --variable=title-meta:Drift \
  --variable=author-meta:"Daniel Hardman" \
  --variable=documentclass:book \
  --variable=classoption:twoside \
  --variable=classoption:openany \
  --variable=fontsize:11pt \
  --variable=indent:true \
  --variable=geometry:paperwidth=6in \
  --variable=geometry:paperheight=9in \
  --variable=geometry:inner=0.875in \
  --variable=geometry:outer=0.75in \
  --variable=geometry:top=0.75in \
  --variable=geometry:bottom=0.75in \
  --include-in-header=build/pdf-header.tex \
  --standalone \
  --output=".ignored/$name.pdf"
echo "wrote .ignored/$name.pdf"
