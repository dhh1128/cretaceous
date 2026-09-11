"""The fast suite. Every test here is a thin front end over a function in checks.py.

    uv run --with pytest pytest tools/            # everything deterministic, ~1s
    uv run --with pytest pytest tools/ -k day     # one category
    uv run --with pytest pytest tools/ -m llm     # the lens tier (not yet built)

Each violation is parametrized into its own case, so a failure reads as
`test_day_tokens[plan/tech-rules.md:21]` and the test id is the change-set row.
A clean check parametrizes to a single `[clean]` case that passes, so a check that
finds nothing still reports green rather than vanishing into a skip.
"""

from __future__ import annotations

import pytest

from checks import CHECKS, Violation


def cases(name: str):
    """Violations for one check, or a single None sentinel when it is clean."""
    found = CHECKS[name]()
    return found or [None]


def ident(v: Violation | None) -> str:
    return "clean" if v is None else str(v)


def _assert(v: Violation | None) -> None:
    assert v is None, v.message


def check(name: str):
    """Build a test function for one check, parametrized over its violations."""
    def decorator(fn):
        return pytest.mark.parametrize("v", cases(name), ids=ident)(fn)
    return decorator


@check("day_tokens")
def test_day_tokens(v):
    """Every day named anywhere exists in the calendar, and no range runs backward."""
    _assert(v)


@check("calendar_owns_distances")
def test_calendar_owns_distances(v):
    """No file but the calendar carries a per-day distance column."""
    _assert(v)


@check("file_refs")
def test_file_refs(v):
    """Every file the corpus points at exists."""
    _assert(v)


@check("section_refs")
def test_section_refs(v):
    """Every `file.md` section N citation resolves to a heading numbered N."""
    _assert(v)


@check("frontmatter")
def test_frontmatter(v):
    """Every file carries one of exactly three approval values."""
    _assert(v)


@check("approval_not_stale")
def test_approval_not_stale(v):
    """No file's last commit postdates its approval."""
    _assert(v)


@check("approval_stated_once")
def test_approval_stated_once(v):
    """A file's approval state is stated in its own frontmatter and nowhere else."""
    _assert(v)


@check("us_english")
def test_us_english(v):
    """US English everywhere."""
    _assert(v)


@check("closed_list_uncounted")
def test_closed_list_uncounted(v):
    """Nobody states how many terms the closed vocabulary holds."""
    _assert(v)


@check("reserved_species_unspent")
def test_reserved_species_unspent(v):
    """Species held in reserve are not spent in an active allocation."""
    _assert(v)


@check("dated_provenance")
def test_dated_provenance(v):
    """Knowledge files carry what is true, not how it got approved."""
    _assert(v)


@check("overt_plant_budget")
def test_overt_plant_budget(v):
    """The foreshadow ledger carries the number of overt plants it budgets."""
    _assert(v)
