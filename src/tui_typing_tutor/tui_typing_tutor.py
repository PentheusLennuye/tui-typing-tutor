#!/usr/bim/env python3
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

from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widgets import Header, Label


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
            yield Label(content=a, classes="keycap", id=f"{self.row_name}{x:02d}")
            x += 1


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


class TUITypingTutor(App[None]):
    """The application root window."""

    CSS_PATH = "../data/default.tcss"

    def __init__(self):
        """Initialize data structures."""
        super().__init__()
        self.keyboard = (("ad", "qwfrbyuiop"), ("ac", "asdtgmnel;"), ("ab", "zxcvbkh,./"))
        self.last = None
        self.non_alphanumerics = {".": "full_stop", ";": "semicolon", ",": "comma", "/": "slash"}

    def compose(self) -> ComposeResult:
        """Set the displays."""
        yield Header()
        yield VerticalScroll(Keyboard("Tarmak2-DHm", keyboard=self.keyboard))

    def action_keypress(self, key: str) -> None:
        """Update keyboard visual."""
        key_status = self.query(f"#{key}")
        if self.last:
            self.last.remove_class("hit")
        self.last = key_status
        key_status.add_class("hit")

    def on_mount(self) -> None:
        """Bind Keys."""
        for row in self.keyboard:
            i = 1
            for glyph in row[1]:
                if glyph not in self.non_alphanumerics:
                    self.bind(glyph, f"keypress('{row[0]}{i:02d}')")
                else:
                    self.bind(self.non_alphanumerics[glyph], f"keypress('{row[0]}{i:02d}')")
                i += 1


if __name__ == "__main__":
    app = TUITypingTutor()
    app.run()
