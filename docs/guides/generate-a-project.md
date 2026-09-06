# Generate a project

The `build` command generates a skeleton from a bootstrap:

```console
$ bootstrap build --help
usage: bootstrap build [-h] [--dest DESTINATION_DIR] {application,package,bootstrap} ...

options:
  --dest DESTINATION_DIR
                        Destination directory for generating. Current directory by default.
```

`--dest` is common to every bootstrap. Everything after the bootstrap name is that
bootstrap's own CLI — always check it with `--help` first.

## Application vs. package

Both produce a minimal project wired for `black`, `isort`, `flake8`, `mypy` and
`tox`.

`application`
: A *final* project — nothing is built or published from it. Its `tox` config
  covers formatting, code style, type checks, and tests with coverage.

`package`
: An *intermediate* project — meant to be built and distributed. Its `tox` config
  adds documentation generation, building distributions, and uploading to PyPI /
  Test PyPI.

## Generate an application

```console
$ bootstrap build application --name=demo-app --description="The demo application"
```

Required options:

`--name`
: Name of the application. Must be a valid Python identifier once normalised
  (`demo-app` → package dir `demo_app`).

`--description`
: Short description, used in `pyproject.toml` and `README.md`.

Result:

```console
$ tree -L 2 .
├── CHANGELOG.md
├── pyproject.toml
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── demo_app
└── tests
    └── __init__.py
```

## Generate a package

Same shape, using the `package` bootstrap:

```console
$ bootstrap build --dest=./demo-lib package --name=demo-lib --description="The demo library"
```

## See also

- {doc}`../reference/cli` — the full, generated CLI reference.
- {doc}`../concepts/architecture` — what happens during generation.
