# Bootstrapping of Python projects
Provides functionality for generating skeletons for Python projects.

[![PyPI](https://img.shields.io/pypi/v/ak-py-bootstrap.svg)](https://pypi.org/project/ak-py-bootstrap/)
[![Python](https://img.shields.io/pypi/pyversions/ak-py-bootstrap.svg)](https://pypi.org/project/ak-py-bootstrap/)
[![ci](https://github.com/ABKorotky/py-bootstrap/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ABKorotky/py-bootstrap/actions/workflows/ci.yml)
[![coverage](https://codecov.io/gh/ABKorotky/py-bootstrap/branch/main/graph/badge.svg)](https://codecov.io/gh/ABKorotky/py-bootstrap)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ABKorotky/py-bootstrap/blob/main/LICENSE)
[![Documentation Status](https://app.readthedocs.org/projects/ak-py-bootstrap/badge/?version=stable)](https://ak-py-bootstrap.readthedocs.io/en/stable/)

<!-- Badge hrefs must be absolute: this README also renders on PyPI, where
     relative links 404. -->

# For Consumers

## Installation
Create and activate a virtual environment if missed:
```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

Install the package:
```bash
pip install ak-py-bootstrap
```
During installing the package creates an entry-point `bootstrap`.

## Using

### Getting help
Call the tool with `-h`/`-help` argument:
```bash
bootstrap --help
```
It shows the following text:
```bash
usage: bootstrap [-h] {list,build,export,register} ...
...
Bootstraps management operations:
  {list,build,export,register}
    list                Finds and prints the list of available bootstraps with brief description.
    build               Generates a skeleton of something from given bootstrap.
    export              Exports a bootstrap by given name.
    register            Registers a new bootstrap.
```

### Getting a list of enabled / registered bootstraps
Call the following command:
```bash
bootstrap list
```
It should show something like:
```bash
...
application: Provides bootstrapping for Python Applications
package: Provides bootstrapping for Python Packages
...
```
Both of these subcommands provide a minimal skeleton of Python Project based on `black`, `isort`, `flake`, `mypy` and `tox` automation tool.

`Application` is a "final" project in `bootstrap` terms.

`Package` is an "intermediate" project in `bootstrap` terms.

The difference between them is the following: no need to build some package(s) from `applications` but it's important to do for `packages`.
So, `tox` tool provides for `applications` a minimal set of predefined `commands`:
- reformatting using `black` and `isort` tools.
- check code style using `black` and `flake` tools.
- check annotations using `mypy tool`.
- running tests based on `unittests` framework and calculating a level of coverage using `coverage` tool.


`tox` tool provides several additional `commands` for `packages:
- generating documentation based on `sphinx` framework.
- building versions of packages.
- publishing prepared archives in PyPI or Test PyPI.

You can prepare and register your own bootstraps for speeding up your work.
See topics below how to do it.

### Generating a skeleton of something
The main feature of the tool.

First of all, let's show on the help text of `build` command:
```bash
bootstrap build --help
```
You should see something like:
```bash
usage: bootstrap build [-h] [--dest DESTINATION_DIR] {application,package} ...
...
options:
  ...
  --dest DESTINATION_DIR
                        Specifies the destination directory for generating. Current directory by default.
Found bootstraps:
  {application,package}
    application         Generates a skeleton of a Python Application
    package             Generates a skeleton of a Python Package
```
The important here is the following:
- `--dest` argument. It's a common argument for all bootstraps. It specifies a target directory on a file system. Current directory by default.

#### Getting help for every bootstrap
Every bootstrap can provide own CLI interface.
So, it's important to examine them before using.

Call the following command:
```bash
bootstrap build application --help
```
It should render something like:
```bash
usage: bootstrap build application [-h] --name NAME --description DESCRIPTION [--repo REPO]
...
options:
  ...
  --name NAME           Specifies name of the application
  --description DESCRIPTIORepositoryN
                        Specifies description of the application.
```
As you can see, the required arguments are:
- `name`. it specifies a name of the application. It should be python-compatible.
- `description`. it specifies a brief description of a generated application.

#### Generating a skeleton of a python application
After working with help text, we are ready to generate something.
Call the following command:
```bash
bootstrap build application --name=demo-app --description="The Demo python Application"
```
Check the file system:
```bash
tree -L2
```
You should see something like:
```bash
├── CHANGELOG.md
├── pyproject.toml
├── README.md
├── requirements-dev.txt
├── requirements.txt
└── tests
    └── __init__.py
```
So, you have got:
- prepared `pyproject.toml` file with minimal configuration for the mentioned above tools.
- minimal `README.md` file.
- `demo_app` directory where you will place code of your application in the future.
- `tests` directory where you will place future unit tests for testing you application.

Congratulations! Now you are ready to make the first commit in your new application.

Generating a skeleton of python package is similar.

### Preparing your own bootstraps
Bootstrap is a directory of the following structure:
- `__entry_point__.py` file. It's an entry point into every bootstrap. It provides logic for generating bootstraps.
- any set of any files or directories that provide content for the bootstrap.

There are two ways how to prepare a new custom bootstrap:
- from scratches.
- based on existed one.

#### Preparing new bootstrap from scratches
Working with `bootstrap list` command you can mention that exist one more bootstrap: `boostrap`.
Yes, this bootstrap provides generating new ... bootstraps.

Call the following command:
```bash
bootstrap build --dest=demo-bootstrap bootstrap --name=demo-bs --description="The Demo bootstrap"
```
Examine a local file system:
```bash
tree -L2 demo-bootstrap/
```
You should see something like:
```bash
demo-bootstrap/
├── demo-file.txt.tmpl
└── __entry_point__.py

1 directory, 2 files
```

It's a skeleton of new bootstrap.
Now it's able to prepare any static files or templates for generating a dynamic content for the bootstrap.
In `demo-file.txt.tmpl` you can find placeholders that the tool provides by default.

#### Export existed bootstrap
Instead developing bootstraps from scratches, it's able to export one of existed bootstraps and modify it.

Call the following command:
```bash
bootstrap export --dest=bs-application-copy application
```
In `bs-application-copy` you can find:
- original `__entry_point__.py` file.
- a set of static files and templates that provide content of `application` bootstrap.

Please examine these files. That's the best way to understand bootstrapping functionality in details.

Now it's able to modify a cloned bootstrap files for reaching your aims.

### Register new bootstraps
After developing new bootstrap but before using need to register this one in the tool.
`register` command is responsible to do it.

Call the following command for getting help text:
```bash
bootstrap register --help
```
You can see something like:
```bash
usage: bootstrap register [-h] --name BOOTSTRAP_NAME --source SOURCE_PATH [-y]
...
options:
  --name BOOTSTRAP_NAME
                        Specifies name of registered bootstrap template.
  --source SOURCE_PATH  Specifies the source directory with metadata and bootstrap templates. Current directory by default.
  -y, --yes-upload      Do not prompt for confirmation.
```
The required arguments are:
- `--name`. It specifies the name of new bootstrap in the tool.
- `--source`. It specifies a directory with implemented bootstrap.
- `-y` / `--yes-upload`. The argument disables interactive mode. A system won't print a confirmation prompt with waiting an input from a developer.

So, let's register a prepared new bootstrap:
```bash
bootstrap register --name=demo --source=demo-bootstrap
```
Confirm uploading by typing `y`.

Check registering by calling `bootstrap list`. It should show new `demo` bootstrap in a list of enabled.

That's all. Now it's able to use a registered bootstrap in your work.

NB: the system is very straightforward, it doesn't make any conclusions instead of you. The system allows overriding bootstraps. 
That's pros and cons at the same time.
On the one hand, it's very easy to test new bootstraps, just fix templates, upload changes and check a result of generating immediately.
On the other hand, it's easy to break a current bootstrap in case you make a decision to REPLACE existed one.
So, it's a developer's duty to care about what exactly they register.

### Embed package bootstraps as plugins
Define in yours `pyproject.toml` file the following section:
```toml
[project.entry-points.py_bootstrap_templates]
<your-package-name> = "<package-root-dir>.py_bootstrap.templates"
```
Create the following files structure:
```bash
<package-root-dir>
└── py_bootstrap
    └── templates
        ├── <your-bootstrap-dir>
        │   ├── __entry_point__.py
        │   ...
        ├── <your-another-bootstrap-dir>
        │   ├── __entry_point__.py
        │   ...
        └── __init__.py
```
Put into `<package-root-dir>/py_bootstraps/templates/__init__.py` file the following content:
```python
__all__ = ("ENABLED_TEMPLATES",)

ENABLED_TEMPLATES = [
    "<your-bootstrap-dir>",
    "your-another-bootstrap-dir",
]
```
That's all! Build a new version of the package, install it in some virtual environment together with `ak-py-bootstrap` package and enjoy of working with package's bootstraps.

Running `bootstrap list` you will see something like:
```bash
...
your-bootstrap-dir: Your bootstrap description.
your-another-bootstrap-dir: Your another bootstrap description.
...
```

## For developers

### Cloning the project
Run the following commands:
```bash
git clone https://github.com/ABKorotky/py-bootstrap.git
cd py_bootstrap
```

### Prepare a virtual environment for developing
Run the following commands:
```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e . --group dev
```
Dev tooling is declared as [PEP 735](https://peps.python.org/pep-0735/) dependency
groups in `pyproject.toml` (`test`, `format`, `cs`, `ann`, `doc`, `changelog`,
`scm`, `dist`, `release`, and the umbrella `dev`). The tool has no runtime
dependencies.

### Using make in development
Development and release tasks run through `make`. Each target installs the
dependency group it needs into a single `.venv` on demand, so the toolchain is
provisioned lazily rather than duplicated per task:
- `deps`. Installs every dev dependency into `.venv`.
- `cs`. Code Style. Checks project's code style using `isort`, `black` and `flake8` tools.
- `ann`. Annotation. Checks types annotations in the project using `mypy` tool.
- `test`. Unit Tests with Coverage. Checks that `tox.ini`, the `pyproject.toml` classifiers and the `ci.yml` matrix agree on the supported interpreters, then runs the suite on each of them via `tox`. `make test PY_ENV=py313` runs just one.
- `check`. Runs `cs`, `ann` and `test`.
- `format`. Formatting. Reformats code in the project using `black` and `isort` tools.
- `doc`. Documentation. Generates project's documentation using `sphinx` tool.
- `cl-preview VERSION=X.Y.Z`. Changelog Draft. Previews the section the `changelog.d/` fragments would produce.
- `cl-check`. Changelog Check. Fails if the branch adds no news fragment (CI runs this on every PR).
- `cl-build VERSION=X.Y.Z`. Changelog. Collates `changelog.d/` fragments into `CHANGELOG.md` and removes them.
- `cut-tag VERSION=X.Y.Z`. Verifies the version is releasable and unused and the working tree is clean, writes the `## [X.Y.Z]` section, commits it as `Prepare X.Y.Z version` and tags `vX.Y.Z`.
- `dist-build`. Builds the sdist and wheel into `dist/` from a clean working tree, then installs the wheel into a throwaway virtualenv and checks `bootstrap list` works.
- `dist-upload`. Uploads `DIST` (default `dist/*`) to `PYPI` (default `pypi`) after `twine check --strict`.
- `release VERSION=X.Y.Z [PYPI=testpypi]`. The whole flow: `cut-tag`, `dist-build`, `dist-upload`, stopping at the first failure.
- `clean` / `venvclean`. Removes build, test and doc artefacts / also removes the virtualenvs (`.venv` and `.tox/`).

Run `make` with no target for the full list.

### Using tox in development
`tox` is kept for one job: running the test suite against every supported
interpreter. `tox` runs `py313` and `py314`; `tox -e py313` runs just one.
Everything else lives in the `Makefile`.

### Development rules and agreements
Follow Python's principles [PEP 20 – The Zen of Python](https://peps.python.org/pep-0020/):
- Simple is better than complex.
- Explicit is better than implicit. And so on...

Follow ["SOLID"](https://en.wikipedia.org/wiki/SOLID) principles:
- Single responsibility principle.
- Open–closed principle.
- Liskov substitution principle.
- Interface segregation principle.
- Dependency inversion principle.

### Branching model
Based on "GitHub-Flow", extended by release branches on demand.

**Branches**
- `main` is the default stable branch; stable distributions are released from it.
- Develop on `<feature>` branches — commit count and messages there are not limited.
- Older lines live on `release/<major>.<minor>` branches, cut from that line's last tag. A release branch carries its own `CHANGELOG.md` and `changelog.d/`.

**Merging** — enforced by GitHub, not done by hand:
- The only enabled merge method is **squash**, so every PR lands as one commit.
- A ruleset on `main` and `release/*` requires a PR, passing `ci` checks (`cs`, `ann`, `utc`, `doc`), the `changelog` check, **linear history** (no merge commits), and the **merge queue**.
- The merge queue rebases the PR onto the current target, re-runs the checks, and fast-forwards it in — no manual squash, rebase, or `--ff-only`. Enable auto-merge on the PR and leave it.

**Tags & releases**
- Tag per [PEP 440](https://peps.python.org/pep-0440/), `v`-prefixed: `vX.Y.Z`, `vX.Y.ZrcN`. Merging into `main` is an intention to release, so almost every commit on `main` is tagged.
- Cut a release the same way on `main` or a release branch: `make release VERSION=X.Y.Z` (see [Releasing new distributions flow](#releasing-new-distributions-flow)). The `release` workflow accepts any `v*` tag whose commit is reachable from `main` or a `release/*` branch.
- Tags on `main` must increase monotonically. Do **not** tag `v0.2.0 -> v0.2.1 -> v0.3.0 -> v0.2.2`; instead branch `release/0.2` from `v0.2.1`, fix there, and tag `v0.2.2`.
- Move fixes between lines with `cherry-pick` — e.g. cherry-pick the `v0.2.2` fix from `release/0.2` into `main` and ship it as `v0.3.2`.

Recap: history on `main` stays a straight line, with release branches forking off tag points.

### Releasing new distributions flow

The project version comes from the git tag (`setuptools-scm`), `CHANGELOG.md` is
assembled by `towncrier` from news fragments in `changelog.d/`, and publishing is
done by the `release` GitHub Actions workflow through PyPI Trusted Publishing — no
version constant to bump, no tokens, no manual `twine`. Setup and details:
[`docs/releasing/`](docs/releasing/). Tags are `v`-prefixed (`v0.10.0`);
`setuptools-scm` also reads the older bare tags.

1. Create a `feature` branch from `main` or a release one.
2. Make the changes. Run `make format` and `make check` during development.
3. Add a news fragment under `changelog.d/` describing the change (see
   [`changelog.d/README.md`](changelog.d/README.md)); `make cl-check` mirrors
   what CI enforces on the PR.
4. Run `make doc` and examine the generated documentation.
5. Squash to one commit, rebase on the target branch, clean the diff.
6. Run `make format`, then `make check`, on the final commit; ensure both pass.
   Run `tox` too if the change could be interpreter-sensitive.
7. Merge the `feature` branch into the target (`main` or `release/<major>.<minor>`).
8. On the merge commit, decide the version and cut the release:
   ```
   make cl-preview VERSION=0.10.0   # read the section the fragments will produce
   make cut-tag VERSION=0.10.0      # verify, write CHANGELOG.md, commit, tag v0.10.0
   make dist-build                  # build and check the wheel installs
   make dist-upload                 # -> PyPI; PYPI=testpypi to rehearse
   git push origin <branch> --follow-tags
   ```
   `make release VERSION=0.10.0` runs those three steps in one go.
9. Validate in a fresh environment: `pip install ak-py-bootstrap`.

To rebuild an already released version, check out its tag and run
`make dist-build dist-upload` — `dist-build` derives the version from the tag,
so the artefacts are identical to the original.

Use the same flow for releasing distributions from release branches.
