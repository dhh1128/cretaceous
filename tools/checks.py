"""Consistency checks over the Cretaceous corpus.

Every check is a plain function taking the loaded corpus and returning a list of
Violations. The pytest suite in test_consistency.py is a thin front end over these;
report.py is a second front end that emits a markdown change set.

Two rules govern what may be written here, and both exist because this corpus has
already been damaged by their opposites:

1. A check asserts a RELATIONSHIP, never a VALUE. "Every day named anywhere exists
   in the calendar" is a check. "The savanna is 6 km" is a second copy of the
   calendar wearing a test costume, and it would freeze an unapproved number into
   a new authority. The only literals permitted are spelling blacklists and the
   shapes of citations.

2. Anything the corpus declares about itself is read FROM the corpus at runtime --
   the day range from the calendar table, the US-English word list from AGENTS.md,
   the closed-vocabulary count from lingo.md. A check that hardcodes one of those
   is the seventh copy of a fact, and it will drift.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Files referenced by the corpus that legitimately live outside the repo.
EXTERNAL_REFS = {"viking.md", "cordimancy.md"}

# Directories whose contents are working notes, not corpus.
SKIP_DIRS = {".ignored", ".git", "tools"}

DASHES = "\u2013\u2014-"  # en dash, em dash, hyphen

NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20,
}


@dataclass(frozen=True)
class Violation:
    file: str
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.file}:{self.line}"


# --------------------------------------------------------------------------
# corpus loading
# --------------------------------------------------------------------------

@cache
def tracked_md() -> tuple[str, ...]:
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "*.md"],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    return tuple(p for p in out if not any(p.startswith(d + "/") for d in SKIP_DIRS))


@cache
def corpus() -> dict[str, list[str]]:
    """path -> list of lines, 0-indexed (so line numbers are index + 1)."""
    return {p: (ROOT / p).read_text(encoding="utf-8").splitlines() for p in tracked_md()}


def lines_of(path: str) -> list[str]:
    return corpus().get(path, [])


def iter_lines():
    for path, lines in corpus().items():
        for i, line in enumerate(lines, start=1):
            yield path, i, line


def section(path: str, heading_re: str) -> list[tuple[int, str]]:
    """Lines of the section whose heading matches, up to the next heading of the
    same or shallower depth. Returns (line_number, text) pairs."""
    lines = lines_of(path)
    start = depth = None
    for i, line in enumerate(lines):
        m = re.match(r"^(#+)\s", line)
        if start is None:
            if m and re.search(heading_re, line):
                start, depth = i, len(m.group(1))
        elif m and len(m.group(1)) <= depth:
            return [(n + 1, lines[n]) for n in range(start + 1, i)]
    if start is None:
        return []
    return [(n + 1, lines[n]) for n in range(start + 1, len(lines))]


def table_rows(body: list[tuple[int, str]]) -> list[tuple[int, list[str]]]:
    """Markdown table rows in a section, minus header and separator."""
    rows = []
    for n, line in body:
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            rows = []           # separator: everything before it was the header
            continue
        rows.append((n, cells))
    return rows


def plain(cell: str) -> str:
    return re.sub(r"[*`]", "", cell).strip()


# --------------------------------------------------------------------------
# the authorities, parsed from the corpus rather than restated here
# --------------------------------------------------------------------------

CALENDAR = "plan/journey-calendar.md"


@cache
def calendar() -> dict[int, dict[str, str]]:
    """day -> {where, km, cum}, read from journey-calendar.md's own table."""
    days: dict[int, dict[str, str]] = {}
    for _, cells in table_rows(section(CALENDAR, r"The calendar")):
        if len(cells) < 4:
            continue
        head = plain(cells[0])
        m = re.fullmatch(rf"(\d+)(?:\s*[{DASHES}]\s*(\d+))?", head)
        if not m:
            continue
        lo = int(m.group(1))
        hi = int(m.group(2) or m.group(1))
        for d in range(lo, hi + 1):
            days[d] = {"where": plain(cells[1]), "km": plain(cells[2]), "cum": plain(cells[3])}
    return days


@cache
def day_range() -> tuple[int, int]:
    days = calendar()
    if not days:
        raise RuntimeError(f"could not parse the day table in {CALENDAR}")
    return min(days), max(days)


@cache
def british_words() -> list[str]:
    """The US-English blacklist, read out of the grep command in AGENTS.md section 5."""
    text = "\n".join(lines_of("AGENTS.md"))
    m = re.search(r"grep -InE '\\b\((.*?)\)\\b'", text)
    words = set(m.group(1).split("|")) if m else set()
    # Found in the corpus and not yet in AGENTS.md section 5. These belong there,
    # not here -- see tools/README.md, "the one place this file cheats".
    words |= {"armoured", "synthesised", "energised", "micrometres", "cruellest",
              "kilometres", "metres", "travelling", "marvellous", "sceptical"}
    return sorted(words)


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------

DAY_RUN = re.compile(
    rf"\bDays?\s+(\d+(?:\s*(?:[{DASHES}]|,|\band\b|\bto\b|\bor\b)\s*\d+)*)", re.I
)


def check_day_tokens() -> list[Violation]:
    """Every day named anywhere is a day the calendar has, and no range runs backward."""
    lo, hi = day_range()
    out = []
    for path, n, line in iter_lines():
        if path == CALENDAR:
            continue
        for m in DAY_RUN.finditer(line):
            run = m.group(1)
            for d in (int(x) for x in re.findall(r"\d+", run)):
                if not lo <= d <= hi:
                    out.append(Violation(path, n, f"Day {d} is outside the calendar's {lo}-{hi}: {m.group(0)!r}"))
            for a, b in re.findall(rf"(\d+)\s*[{DASHES}]\s*(\d+)", run):
                if int(a) >= int(b):
                    out.append(Violation(path, n, f"range runs backward or is degenerate: {m.group(0)!r}"))
    return out


def check_calendar_owns_distances() -> list[Violation]:
    """Only the calendar carries a per-day distance column. A second copy drifts;
    one did, between journey-calendar.md and body-and-resources.md section 3."""
    out = []
    for path, lines in corpus().items():
        if path == CALENDAR:
            continue
        for n, line in enumerate(lines, start=1):
            if not line.strip().startswith("|"):
                continue
            cells = [plain(c).lower() for c in line.strip().strip("|").split("|")]
            if "km" in cells and "day" in cells:
                out.append(Violation(path, n, "a table with both a 'day' and a 'km' column duplicates the calendar"))
    return out


FILE_REF = re.compile(r"`([\w./-]+\.md)`")


def check_file_refs() -> list[Violation]:
    """Every file the corpus points at exists."""
    known = set(tracked_md()) | {Path(p).name for p in tracked_md()}
    known |= EXTERNAL_REFS
    out = []
    for path, n, line in iter_lines():
        for ref in FILE_REF.findall(line):
            if ref in known or Path(ref).name in known:
                continue
            out.append(Violation(path, n, f"points at `{ref}`, which does not exist"))
    return out


SECTION_REF = re.compile(r"`([\w./-]+\.md)`\s*(?:\u00a7|section\s*)(\d+(?:\.\d+)?)")


def check_section_refs() -> list[Violation]:
    """Every `file.md` section N citation resolves to a heading numbered N in that file."""
    by_name = {Path(p).name: p for p in tracked_md()}
    out = []
    for path, n, line in iter_lines():
        for ref, num in SECTION_REF.findall(line):
            target = by_name.get(Path(ref).name)
            if target is None:
                continue                      # check_file_refs owns that failure
            # Headings in this corpus are variously "## 1. The calendar" and
            # "### **1.2 Pre-Impact Geology**", so strip emphasis before matching.
            heads = "\n".join(re.sub(r"[*_]", "", l) for l in lines_of(target) if l.startswith("#"))
            if not re.search(rf"^#+\s*{re.escape(num)}[.\s]", heads, re.M):
                out.append(Violation(path, n, f"cites `{ref}` section {num}, which has no such heading"))
    return out


FRONTMATTER = re.compile(r"^approval: (unapproved|(?:provisional|approved) \d{4}-\d{2}-\d{2})$")


def check_frontmatter() -> list[Violation]:
    """Every file carries one of exactly three approval values (AGENTS.md section 2)."""
    out = []
    for path, lines in corpus().items():
        if len(lines) < 3 or lines[0] != "---":
            out.append(Violation(path, 1, "no frontmatter block"))
            continue
        if not FRONTMATTER.match(lines[1]):
            out.append(Violation(path, 2, f"approval line is {lines[1]!r}; must be unapproved, or approved/provisional plus a date"))
    return out


def check_approval_not_stale() -> list[Violation]:
    """A file whose last commit postdates its approval has changed since it was read."""
    out = []
    for path, lines in corpus().items():
        if len(lines) < 2:
            continue
        m = re.match(r"^approval: (?:approved|provisional) (\d{4}-\d{2}-\d{2})$", lines[1])
        if not m:
            continue
        committed = subprocess.run(
            ["git", "-C", str(ROOT), "log", "-1", "--format=%ad", "--date=short", "--", path],
            capture_output=True, text=True,
        ).stdout.strip()
        if committed and committed > m.group(1):
            out.append(Violation(path, 2, f"approved {m.group(1)} but last committed {committed}"))
    return out


def check_readme_matches_frontmatter() -> list[Violation]:
    """README's approval table and the files' own frontmatter are two records of the
    same fact. They disagree for five files today, so there is no single answer to
    which files are approved. The table should be generated, not written."""
    out = []
    readme = lines_of("README.md")
    by_name = {Path(p).name: p for p in tracked_md()}
    for n, line in enumerate(readme, start=1):
        m = re.match(r"^\|\s*`([\w./-]+\.md)`\s*\|.*\|\s*(.+?)\s*\|\s*$", line)
        if not m:
            continue
        target = by_name.get(Path(m.group(1)).name)
        if target is None:
            continue
        claim = plain(m.group(2)).lower()
        # Order matters: "no. Its rows can be approved now" is a no, and a substring
        # search for "approved" reads it as a yes.
        if claim.startswith("no"):
            says = "no"
        elif claim.startswith("yes") or "approved" in claim or "reviewed" in claim:
            says = "yes"
        else:
            says = None
        head = lines_of(target)[1] if len(lines_of(target)) > 1 else ""
        state = ("approved" if head.startswith("approval: approved")
                 else "provisional" if head.startswith("approval: provisional")
                 else "unapproved")
        # Only clear disagreements. Provisional against "reviewed and corrected" is
        # a difference of register, not of fact, and the table should be generated
        # anyway -- see tools/README.md.
        if (says == "yes" and state == "unapproved") or (says == "no" and state == "approved"):
            out.append(Violation(
                "README.md", n,
                f"table says {'approved' if says == 'yes' else 'not approved'} for {m.group(1)}, "
                f"frontmatter says {state}"))
    return out


def check_us_english() -> list[Violation]:
    """US English everywhere (AGENTS.md section 5). The word list is read from AGENTS.md."""
    pattern = re.compile(rf"\b({'|'.join(british_words())})\b", re.I)
    out = []
    for path, n, line in iter_lines():
        if path == "AGENTS.md":
            continue              # the file that defines the list quotes every word in it
        for m in pattern.finditer(line):
            out.append(Violation(path, n, f"British spelling {m.group(0)!r}"))
    return out


def check_lingo_closed_list() -> list[Violation]:
    """lingo.md declares itself closed at a stated count. Count the rows and believe them."""
    path = "kb/worldbuilding/lingo.md"
    terms = [l for l in lines_of(path) if re.match(r"^\|\s*\*\*[a-z-]+\*\*", l)]
    actual = len(terms)
    out = []
    pattern = re.compile(r"closed\D{0,40}?\b(" + "|".join(NUMBER_WORDS) + r")\b", re.I)
    for p, n, line in iter_lines():
        for m in pattern.finditer(line):
            if "lingo" not in line and p != path:
                continue
            claimed = NUMBER_WORDS[m.group(1).lower()]
            if claimed != actual:
                out.append(Violation(p, n, f"claims the closed list holds {claimed} terms; {path} has {actual}"))
    return out


def check_reserved_species_unspent() -> list[Violation]:
    """milieu-allocation.md holds species in reserve and forbids spending them."""
    path = "plan/milieu-allocation.md"
    lines = lines_of(path)
    reserve: list[str] = []
    reserve_line = 0
    for n, line in enumerate(lines, start=1):
        if "held in reserve" in line:
            reserve_line = n
            reserve = [plain(x).rstrip(".") for x in line.split(":", 1)[1].split(",")]
            reserve = [r for r in (x.strip() for x in reserve) if re.fullmatch(r"[A-Z][a-z]+", r)]
            break
    out = []
    for name in reserve:
        for n, line in enumerate(lines, start=1):
            if n != reserve_line and name in line:
                out.append(Violation(path, n, f"{name} is held in reserve at line {reserve_line} and spent here"))
    return out


def check_dated_provenance() -> list[Violation]:
    """AGENTS.md section 2: approval history does not go in knowledge files -- no dates,
    no 'Daniel said', no 'struck on'. Instruction that merely names him is fine."""
    pattern = re.compile(
        r"\b(20\d{2}-\d{2}-\d{2}"
        r"|Daniel(?:'s)?\s+(?:ruling|approval|correction|decision)"
        r"|(?:struck|approved|reverted|added|removed|moved)\s+(?:on|in)\s+20\d{2})", re.I)
    out = []
    for path, n, line in iter_lines():
        if not (path.startswith("plan/") or path.startswith("kb/")):
            continue
        if n <= 3:
            continue              # the frontmatter's own date
        for m in pattern.finditer(line):
            out.append(Violation(path, n, f"dated provenance in a knowledge file: {m.group(0)!r}"))
    return out


def check_overt_plant_budget() -> list[Violation]:
    """foreshadow-and-motif.md budgets a stated number of 'overt' plants. Count them."""
    path = "plan/foreshadow-and-motif.md"
    declared = None
    for n, line in enumerate(lines_of(path), start=1):
        if "overt" in line.lower() and "|" in line:
            m = re.search(r"\*\*(" + "|".join(NUMBER_WORDS) + r")\*\*", line, re.I)
            if m:
                declared = (NUMBER_WORDS[m.group(1).lower()], n)
                break
    if declared is None:
        return []
    rows = table_rows(section(path, r"The ledger"))
    actual = sum(1 for _, cells in rows if cells and "overt" in plain(cells[-1]).lower())
    if actual != declared[0]:
        return [Violation(path, declared[1], f"budgets {declared[0]} overt plants; the ledger carries {actual}")]
    return []


CHECKS = {
    "day_tokens": check_day_tokens,
    "calendar_owns_distances": check_calendar_owns_distances,
    "file_refs": check_file_refs,
    "section_refs": check_section_refs,
    "frontmatter": check_frontmatter,
    "approval_not_stale": check_approval_not_stale,
    "readme_matches_frontmatter": check_readme_matches_frontmatter,
    "us_english": check_us_english,
    "lingo_closed_list": check_lingo_closed_list,
    "reserved_species_unspent": check_reserved_species_unspent,
    "dated_provenance": check_dated_provenance,
    "overt_plant_budget": check_overt_plant_budget,
}


def run_all() -> dict[str, list[Violation]]:
    return {name: fn() for name, fn in CHECKS.items()}
