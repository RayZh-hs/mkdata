from typing import Callable, Dict

def test(inputs: Dict[str, Callable[[], str]]):
    assert("file" in inputs)
    input = inputs["file"]
    
    assert(input() == "10")