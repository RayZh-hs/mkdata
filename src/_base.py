import abc

from _utils import match_counts
from parser import ParsedSyntaxBlock


class CodeBlock(abc.ABC):
    @abc.abstractmethod
    def __init__(self, script: list[str]):
        pass
    
    @abc.abstractmethod
    def execute(self):
        pass


class Syntax(abc.ABC):
    """\
    class Syntax
    
    A Syntax class defines a syntax block in the mkdata script.
    Syntaxes start with an @ symbol.
    """

    identifier = None
    block_count = 1

    def __init__(self, script: ParsedSyntaxBlock):
        assert(script.id == self.identifier)
        if not match_counts(len(script.blocks), self.block_count):
            raise SyntaxError(f"Syntax {self.identifier} should be followed by block count {self.block_count}, but got {len(script.blocks)}")

    @abc.abstractmethod
    def execute(self):
        pass

    @classmethod
    def from_identifier(cls, identifier: str):
        for syntax in cls.__subclasses__():
            if syntax.identifier == identifier:
                return syntax
        raise SyntaxError(f"Syntax {identifier} is not defined")
