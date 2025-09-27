from __future__ import annotations
import importlib.util
import io
import random
import shutil
from contextlib import ExitStack, contextmanager, redirect_stderr, redirect_stdout
from functools import partial
from pathlib import Path
from typing import Callable, Dict, Iterable

import pytest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

from mkdata._env import env  # noqa: E402
from mkdata.interpreter import Interpreter  # noqa: E402


RESOURCE_DIR = Path(__file__).parent / "resources"
DUMPS_DIR = Path(__file__).parent / "dumps"


def reset_env() -> None:
    env["context"].clear()
    env["print"] = partial(print, end="", flush=True)


def close_active_redirect() -> None:
    current = env.get("print")
    if isinstance(current, partial) and current.keywords:
        target = current.keywords.get("file")
        if target not in (None, sys.stdout, sys.stderr):
            target.close()


@contextmanager
def pushd(target: Path):
    previous = Path.cwd()
    os.chdir(target)
    try:
        yield
    finally:
        os.chdir(previous)


def make_reader(lines: Iterable[str]) -> Callable[[], str]:
    normalized = [line.strip() for line in lines]
    iterator = iter(normalized)

    def _reader() -> str:
        try:
            return next(iterator)
        except StopIteration as exc:  # pragma: no cover - mirrors input() semantics
            raise EOFError("No more data") from exc

    return _reader


def normalize_lines(raw: str) -> list[str]:
    if not raw:
        return []
    return raw.splitlines()


def build_streams(dump_dir: Path, stdout_text: str, stderr_text: str) -> Dict[str, Callable[[], str]]:
    streams: Dict[str, Callable[[], str]] = {}

    def register(name: str, text: str) -> None:
        lines = normalize_lines(text)
        if lines:
            streams[name] = make_reader(lines)

    register("stdin", stdout_text)
    register("stderr", stderr_text)

    for path in sorted(dump_dir.glob("**/*")):
        if path.is_file():
            register(str(path.relative_to(dump_dir)), path.read_text())

    return streams


def load_validator_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load validator module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def iter_resource_cases():
    for gen_path in sorted(RESOURCE_DIR.glob("*.gen")):
        validator_path = gen_path.with_suffix(".py")
        if validator_path.exists():
            yield pytest.param(gen_path, validator_path, id=gen_path.stem)


def seed_random_for_case(gen_path: Path) -> None:
    seed_value = hash(gen_path.stem) & 0xFFFFFFFF
    random.seed(seed_value)


@pytest.mark.parametrize("gen_path, validator_path", list(iter_resource_cases()))
def test_resource_generators(gen_path: Path, validator_path: Path):
    reset_env()
    seed_random_for_case(gen_path)

    script = gen_path.read_text()
    case_dump_dir = DUMPS_DIR / gen_path.stem
    if case_dump_dir.exists():
        shutil.rmtree(case_dump_dir)
    case_dump_dir.mkdir(parents=True, exist_ok=True)

    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    with ExitStack() as stack:
        stack.enter_context(redirect_stdout(stdout_buffer))
        stack.enter_context(redirect_stderr(stderr_buffer))
        stack.enter_context(pushd(case_dump_dir))
        interpreter = Interpreter(script)
        interpreter.run()

    streams = build_streams(case_dump_dir, stdout_buffer.getvalue(), stderr_buffer.getvalue())
    validator = load_validator_module(validator_path)
    validator.test(streams)

    close_active_redirect()
    reset_env()
