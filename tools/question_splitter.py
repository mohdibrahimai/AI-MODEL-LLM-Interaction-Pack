"""Simple heuristic for splitting a compound question into atomic subquestions.

This module provides a single function, `split_question`, that tries to decompose
a user query into separate sub‑questions.  It uses regular expressions to split
on question marks, the words "and" / "or" and commas.  It is intentionally
naïve but sufficient for demonstration purposes.
"""

from __future__ import annotations

import re
from typing import List

__all__ = ["split_question"]


def split_question(question: str) -> List[str]:
    """Split a compound question into atomic subquestions.

    Parameters
    ----------
    question : str
        The raw user question string.

    Returns
    -------
    list of str
        A list of individual subquestions with leading/trailing whitespace removed.

    Examples
    --------
    >>> split_question("What is P and what is NP?")
    ['What is P', 'what is NP']
    """
    if not isinstance(question, str):
        return []
    # Remove trailing question marks for splitting and lower‑case the conjunctions
    # Use word boundaries to avoid splitting within words.
    parts = re.split(r"\?\s*|\band\b|\bor\b|,", question, flags=re.IGNORECASE)
    cleaned = [p.strip() for p in parts if p and p.strip()]
    return cleaned


if __name__ == "__main__":  # pragma: no cover
    # Example usage when run as a script
    import sys
    for line in sys.stdin:
        subs = split_question(line.rstrip("\n"))
        print(subs)