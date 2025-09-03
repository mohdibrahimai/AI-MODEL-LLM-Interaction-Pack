"""Normalize the tone of answers.

The `normalize_tone` function removes common hedging words (e.g., "might",
"maybe", "perhaps") and trims extra whitespace.  It is meant to make
answers more direct and confident without changing factual content.  In a more
robust system, this function could handle register shifts or domain‑specific
style guides.
"""

from __future__ import annotations

from typing import List

__all__ = ["normalize_tone"]


def normalize_tone(text: str) -> str:
    """Return a string with hedging words removed.

    Parameters
    ----------
    text : str
        The answer text to normalise.

    Returns
    -------
    str
        The text with common hedging words removed and extra spaces collapsed.

    Examples
    --------
    >>> normalize_tone("It might perhaps be possible to solve this")
    'It be possible to solve this'
    """
    if not isinstance(text, str):
        return ""
    hedges = {"might", "maybe", "perhaps", "could", "possibly"}
    tokens: List[str] = text.split()
    filtered = [t for t in tokens if t.lower().strip(",.!?") not in hedges]
    return " ".join(filtered)


if __name__ == "__main__":  # pragma: no cover
    import sys
    print(normalize_tone(sys.stdin.read()))