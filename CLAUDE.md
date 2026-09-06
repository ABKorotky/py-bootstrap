# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## File Size Rule

Applies to **every** `CLAUDE.md` in this repo — this file is always loaded, so the rule is stated
once here and never repeated in the per-directory files.

- Maximum limit: 200 rows/lines.
- Never add notes, logs, or explanations that push the file over this limit.
- Delete old or unused instructions before adding new ones.
- Don't duplicate info between CLAUDE.md files — document a thing in the directory that owns it and
  link to it from elsewhere.

## What this is

`ak-py-bootstrap` — a zero-runtime-dependency CLI (`bootstrap`) that generates Python
project skeletons from *bootstraps* (templates). Python >= 3.13 only. Package dir is
`py_bootstrap/`; distribution name is `ak-py-bootstrap`.

## Commands

Everything goes through `make` (run `make` alone for the target list). Each target
installs only the PEP 735 dependency group it needs into a single `.venv` and stamps it
in `.venv/.stamps/`, so re-runs are free.

```bash
make deps          # install the `dev` group + editable install
make format        # isort + black (write)
make cs            # isort/black --check + flake8
make ann           # mypy
make test          # tox: full suite under coverage on py313 and py314
make check         # everything the `ci` workflow runs, same targets
make doc           # sphinx-apidoc into docs/modules/ then sphinx-build into docs/build/
```

Narrower test runs (the suite is stdlib `unittest`, no pytest):

```bash
make test PY_ENV=py313
```

```bash
.venv/bin/python -m unittest tests.operations.test_build_bootstrap.DefaultBuildBootstrapOperationTestCase.test_run
```

`tox` exists *only* to run the suite across interpreters (`py313`, `py314`); every other
task lives in the `Makefile`. ... and leCoverage has `fail_under = 95`.

Line length differs by tool on purpose: black formats at 80, flake8 allows 88.

## Changelog fragments are mandatory

Every PR must add one file to `changelog.d/` named `<issue>.<type>.md`, or `+<slug>.<type>.md`
when there is no issue number (types: `added`/`changed`/`deprecated`/`removed`/`fixed`/`security`).
CI enforces this; `make cl-check` mirrors it. Version numbers come from `setuptools-scm`
tags, never from a file. Releases: `make release VERSION=X.Y.Z` publishes to the real
PyPI — pass `PYPI=testpypi` to rehearse; it refuses to run on a dirty tree.

## Architecture

`docs/concepts/architecture.md` is the canonical description and is kept current — read it
before making structural changes. The essentials:

**Operation objects, not functions.** Every unit of work is a `BaseOperation` subclass with
a `run()`. CLI-facing ones (`BaseCliOperation`) additionally have a *classmethod*
`prepare_cli_parser(parser, prefix)` that registers argparse arguments, and receive their
parsed `Namespace` via `set_cli_namespace()`. Construction takes no arguments — collaborators
are injected through `set_*` methods before `run()`. Follow this shape for new operations.

**Two-phase CLI.** `py_bootstrap/scripts/bootstrap.py` builds the parser tree by walking
operation classes, then dispatches at `run()` time by reading the subcommand out of the
namespace. Because `build`/`export` add one sub-parser per discovered bootstrap, *building
the parser already imports every bootstrap's `__entry_point__`* — parser construction must
stay side-effect free. `build_parser()` in that module is the hook `sphinx-argparse` uses to
render `docs/reference/cli.md`.

**Discovery via entry points.** Bootstraps are found through the `py_bootstrap_templates`
setuptools entry-point group (`BaseBootstrapsOperation.find_bootstraps()`). Each contributing
package points at a `...py_bootstrap.templates` module exposing `ENABLED_TEMPLATES` — a list
of subdirectory names, each of which must contain `__entry_point__.py`. This project registers
its own built-ins the same way (`py_bootstrap/templates/__init__.py`), so built-in, registered
and third-party plugin bootstraps are indistinguishable to the tool. Import failures during
discovery are logged and skipped, never raised.

**A bootstrap's `__entry_point__.py`** must define module-level `DESCRIPTION` plus
`BuildOperation` and `ExportOperation` classes — `register` validates by string-searching the
file for those two names. Subclass `DefaultBuildBootstrapOperation` to get the standard
`--name`/`--description` options and the derived `python_name`/`upper_name`/`class_name`/`title`
placeholders; subclass `BaseBuildBootstrapOperation` directly for something bespoke. Override
`build_context()` and always `super()` into it.

**Files processors** (`py_bootstrap/files_processors/`) do the actual walking and writing.
`CopyFilesProcessor` copies verbatim (used by `export` and `register`);
`GenerateFilesProcessor` subclasses it and adds templating (used by `build`).

### Templating rules (easy to get wrong)

- Rendering is plain `str.format(**context)` — the context is a flat `str -> str` map. Literal
  braces in template content must be doubled.
- **Destination paths are rendered too**, not just file content. Hence a directory named
  `{python_name}/` in a bootstrap becomes a directory named after the project.
- A file is templated only if it ends in `.tmpl`; the suffix is stripped on output. To emit a
  file that itself ends in `.tmpl`, name it `*.tmpl.tmpl` (see `templates/bootstrap/`).
- `{empty}` renders to `""` and exists so template files can produce dotfiles:
  `{empty}.gitignore.tmpl` -> `.gitignore`. A bare `.gitignore` in the bootstrap dir would be
  swallowed by this repo's own tooling.
- `__entry_point__.py` is skipped by `build` but copied by `export`/`register`.

## Tests

`tests/` mirrors the package layout. Fixtures live in two places with different roles:
`tests/tst_templates/` is an importable package of bootstrap fixtures (including deliberately
broken ones: `test_missed_entry_point`, `test_wrong_entry_point`), while
`tests/tst-register-bootstrap-source/` is a non-importable directory used as a `register`
source. Tests exercise operations by constructing them and feeding a hand-built
`argparse.Namespace` rather than by going through the CLI; `tests/scripts/test_bootstrap.py`
is the exception that drives `main()` end to end. Tests that write files create them under
the CWD and clean up in `tearDown`.

mypy excludes `templates/` and `tst_templates/` (they contain intentionally invalid template
syntax) and relaxes several error codes for `tests.*`.

## Notes

- The `Makefile` is the source of truth for how the checks actually run.
- `docs/modules/` and `docs/build/` are generated; never edit them by hand.
