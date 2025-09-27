<div align="center">
  <img src="./public/logo.png" alt="mkdata-logo" width="180">
</div>

# MkData

> Simple but powerful batch data generator for deterministic or randomized datasets.

## Highlights

- Lean Python DSL for rapid data synthesis.
- Batch-friendly CLI with stdin streaming and file-based workflows.
- Extensible via inline Python blocks and a rich prebuilt toolbox (`math`, `random`, `rint`, `rstr`, `rfloat`).

## Installation

### From PyPI

```bash
pip install mkdata
```

### Using UV

```bash
# Assuming you have UV installed, run:
uv tool install mkdata
```

### From source

1. Clone the repository: `git clone https://github.com/RayZh-hs/mkdata.git && cd mkdata`.
2. Build a wheel: `python -m build`.
3. Install the freshest artifact: `pip install "$(ls dist/mkdata-*-py3-none-any.whl | sort | tail -n 1)"`.

## Quick start

Run a generator script (conventionally `*.gen`):

```bash
mkdata path/to/script.gen
```

Reading from stdin instead of a file:

```bash
mkdata -
```

You can find examples to run in the `examples/` directory.

### Minimal example

```
Save this file to hello.gen

@run {
  n: rint(1, 100) \n        # Random integer between 1 and 100, inclusive
  @loop n {                 # Repeat n times
    rint(1, 20)             # By default entries concat with space
  }
  \n                        # End with newline
}
```

```bash
mkdata hello.gen
```

You should see the output in `stdout`, eg.

```
5
17 3 19 8 4
```

A full set of examples is available in the `examples/` directory.

## Language overview

### Sentences

```
(%)(variable:) expression (\suffix) (# comment)
```

- `%` hides output while still evaluating the expression.
- `variable` stores the evaluated result in the runtime environment.
- `expression` must be valid Python.
- `\` suffix customizes the string appended to the output (`\n` for newline, omit for empty).

### Directives

Use `@` to introduce a directive. They can be nested and combined freely.

You must use braces `{ ... }` to denote the scope of a directive. Scopes should follow the Google convention for braces (opening brace on the same line, closing brace on its own line, unless an opening brace follows immediately).

| Directive | Purpose |
| --- | --- |
| `@run { ... }` | Defines an execution scope and starts the interpreter loop. |
| `@python { ... }` | Executes embedded Python for custom helpers. |
| `@redirect stdout\|stderr\|path` | Redirects output to standard streams or files. |
| `@loop count { ... }` | Repeats a block `count` times. |
| `@for target in iterable { ... }` | Iterates with optional index tracking. |
| `@any { ... } { ... }` | Picks one block at random (weights optional). |

## Development

1. Create a virtual environment and activate it.
2. Install locally in editable mode: `pip install -e .`.
3. Install tooling: `pip install pytest`.
4. Run the test suite: `pytest`.

Formatters, linters, and additional tooling are welcome. See `CONTRIBUTING.md` for coordination tips.

## Project links

- Contribution guide: [`CONTRIBUTING.md`](./CONTRIBUTING.md)
- Release highlights: [`CHANGELOG.md`](./CHANGELOG.md)
- License: [`LICENSE`](./LICENSE)

## Attributions

This project uses the following open source packages:
- [pytest](https://pytest.org) for end-to-end testing.

The project's [logo](https://www.flaticon.com/free-icons/bar-chart) is designed by apien from Flaticon.