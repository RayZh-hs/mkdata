import random
from math import *  # type: ignore # noqa: F401,F403
from typing import List, Optional

# Standard random utilities

def rint(a: int, b: int) -> int:
    """Return a random integer N such that a <= N <= b."""
    return random.randint(a, b)

def r(a: int, b: int) -> int:
    """Alias for rint(a, b)."""
    return rint(a, b)

def rfloat(a, b, digits: int = 6) -> float:
    """Return a random float N such that a <= N <= b, rounded to 'digits' decimal places."""
    ans = (b - a) * random.random() + a
    return round(ans, digits)

def rstr(chars: str, length: int, weight: Optional[List[int]] = None) -> str:
    """Generate a random string of given length from the specified character set.
    
    The 'chars' parameter can include ranges like 'a-z' or '0-9'.
    The 'weight' parameter, if provided, should be a list of weights corresponding to each
    character in the expanded character set.
    """
    def _expand_chars(chars: str) -> str:
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

    expanded_chars = _expand_chars(chars)
    if weight and len(weight) != len(expanded_chars):
        raise ValueError(
            "Weight list must have the same length as the expanded character set."
        )
    return "".join(random.choices(expanded_chars, weights=weight, k=length))
