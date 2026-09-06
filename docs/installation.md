# Installation

`py-bootstrap` requires **Python 3.13 or newer**.

## From PyPI

```console
$ python3.13 -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
$ pip install ak-py-bootstrap
```

Installing the package adds the `bootstrap` entry-point command.

## Pre-releases

Release candidates are published to PyPI but hidden from `pip` by default. Opt in
with `--pre`:

```console
$ pip install --pre ak-py-bootstrap
```

## Verify

```console
$ bootstrap --help
$ bootstrap list
```

`bootstrap list` should print the built-in bootstraps (`application`, `package`,
`bootstrap`) plus any you have {doc}`registered <guides/register-a-bootstrap>` or
that ship as {doc}`plugins <guides/distribute-bootstraps-as-a-plugin>`.
