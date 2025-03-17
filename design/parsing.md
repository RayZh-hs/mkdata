# Design of Semantic Parsers

## Code Blocks

A code block is a collection of strings that define a specific region in the original source code. It is extracted from the source code and can be executed through the `execute(context)` method.

All code blocks derive from the `CodeBlock` abstract class.

Code Blocks include: PlainCodeBlock, GenCodeBlock, and PythonCodeBlock.

The interpreter, when initiated, creates a PlainCodeBlock, and calls the `execute()` method on `Interpreter.run()`. The interpreter passes on the global configurations in the context param.

## Syntax

A Syntax is a decorated code block. It contains a code block and can execute it, along with additional logic like loop repetition, random selection, etc.

```
@[id] [params] {
    [code block 1]
}
{
    [code block 2]
} {
    [code block 3]
}
```