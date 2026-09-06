# News fragments

Every change that users should know about adds **one file** to this directory.
At release time `towncrier build --version X.Y.Z` collates them into a new
`CHANGELOG.md` section and deletes them.

## Filename

```
<issue>.<type>.md
```

* `<issue>` - the GitHub issue or PR number (e.g. `42`). If there is none, use a
  short slug prefixed with `+` (e.g. `+setuptools-scm`). The `+` keeps it out of
  the "issue" numbering.
* `<type>` - one of: `added`, `changed`, `deprecated`, `removed`, `fixed`,
  `security` (Keep a Changelog categories).

Examples: `42.added.md`, `57.fixed.md`, `+refactor-operations.changed.md`.

## Content

One entry, written in past tense as it should read in the changelog. Markdown is
fine. Example:

```
Add `tox.ini` to the `package` bootstrap. See `py_bootstrap/templates/package/tox.ini`.
```

## Commands

```
make cl-preview VERSION=X.Y.Z   # preview the collated result
make cl-check                   # what CI runs on your PR (also part of `make check`)
make cl-build VERSION=X.Y.Z     # write CHANGELOG.md and remove fragments
```

`make cut-tag VERSION=X.Y.Z` runs `cl-build` as part of cutting a release, so
you rarely call it by hand.

This `README.md` is ignored by towncrier (`ignore = ["README.md"]` in
`pyproject.toml`).
