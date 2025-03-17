import re

from _env import env
from _utils import remove_comments


def execute_sentence(sentence: str):
    """\
    execute a sentence, ie. a line of mkdata script
    
    a mkdata sentence is formatted as follows:
    (%)(variable: ) expression (\\(n)) (#comment)
    
    Keyword arguments:
    sentence -- the sentence to execute
    """

    silent_mode = False
    var = None
    suffix = " "
    sentence = sentence.strip()
    out_stream = env["print"]
    explicit_suffix = False

    # handle comments
    if "#" in sentence:
        # remove everything after the comment
        sentence = remove_comments(sentence)
    if sentence == "":
        return
    # handle silent mode
    if sentence.startswith("%"):
        silent_mode = True
        sentence = sentence[1:].strip()
    # handle assignment
    if m := re.search(r"^(?P<variable>\w+):", sentence):
        var = m.group("variable")
        sentence = sentence[len(var) + 1 :].strip()
    # handle suffix
    if m := re.search(r"\\(?P<suffix>[sn]?)\s*$", sentence):
        explicit_suffix = True
        if m.group("suffix") == "":
            suffix = ""
        elif m.group("suffix") == "n":
            suffix = "\n"
        # remove everything after the last backslash
        sentence = sentence[: sentence.rindex("\\")]
    # what is left should be a python expression (or nothing)
    try:
        if sentence != '':
            eval_ret = eval(sentence, env["context"], env["context"])
        else:
            eval_ret = None
        if var is not None:
            env["context"][var] = eval_ret
        if eval_ret is not None and not silent_mode:
            out_stream(str(eval_ret))
        if (eval_ret is not None or explicit_suffix) and not silent_mode:
            out_stream(suffix)
    except Exception as e:
        raise SyntaxError(f"Error while executing expression '{sentence}': {e}") from e


def execute_python_block(block: str):
    """\
    execute a block of python code
    
    Keyword arguments:
    block -- the block to execute
    """
    context = env["context"]
    try:
        exec(block, context, context)
    except Exception as e:
        raise SyntaxError(f"Error while executing python block: {e}") from e


def evaluate_python_expression(expression: str):
    """\
    evaluate a python expression
    
    Keyword arguments:
    expression -- the expression to evaluate
    """
    context = env["context"]
    try:
        return eval(expression, context, context)
    except Exception as e:
        raise SyntaxError(f"Error while evaluating python expression: {e}") from e


if __name__ == '__main__':
    execute_sentence(r"\n")