"""Tools package for the interaction pack.

This file marks the directory as a Python package and exposes the core
functions for convenience imports.
"""

from .question_splitter import split_question  # noqa: F401
from .citation_deduper import dedupe_citations  # noqa: F401
from .tone_normalizer import normalize_tone  # noqa: F401