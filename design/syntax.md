# Syntax Design

This file contains the design for the new syntax used in the mkdata project.

## Scope

In every .mkd file, @run defines a script scope, where the interpreter parses data within. Every .mkd file should only have one @run block.

```
is ignored
@run {
    # SCRIPT SCOPE
}
is ignored
```

## Line

A line defines a single statement(more precisely, a single expression), and occupies exactly one line. Empty lines are ignored.

The anatomy of a line:

```
(%)(variable: ) expression (\(n)) (comment)
```

We shall look through this line one block at a time.

1. **%** If a line starts with a %, it invokes the hidden mode, where the expression is evaluated, but nothing is outputted. In hidden mode, the suffix (\\(n)) does not work.
2. **variable** If variable is present, the result of the expression is stored within the variable.
3. **expression** The expression to be evaluated in python. This must be an eval-able expression.
4. **\\** Suffix: unless in hidden mode, the suffix is what is appended to the output. By default, ' ' is added. \\ changes the suffix to nothing, and \\n changes the suffix to a newline character.
5. **comment** A comment is a string that starts with a #. It is ignored by the interpreter.

Some examples:
```
@run {
    n: r(1, 100)        \n
    %m: n + 1
    @loop n {
        "create"
        a: r(1, 5)
        b: r(1, 5)      # this is a comment
        "query"
        % a = a * b
        a + 1           \n
    }
}
```

## Keywords

Keywords are non-python expressions starting with @. They are used to create functionality and communicates with the interpreter.

### @ redirect

```
@redirect [path: expr]
```

Redirects the output to a file specified by the expression. If path is stdout, then the output is redirected to the standard output (default behavior). This is the only keyword that can be used outside the script scope, and is advised to be used at the beginning of the file.

### @ run

```
@run {
    ...
}
```

Defines a script scope, and starts the interpreter cycle.

It is followed by a single brace block.

### @ python

```
@run {
    @python {
        ...
    }
}
```

Only available in the script scope, allowing the user to execute a python script block.

### @ loop

```
@loop [times: expr] {
    ...
}
```

The same as repeating all that is inside the block for `times` times.

### @ for

```
@for [variable: expr] in [times: expr] {
    ...
}
```

Same as @ loop, but creates a variable that updates according to the iteration count.

### @ any

```
@any
    {
        ...
    }
    {
        ...
    }
...
```

Randomly selects one of the blocks to execute, most likely to be used within a loop to create random scenarios.

```
@any
    [chance: expr] {
        ...
    }
    [chance: expr] {
        ...
    }
```

ALternatively, specify how likely each block is to be executed. An assertion error is raised if the sum of all chances is not 100%. If no chance is specified, all blocks have an equal chance.

## Predefined Functions

A set of predefined python functions are available for use in script scope. They aim to provide a simpler interface for the user to generate random data.

### Pre-imports

These modules are imported by default:

- math
- random

### Custom Functions

- rint(a, b): returns a random integer x such that a <= x < b.
- r(a, b): alias for rint.
- rdouble(a, b): returns a random float x such that a <= x < b.
- rstr(chars, len): returns a random string of length len, with characters from chars. Chars is a char-collection, which can be list of characters, or a string consisting of ranges (beg-end) and individual characters. Raw string literals are provided to the interpreter and then escaped. Specially, \\- is used to escape a dash.
