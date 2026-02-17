"""[A one-line summary of the module or program, ended with a period].

test_tui_typing_tutor.py Copyright 2026 George Cummings

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in
compliance with the License.

You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing permissions and limitations under the
License.


Description:

This test ensures that python unit testing works. Once the stub _tui_typing_tutor.py_
file is modified, this test can be deleted.
"""

from unittest import TestCase
from tui_typing_tutor import tui_typing_tutor as t

class TestX(TestCase):
    """Testing all the methods of class X."""

    def setUp(self):
        """Each test will use the same class, but separate objects."""
        self.x = t.X()

    def test_X_public_function_works_with_int_as_string(self):
        """The public function will return an integer from a string."""
        assert self.x.public_function("5") == 5

    def test_X_public_function_returns_none_on_bad_string(self):
        """The public function string catches a value error."""
        assert self.x.public_function("five") == None

