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

import datetime as _dt
import hashlib
import re
import subprocess
from collections import defaultdict
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
def british_spellings() -> dict[str, str]:
    """British -> American, from tools/british-english.txt. 1,818 pairs, vendored.

    This replaced a hand-written list of 25 words in AGENTS.md §5. That list caught
    recurrences and nothing else: every word on it was there because someone had
    already made the mistake, which is why `plan/humour-plan.md` sat in the tree for
    days. A real difference list catches a first occurrence.
    """
    pairs, allowed = {}, set()
    for line in (ROOT / "tools" / "british-english.txt").read_text(encoding="utf-8").splitlines():
        if line.startswith("!"):
            allowed.add(line[1:].split()[0].lower())
        elif line and not line.startswith("#") and "\t" in line:
            b, a = line.split("\t", 1)
            pairs[b.lower()] = a.strip()
    return {b: a for b, a in pairs.items() if b not in allowed}


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


FRONTMATTER = re.compile(r"^approval: (unapproved|(?:provisional|approved) [0-9a-f]{8})$")


def body_hash(text: str) -> str:
    """Eight hex characters over the body, ignoring the frontmatter and trailing space.

    The marker carries this instead of a date. A date had day granularity, which this
    corpus defeats routinely, and it had to be typed and bumped by hand. A hash is
    written by tooling, is exact, survives any reformat of the frontmatter, and makes
    staleness a comparison rather than an argument about commit ordering. Re-approval
    is expressible, which a bare `approved` marker could not do: approved-to-approved
    is a no-op and git cannot see it."""
    return hashlib.sha256(_body(text).encode("utf-8")).hexdigest()[:8]


def _commit_time(*args: str) -> int | None:
    """Unix timestamp of the most recent commit matching the given log arguments."""
    out = subprocess.run(["git", "-C", str(ROOT), "log", "-1", "--format=%ct", *args],
                         capture_output=True, text=True).stdout.splitlines()
    return int(out[0]) if out and out[0].strip().isdigit() else None


def _marker_value(line: str) -> str:
    """The marker's meaning, with formatting and any legacy date stripped off."""
    m = re.match(r"^approval:\s*(approved|provisional|unapproved)\b", line.strip())
    return m.group(1) if m else ""


def _body(text: str) -> str:
    """Everything after the frontmatter block, normalized for trailing whitespace."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, min(len(lines), 8)):
            if lines[i].strip() == "---":
                lines = lines[i + 1:]
                break
    return "\n".join(l.rstrip() for l in lines).strip()


@cache
def _marker_set_at(path: str) -> tuple[int, str] | None:
    """When the marker last *changed meaning*, as a timestamp.

    Deliberately not "when line 2 last changed". Migrating every marker from
    `approved 2026-09-10` to `approved` touched line 2 of every file in the corpus,
    and a line-based answer would have read that reformat as a fresh approval --
    silently re-approving three files that were known to be stale. A check a
    formatting pass can defeat is not a check."""
    out = subprocess.run(
        ["git", "-C", str(ROOT), "log", "--format=%x00%ct %H", f"-L2,2:{path}"],
        capture_output=True, text=True).stdout
    for block in out.split("\0"):
        lines = block.splitlines()
        head = lines[0].split() if lines else []
        if len(head) != 2 or not head[0].isdigit():
            continue
        when = (int(head[0]), head[1])
        # Only the hunk body counts: "--- a/path" and "+++ b/path" are headers, not content.
        try:
            body = lines[lines.index(next(l for l in lines if l.startswith("@@"))) + 1:]
        except StopIteration:
            continue
        before = [_marker_value(l[1:]) for l in body if l.startswith("-")]
        after = [_marker_value(l[1:]) for l in body if l.startswith("+")]
        if (before[0] if before else "") != (after[0] if after else ""):
            return when          # newest commit where the meaning actually moved
    return None


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
    """A file whose body no longer hashes to what its marker records has changed
    since Daniel read it. No git, no dates, and uncommitted edits are visible."""
    out = []
    for path, lines in corpus().items():
        if len(lines) < 2:
            continue
        m = re.match(r"^approval: (?:approved|provisional) ([0-9a-f]{8})$", lines[1])
        if not m:
            continue
        now = body_hash((ROOT / path).read_text(encoding="utf-8"))
        if now != m.group(1):
            out.append(Violation(path, 2, f"body is {now}; the marker records {m.group(1)}"))
    return out


# A claim phrase, not the bare word: "is approved", "are recent and unapproved",
# "is itself unapproved". This deliberately misses "No approved prose exists yet"
# and "four [provisional] names", which are not claims about a file's marker --
# and it will also miss a trailing "Both are unapproved" that names its files a
# sentence earlier. A narrower net with no false alarms beats a wider one nobody
# trusts; see tools/README.md.
APPROVAL_WORD = re.compile(
    r"\b(?:is|are|was|were|remains?|stays?|both are|it is|itself)\s+(?:\w+\s+){0,3}(?:un)?approved\b",
    re.I)


def check_approval_stated_once() -> list[Violation]:
    """A file's approval state is stated in its own frontmatter and nowhere else.
    README used to carry a second copy and it was wrong about five files. This
    check exists so the copy does not come back."""
    names = {Path(p).name for p in tracked_md()} | set(tracked_md())
    out = []
    for path, n, line in iter_lines():
        if path == "AGENTS.md" or n <= 3:
            continue              # AGENTS.md defines the scheme; line 2 is the marker itself
        if not APPROVAL_WORD.search(line):
            continue
        named = [r for r in FILE_REF.findall(line) if r in names or Path(r).name in names]
        if named:
            out.append(Violation(path, n, f"states an approval state for {', '.join(named)}; "
                                          "the frontmatter of that file is the only place it belongs"))
    return out


def check_us_english() -> list[Violation]:
    """US English everywhere, in prose and in filenames (AGENTS.md §5)."""
    spellings = british_spellings()
    pattern = re.compile(rf"\b({'|'.join(sorted(spellings, key=len, reverse=True))})\b", re.I)
    out = []
    # Filenames count. `plan/humour-plan.md` survived for days because this check only
    # ever read line content, and nothing in the suite looked at a path.
    for path in corpus():
        for m in pattern.finditer(Path(path).name.replace("-", " ")):
            out.append(Violation(path, 1, f"British spelling in the filename: "
                                          f"{m.group(0)!r} → {spellings[m.group(0).lower()]!r}"))
    for path, n, line in iter_lines():
        # A blockquote is a verbatim quotation -- prompts/style-canon.md is built from
        # passages of Daniel's own novels. Correcting one would falsify the source.
        if line.lstrip().startswith(">"):
            continue
        for m in pattern.finditer(line):
            out.append(Violation(path, n, f"{m.group(0)!r} → {spellings[m.group(0).lower()]!r}"))
    return out


def check_closed_list_uncounted() -> list[Violation]:
    """Nobody states how many terms the closed vocabulary holds. The terms are canon;
    the count is incidental, and four files carried a number that had been wrong since
    the file was created. A fact nothing depends on is a fact that only drifts."""
    path = "kb/worldbuilding/lingo.md"
    pattern = re.compile(r"closed\D{0,40}?\b(" + "|".join(NUMBER_WORDS) + r")\b", re.I)
    out = []
    for p, n, line in iter_lines():
        if "lingo" not in line and p != path:
            continue
        for m in pattern.finditer(line):
            out.append(Violation(p, n, f"states a count for the closed list ({m.group(1)}); "
                                       "the list is closed, and its length is nobody's business"))
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
            continue              # the frontmatter fence
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


# --------------------------------------------------------------------------
# rule blocks -- see tools/RULES.md
# --------------------------------------------------------------------------

SHAPES = {
    "cardinality": "Every {every} has {has}.",
    "uniqueness": "No {every} appears in more than one {has}.",
    "bijection": "Every {every} has a matching {has}, and every {has} a matching {every}.",
    "membership": "Every {every} is drawn from {has}.",
    "ordering": "Every {every} comes before {has}.",
}
REQUIRED = ("id", "shape", "every", "has", "evidence", "status")
RULE_BLOCK = re.compile(r"^```rule\n(.*?)^```", re.M | re.S)


@dataclass(frozen=True)
class Rule:
    file: str
    line: int
    fields: dict[str, str]

    @property
    def id(self) -> str:
        return self.fields.get("id", "<no id>")

    @property
    def ratified(self) -> bool:
        return self.fields.get("status", "").startswith("ratified")

    def render(self) -> str:
        tmpl = SHAPES.get(self.fields.get("shape", ""))
        body = tmpl.format(**self.fields) if tmpl else "<unrenderable: unknown shape>"
        return f"**{self.id}** — {body} *({self.fields.get('status', '?')})*"


@cache
def rules() -> tuple[Rule, ...]:
    found = []
    for path, lines in corpus().items():
        text = "\n".join(lines)
        for m in RULE_BLOCK.finditer(text):
            line = text[: m.start()].count("\n") + 1
            fields = {}
            for raw in m.group(1).splitlines():
                if ":" in raw:
                    k, v = raw.split(":", 1)
                    fields[k.strip()] = v.strip()
            found.append(Rule(path, line, fields))
    return tuple(found)


def check_rules_wellformed() -> list[Violation]:
    """Every rule block parses, carries the required fields, uses a known shape, has a
    unique id, and -- if ratified -- names a checker that exists. Daniel ratifies; a
    session that ratifies its own rule has rebuilt the trapdoor the frontmatter had."""
    out, seen = [], {}
    for r in rules():
        for key in REQUIRED:
            if key not in r.fields:
                out.append(Violation(r.file, r.line, f"rule {r.id}: no {key!r} field"))
        if r.fields.get("shape") not in SHAPES:
            out.append(Violation(r.file, r.line, f"rule {r.id}: unknown shape {r.fields.get('shape')!r}"))
        if r.id in seen:
            out.append(Violation(r.file, r.line, f"rule id {r.id!r} is already used at {seen[r.id]}"))
        seen[r.id] = f"{r.file}:{r.line}"
        if not r.fields.get("evidence"):
            out.append(Violation(r.file, r.line, f"rule {r.id}: no evidence, so it is a guideline and must not be a test"))
        if r.ratified and r.fields.get("check") not in CHECKS:
            out.append(Violation(r.file, r.line, f"rule {r.id} is ratified but its checker {r.fields.get('check')!r} does not exist"))
    return out


ALLOC = "plan/milieu-allocation.md"


def _species_rows() -> list[tuple[int, str, list[int]]]:
    """(line, colony name or binomial, days) for each row of the species table."""
    rows = []
    for n, cells in table_rows(section(ALLOC, r"Species allocation")):
        if len(cells) < 2:
            continue
        # Rows read "*Quetzalcoatlus* — **flybeak**" or "*Haidomyrmecinae* — hell ants"
        # or bare "*Mosasaurus*". The colony name is what the sensory lists use, so
        # take the last em-dash segment, and keep a stem so Mosasaurus finds mosasaur.
        label = plain(cells[0]).split("—")[-1].strip()
        days = [int(x) for x in re.findall(r"\d+", plain(cells[1]))]
        rows.append((n, label, days))
    return rows


def _stems(label: str) -> list[str]:
    out = {label}
    if label.endswith("us"):
        out.add(label[:-2])
    if label.endswith("s"):
        out.add(label[:-1])
    return sorted(out, key=len, reverse=True)


def check_species_showcase_count() -> list[Violation]:
    """Every species row in the allocation table names at most two days."""
    return [Violation(ALLOC, n, f"{label} is allocated to {len(days)} days ({days})")
            for n, label, days in _species_rows() if len(days) > 2]


def check_allocation_day_agreement() -> list[Violation]:
    """A species named in both the allocation table and the sensory lists carries the
    same day in each. Section 5 says outright: "Each of these is owned once. The number
    is the day." They disagreed in three places after the day sweep missed section 5."""
    sensory = [(n, line) for n, line in section(ALLOC, r"Sensory allocation")
               if "·" in line]
    out = []
    for _, label, days in _species_rows():
        if not days or len(label) < 4:
            continue
        for n, line in sensory:
            for stem in _stems(label):
                hits = list(re.finditer(rf"\b{re.escape(stem)}\w*\b[^·]*?\((\d+)\)", line, re.I))
                if not hits:
                    continue
                for m in hits:
                    if int(m.group(1)) not in days:
                        out.append(Violation(ALLOC, n, f"{label} is day {days} in the species table "
                                                       f"and ({m.group(1)}) in the sensory lists"))
                break                 # longest stem that matched wins
    return out


FORESHADOW = "plan/foreshadow-and-motif.md"


def check_plant_payoff_bijection() -> list[Violation]:
    """Every plant in the ledger has a payoff and an address at both ends, and the
    reverse. The ledger's own validator asks for exactly this, in both directions."""
    out = []
    for n, cells in table_rows(section(FORESHADOW, r"The ledger")):
        if len(cells) < 5:
            out.append(Violation(FORESHADOW, n, f"ledger row has {len(cells)} cells, not 6"))
            continue
        for label, cell in (("plant", cells[1]), ("plant address", cells[2]),
                            ("payoff", cells[3]), ("payoff address", cells[4])):
            if not plain(cell) or plain(cell) in {"—", "-", "?"}:
                out.append(Violation(FORESHADOW, n, f"row {plain(cells[0])} has no {label}"))
    return out


def check_biome_covers_every_day() -> list[Violation]:
    """Every day the calendar has falls inside at least one biome band."""
    covered = set()
    for _, cells in table_rows(section(ALLOC, r"Biome bands")):
        if len(cells) < 2:
            continue
        for a, b in re.findall(rf"(\d+)(?:\s*[{DASHES}]\s*(\d+))?", plain(cells[1])):
            covered.update(range(int(a), int(b or a) + 1))
    lo, hi = day_range()
    missing = [d for d in range(lo, hi + 1) if d not in covered]
    return [Violation(ALLOC, 1, f"no biome band covers day {d}") for d in missing]


CHECKS = {
    "day_tokens": check_day_tokens,
    "rules_wellformed": check_rules_wellformed,
    "species_showcase_count": check_species_showcase_count,
    "allocation_day_agreement": check_allocation_day_agreement,
    "biome_covers_every_day": check_biome_covers_every_day,
    "plant_payoff_bijection": check_plant_payoff_bijection,
    "calendar_owns_distances": check_calendar_owns_distances,
    "file_refs": check_file_refs,
    "section_refs": check_section_refs,
    "frontmatter": check_frontmatter,
    "approval_not_stale": check_approval_not_stale,
    "approval_stated_once": check_approval_stated_once,
    "us_english": check_us_english,
    "closed_list_uncounted": check_closed_list_uncounted,
    "reserved_species_unspent": check_reserved_species_unspent,
    "dated_provenance": check_dated_provenance,
    "overt_plant_budget": check_overt_plant_budget,
}


def run_all() -> dict[str, list[Violation]]:
    return {name: fn() for name, fn in CHECKS.items()}


# --------------------------------------------------------------------------
# the rescene tier — written before the rescene so red means something
#
# The scene list is about to be rebuilt from 38 entries to roughly 69, renumbered
# sequentially, with chapters drawn over it. These checks assert the relationship
# between that list and the layers that assign work to it. They are expected to be
# RED throughout the rebuild and green at the end; the red count at the start is
# the record that green was reached by doing the work rather than by weakening a
# check. See tools/README.md.
# --------------------------------------------------------------------------

SCENES = "plan/scene-list.md"
PACING = "plan/pacing-and-stakes.md"

# Two entry formats live in the file at once: Act 1 was rescened into
# `### 4.3 — [LONG] [Day 3, pre-dawn] [KEO] …` and Acts 2-3 are still the older
# `6.2 [Day 8] [TEVA] [The River] …`. Read whichever is there; the rescene will
# settle on one and this keeps working when it does.
# The id itself is deliberately loose. Three schemes are live during the rebuild --
# `4.3` from the Act 1 rescene, `6.2` from the old act-major list, and the provisional
# day-keyed `D7.1` -- and a fourth, sequential integers, arrives at the renumber. The
# check's business is the relationship between a scene and its day, not the spelling
# of its address, so it reads whatever is there.
SCENE_ENTRY = re.compile(r"^(?:#{2,4}\s*)?([A-Za-z]?\d+(?:\.\d+)?)\s*(?:[\u2013\u2014-]\s*)?\[")
SCENE_DAY = re.compile(r"\[Day\s+(\d+)", re.I)


def scenes() -> list[tuple[int, str, str]]:
    """(line number, scene id, full entry line) for every scene in the list."""
    out = []
    for n, line in enumerate(lines_of(SCENES), start=1):
        m = SCENE_ENTRY.match(line.strip())
        if m:
            out.append((n, m.group(1), line))
    return out


def check_scene_day_tags() -> list[Violation]:
    """Every scene carries a day tag, and it is a day the calendar has.

    The safety net for the renumber: a scene that loses its day during the sweep
    stops being placeable in the world, and nothing else would notice."""
    lo, hi = day_range()
    out = []
    for n, sid, line in scenes():
        m = SCENE_DAY.search(line)
        if not m:
            out.append(Violation(SCENES, n, f"scene {sid} carries no day tag"))
        elif not lo <= int(m.group(1)) <= hi:
            out.append(Violation(SCENES, n,
                                 f"scene {sid} is tagged Day {m.group(1)}, which the calendar does not have"))
    return out


def tables(body: list[tuple[int, str]]) -> list[list[tuple[int, list[str]]]]:
    """Every markdown table in a section, separately.

    `table_rows` assumes one table per section and discards everything before each
    separator line, so a section holding three tables returns only the last one's
    rows. Sections here routinely hold several."""
    out, rows = [], []
    for n, line in body:
        if not line.strip().startswith("|"):
            if rows:
                out.append(rows)
                rows = []
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            rows = []           # separator: everything before it was the header
            continue
        rows.append((n, cells))
    if rows:
        out.append(rows)
    return out


def _proposed_per_day() -> dict[int, int]:
    """The per-day scene counts pacing-and-stakes §5 proposes, read at runtime.

    §5 holds three tables -- the act totals and one per-day table for each of Acts
    2 and 3 -- so they are read separately and the act totals fall out on the
    column count."""
    want = {}
    for rows in tables(section(PACING, r"Proposed shape")):
        for n, cells in rows:
            if len(cells) < 3:
                continue
            day, count = plain(cells[0]), plain(cells[1])
            if day.isdigit():
                m = re.search(r"\d+", count)
                if m:
                    want[int(day)] = int(m.group())
    return want


def check_scenes_per_day() -> list[Violation]:
    """Each day holds the number of scenes the pacing proposal asks for.

    This is the rescene's progress bar. It goes red on every day the rebuild has
    not reached yet and clears one day at a time. Act 1 is already rescened, so
    its days should be green from the start."""
    have = defaultdict(int)
    for _, _, line in scenes():
        m = SCENE_DAY.search(line)
        if m:
            have[int(m.group(1))] += 1
    out = []
    for day, want in sorted(_proposed_per_day().items()):
        if have[day] != want:
            out.append(Violation(PACING, 1,
                                 f"Day {day}: §5 proposes {want} scenes, the list holds {have[day]}"))
    return out


def check_act_composition() -> list[Violation]:
    """Every act holds the number of scenes its own heading claims.

    The scene list's act headings state a count; the entries under them are the
    fact. An act that says fourteen and holds nine is the failure mode a rebuild
    produces silently."""
    lines = lines_of(SCENES)
    acts, current, claimed = defaultdict(int), None, {}
    for n, line in enumerate(lines, start=1):
        if re.match(r"^##\s+ACT\b", line, re.I):
            current = line.strip()
            m = re.search(r"(\d+)\s+scenes", line, re.I)
            claimed[current] = (n, int(m.group(1))) if m else None
        elif current and SCENE_ENTRY.match(line.strip()):
            acts[current] += 1
    out = []
    for act, want in claimed.items():
        if want is None:
            continue
        n, count = want
        if acts[act] != count:
            out.append(Violation(SCENES, n,
                                 f"{act.lstrip('# ')[:28]!r} claims {count} scenes and holds {acts[act]}"))
    return out


# The word is eliminated from the corpus entirely -- not retired as an organizing
# term, and the ordinary craft sense goes with the rest. README's open-work item 5
# is the one place allowed to name it, because that is where the elimination is
# explained.
UNIT_WORD = re.compile(r"\bbeats?\b", re.I)
UNIT_WORD_EXEMPT = ("README.md",)
# `content/superseded/` and `content/rejected/` are the record of what was actually
# drafted, and two of their instances are the ordinary English word -- a wingbeat and
# a heartbeat. Rewording them would both falsify the record and change prose that is
# kept precisely as a negative example. Same exemption, same reason, as `retired_claims`.
UNIT_WORD_EXEMPT_DIRS = ("content/superseded/", "content/rejected/")


def check_eliminated_unit_word() -> list[Violation]:
    """The eliminated unit word appears nowhere outside the item that explains it.

    Reports locations only. The replacement is a rewording decision per instance --
    'worth a beat' and 'the last beat of his arc' do not take the same word -- so a
    check that proposed substitutions would be proposing prose."""
    out = []
    for path, n, line in iter_lines():
        if path in UNIT_WORD_EXEMPT or path.startswith(UNIT_WORD_EXEMPT_DIRS):
            continue
        # Blockquotes in style-canon are verbatim passages from Daniel's own
        # novels. None of them currently carries the word, but rewording one
        # would falsify the source, so the exemption is here before it is needed
        # -- the same reason `us_english` exempts quotations.
        if line.lstrip().startswith(">"):
            continue
        for m in UNIT_WORD.finditer(line):
            a, b = max(0, m.start() - 34), min(len(line), m.end() + 34)
            out.append(Violation(path, n, f"{m.group()!r} — …{line[a:b].strip()}…"))
    return out


EPIGRAPHS = "content/epigraphs.md"
LEDGER = "plan/knowledge-ledger.md"


def check_epigraph_count() -> list[Violation]:
    """The epigraph suite's declared size equals the fragments that exist.

    Three numbering systems are live in this channel and the species ladder runs
    through it, so a reader reaching for the wrong table gets the wrong fragment."""
    fragments = [n for n, line in enumerate(lines_of(EPIGRAPHS), start=1)
                 if re.match(r"^###\s+\d+\s+[–—-]", line)]
    out = []
    for n, line in enumerate(lines_of(LEDGER), start=1):
        m = re.match(r"^\*{0,2}(\w+)\*{0,2},\s*plus a coda\.?\s*$", line.strip())
        if not m:
            continue
        claimed = NUMBER_WORDS.get(m.group(1).lower())
        if claimed is None:
            continue
        if claimed + 1 != len(fragments):
            out.append(Violation(LEDGER, n,
                                 f"the suite is declared as {m.group(1)} plus a coda "
                                 f"({claimed + 1}); {EPIGRAPHS} holds {len(fragments)}"))
    return out


CHECKS.update({
    "scene_day_tags": check_scene_day_tags,
    "scenes_per_day": check_scenes_per_day,
    "act_composition": check_act_composition,
    "eliminated_unit_word": check_eliminated_unit_word,
    "epigraph_count": check_epigraph_count,
})


# --------------------------------------------------------------------------
# the content tier — the shape of the list is not the content of a scene
#
# Every check above this line asserts something about the list: how many scenes a
# day holds, whether an act's count matches its heading, whether a day tag resolves.
# All of them pass on empty stubs. These two are the first that look inside a scene,
# and they exist because a rescene pass dropped six items canon had allocated to a
# day and nothing said a word.
# --------------------------------------------------------------------------

def _allocated_by_day() -> dict[int, list[tuple[int, str]]]:
    """Items the allocation assigns to a day, from the tables that name *things*.

    The mentionable/ambient distinction needs no new column: §2's biome bands are
    ambient by nature -- a scene set in open-canopy woodland need not say so -- while
    the species and small-life tables name things that go on the page. The section
    a row lives in is the declaration."""
    out = defaultdict(list)
    for heading in (r"Species allocation", r"Small life"):
        for rows in tables(section(ALLOC, heading)):
            for n, cells in rows:
                if len(cells) < 2:
                    continue
                for a, b in re.findall(rf"(\d+)(?:\s*[{DASHES}]\s*(\d+))?", plain(cells[1])):
                    for d in range(int(a), int(b or a) + 1):
                        out[d].append((n, plain(cells[0])))
    return out


_ALLOC_STOPWORDS = frozenset({
    "herd", "wild", "from", "with", "that", "this", "them", "they", "their",
    "small", "life", "band", "relatives", "pots", "resin", "nesting",
})


def _alloc_keys(label: str) -> list[str]:
    """Search keys from a row's own label, singular and plural.

    Matched on a six-character prefix rather than the whole word, because the page
    and the table rarely agree on the ending: the allocation says *Grounders* and a
    scene says *a grounder*, the allocation says *Mosasaurus* and the scene says
    *the Mosasaur*. Four false positives came from exactly that, and stripping a
    trailing s fixed the first pair and broke the second."""
    words = [w for w in re.findall(r"[a-z]{4,}", re.sub(r"[*`]", " ", label).lower())
             if w not in _ALLOC_STOPWORDS][:3]
    return [w[:6] for w in words]


def _scene_text_by_day() -> dict[int, str]:
    text, day = defaultdict(str), None
    for n, line in enumerate(lines_of(SCENES), start=1):
        if SCENE_ENTRY.match(line.strip()):
            m = SCENE_DAY.search(line)
            day = int(m.group(1)) if m else None
        elif line.startswith("#"):
            day = None
        if day is not None:
            text[day] += " " + line.lower()
    return text


def check_allocation_covered() -> list[Violation]:
    """Every species or small-life item allocated to a day appears in a scene on it.

    **This is a net and not a proof, in both directions.** The search key is derived
    from the allocation row's own label, so a scene that names an animal by the
    colony's word while the row names it by binomial reads as a miss -- the croc is
    the standing example. The fix when it starts costing more than it catches is a
    declared key column in the allocation table, which is a change to an approved
    file and therefore Daniel's. Days with no scenes at all are skipped: their
    coverage is `scenes_per_day`'s business, and reporting it twice would double-count
    the same missing work."""
    scened = _scene_text_by_day()
    out = []
    for day, items in sorted(_allocated_by_day().items()):
        if day not in scened:
            continue
        for n, label in items:
            keys = _alloc_keys(label)
            if keys and not any(k in scened[day] for k in keys):
                out.append(Violation(ALLOC, n,
                                     f"Day {day} has scenes and none mentions {label!r}"))
    return out


LADDERS = re.compile(r"\*\*Ladders:\*\*\s*E(\d+)\s*P(\d+)\s*S(\d+)\s*X(\d+)", re.I)


def _scene_ladders() -> list[tuple[int, str, tuple[int, ...]]]:
    """(line, scene id, four ladder values) for scenes that carry them, in file order."""
    lines, out, pending = lines_of(SCENES), [], None
    for n, line in enumerate(lines, start=1):
        m = SCENE_ENTRY.match(line.strip())
        if m:
            pending = (n, m.group(1))
            continue
        if pending:
            lm = LADDERS.search(line)
            if lm:
                out.append((pending[0], pending[1], tuple(int(g) for g in lm.groups())))
                pending = None
            elif SCENE_ENTRY.match(line.strip()) or line.startswith("#"):
                pending = None
    return out


def check_every_scene_moves_a_ladder() -> list[Violation]:
    """No two consecutive scenes carry identical ladder values.

    `pacing-and-stakes.md` §6: every scene moves at least one ladder, and a scene
    that moves none is cut. Only consecutive pairs where **both** scenes carry values
    are compared, so this grows teeth as the rescene fills them in rather than
    failing on the entries that have not been rebuilt yet."""
    rungs = _scene_ladders()
    out = []
    for (_, prev_id, prev), (n, sid, cur) in zip(rungs, rungs[1:]):
        if prev == cur:
            out.append(Violation(SCENES, n,
                                 f"scene {sid} moves no ladder from {prev_id}: "
                                 f"both E{cur[0]} P{cur[1]} S{cur[2]} X{cur[3]}"))
    return out


def ladders_all_moving() -> list[tuple[str, str]]:
    """Consecutive pairs where all four ladders move. Reported, never failed.

    §6 says the ladders must not all move together, and means it about the run --
    *if all four climb in every scene the book is monotonous*. That is a ceiling on a
    rate, and no number for it exists in the corpus. Inventing one here would be the
    suite enforcing something nobody decided, so `report.py` prints the pairs and the
    proportion and leaves the judgment where it belongs."""
    rungs = _scene_ladders()
    return [(p_id, sid) for (_, p_id, p), (_, sid, c) in zip(rungs, rungs[1:])
            if all(a != b for a, b in zip(p, c))]


CHECKS.update({
    "allocation_covered": check_allocation_covered,
    "every_scene_moves_a_ladder": check_every_scene_moves_a_ladder,
})


def check_scenes_in_day_order() -> list[Violation]:
    """Scene entries appear in non-decreasing day order.

    The list is read as a sequence by anything that asks a question about
    neighbors -- `every_scene_moves_a_ladder` compares consecutive entries, and so
    will the POV-run and size-alternation checks when they exist. A block inserted
    in the wrong place makes all of them compare scenes that are not adjacent in
    story time and say nothing about it. Written after a rescene pass put Days 6
    through 9 in front of Days 4 and 5, so the file ran 3, 6, 7, 8, 9, 4, 5, 10."""
    out, prev, prev_id = [], None, None
    for n, sid, line in scenes():
        m = SCENE_DAY.search(line)
        if not m:
            continue
        day = int(m.group(1))
        if prev is not None and day < prev:
            out.append(Violation(SCENES, n,
                                 f"scene {sid} is Day {day} and follows {prev_id} on Day {prev}"))
        prev, prev_id = day, sid
    return out


CHECKS["scenes_in_day_order"] = check_scenes_in_day_order



# --------------------------------------------------------------------------
# retired claims — a ruling that is not checkable is a ruling that gets re-made
# --------------------------------------------------------------------------

RETIRED_EXEMPT_DIRS = ("content/superseded/", "content/rejected/")
RETIRED_EXEMPT_FILES = ("AGENTS.md",)


@cache
def retired_claims() -> tuple[tuple[str, str], ...]:
    """(phrase, what is true instead), read from AGENTS.md §7 at runtime."""
    out = []
    for _, cells in table_rows(section("AGENTS.md", r"Retired claims")):
        if len(cells) >= 2 and cells[0].startswith("`"):
            out.append((plain(cells[0]), plain(cells[1])))
    return tuple(out)


def check_retired_claims() -> list[Violation]:
    """No tracked file states a claim Daniel has retired.

    The failure this exists for is not that a ruling is ignored -- it is that a
    ruling is *applied by memory*, across twenty-five files, and memory misses
    some. Five rulings made on 2026-09-12 were still contradicted in live plan
    files hours later, two of them in files the session believed it had fixed.

    A line carrying `[retired]` is exempt, which is how a file cites a retired
    claim in order to correct it. Per line, so a paragraph cannot be quietly
    excused."""
    out = []
    for path, n, line in iter_lines():
        if path in RETIRED_EXEMPT_FILES or path.startswith(RETIRED_EXEMPT_DIRS):
            continue
        if "[retired]" in line:
            continue
        low = line.lower()
        for phrase, instead in retired_claims():
            if phrase.lower() in low:
                out.append(Violation(path, n, f"retired: {phrase!r} — {instead[:88]}"))
    return out


CHECKS["retired_claims"] = check_retired_claims


# --------------------------------------------------------------------------
# the shape of a scene entry, and the order of the layers hung on it
# --------------------------------------------------------------------------

LINGO = "kb/worldbuilding/lingo.md"

# The POV is the bracket immediately after the day bracket, in BOTH live entry
# formats -- `[LONG] [Day 1, evening] [TEVA] [Vitarium]` and the older
# `[Day 10] [KEO] [Open Savanna] [LOW (Hubris)]`. Reading it by position from the
# left would need a rule per format; reading it by position from the day needs
# none, and the day is the corpus's own stable key during the renumber.
BRACKETS = re.compile(r"\[([^\[\]]*)\]")
DAY_BRACKET = re.compile(r"^\s*Day\s+\d", re.I)


def _scene_fields(line: str) -> tuple[list[str], int | None]:
    """(bracketed fields, index of the day bracket) for a scene entry line."""
    fields = [b.strip() for b in BRACKETS.findall(line)]
    day_at = next((i for i, f in enumerate(fields) if DAY_BRACKET.match(f)), None)
    return fields, day_at


def scene_povs() -> list[tuple[int, str, str]]:
    """(line, scene id, POV) for every scene that names one, in file order.

    A scene carrying no POV is skipped rather than counted as a break in the run,
    because a run of one head interrupted by an entry that forgot to say whose
    head it is has not stopped being a run. `scene_entry_complete` owns that
    failure; all 70 entries name one today."""
    out = []
    for n, sid, line in scenes():
        fields, day_at = _scene_fields(line)
        if day_at is not None and day_at + 1 < len(fields):
            out.append((n, sid, fields[day_at + 1]))
    return out


@cache
def closed_vocabulary() -> frozenset[str]:
    """The colony's closed word list, read from lingo.md's own tables.

    The terms and the free compounds only -- not the bold in the surrounding
    prose, which is emphasis rather than vocabulary. Hyphenated compounds
    contribute their parts too, because a scene says *croc* where the list says
    *croc-spike*."""
    terms: set[str] = set()
    for heading in (r"^#+\s*The list", r"^#+\s*Free compounds"):
        body = section(LINGO, heading)
        # `tables`, not `table_rows`: the section holds four tables and
        # `table_rows` would return only the last one's rows, leaving the other
        # three to be scraped as prose.
        in_table = {n: cells for rows in tables(body) for n, cells in rows}
        for n, line in body:
            if n in in_table:
                found = [plain(in_table[n][0])]
            else:
                found = re.findall(r"\*\*([a-z][a-z-]*)\*\*", line)
            for term in found:
                for part in term.lower().split("-"):
                    if part:
                        terms.add(part)
    return frozenset(terms)


# `_alloc_keys` truncates each label word to six characters, so a key SHORTER
# than six is a whole short word -- and short words are the ones that collide.
# `croc`, `fish`, `ants` and `hell` between them account for most of the noise
# measured against the scene list.
MIN_OFF_DAY_KEY = 6


def check_allocation_off_day() -> list[Violation]:
    """An allocated item shows up on a day it was not allocated to.

    The inverse of `allocation_covered`, and the repetition instrument
    `milieu-allocation.md` exists to be: a world is finite, each striking thing is
    assigned to one or two days, and spending it a third time is how a book comes
    to feel small.

    **Not registered, and the reasoning is in `tools/README.md`.** Two things
    defeat it against the scene list. §3 of the allocation permits the thing this
    would fail -- *after its day it may be referenced but not re-described* -- and
    nothing mechanical separates a reference from a re-description. And the scene
    list is a plan rather than prose, so most of what fires is the plan discussing
    its own allocations. It is kept because the check it wants to be is the one
    README lists as blocked on prose, and this is the half of it that can be
    written now."""
    scened = _scene_text_by_day()
    vocabulary = closed_vocabulary()
    out = []
    allocated: dict[tuple[int, str], set[int]] = defaultdict(set)
    for day, items in _allocated_by_day().items():
        for n, label in items:
            allocated[(n, label)].add(day)
    for (n, label), days in sorted(allocated.items()):
        keys = [k for k in _alloc_keys(label)
                if len(k) >= MIN_OFF_DAY_KEY
                and not any(term.startswith(k) for term in vocabulary)]
        if not keys:
            continue
        for day in sorted(scened):
            if day in days:
                continue
            hit = [k for k in keys if re.search(rf"\b{k}\w*\b", scened[day])]
            if hit:
                out.append(Violation(ALLOC, n,
                                     f"{label!r} is allocated to {sorted(days)} and a Day {day} "
                                     f"scene names it ({', '.join(hit)})"))
    return out


POV_CEILING = re.compile(
    r"no more than\s+(" + "|".join(NUMBER_WORDS) + r"|\d+)\s+consecutive scenes?\s+in\s+one POV",
    re.I)


def _declared_pov_run() -> tuple[int, int] | None:
    """(ceiling, line) from pacing-and-stakes.md's own sentence, or None."""
    for n, line in enumerate(lines_of(PACING), start=1):
        m = POV_CEILING.search(line)
        if m:
            token = m.group(1).lower()
            return (NUMBER_WORDS.get(token, 0) or int(token)), n
    return None


def check_pov_run_length() -> list[Violation]:
    """A run of scenes in one head long enough that the rotation stops being one.

    Three POVs that take turns are a promise to the reader, and a stretch that
    forgets to rotate reads as a different book for as long as it lasts. The
    ceiling is not a number this file may choose: `pacing-and-stakes.md` owns
    scene shape and has to say it, in a sentence of the form *no more than N
    consecutive scenes in one POV*. Until it does, the check reports the missing
    declaration rather than a default, because a default invented here would be
    the suite enforcing a decision nobody made."""
    declared = _declared_pov_run()
    if declared is None:
        return [Violation(PACING, 1,
                          "no ceiling on consecutive same-POV scenes is declared anywhere; "
                          "this file owns scene shape and is where it belongs")]
    ceiling, where = declared
    povs = scene_povs()
    out, start, run = [], None, 0
    for i, (n, sid, pov) in enumerate(povs + [(0, "", None)]):
        if start is not None and pov == start[2]:
            run += 1
            continue
        if start is not None and run > ceiling:
            out.append(Violation(SCENES, start[0],
                                 f"{run} consecutive scenes in {start[2]}, from {start[1]} "
                                 f"to {povs[i - 1][1]}; {PACING}:{where} allows {ceiling}"))
        start, run = (n, sid, pov), 1
    return out


def _size_bands() -> list[str]:
    """The size vocabulary, from the sizing table in pacing-and-stakes.md §4."""
    return [plain(cells[0]).lower()
            for _, cells in table_rows(section(PACING, r"Scene sizing"))
            if cells and plain(cells[0])]


def check_scene_entry_complete() -> list[Violation]:
    """A scene entry that does not say what the format promises it says.

    Every layer downstream reads these fields off the entry: the ladders feed
    `every_scene_moves_a_ladder`, the day feeds everything indexed by day, and the
    POV feeds the rotation. An entry missing one is invisible to whichever check
    would have caught the defect, and it fails silently rather than loudly --
    `scenes_per_day` counted the day-keyed entries as absent for a whole rescene
    because the pattern that found them had not been widened yet.

    `**Hazard:**` is deliberately not required. It arrived after the format did
    and the entries that predate it are not defective for lacking it."""
    bands = _size_bands()
    lines = lines_of(SCENES)
    entries = [(i, l) for i, l in enumerate(lines) if SCENE_ENTRY.match(l.strip())]
    out = []
    for idx, (i, line) in enumerate(entries):
        end = entries[idx + 1][0] if idx + 1 < len(entries) else len(lines)
        body = "\n".join(lines[i + 1:end])
        fields, day_at = _scene_fields(line)
        missing = []
        if bands and not (fields and any(fields[0].lower().startswith(b) for b in bands)):
            missing.append("size band")
        if day_at is None:
            missing.append("day")
        else:
            if day_at + 1 >= len(fields):
                missing.append("POV")
            if day_at + 2 >= len(fields):
                missing.append("place")
        if "**Ladders:**" not in body:
            missing.append("**Ladders:**")
        if "**Ends on:**" not in body:
            missing.append("**Ends on:**")
        if missing:
            sid = SCENE_ENTRY.match(line.strip()).group(1)
            out.append(Violation(SCENES, i + 1, f"scene {sid} carries no {', '.join(missing)}"))
    return out


# Three address schemes are live in the layers at once -- `4.3` from the old
# act-major list, `D7.2` from the day-keyed rescene, and bare day references --
# and the day is the only key all three share. So the map is built from the scene
# list's own entries, and an entry that records what it used to be called
# (`*was 6.1*`) contributes that name too, since the layers still cite it.
SCENE_ALIAS = re.compile(r"\bwas (?:part of )?([A-Za-z]?\d+\.\d+)")
SCENE_ADDR = re.compile(r"\b([A-Za-z]?\d+\.\d+)\b")
DAY_ADDR = re.compile(r"\b(?:Days?|Nights?)\s+(\d+)", re.I)


@cache
def scene_days_by_address() -> dict[str, int]:
    """Every address a scene answers to -> its day. Current ids win over aliases."""
    current, aliases = {}, {}
    for _, sid, line in scenes():
        m = SCENE_DAY.search(line)
        if not m:
            continue
        day = int(m.group(1))
        current[sid] = day
        for old in SCENE_ALIAS.findall(line):
            aliases.setdefault(old, day)
    return {**aliases, **current}


@cache
def scene_position_by_address() -> dict[str, int]:
    """address -> its ordinal position in the scene list, aliases included.

    **Position in the file is the ordering, not anything parsed out of the id**,
    and that is the only way to compare two schemes at once. In the day-major
    scheme the minor number sequences the day, so `D2.5` follows `D2.3`. In the
    older scheme the *major* number does, because it was an outline unit — so
    `4.1` is late that night and `2.5` is that afternoon, and reading the minor
    number puts them backwards. `scenes_in_day_order` already guarantees the days
    ascend down the file, so file order is story order and it needs no parsing.

    Written after a corrected ledger row stayed red: the row was right and the
    comparison was wrong."""
    pos, where = {}, scene_days_by_address()
    order = {sid: i for i, (_, sid, _) in enumerate(scenes())}
    for addr in where:
        if addr in order:
            pos[addr] = order[addr]
    # aliases inherit the position of the entry that records them
    for i, (n, sid, line) in enumerate(scenes()):
        for alias in re.findall(r"\*was (?:part of )?([A-Za-z]?\d+\.\d+)\*", line):
            pos.setdefault(alias, i)
    return pos


def _addresses(cell: str) -> list[tuple[int, int | None, str]]:
    """(day, position in the scene list, as written) for every address in a cell.

    Sorted earliest first, and a bare day reference sorts ahead of a scene on the
    same day because it names the whole day rather than a position inside it."""
    where, pos = scene_days_by_address(), scene_position_by_address()
    found = [(where[tok], pos.get(tok), tok)
             for tok in SCENE_ADDR.findall(cell) if tok in where]
    found += [(int(d), None, f"Day {d}") for d in DAY_ADDR.findall(cell)]
    return sorted(found, key=lambda a: (a[0], -1 if a[1] is None else a[1]))


def unresolved_payment_addresses() -> list[tuple[int, str, str, str]]:
    """Ledger cells naming no address that resolves. Reported, never failed.

    `Act 1`, `book 2`, `13.x` and `7–9` are four different kinds of not-a-scene,
    and guessing which day any of them means would be the suite inventing an
    ordering. Whether every cited address resolves is its own invariant, and
    `tools/README.md` has it blocked on the renumber."""
    out = []
    for n, cells in table_rows(section(FORESHADOW, r"The ledger")):
        if len(cells) < 5:
            continue
        for end, cell in (("plant", plain(cells[2])), ("payoff", plain(cells[4]))):
            if not _addresses(cell):
                out.append((n, plain(cells[0]), end, cell))
    return out


def check_payment_order() -> list[Violation]:
    """A payoff that lands before the scene that plants it.

    A plant only works forward. Read in order, a payoff that arrives first is not
    a quiet plant paying off -- it is a scene explaining something the reader has
    no reason to be holding, and then a later scene setting up what they were
    already told. The ledger's addresses are what the drafting order is built
    from, so a reversed pair sends the writing pass at it backwards.

    Days rather than addresses, because three numbering schemes are live at once
    and only the day is stable. Where both ends land on the same day the position
    inside it decides, and a cell whose address resolves to nothing is left to
    `unresolved_payment_addresses` rather than guessed at."""
    out = []
    for n, cells in table_rows(section(FORESHADOW, r"The ledger")):
        if len(cells) < 5:
            continue
        plant = _addresses(plain(cells[2]))
        payoff = _addresses(plain(cells[4]))
        if not plant or not payoff:
            continue
        (p_day, p_minor, p_at), (y_day, y_minor, y_at) = plant[0], payoff[0]
        backward = y_day < p_day or (
            y_day == p_day and p_minor is not None and y_minor is not None and y_minor < p_minor)
        if backward:
            out.append(Violation(FORESHADOW, n,
                                 f"row {plain(cells[0])} plants at {p_at} (Day {p_day}) and pays "
                                 f"at {y_at} (Day {y_day}), which is earlier"))
    return out


CHECKS.update({
    "pov_run_length": check_pov_run_length,
    "scene_entry_complete": check_scene_entry_complete,
    "payment_order": check_payment_order,
})


# --------------------------------------------------------------------------
# the renumber's permanent verifier
# --------------------------------------------------------------------------

# The retired address form: a bare `N.N` where the first number was an outline
# unit. Scene ids are `D<day>.<n>` now, so any surviving bare pair is either a
# stale pointer or a number that was never an address.
LEGACY_ADDR = re.compile(r"(?<![\w.§⟪])(\d{1,2}\.\d{1,2}(?:\.\d{1,3})?)(?![\w])")
LEGACY_UNIT = re.compile(
    r"^\s*(?:[-–—]\s*[\d.]+\s*)?(m\b|km\b|kg\b|cm\b|mm\b|%|×|x\b|meters?\b|metres?\b"
    r"|tonnes?\b|hours?\b|words?\b)")
LEGACY_EXEMPT_DIRS = ("content/superseded/", "content/rejected/")
# AGENTS.md section 7 has to name what it forbids, exactly as it does for the
# retired phrases. Same file, same reason, same exemption.
LEGACY_EXEMPT_FILES = ("AGENTS.md",)


@cache
def legacy_ids() -> frozenset[str]:
    """Every retired scene address, read from AGENTS.md section 7 at runtime.

    It used to derive these from the scene list's `*was N.N*` notes, which was
    right while those notes existed and wrong the moment they came out -- the
    check would have quietly lost most of what it knew about at exactly the
    point the bridge was demolished. Declaring them makes the prohibition
    outlive the migration that produced it."""
    body = "\n".join(t for _, t in section("AGENTS.md", r"Retired claims"))
    m = re.search(r"Retired scene addresses\.\*\*(.+?)`no_legacy_addresses`", body, re.S)
    return frozenset(re.findall(r"`(\d{1,2}\.\d{1,2})`", m.group(1))) if m else frozenset()


def check_no_legacy_addresses() -> list[Violation]:
    """No file cites a scene by its retired outline-unit address.

    Scene ids are `D<day>.<n>`. The renumber that made them so had to move 261
    references, and **four of the fourteen Act 1 mappings kept their digits** --
    `2.3` became `D2.3` -- so a reference the sweep missed does not look wrong,
    it looks almost right. This is the check that makes that visible, and it is
    permanent rather than a one-off, because the failure it guards against is
    somebody writing `2.3` again from memory a month from now.

    A `*was N.N*` note is exempt: it is a deliberate citation of a dead address,
    the same case `[retired]` covers. So are the drafted scenes under
    `content/superseded/` and `content/rejected/`, which are the record of what
    was written and not a place anyone navigates from."""
    ids, out = legacy_ids(), []
    for path, n, line in iter_lines():
        if path in LEGACY_EXEMPT_FILES or path.startswith(LEGACY_EXEMPT_DIRS) or "[retired]" in line:
            continue
        for m in LEGACY_ADDR.finditer(line):
            tok = m.group(1)
            scene = tok if tok in ids else ".".join(tok.split(".")[:2])
            if scene not in ids:
                continue
            if re.search(r"\*was (?:part of )?$", line[:m.start(1)]):
                continue
            if LEGACY_UNIT.match(line[m.end(1):]):
                continue
            if re.match(r"^#{1,6}\s*\**\s*$", line[:m.start(1)]):
                continue
            out.append(Violation(path, n, f"retired address {tok!r} — scene ids are D<day>.<n>"))
    return out


CHECKS["no_legacy_addresses"] = check_no_legacy_addresses
