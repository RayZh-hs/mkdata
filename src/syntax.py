"""
syntax.py

In mkdata scripts, syntaxes are called by the user using the @ symbol.

Syntaxes are defined in the syntax module, and are in essence wrapper classes around code blocks.
Each syntax class is a subclass of the abstract Syntax class, which defines the basic structure of a syntax.
A syntax instance, when initialized, is passed a ParsedSyntaxBlock object, which contains the parsed syntax block.
This information is used to construct code blocks within every syntax.

The construction happens in compile time.
"""

import sys
from functools import partial

from random import choices

from _base import Syntax
from _env import env

from execute import evaluate_python_expression
from parser import ParsedSyntaxBlock
from code_block import CodeBlockGen, CodeBlockPython


class SyntaxRun(Syntax):
    """\
    class SyntaxRun
    
    The SyntaxRun class defines the @run syntax block.
    
    @run is used to define an execution scope.
    Only the first execution scope will be executed by the interpreter.
    
    ```
    @run {
        [gen code block]
    }
    ```
    """

    identifier = "run"
    block_count = 1

    def __init__(self, script: ParsedSyntaxBlock):
        super().__init__(script)
        self.code_block = CodeBlockGen(script=script.blocks[0])

    def execute(self):
        self.code_block.execute()


class SyntaxRedirect(Syntax):
    """\
    class SyntaxRedirect
    
    The SyntaxRedirect class defines the @redirect syntax block.
    
    The @redirect syntax block is used to redirect the output of the print function.
    The output can be redirected to stdout, stderr, or a file (defined as a path, as a python expression).
    
    ```
    @redirect stdout
    @redirect stderr
    @redirect [expression]
    ```
    """

    identifier = "redirect"
    block_count = 0

    def __init__(self, script: ParsedSyntaxBlock):
        super().__init__(script)
        self.where = script.args

    def execute(self):
        if self.where == "stdout":
            env["print"] = partial(print, end="", flush=True, file=sys.stdout)
        elif self.where == "stderr":
            env["print"] = partial(print, end="", flush=True, file=sys.stderr)
        else:
            # The user can redirect to a file, whose path is given by the expression in self.where
            try:
                file_path = evaluate_python_expression(self.where)
            except Exception as e:
                raise RuntimeError(f"Failed to evaluate expression {self.where}") from e
            # Create a new file and redirect the print function to it
            if not (file_path := str(file_path)):
                raise RuntimeError(f"Failed to evaluate expression {self.where}")
            try:
                file_obj = open(file_path, "w")
            except Exception as e:
                raise RuntimeError(
                    f"Failed to create or access file {file_path}"
                ) from e
            env["print"] = partial(print, end="", flush=True, file=file_obj)


class SyntaxPython(Syntax):
    """\
    class SyntaxPython
    
    The SyntaxPython class defines the @python syntax block.
    
    The @python syntax block is used to execute a block of python code, that interacts directly with the context.
    
    
    ```
    @python {
        [python code block]
    }
    ```
    """

    identifier = "python"
    block_count = 1

    def __init__(self, script: ParsedSyntaxBlock):
        super().__init__(script)
        self.code_block = CodeBlockPython(script=script.blocks[0])

    def execute(self):
        self.code_block.execute()


class SyntaxLoop(Syntax):
    """\
    class SyntaxLoop
    
    The SyntaxLoop class defines the @loop syntax block.
    
    The loop syntax block is used to iterate over the gen code block within for several times.
    
    ```
    @loop [expression] {
        [gen code block]
    }
    ```
    """

    identifier = "loop"
    block_count = 1

    def __init__(self, script: ParsedSyntaxBlock):
        super().__init__(script)
        self.iterations_literal = (script.args)
        self.code_block = CodeBlockGen(script=script.blocks[0])

    def execute(self):
        iterations = evaluate_python_expression(self.iterations_literal)
        for _ in range(iterations):
            self.code_block.execute()


class SyntaxFor(Syntax):
    """\
    class SyntaxFor
    
    The SyntaxFor class defines the @for syntax block.
    
    Same as loop, but keeps track of the current iteration count in a variable.
    
    
    ```
    @for [variable] in [expression] {
        [gen code block]
    }
    ```
    """

    identifier = "for"
    block_count = 1

    def __init__(self, script: ParsedSyntaxBlock):
        super().__init__(script)
        self.variable, self.times = script.args.split(" in ")
        self.variable.strip()
        self.times.strip()
        self.code_block = CodeBlockGen(script=script.blocks[0])

    def execute(self):
        evaluated_expr = evaluate_python_expression(self.times)
        for idx in range(evaluated_expr):
            env["context"][self.variable] = idx
            self.code_block.execute()


class SyntaxAny(Syntax):
    """\
    class SyntaxAny
    
    The SyntaxAny class defines the @any syntax block.
    
    The any syntax block is used to randomly pick one of the gen code blocks to execute in an array.
    
    There are two syntax variations:
    ```
    @any {
        [gen code block]
    } {
        [gen code block]
    } ...
    ```
    In this case, the blocks are equally likely to be picked.
    
    ```
    @any [weight 1] [weight 2] ... {
        [gen code block 1]
    } {
        [gen code block 2]
    } ...
    ```
    In this case, the blocks are picked with the given probabilities.
    """

    identifier = "any"
    block_count = "+"

    def __init__(self, script: ParsedSyntaxBlock):
        super().__init__(script)
        if script.args:
            self.weights = [int(weight) for weight in script.args.split()]
        else:
            self.weights = [1] * len(script.blocks)
        self.code_blocks = [CodeBlockGen(script=block) for block in script.blocks]

    def execute(self):
        block = choices(self.code_blocks, weights=self.weights)[0]
        block.execute()
