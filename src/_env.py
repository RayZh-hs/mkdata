"""
environment.py

The environment module contains the environment variables that are used by the interpreter to execute the script,
keeping track of the sandbox environment that the script runs in.
"""

from functools import partial

env = {
    "context": {},
    "output": partial(print, end=""),
}
