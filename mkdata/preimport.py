import random
from math import *  # type: ignore # noqa: F401,F403
from typing import Any, List, Optional, Self, Iterator

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

def rarray(min: int, max: int, length: int, unique: bool = True):
    """Generate an array of random integers within a specified range. Defaults to unique values.
    
    If 'unique' is True, all integers in the array will be unique.
    """
    if unique:
        if length > (max - min + 1):
            raise ValueError("Length exceeds the number of unique values in the range.")
        return random.sample(range(min, max + 1), length)
    else:
        return [random.randint(min, max) for _ in range(length)]


# Extended random utilities

def noise(value: float, min: float = 0, max: float = 0) -> float:
    """Add random noise to a given value within the specified min and max bounds."""
    if min > max:
        raise ValueError("Minimum noise cannot be greater than maximum noise.")
    return value + random.uniform(min, max) * value


# Generator utilities

class Generator:
    def __init__(self, generator: Iterator[Any], size: Optional[int] = None):
        self.iter = iter(generator)
        self.transforms = []
        self.size = size
    
    def __iter__(self):
        return self

    def __next__(self):
        val = next(self.iter)
        return self.apply_transforms(val)

    def next(self):
        val = next(self.iter)
        return self.apply_transforms(val)
    
    def transform(self, func: Any, *args, **kwargs) -> Self:
        self.transforms.append((func, args, kwargs))
        return self
    
    def apply_transforms(self, val: Any) -> Any:
        for func, args, kwargs in self.transforms:
            val = func(val, *args, **kwargs)
        return val

    @classmethod
    def from_list(cls, lst: List[Any]) -> Self:
        return cls(iter(lst), size=len(lst))
    
    @classmethod # alias for from_list
    def from_array(cls, arr: List[Any]) -> Self:
        return cls(iter(arr), size=len(arr))
    
    @classmethod
    def from_function(cls, func: Any, *args, **kwargs) -> Self:
        return cls(iter(func(*args, **kwargs)))

    @classmethod
    def of_int(cls, min: int, max: int, unique: bool = False) -> Self:
        if unique:
            if max - min + 1 <= 0:
                raise ValueError("Invalid range for unique integers.")
            return cls(iter(random.sample(range(min, max + 1), max - min + 1)))
        else:
            return cls(iter(random.randint(min, max) for _ in iter(int, 1)))
    
    @classmethod
    def of_float(cls, min: float, max: float) -> Self:
        return cls(iter(random.uniform(min, max) for _ in iter(int, 1)))
    
    @classmethod
    def int_progression(cls, lst: List[int], noise_ratio: float | tuple[float, float] = 0) -> Self:
        """Preset that generates integers based on a list with optional noise."""
        if isinstance(noise_ratio, tuple):
            min_noise, max_noise = noise_ratio
        else:
            min_noise, max_noise = -noise_ratio, 0
        return cls.from_list(lst).transform(noise, min=min_noise, max=max_noise).transform(int)