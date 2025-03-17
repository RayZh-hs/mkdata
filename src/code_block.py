"""
code_block.py

A code block is a block of code that can be executed.
It is an important building stone for mkdata scripts, and is used internally.

Code blocks are constructed by and exposed to the user as syntaxes, which can be thought of as decorated code blocks.
"""

from _base import Syntax, CodeBlock
from parser import identify_syntax_in_line, parse_syntax_block
from sentence import Sentence
from environment import env


class CodeBlockGen(CodeBlock):
    def __init__(self, script: list[str]):
        executables = []
        idx = 0
        while idx < len(script):
            line = script[idx]
            identity = identify_syntax_in_line(line)
            if identity is None:
                # This is an ordinary sentence
                executables.append(Sentence(line))
            else:
                # This is a syntax block
                syntax = Syntax.from_identifier(identity)
                executables.append(syntax(parse_syntax_block(script, idx)))

    def execute(self):
        for executable in self.executables:
            executable.execute()


class CodeBlockPython(CodeBlock):
    def __init__(self, script: str):
        self.script = script
        self.compiled = compile(script, "<string>", "exec")

    def execute(self):
        exec(self.compiled, env["context"])
