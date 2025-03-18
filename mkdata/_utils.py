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


def remove_comments(code: str) -> str:
    in_string = False
    escape = False
    for i, char in enumerate(code):
        if char == "#" and not in_string:
            return code[:i].rstrip()
        if char in "'\"":
            if not escape:
                if in_string == char:
                    in_string = False
                elif not in_string:
                    in_string = char
        escape = (char == "\\" and not escape)
    return code.rstrip()