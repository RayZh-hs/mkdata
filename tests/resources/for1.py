from typing import Callable, Dict

def test(inputs: Dict[str, Callable[[], str]]):
    assert(len(inputs) == 1 and "stdin" in inputs)
    input = inputs["stdin"]
    
    for i, j in enumerate([1, 3, 5]):
        assert(input() == f"{i} {j}")