"""
parser.py

The parser module contains the parser for syntax blocks in the MkData script.

It is responsible for turning the raw script (list of strings) to a ParsedSyntaxBlock object,
containing the id, args and list of string blocks (list of list of strings), as well as the length the script covers.
"""

import re
from copy import deepcopy
from dataclasses import dataclass, field
from typing import List

from mkdata._utils import count_indentations, remove_comments

@dataclass
class ParsedSyntaxBlock:
    """\
    class ParsedSyntaxBlock
    
    The ParsedSyntaxBlock class is a data class that contains information about a parsed syntax block.
    It is used to construct syntaxes at compile time.
    """
    
    identity: str
    args: str
    blocks: List[List[str]] = field(default_factory=list)
    end: int = 0
    
    @classmethod
    def from_script(cls, raw_script: List[str], start: int) -> "ParsedSyntaxBlock":
        """Parses a syntax block from a script starting at a given index."""
        first_line, brace_opened = cls._parse_header(raw_script[start])
        header_match = re.match(r"\s*@(?P<identity>\w+)(?P<args>.*)$", first_line)

        if not header_match:
            raise SyntaxError(f"Invalid syntax block header: '{first_line}'")

        identity = header_match.group("identity")
        args = header_match.group("args").strip()

        indent_count = count_indentations(first_line)
        blocks, end_idx = cls._parse_blocks(raw_script, start + 1, indent_count, brace_opened)

        return cls(identity=identity, args=args, blocks=blocks, end=end_idx)

    @staticmethod
    def _parse_header(line: str) -> tuple[str, bool]:
        """Parses the first line of a block and determines if it has an opening brace."""
        line = remove_comments(line)
        return (line[:-1], True) if line.endswith("{") else (line, False)

    @classmethod
    def _parse_blocks(cls, script: List[str], idx: int, indent_count: int, brace_opened: bool) -> tuple[List[List[str]], int]:
        """Extracts block content while maintaining indentation consistency."""
        blocks = []
        block_memory = []
        block_indent_memory = count_indentations(script[idx]) if idx < len(script) else 0

        while brace_opened or (idx < len(script) and count_indentations(script[idx]) >= indent_count):
            if idx >= len(script):
                raise SyntaxError("Unexpected end of script while parsing syntax block")

            line = script[idx].rstrip()

            if not line:  # Skip empty lines
                idx += 1
                continue

            if count_indentations(line) == indent_count:
                if line.lstrip().startswith("}"):
                    if not brace_opened:
                        raise SyntaxError(f"Unexpected closing brace: '{line}'")
                    brace_opened = False
                    blocks.append(deepcopy(block_memory))
                if line.endswith("{"):
                    if brace_opened:
                        raise SyntaxError(f"Unexpected opening brace: '{line}'")
                    brace_opened = True
                    block_memory.clear()
                    block_indent_memory = count_indentations(script[idx + 1])
                if not re.match(r"^\s*}?\s*{?$", line):
                    break
            else:
                if len(line) < indent_count:
                    raise SyntaxError(f"Unexpected indentation in line: '{line}'")

                if line.strip() != '':
                    block_memory.append(line[block_indent_memory:])
            
            idx += 1

        return blocks, idx


def parse_syntax_block(script: list[str], start: int) -> ParsedSyntaxBlock:
    return ParsedSyntaxBlock.from_script(script, start)


def identify_syntax_in_line(line: str):
    line = line.strip()
    if line.startswith("@"):
        return line.split()[0][1:]
    return None


if __name__ == '__main__':
    s = '''\
@redirect "./out"

stopping here
'''
    script = s.split("\n")
    a = parse_syntax_block(script, 0)
    print(a)