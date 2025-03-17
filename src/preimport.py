import random
from math import *
from typing import List, Optional

rint = random.randint
r = rint


def rdouble(a, b):
    return (b - a) * random.random() + a


def expand_chars(chars: str) -> str:
    result = []
    i = 0
    while i < len(chars):
        if i + 2 < len(chars) and chars[i + 1] == "-" and chars[i] != "\\":
            result.extend(chr(c) for c in range(ord(chars[i]), ord(chars[i + 2]) + 1))
            i += 3
        else:
            if chars[i] == "\\" and i + 1 < len(chars):
                i += 1  # Skip the escape character
            result.append(chars[i])
            i += 1
    return "".join(result)


def rstr(chars: str, length: int, weight: Optional[List[int]] = None) -> str:
    expanded_chars = expand_chars(chars)
    if weight and len(weight) != len(expanded_chars):
        raise ValueError(
            "Weight list must have the same length as the expanded character set."
        )
    return "".join(random.choices(expanded_chars, weights=weight, k=length))
