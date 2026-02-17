#!/usr/bin/env bash

[ -d .venv ] || poetry install

poetry run src/tui_typing_tutor/tui_typing_tutor.py

