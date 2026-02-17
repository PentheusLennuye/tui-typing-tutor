---
date: 2025-12-13
tags: [python, documentation, zettel, personal knowledge management]
author: George Cummings
---

# Zettelmaker

This project creates Zettels through the use of templates. It is meant to
supplement a personal knowledge management system on Obsidian.

Much as Obsidian has a great template method (Alt-T is your friend), Obsidian is
not permitted in some workplaces due to its licensing. This library is there so
one can create zettels on a terminal.

## Licence

The code and documentation is licensed under the Apache 2.0 licence. See [LICENSE](LICENSE).


## Project layout

```text
mkdocs.yml    # The documentation configuration file.
docs/
    index.md  # The documentation homepage.
    ...       # Other markdown pages, images and other files.
examples/     # How to use the library
src/          # The executable and libraries. As it expands, so will the folders
test/         # Unit testing. Functional and integration testing are not applicable.
```

## Development

```bash
make setup
```

