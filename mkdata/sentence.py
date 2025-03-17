from mkdata.execute import execute_sentence


class Sentence:
    def __init__(self, line: str):
        self.line = line

    def execute(self):
        execute_sentence(self.line)
