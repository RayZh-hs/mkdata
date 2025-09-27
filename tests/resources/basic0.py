from typing import Callable, Dict

def test(inputs: Dict[str, Callable[[], str]]):
    assert(len(inputs) == 1 and "stdin" in inputs)
    input = inputs["stdin"]
    
    n = int(input())
    assert(1 <= n <= 10)
    x = input().strip().split(' ')
    assert(len(x) == n)
    for v in x:
        assert(1 <= int(v) <= n)