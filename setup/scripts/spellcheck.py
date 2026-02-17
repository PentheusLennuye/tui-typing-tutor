#!/usr/bin/env python
"""Using the enchant-2 module, check the spelling of a file or directory.

concise_and_catchy_name/setup/scripts/spellcheck.py Copyright 2025 George Cummings

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in
compliance with the License. You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing permissions and limitations under the
License.

Usage:
   spellcheck.py [-d <language>] [-p <personal dictionary>,...] <path>

"""

from collections import namedtuple
import pathlib
import sys

import argparse
import enchant
from enchant import checker, tokenize

DEFAULT_LANG = "en_CA"
MAX_SUGGESTIONS = 7

OK = 0
ERR_FILE = 1
ERR_SPELLING = 2
DEBUG = 3

State = namedtuple("State", ["args", "proofreader", "pwl"])


def main() -> list:
    """Start here."""
    filepaths: list = []
    state = set_state()

    if not state.args.filepaths:  # No files, no spell check!
        print("No files specified")
        return []
    for filepath in state.args.filepaths:
        filepaths += find_files(filepath)

    errors = []
    for filepath in filepaths:
        state.proofreader.set_text(read_file(filepath))
        errors += process_proofreader(state, filepath)

    return errors


def set_state() -> State:
    """Define the objects that are passed around the functions."""
    args: argparse.Namespace
    proofreader: checker.SpellChecker
    pwl: enchant.Dict

    args = parse_arguments()
    proofreader = checker.SpellChecker(
        args.dictionary,
        filters=[tokenize.EmailFilter, tokenize.URLFilter],  # type: ignore[reportArgumentType]
        chunkers=[tokenize.HTMLChunker],  # type: ignore[reportArgumentType]
    )
    if args.personal is not None:
        pwl = enchant.request_pwl_dict(args.personal)
    else:
        pwl = enchant.Dict()

    return State(args, proofreader, pwl)


def parse_arguments():
    """Pull in the user CLI command modifiers."""
    parser = argparse.ArgumentParser(
        prog="spellcheck.py", description="Check the spelling on files using the enchant-2 library"
    )
    parser.add_argument(
        "-d",
        "--dictionary",
        type=str,
        required=False,
        metavar="language",
        help="The language available on your system.",
        default=DEFAULT_LANG,
    )
    parser.add_argument(
        "-p",
        "--personal",
        type=str,
        required=False,
        metavar="pwl",
        help="A whitelist word files to supplement the main language dictionary",
    )
    parser.add_argument(
        "filepaths",
        nargs="*",  # no filepaths are ok. No spell check!
        type=str,
        help="A space-delimited list of files and paths to inspect",
    )
    return parser.parse_args()


def find_files(filepath: str) -> list:
    """Drill down a subdirectory and return the paths of all their files."""
    l_filepath = pathlib.Path(filepath)
    if l_filepath.is_file():
        return [l_filepath]

    files = list(l_filepath.rglob("**/*"))
    return [f for f in files if f.is_file()]


def read_file(filepath: str) -> str:
    """Read the contents of a file or exit the program entirely."""
    try:
        with open(filepath, "r", encoding="utf-8") as file_pointer:
            return file_pointer.read()
    except IOError as e:
        print(f"error reading file {e.filename}: {e.strerror}")
        sys.exit(ERR_FILE)


def process_proofreader(state: State, filepath: str) -> list:
    """Investigate every error found in a file and correct if possible.

    Args:
        the state, including:
            args: the user cli switches and arguments
            proofreader: the spellchecker iterator full of errors
            pwl: the personal word-list dictionary

    Returns:
        A list of tuples (filepath, word) that have not been resolved.
    """

    errors = []
    for err in state.proofreader:
        word = str(err.word)
        if state.pwl.check(word):  # If the word is in the whitelist, no foul
            continue
        print(f"{filepath}: {word} not found.")
        if learn_text(state, word):
            continue
        errors += (filepath, word)
    return errors


def learn_text(state: State, word: str) -> bool:
    """Add the word to the personal word list file or not."""
    yes_no: str = "continue"
    while yes_no not in ["Y", "y", "N", "n", ""]:
        yes_no = input(f"Add {word} to the custom dictionary [Y/n]? ").strip()
        if yes_no in ["N", "n"]:
            return False
        if yes_no not in ["Y", "y", ""]:
            continue
    state.pwl.add(word)
    print("Added")
    return True


if __name__ == "__main__":  # pragma: no cover
    results = main()
    if len(results) > 0:
        print(f"Errors: {results}")
        sys.exit(ERR_SPELLING)
