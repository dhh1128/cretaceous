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

import sys

import pytest

from checks import CHECKS, rules


def holds(name: str) -> None:
    """Pass silently, or fail once with every violation listed."""
    violations = CHECKS[name]()
    if violations:
        listing = "\n".join(f"  {v.file}:{v.line} — {v.message}" for v in violations)
        pytest.fail(f"{len(violations)} violations:\n{listing}", pytrace=False)


_ADVISED = False

WORD_FIGURE_ADVICE = """
─── NOTE FOR THE AI READING THIS OUTPUT ───────────────────────────────────────
`shared_figures_owned` only sees figures written as DIGITS — `6 m`, `206 years`.
A figure written in WORDS is caught by `word_figures` instead, which requires the
line to carry an inline `<!-- @WF-key: value -->` claim whose value repeats the
number. Both are enforced; between them they cover the figure surface.

**So when you state a figure in words in this corpus, annotate the line.** The
key names the PROPOSITION and never the number — `@WF-route.overland: 80km`, not
`@WF-eighty`— because `claims_agree` fails on one key holding two values, and
keying by digits would collide unrelated facts that share a number.

**If a word-figure is genuinely not a shared figure, it does not get annotated —
it gets a row in `plan/figure-owners.md`'s word-form table with a reason.** *Two
days* is twenty-nine unrelated statements; *fifteen meters* is three different
heights. Annotating those would assert they are one fact, which is worse than
leaving them alone. Suggest that table to Daniel before you suggest a claim.
───────────────────────────────────────────────────────────────────────────────
"""


def _advise_on_word_figures(capsys) -> None:
    """Say the quiet part on every green run, once, where capture cannot eat it.

    `capsys.disabled()` and not a bare write to `sys.stderr` or even
    `sys.__stderr__`: pytest's default `--capture=fd` redirects the file
    descriptors themselves, so both are swallowed on a passing run -- which is
    exactly the run this needs to survive. Suspending capture is the only spelling
    that reaches a terminal."""
    global _ADVISED
    if _ADVISED:
        return
    _ADVISED = True
    with capsys.disabled():
        sys.stderr.write(WORD_FIGURE_ADVICE)
        sys.stderr.flush()


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


# --- the shape of an entry, and the order of the layers hung on it ----------

def test_no_run_of_scenes_exceeds_the_declared_pov_ceiling():
    """Red until pacing-and-stakes.md declares the ceiling. The number is Daniel's."""
    holds("pov_run_length")


def test_every_scene_entry_carries_its_required_fields():
    """A field an entry does not carry is a field no other check can read."""
    holds("scene_entry_complete")


def test_no_payoff_lands_before_its_plant():
    """A plant only works forward, and the ledger is what the drafting order reads."""
    holds("payment_order")


def test_no_retired_scene_address_survives():
    """Four of the Act 1 mappings kept their digits, so a missed one looks almost right."""
    holds("no_legacy_addresses")


# --- post-renumber: the address checks the rescene was blocking ------------

def test_every_scene_address_resolves():
    """261 references were rewritten by script in one pass; this says the pass landed."""
    holds("scene_addresses_resolve")


def test_every_requires_pointer_names_a_scene():
    """The address half is checkable; the payload half is not, and no proxy for it belongs here."""
    holds("requires_resolve")


def test_every_taxon_named_in_the_plan_exists_in_the_research():
    """milieu-brief states the precedence: the specialist file wins."""
    holds("taxa_in_research")


# --- the hooks layer ------------------------------------------------------

def test_scene_endings_match_the_measured_distribution_for_their_purpose():
    """A relationship scene settles 57% of the time; a flat hook rule writes it wrong."""
    holds("ending_distribution")


# --- the scene maps ------------------------------------------------------

def test_every_scene_map_answers_every_field_the_schema_requires():
    """A mapper cannot enumerate what he did not notice; IN is a form for that reason."""
    holds("scene_map_in_complete")


def test_every_backward_pointer_names_a_scene_and_a_move_that_exist():
    """Forward closure catches contradictions; this catches a fact that simply appeared."""
    holds("scene_map_backward_closure")


def test_every_identifier_resolves_to_the_file_that_owns_it():
    """A check cannot tell a typo from a new id unless one file owns the id space."""
    holds("identifiers_resolve")


def test_every_figure_stated_twice_has_an_owner(capsys):
    """A proposition stated once cannot contradict itself; repetition is the drift surface.

    This check is blind to half the drift surface, so it says so on the way past --
    see the note it prints. Written to `sys.__stderr__` rather than `sys.stderr`
    because pytest captures the latter and swallows it on a passing run, which is
    exactly the run where the reminder is needed."""
    holds("shared_figures_owned")
    _advise_on_word_figures(capsys)


def test_no_claim_key_is_asserted_two_ways():
    """Two assertions that are each well-formed and jointly false; nothing else sees these."""
    holds("claims_agree")
