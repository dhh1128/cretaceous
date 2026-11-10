"""Unit tests for the three exemptions novel-method edition 1 asked the suite to make.

    uv run --with pytest pytest tools/ -k exemption

Runbook B1 and B3 (Q-QFMG): an approved file changed only under commits citing a
ruling passes the staleness check, and the spelling and provenance checks skip
verbatim quotations and the date that opens an event record. The corpus tests in
`test_consistency.py` show the checks hold on this book; these show each exemption
does what it says on inputs built to probe it, including the cases it must still
catch, so that an exemption cannot quietly widen into a hole.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

import checks


def _with_corpus(monkeypatch, files: dict[str, str], root: Path | None = None) -> None:
    monkeypatch.setattr(checks, "corpus", lambda: {p: t.splitlines() for p, t in files.items()})
    if root is not None:
        monkeypatch.setattr(checks, "ROOT", root)


FM = "---\napproval: unapproved\n---\n"


# --- verbatim quotations ---------------------------------------------------

def test_exemption_quotation_is_blanked_outside_content():
    line = 'He wrote "a likeable colour" and left.'
    out = checks.unquoted("plan/x.md", line)
    assert "colour" not in out and len(out) == len(line) and out.endswith("and left.")
    curly = "He wrote “a likeable colour” and left."
    assert "colour" not in checks.unquoted("plan/x.md", curly)


def test_exemption_quotation_does_not_cover_dialogue_in_prose():
    line = '"Mind the colour," Teva said.'
    assert checks.unquoted("content/D1.1.md", line) == line


def test_exemption_spelling_skips_quotations_and_still_catches_the_rest(monkeypatch):
    _with_corpus(monkeypatch, {
        "plan/a.md": FM + 'His words: "the colour of it".\n',
        "plan/b.md": FM + "The colour of it.\n",
        "content/c.md": FM + '"The colour of it," she said.\n',
    })
    flagged = {v.file for v in checks.check_us_english()}
    assert flagged == {"plan/b.md", "content/c.md"}


# --- dates on event records --------------------------------------------------

@pytest.mark.parametrize("line", [
    "- 2026-11-01: the first rain",
    "| 2026-11-01 | the first rain |",
    "### 2026-11-01",
    "3. **2026-11-01** the first rain",
])
def test_exemption_event_record_date_is_found(line):
    span = checks.event_date_span(line)
    assert span and line[span[0]:span[1]] == "2026-11-01"


@pytest.mark.parametrize("line", [
    "Approved on 2026-11-01 by the session.",
    "The rain came (2026-11-01).",
])
def test_exemption_a_date_inside_a_sentence_is_not_an_event_record(line):
    assert checks.event_date_span(line) is None


def test_exemption_provenance_skips_event_dates_and_quotations_and_still_catches_the_rest(monkeypatch):
    _with_corpus(monkeypatch, {
        "plan/log.md": FM + "- 2026-11-01: the first rain\n",
        "plan/quote.md": FM + 'He said "that is Daniel\'s ruling" and sat.\n',
        "plan/history.md": FM + "Struck on 2026-09-10.\n",
        "plan/second.md": FM + "- 2026-11-01: approved on 2026-11-02\n",
        "plan/ruling.md": FM + "Per Daniel's ruling, the river floods.\n",
    })
    found = sorted((v.file, v.message) for v in checks.check_dated_provenance())
    files = [f for f, _ in found]
    assert "plan/log.md" not in files and "plan/quote.md" not in files
    assert "plan/history.md" in files and "plan/ruling.md" in files
    # The leading date is exempt; the approval history after it is not.
    second = [m for f, m in found if f == "plan/second.md"]
    assert second and all("2026-11-01" not in m for m in second)


# --- approved files changed under a cited ruling -----------------------------

def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t",
                    "-c", "commit.gpgsign=false", *args], check=True, capture_output=True)


def _stamped(body: str, kind: str = "approved") -> str:
    return f"---\napproval: {kind} {checks.body_hash(body)}\n---\n{body}"


@pytest.fixture
def repo(tmp_path, monkeypatch):
    _git(tmp_path, "init", "-q")
    (tmp_path / "plan").mkdir()
    for name, kind in (("a.md", "approved"), ("p.md", "provisional")):
        (tmp_path / "plan" / name).write_text(_stamped("The river floods.\n", kind), encoding="utf-8")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "approve")

    def load():
        return {f"plan/{n}": (tmp_path / "plan" / n).read_text(encoding="utf-8").splitlines()
                for n in ("a.md", "p.md")}
    monkeypatch.setattr(checks, "corpus", load)
    monkeypatch.setattr(checks, "ROOT", tmp_path)
    return tmp_path


def _edit(repo: Path, name: str, message: str | None) -> None:
    p = repo / "plan" / name
    p.write_text(p.read_text(encoding="utf-8") + "It floods in spring.\n", encoding="utf-8")
    if message is not None:
        _git(repo, "commit", "-q", "-am", message)


def test_exemption_cited_change_to_an_approved_file_passes(repo):
    _edit(repo, "a.md", "Spring floods (Q-R9AF)")
    assert checks.check_approval_not_stale() == []


def test_exemption_uncited_change_to_an_approved_file_still_fails(repo):
    _edit(repo, "a.md", "Spring floods")
    assert [v.file for v in checks.check_approval_not_stale()] == ["plan/a.md"]


def test_exemption_uncommitted_change_to_an_approved_file_still_fails(repo):
    _edit(repo, "a.md", None)
    assert [v.file for v in checks.check_approval_not_stale()] == ["plan/a.md"]


def test_exemption_does_not_cover_provisional_files(repo):
    _edit(repo, "p.md", "Spring floods (Q-R9AF)")
    assert [v.file for v in checks.check_approval_not_stale()] == ["plan/p.md"]
