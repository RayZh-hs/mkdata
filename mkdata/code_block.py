"""
code_block.py

A code block is a block of code that can be executed.
It is an important building stone for mkdata scripts, and is used internally.

Code blocks are constructed by and exposed to the user as syntaxes, which can be thought of as decorated code blocks.
"""

from typing import List

from mkdata._base import Syntax, CodeBlock
from mkdata._env import env
from mkdata.parser import identify_syntax_in_line, parse_syntax_block
from mkdata.sentence import Sentence


class CodeBlockGen(CodeBlock):
    def __init__(self, script: list[str]):
        self.executables = []
        idx = 0
        while idx < len(script):
            line = script[idx]
            identity = identify_syntax_in_line(line)
            if identity is None:
                # This is an ordinary sentence
                self.executables.append(Sentence(line))
                idx += 1
            else:
                # This is a syntax block
                syntax = Syntax.from_identifier(identity)
                parsed_block = parse_syntax_block(script, idx)
                self.executables.append(syntax(parsed_block))
                idx = parsed_block.end

    def execute(self):
        for executable in self.executables:
            executable.execute()


class CodeBlockPython(CodeBlock):
    def __init__(self, script: List[str]):
        self.script: str = '\n'.join(script)
        self.compiled = compile(self.script, "<string>", "exec")

    def execute(self):
        exec(self.compiled, env["context"])
