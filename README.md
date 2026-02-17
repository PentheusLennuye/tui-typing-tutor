---
date: 2026-02-16
tags: [python]
author: George Cummings
---

# TUI Typing Tutor

This is a typing tutor, usable on any console. It permits easy
keyboard map additions, and can be used over a terminal rather than a
GUI.

## Licence

The code and documentation is licensed under the Apache 2.0 licence.
See the LICENSE file in the repository.

## Security

The code security policy, including how to log an issue, is in
SECURITY.md in the repository.

## Project layout

```text
.
├── CHANGELOG.md            A description of changes per version
├── docs                    Project documentation, in mkdocs format
├── Makefile                Automated tasks like environment setup, linting, and spellchecking
├── mkdocs.yml              The configuration file for the docs/ directory
├── poetry.lock
├── pyproject.toml
├── setup                   Environment support files
│   ├── dictionaries
│   ├── githooks
│   ├── githook_setup.sh
│   ├── preferences         Local preferences, see setup/preferences/examples/README.md
│   └── scripts
├── src
│   ├── tui_typing_tutor This project
│   ├── data                Supporting files such as json, text, toml, etc.
│   └── examples            How to use the code
└── tests
    ├── functional          BDD tests
    └── unit                Unit tests
```

## Development

A Python development environment is encoded within this repository. To
use it, execute:

```bash
make setup
```

### Unit and Functional Tests

```bash
make tests
```

If you want to know why coverage failed, you can run down the details.

```bash
make detail
```

Of course, since you are using test-driven development as a
discipline, you will not need it that much, will you?

### Spell Checking

```bash
make spellcheck
```

If you disagree with the spell checker, add words to
`setup/dictionaries/whitelist`.

### Linting

```bash
make lint
```

### Version Control

If you wish to confirm that you have set your version numbers against
the next-higher branch in your development framework, run the
following:

```bash
make version-control
```

It will run during `git push`, but it will only warn, not fail.

### Committing and Pushing Changes

The pre-hooks will ensure you have run static checks before pushing to
a repository.
