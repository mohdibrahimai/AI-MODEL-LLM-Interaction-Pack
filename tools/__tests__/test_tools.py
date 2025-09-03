import pytest

from tools.question_splitter import split_question
from tools.citation_deduper import dedupe_citations
from tools.tone_normalizer import normalize_tone


def test_split_question_simple():
    assert split_question("What is P and what is NP?") == ["What is P", "what is NP"]


def test_dedupe_citations():
    assert dedupe_citations(["a", "b", "a", "", "c", "b"]) == ["a", "b", "c"]


def test_normalize_tone():
    text = "It might perhaps be possible to solve this, maybe."
    assert normalize_tone(text) == "It be possible to solve this,"