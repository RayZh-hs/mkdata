"""
interpreter.py

The core interpreter of the MkData program.

Every .gen script is passed in as a string to the Interpreter constructor,
and Interpreter.run() is called to execute the script.
"""

import logging
import os

from execute import execute_python_block

from syntax import SyntaxRun, SyntaxRedirect
from parser import parse_syntax_block, ParsedSyntaxBlock


class Interpreter:
    def __init__(self, raw_script: str):
        super().__init__()
        self.script = raw_script.replace('\t', '  ').split("\n")
        self.preimport_path = os.path.join(os.path.dirname(__file__), "preimport.py")

    def run(self):
        # Before running the script, execute the preimport.py file
        with open(self.preimport_path, 'r') as f:
            preimport_contents = f.read()
            execute_python_block(preimport_contents)
        try:
            for idx, line in enumerate(self.script):
                line = line.strip()
                if line.startswith("@"):
                    # this means that the line creates a syntax block
                    if line.startswith("@redirect"):
                        # invoke the redirect syntax to redirect the output
                        # It's perhaps more efficient to do it right here
                        r_args = line[len("@redirect"):]
                        syntax = SyntaxRedirect(
                            ParsedSyntaxBlock(identity='redirect', args=r_args)
                        )
                        syntax.execute()
                        continue
                    elif line.startswith("@run"):
                        # this means that the line is a run block
                        if idx + 1 < len(self.script):
                            block = parse_syntax_block(
                                self.script, idx
                            )
                            syntax = SyntaxRun(block)
                            syntax.execute()
                        return
                    else:
                        raise SyntaxError(
                            f"Syntax block outside of execution scope: {line}"
                        )
            logging.warning(
                "No execution scope found in the .gen script. The interpreter will exit."
            )
        except SyntaxError as se:
            raise SyntaxError("Syntax Error: Raised from script execution") from se
