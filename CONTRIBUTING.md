# Contributing to MkData

Thanks for your interest in improving MkData! This guide outlines the preferred workflow so we can review and ship contributions smoothly.

## Getting started

1. **Fork & clone** the repository, then create a feature branch from `main`.
2. **Create an isolated Python environment** (e.g. `python -m venv .venv` and `source .venv/bin/activate`).
3. **Install dependencies** in editable mode:
   - `pip install -e .`
   - `pip install pytest`
4. **Run the test suite** to make sure everything is green before and after your changes: `pytest`.

## Making changes

- Follow the existing code style. If in doubt, mirror the surrounding code.
- Add or update tests whenever you change behavior or fix a bug.
- Update documentation (`README.md`, `design/`, `examples/`) if user-facing behavior shifts.
- Record noteworthy changes in `CHANGELOG.md` under the `Unreleased` section.
- Keep commits focused and include clear, descriptive messages.

## Submitting a pull request

1. Ensure your branch is up to date with `main` and tests pass.
2. Fill in the PR template (if available) with context, screenshots, and testing notes.
3. Highlight anything that still needs work or decisions so reviewers can help quickly.

## Code of conduct

Please be respectful and inclusive. If you encounter any issues or behavior that violates these principles, reach out to the maintainers listed in `pyproject.toml`.

We appreciate your time and collaboration—thank you for helping MkData grow!
