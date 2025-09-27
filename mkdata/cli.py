#!/usr/bin/env python3

"""
MkData

This is the entrypoint for the mkdata project.
"""

import argparse
import logging
import os
import sys

from mkdata import __version__
from mkdata.interpreter import Interpreter

def main():
    parser = argparse.ArgumentParser(description="MkData: Simple but powerful batch data generator based on Python.")
    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--verbose", action="store_true", help="enable verbose logging")
    parser.add_argument("script", type=str, help="path to .gen file, use - to read from stdin")
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)
    if args.script != '-':
        logging.info(f"Reading the script from {args.script}")
        if os.path.exists(args.script):
            with open(args.script, "r") as f:
                config = f.read()
                logging.debug(f"Read the script: {repr(config)}")
        else:
            logging.error(f"Script file {args.script} not found")
            return
    else:
        # The config is read from stdin
        logging.debug("Reading the script from stdin")
        config = ""
        for line in sys.stdin:
            config += line
            logging.debug(f"Updated script file: {repr(config)}")
        logging.debug(f"Completed script file: {repr(config)}")
    
    # Use the script to construct and launch the mkdata interpreter
    interpreter = Interpreter(config)
    interpreter.run()


if __name__ == "__main__":
    main()