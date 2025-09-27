# Changelog

All notable changes to this project will be documented in this file. This format follows the principles of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Note that fixes to documentation, tests and other non-code files will **not** result in a change in version, and are therefore not listed here. List the git commit messages to view the entire history.

## [Unreleased]

- Designing and prototyping. Migration from the original gui-based `mkdata` project, now archived.

## [1.1.0]

### Added
- `mkdata` CLI for running generator scripts from files, stdin streams, or an interactive REPL.
- Interpreter directives such as `@run`, `@loop`, `@for`, `@any`, `@python`, and `@redirect`.
- Built-in helpers for random data generation (`rint`, `rstr`, `rfloat`) alongside `math` and `random` modules.
- Example generator programs and automated tests covering core interpreter flows.


## [1.1.1]

### Added
- Allow `@for` loops to iterate over any Python iterable, while maintaining backward compatibility with integer ranges.
- `@for idx, value` support for enumeration with index and value unpacking.

## [1.2.0]

### Changed
- Moved registry information to `__init__.py`.
- Update `pyproject.toml` to use latest license injection format.

### Added
- CI workflow via Github Actions for automated testing on pushes and PRs.
- PyPI publishing workflow via Github Actions.
