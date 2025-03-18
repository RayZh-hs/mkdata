<div align="center">
  <img src="./img/logo.png" alt="mkdata-logo" width="180">
</div>

# MkData

Simple but powerful batch data generator based on Python.

---

## Installation

### Method 1: Using pip (preferred)

Use this command system-wide or within virtual environments to install the package:

```bash
pip install mkdata
```

### Method 2: Manual installation

First clone the repository:

```bash
git clone https://github.com/RayZh-hs/mkdata.git
cd mkdata
```

You can run the following commands to build and install the package:

```bash
python -m build
pip install "$(ls dist/mkdata-*-py3-none-any.whl | sort | tail -n 1)"
```

The last line scans the `dist` directory and installs the latest wheel package.

## Usage

MkData is a command-line tool that creates batch data. When you launch the program without any arguments, it will enter input mode, where you can type in mkdata scripts, and invoke EOF to . More commonly, you would want to run the program with a script file (conventionally *.gen) using the following command:

```bash
mkdata /path/to/gen
```

If you would like to read from stdin (e.g. piping from another program), you can use the following command:

```bash
mkdata -
```

For detailed usage, run mkdata with the `-h` flag.

### Script Syntax

A .gen script is a text file. \@ is used to invoke a syntax, else each line within \@run is treated as a sentence.

Example script:

```
This will not be interpreted!

@run {
  # the interpreter will start interpreting from here
  # this is a comment
  a: r(100, 200)        # a is assigned a random integer between 100 and 200, and printed out with trailing ' '
  b: a ** 2         \n  # b is assigned a squared value of a, and printed out with trailing '\n'
  %c: a + b             # c is assigned a + b, but not printed out

  @redirect "out.out"   # this will redirect the output to out.out
  @loop c + 1 {
    # everything within the loop will be executed c + 1 times
    rstr('a-z', a)  \n  # a random string of lowercase alphabets of length a
  }
  @for i in 10 {
    # same as loop, but with i keeping track of the iteration number
    rstr('+-', i, [2,1])    \n  # a random string of +/- of length i, with +:- = 2:1 (probability)
  }
  @python {
    # this is a python block, where you can write python code
    print("Hello, world!")      # this will print "Hello, world!" to the console
    def f(x):
      return x ** 2
  }
  @redirect stdout      # this will redirect the output back to stdout           
  @loop f(a) {
    # you can nest syntaxes
    @any {
      # one of the three blocks will be executed
      rstr('a-z', 5)  \n
    } {
      rstr('A-Z', 5)  \n
    } {
      rstr('0-9', 5)  \n
    }
  }
}

You can write whatever you want here!
```

#### Prebuilt Functions

When the interpreter is launched, an environment is prepared and prebuilt functions are loaded.
These include:
1. all functions from the `math` module;
2. the random module;
3. function rint(a, b) that returns a random integer between a and b (it can be used as r(a, b));
4. function rstr(chars, n, [weights]) that returns a random string of length n, with characters from chars, and weights as the probability of each character appearing (defaults to uniform). You can write '[x]-[y]' to specify a range of characters, and use '\\-' to escape the hyphen;
5. function rfloat(a, b) that returns a random float number between a and b;

You can call them directly in your expressions. You can use \@python to define your own functions and use them at will.

#### Sentence

The anatomy of a sentence:

```
(%)(variable: ) expression (\(n)) (comment)
```
1. **%** If a line starts with a %, it invokes the hidden mode, where the expression is evaluated, but nothing is outputted. In hidden mode, the suffix (\\(n)) does not work.
2. **variable** If variable is present, the result of the expression is stored within the variable.
3. **expression** The expression to be evaluated in python. This must be an eval-able expression.
4. **\\** Suffix: unless in hidden mode, the suffix is what is appended to the output. By default, ' ' is added. \\ changes the suffix to nothing, and \\n changes the suffix to a newline character.
5. **comment** A comment is a string that starts with a #. It is ignored by the interpreter.

#### Syntax

### \@redirect

```
@redirect stdout
@redirect stderr
@redirect [path: expr]
```

Redirects the output to a std stream or file path specified by the expression.
It is advised to be used at the beginning of the file.

### \@run

```
@run {
    ...
}
```

Defines a execution scope, and starts the interpreter cycle.

It is followed by a single brace block.

### \@python

```
@python {
    ...
}
```

Allows the user to execute a python script block.

### \@loop

```
@loop [times: expr] {
    ...
}
```

The same as repeating all that is inside the block for `times` times.

### \@for

```
@for [variable: expr] in [times: expr] {
    ...
}
```
Same as @ loop, but creates a variable that updates according to the iteration count.

### \@any

```
@any {
    ...
} {
    ...
}
...
```

Randomly selects one of the blocks to execute, most likely to be used within a loop to create random scenarios.

```
@any [chance: int] [chance: int] {
    ...
} {
    ...
}
```

ALternatively, specify how likely each block is to be executed, using weights (integers).

## Attributions

The [logo](https://www.flaticon.com/free-icons/bar-chart) is designed by apien from Flaticon.