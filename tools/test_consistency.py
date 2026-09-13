"""The fast suite. Every test here is a thin front end over a function in checks.py.

    uv run --with pytest pytest tools/            # everything deterministic, ~0.5s
    uv run --with pytest pytest tools/ -k day     # one category
    uv run --with pytest pytest tools/ -m llm     # the lens tier (not yet built)

**One test per invariant, not per violation.** The test name states the claim it
exercises, so a failing line reads as a sentence and needs no docstring to decode.
The count of failures is then the count of broken invariants rather than the count
of instances, and the instances go in the failure message as `file:line — what`,
which is the change-set row.

An earlier version parametrized each violation into its own case. It gave tidy
test ids and a badly misleading headline: thirteen dangling pointers and seven
stray dates reported as "20 failed", which reads as twenty problems and is two.
"""

from __future__ import annotations

import pytest

from checks import CHECKS, rules


def holds(name: str) -> None:
    """Pass silently, or fail once with every violation listed."""
    violations = CHECKS[name]()
    if violations:
        listing = "\n".join(f"  {v.file}:{v.line} — {v.message}" for v in violations)
        pytest.fail(f"{len(violations)} violations:\n{listing}", pytrace=False)


# --- the corpus agrees with the calendar ----------------------------------

def test_every_day_named_exists_in_the_calendar():
    """No day outside the calendar's range, and no range running backward."""
    holds("day_tokens")


def test_only_the_calendar_carries_per_day_distances():
    """A second copy of the distance column drifts. One did."""
    holds("calendar_owns_distances")


def test_every_day_falls_inside_a_biome_band():
    holds("biome_covers_every_day")


# --- pointers resolve ------------------------------------------------------

def test_every_file_reference_resolves():
    """Every `file.md` the corpus points at exists."""
    holds("file_refs")


def test_every_section_citation_resolves():
    """Every `file.md` §N finds a heading numbered N in that file."""
    holds("section_refs")


# --- approval is recorded in exactly one place -----------------------------

def test_every_file_carries_an_approval_marker():
    """One of exactly three values, per AGENTS.md §2."""
    holds("frontmatter")


def test_no_file_changed_after_it_was_approved():
    """A file committed later than its approval date has changed since he read it."""
    holds("approval_not_stale")


def test_approval_is_stated_only_in_frontmatter():
    """README carried a second copy and was wrong about five files."""
    holds("approval_stated_once")


def test_no_knowledge_file_carries_approval_history():
    """Knowledge files hold what is true; git holds how it got there."""
    holds("dated_provenance")


# --- declared budgets match their own contents -----------------------------

def test_no_count_is_stated_for_the_closed_vocabulary():
    """The terms are canon; the count was decoration that four files copied wrong."""
    holds("closed_list_uncounted")


def test_no_reserved_species_is_spent():
    holds("reserved_species_unspent")


def test_no_species_is_allocated_more_than_two_days():
    holds("species_showcase_count")


def test_species_days_agree_between_the_table_and_the_sensory_lists():
    holds("allocation_day_agreement")


def test_overt_plants_match_their_stated_budget():
    holds("overt_plant_budget")


# --- house style -----------------------------------------------------------

def test_no_british_spellings():
    holds("us_english")


# --- the rule formalism checks itself --------------------------------------

def test_every_rule_block_is_wellformed():
    """Parses, carries its fields, has evidence, and is not self-ratified."""
    holds("rules_wellformed")


def _ratified():
    found = [r for r in rules() if r.ratified and r.fields.get("check") in CHECKS]
    return found or [None]


@pytest.mark.parametrize("rule", _ratified(), ids=lambda r: r.id if r else "none-ratified")
def test_ratified_rule_holds(rule):
    """Each rule Daniel has ratified. Proposed rules are reported, never failed.

    Parametrized over rules rather than violations: a rule is an invariant, so one
    case per rule keeps the failure count meaningful."""
    if rule is None:
        pytest.skip("no rules ratified yet — see python3 tools/report.py")
    holds(rule.fields["check"])


# --- the rescene tier ------------------------------------------------------
#
# Red until the rescene is done, and that is the point. See checks.py.

def test_every_scene_carries_a_day_the_calendar_has():
    """The safety net for the renumber: a scene that loses its day is unplaceable."""
    holds("scene_day_tags")


def test_every_day_holds_the_scenes_the_pacing_proposal_asks_for():
    """The rescene's progress bar. One line clears per day rebuilt."""
    holds("scenes_per_day")


def test_every_act_holds_the_number_of_scenes_it_claims():
    """An act heading states a count; the entries under it are the fact."""
    holds("act_composition")


def test_the_eliminated_unit_word_appears_nowhere():
    """Locations only -- each instance needs its own replacement word, not a substitution."""
    holds("eliminated_unit_word")


def test_the_epigraph_suite_is_the_size_it_is_declared_to_be():
    holds("epigraph_count")


# --- the content tier ------------------------------------------------------
#
# The first checks that look inside a scene rather than at the shape of the list.

def test_every_allocated_item_appears_in_a_scene_on_its_day():
    """A net, not a proof: the key comes from the allocation row's own label."""
    holds("allocation_covered")


def test_no_two_consecutive_scenes_move_no_ladder():
    """pacing-and-stakes §6: a scene that moves none is cut."""
    holds("every_scene_moves_a_ladder")


def test_scenes_appear_in_day_order():
    """Anything that compares neighboring scenes is meaningless if the list is shuffled."""
    holds("scenes_in_day_order")


def test_no_retired_claim_survives():
    """AGENTS.md §7. A ruling applied by memory across 25 files misses some."""
    holds("retired_claims")
