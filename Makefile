# concise_and_catchy_name/Makefile Copyright 2025 George Cummings
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing permissions and limitations under the
# License.

.DEFAULT_GOAL := unittest
.SILENT:

# ┌───────────────────────────────────────────────────────────────────────────┐
# │                                Variables                                  │
# └───────────────────────────────────────────────────────────────────────────┘

# Directories --------------------------------------------------------------

EXAMPLES = src/examples
ME = src/tui_typing_tutor
PREF_DIR = setup/preferences
PREF_EXAMPLES = $(PREF_DIR)/examples


# Git Commands --------------------------------------------------------------

CHANGED_PYTHON_FILES=$(shell git diff --name-only main src tests | grep -E ".py\b")
CHANGED_JSON_FILES=$(shell git diff --name-only main src tests | grep -E ".json\b")
CHANGED_YAML_FILES=$(shell git diff --name-only main src tests | grep -E ".yaml\b")
CHANGED_DOC_FILES=$(shell git diff --name-only README.md docs/content)

# NixOS peculiarities -------------------------------------------------------

WRAP = $(shell [ -f /etc/NIXOS ] && echo 'nix-shell --run "')
STOP = $(shell [ -f /etc/NIXOS ] && echo '"')

# ┌───────────────────────────────────────────────────────────────────────────┐
# │                                Targets                                    │
# └───────────────────────────────────────────────────────────────────────────┘

# Environment ---------------------------------------------------------------

.PHONY: githooks
githooks:
	setup/githook_setup.sh

.PHONY: defaults 
defaults:
	[ -f code.code-workspace ] || cp $(PREF_EXAMPLES)/code.code-workspace .; \
	[ -f $(PREF_DIR)/black.toml ] || cp $(PREF_EXAMPLES)/black $(PREF_DIR)/black.toml; \
	[ -f $(PREF_DIR)/pylintc ] || cp $(PREF_EXAMPLES)/pylintrc $(PREF_DIR); \
	[ -f /etc/NIXOS ] && ([ -f $(PREF_DIR)/pylintc ] || cp $(PREF_EXAMPLES)/shell.nix .); \
	cp $(PREF_EXAMPLES)/gitignore .gitignore; \

.PHONY: venv
venv:
	$(WRAP)poetry add python@3.13$(STOP); \
	$(WRAP)poetry add -G dev pydantic pyyaml pytest pytest-cov pytest-mock \
		pytest-asyncio mkdocs mkdocs-material mkdocstrings mkdocs-version-annotations black \
		pylint pydocstyle pytest-bdd pyenchant textstat jedi-language-server$(STOP);

.PHONY: git
git:
	if [ ! -d .git ]; \
	  then \
	    git init .; git add .; git commit -m'Initial commit'; \
	    git remote add origin $(ME); \
	fi

.PHONY: setup
setup: defaults venv git githooks

# Version Control ------------------------------------------------------------

.PHONY: version-control
version-control:
	$(WRAP)poetry run setup/scripts/version_control.sh$(STOP)

# Linting --------------------------------------------------------------------

.PHONY: pylint
pylint:
	echo "Running pylint"
	poetry run pylint $(ME) $(EXAMPLES)

.PHONY: pydocstyle
pydocstyle:
	echo "Running pydocstyle..."
	poetry run pydocstyle --convention=google $(ME) $(EXAMPLES)
	echo "ok."

.PHONY: black 
black:
	echo "Running black to force formatting"
	poetry run black $(ME) $(EXAMPLES)

.PHONY: black-diff
black-diff:
	echo "Running black --check --diff"
	poetry run black --check --diff $(ME) $(EXAMPLES)

.PHONY: lint
lint: pylint pydocstyle black-diff


# Spelling --------------------------------------------------------------------

# This requires the "enchant" binary package installed on your system or home
.PHONY: spellcheck
spellcheck:
	echo "Adjusting the whitelist from code.code-workspace"; \
	$(WRAP)poetry run setup/scripts/update_pylint_dictionary.py$(STOP); \
	$(WRAP)poetry run python -c 'import enchant' || \
		(echo 'Please install enchant on your system' && false)$(STOP); \
	echo "Running a spell check on changed code"; \
	${WRAP}poetry run setup/scripts/spellcheck.py -d en_CA -p setup/dictionaries/whitelist \
	    $(CHANGED_PYTHON_FILES)$(STOP);
	echo "Running a spell check on changed docs"; \
	${WRAP}poetry run setup/scripts/spellcheck.py -d en_CA -p setup/dictionaries/whitelist \
	    $(CHANGED_DOC_FILES)$(STOP);

# Documentation --------------------------------------------------------------
.PHONY: docs
docs:
	poetry run mkdocs gh-deploy

# Testing -----------------------------------------------------------------------------
#
# The tests folder has been placed in pyproject.toml, under [tool.pytest.ini_options]
#
# -------------------------------------------------------------------------------------

.PHONY: unittest
unittest:
	echo "Running python unit tests."; \
	poetry run python -m pytest

.PHONY: coverage
coverage:
	echo "Running python unit tests for all green at 100% coverage."; \
	poetry run python -m pytest --cov --cov-report=term-missing | grep 'TOTAL.*100%'

.PHONY: detail
detail:
	echo "Running python unit tests for all green at 100% coverage."; \
	poetry run python -m pytest --cov --cov-report=term-missing

.PHONY: tests
tests: unittest coverage
