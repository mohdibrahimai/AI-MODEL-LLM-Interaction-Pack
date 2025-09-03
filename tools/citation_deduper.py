"""Remove duplicate and irrelevant citations.

This module provides a simple function `dedupe_citations` that eliminates
duplicates from a list of citation identifiers.  It preserves the original
order of first occurrence and ignores falsy values.  In a real system you
might also rank or filter citations based on recency or authority.
"""

from __future__ import annotations

from typing import List

__all__ = ["dedupe_citations"]


def dedupe_citations(citations: List[str]) -> List[str]:
    """Return a list of unique citations in the order of first appearance.

    Parameters
    ----------
    citations : list of str
        A list of citation identifiers (e.g., source names or URLs).

    Returns
    -------
    list of str
        A list with duplicates removed and falsy values skipped.

    Examples
    --------
    >>> dedupe_citations(["a", "b", "a", "", "c"])
    ['a', 'b', 'c']
    """
    seen: set[str] = set()
    deduped: List[str] = []
    for item in citations or []:
        if not item:
            continue
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


if __name__ == "__main__":  # pragma: no cover
    import sys
    print(dedupe_citations([c.strip() for c in sys.stdin.readline().split()]))