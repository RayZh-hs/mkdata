"""
interpreter.py

The core interpreter of the MkData program.

Every .gen script is passed in as a string to the Interpreter constructor,
and Interpreter.run() is called to execute the script.
"""

class Interpreter:
    def __init__(self, script: str):
        self.script = script

    def run(self):
        pass
