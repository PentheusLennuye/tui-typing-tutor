#!/usr/bin/env python3
"""A TUI typing exerciser in Python.

tui_typing_tutor.py Copyright 2026 George Cummings

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in
compliance with the License.

You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing permissions and limitations under the
License.


Description:

"""

import os

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widgets import Header, Label

FRUSTRATION_THRESHOLD = 5  # Mistakes in a row that signals a stop
MAX_WPM = 150
WORD_STOPS = (".", ",", ";", ":", "\t", "-", "?", " ")
TEXT_WIDTH = 70

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


# pylint: disable=too-few-public-methods


class Exercise:
    """A given text with statistics."""

    def __init__(self, text: str):
        """Initialize the stats."""
        self.text = text
        self.index = 0  # pointer to the glyph in play
        self.results = []  # an array of tuples: float time to hit, boolean error
        self.frustration = 0  # mistakes in a row


class TextRow(HorizontalGroup):
    """A row of labels."""

    def __init__(self, text: str, pos: int):
        """Create a pointer to the text."""
        super().__init__()
        self.text = text
        self.pos = pos

    def compose(self) -> ComposeResult:
        """Set up the text."""
        i = self.pos
        for glyph in self.text:
            if glyph == "\n":
                glyph = "¶"
            elif glyph == " ":
                glyph = "·"
            elif glyph == "\t":
                glyph = "     "
            yield Label(content=glyph, classes="letter", id=f"g{i}")
            i += 1


class TextArea(VerticalGroup):
    """Shows the exercise text."""

    def __init__(self, text: str):
        """Initialize the text area."""
        super().__init__()
        self.text = text

    def compose(self) -> ComposeResult:
        """Set up the text."""

        def sentence_stop(left: int):
            """Return the index of the last word stop in a string unless there is a newline"""

            text = self.text[left : left + TEXT_WIDTH]

            # Return the position of the last word stop
            index = max(map(text.rfind, WORD_STOPS))
            if index > -1:
                return left + index

            # Return the last position if there is no word stop
            return left + TEXT_WIDTH - 1

        # Ensure lines are text-wrapped ─────────────────────────────────────────────────
        left = 0  # Left index of a string segment
        right: int  # Right index of a string segment

        err = 0
        while left < len(self.text):
            err += 1

            # Each TextRow ends at the first newline, at the page width, or the end of file.
            newline_pos = self.text[left:].find("\n") + 1
            if newline_pos < 1:  # i.e., never found
                newline_pos = len(self.text)

            right = min(newline_pos, len(self.text), left + TEXT_WIDTH) - 1

            # Ensure words are not chopped.
            if self.text[right] not in WORD_STOPS:
                right = min(len(self.text) - 1, sentence_stop(left))
            yield TextRow(self.text[left : right + 1], left)
            left = right + 1


class GameArea(HorizontalGroup):
    """The text under review."""

    def __init__(self, exercise: Exercise):
        """Initialize the text area."""
        super().__init__()
        self.exercise = exercise

    def compose(self) -> ComposeResult:
        """Set up the game."""
        yield TextArea(self.exercise.text)

    def on_mount(self) -> None:
        """Reset scores and start."""
        self.query_one("#g0").remove_class("letter")
        self.query_one("#g0").add_class("index")


class Row(HorizontalGroup):
    """A 32-key minimal keyboard."""

    def __init__(self, row_name: str, glyph: str):
        """Initialize a row of keys."""
        super().__init__()
        self.alphabet = glyph
        self.row_name = row_name

    def compose(self) -> ComposeResult:
        """Create a row of keys."""
        x = 1
        for a in self.alphabet:
            yield Label(content=a.upper(), classes="keycap", id=f"{self.row_name}{x:02d}")
            x += 1


class Spacebar(HorizontalGroup):
    """A big key."""

    def compose(self) -> ComposeResult:
        """Create the spacebar."""
        yield Label(content="space", classes="space", id="SPCE")
        yield Label(content="⏎", classes="space", id="RTRN")


class Keyboard(VerticalGroup):
    """A 32-key minimal keyboard."""

    def __init__(self, name: str, keyboard: tuple):
        """Initialize a keyboard."""
        super().__init__()
        self.kb_name = name
        self.keyboard = keyboard

    def compose(self) -> ComposeResult:
        """Create a keyboard."""
        yield Label(self.kb_name, id="kb_name")
        for row in self.keyboard:
            yield Row(row[0], row[1])
        yield Spacebar()


class TUITypingTutor(App[None]):
    """The application root window."""

    CSS_PATH = "../data/default.tcss"
    BINDINGS = [
        Binding("enter", "keypress('RTRN', '\\n')"),
        Binding("space", "keypress('SPCE', ' ')"),
    ]

    def __init__(self):
        """Initialize data structures."""
        super().__init__()
        self.keyboard = (("ad", "qwfrbyuiop"), ("ac", "asdtgmnel;"), ("ab", "zxcvjkh,./"))
        self.last = None
        self.non_alphanumerics = {".": "full_stop", ";": "semicolon", ",": "comma", "/": "slash"}
        self.exercise: Exercise

        self._load_game_text()

    def _load_game_text(self):
        """Load the game text from file."""
        with open(os.path.join(DATA_DIR, "sample.txt"), encoding="utf-8") as fp:
            buffer = fp.read()
            buffer = buffer[
                0 : min(len(buffer), (MAX_WPM * 5) + 1)
            ]  # A 'word' is 5 characters including whitespace
            try:
                self.exercise = Exercise(buffer[0 : buffer.rindex(".") + 1])
            except ValueError:
                self.exercise = Exercise("Invalid sample text.")

    def compose(self) -> ComposeResult:
        """Set the displays."""
        yield Header()
        yield VerticalScroll(
            GameArea(self.exercise), Keyboard("GMC-Tarmak2-DHm", keyboard=self.keyboard)
        )

    def on_mount(self) -> None:
        """Bind Keys."""
        for row in self.keyboard:
            i = 1
            for glyph in row[1]:
                if glyph not in self.non_alphanumerics:
                    self.bind(glyph, f"keypress('{row[0]}{i:02d}', '{glyph}')")
                    self.bind(glyph.upper(), f"keypress('{row[0]}{i:02d}', '{glyph.upper()}')")
                else:
                    self.bind(
                        self.non_alphanumerics[glyph], f"keypress('{row[0]}{i:02d}', '{glyph}')"
                    )
                i += 1

    def action_keypress(self, keycode: str, glyph: str) -> None:
        """Update keyboard visual."""
        key = self.query_one(f"#{keycode}")
        if self.last:
            self.last.remove_class("hit")
        self.last = key
        key.add_class("hit")

        game_index = self.exercise.index
        target = self.query_one(f"#g{game_index}")

        if glyph != self.exercise.text[game_index]:
            target.remove_class("index")
            target.add_class("bad_index")
            return

        if target.has_class("index"):  # Not touched by badness
            target.remove_class("index")
            target.add_class("good")
        else:
            target.remove_class("bad_index")
            target.add_class("bad")

        game_index += 1
        if game_index >= len(self.exercise.text):
            raise Exception("End of exercise.")

        while self.exercise.text[game_index] == "\t":
            game_index += 1
            if game_index >= len(self.exercise.text):
                raise Exception("End of exercise.")

        # ┌────────────────────────────────────────────────────────────────────┐
        # │ End of game if the game index >= len of the text                   │
        # └────────────────────────────────────────────────────────────────────┘

        next_target = self.query_one(f"#g{game_index}")
        next_target.remove_class("letter")
        next_target.add_class("index")

        self.exercise.index = game_index


if __name__ == "__main__":
    app = TUITypingTutor()
    app.run()
