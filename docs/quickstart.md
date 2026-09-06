# Quickstart

This walks through generating a Python application skeleton end to end. It assumes
`ak-py-bootstrap` is {doc}`installed <installation>`.

## 1. See what is available

```console
$ bootstrap list
application: Provides bootstrapping for Python Applications
package: Provides bootstrapping for Python Packages
bootstrap: Provides bootstrapping for new bootstraps
```

## 2. Inspect a bootstrap's options

Every bootstrap has its own CLI. Check it before using:

```console
$ bootstrap build application --help
usage: bootstrap build application [-h] --name NAME --description DESCRIPTION

options:
  --name NAME            Specifies name of the application
  --description DESCRIPTION
                        Specifies description of the application.
```

## 3. Generate the skeleton

```console
$ bootstrap build application --name=demo-app --description="The demo application"
```

By default files are written to the current directory. Use `--dest` to target
another directory:

```console
$ bootstrap build --dest=./demo-app application --name=demo-app --description="The demo application"
```

## 4. Look at the result

```console
$ tree -L 2 demo-app
demo-app
├── CHANGELOG.md
├── pyproject.toml
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── demo_app
└── tests
    └── __init__.py
```

You get a `pyproject.toml` pre-configured for `black`, `isort`, `flake8`, `mypy`
and `tox`, a minimal `README.md`, a `demo_app` package directory for your code,
and a `tests` directory. Make your first commit and start working.

## Next steps

- {doc}`guides/generate-a-project` — applications vs. packages, and all options.
- {doc}`guides/write-a-bootstrap` — build your own.
- {doc}`concepts/architecture` — how generation works under the hood.
