from typing import Callable, Dict

def test(inputs: Dict[str, Callable[[], str]]):
    assert("stdin" in inputs)
    n = int(inputs["stdin"]())
    
    for i in range(n):
        assert(f"file{i}" in inputs)
        assert(inputs[f"file{i}"]() == str(i))