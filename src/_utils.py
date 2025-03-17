"""
_utils.py

Utility functions used across the MkData project.
"""


def count_indentations(line: str):
    return len(line) - len(line.lstrip())


def match_counts(true_counts: int, counts: int | str):
    if type(counts) is int:
        return true_counts == counts
    if counts == "+":
        return true_counts >= 1
    if counts == "*":
        return true_counts >= 0
