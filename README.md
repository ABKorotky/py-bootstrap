# Bootstrapping of Python projects
Provides functionality for generating skeletons for Python projects.

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
pip install -i https://test.pypi.org/simple/ ak-py-bootstrap
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
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Using tox tool in development
The package provides the following ['tox' tooling](https://tox.wiki/en/latest/):
- `cs`. Code Style. Checks project's code style using `black` and `flake8` tools.
- `ann`. Annotation. Checks types annotations in the project using `mypy` tool.
- `utc`. Unit Tests with Coverage. Runs project's unit tests and calculates a level of coverage.
- `format`. Formatting. Reformats code in the project using `black` and `isort` tools.
- `doc`. Documentation. Generates project's documentation using `sphinx` tool.
- `build`. Builds an archive for distributing the project via PyPI.
- `upload`. Uploads a prepared distribution archive into one of PyPI (main or test). Uses Test PyPI by default.

Run `tox l` command for details.

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
Based on "GitHub-Flow". Extends by release branches on demand. Rules:
- `main` branch is default stable branch. It uses for releasing new stable distributions.
- Use different `<feature>` branches for developing. Count of commits in feature branches and them messages are not limited.
- Code in "feature" branches should be prepared and tested properly before merging. Running `tox` should pass successfully.
- Merging branches is enabled in the same branch from it was born. Squash commits before merging. Make rebasing on target branch, merge with `--ff-only` strategy.
- Merging code in `main` branch is an intention to release it. So, almost all commits in `main` branch should be tagged.
- Follow [PEP 440](https://peps.python.org/pep-0440/) principles for tagging commits.
- Tags in `<major>.<minor>.<patch>` in `main` branch are placeholders for creating corresponded release branches.
- Use release branches for maintaining several versions at the same time. Format of release branches is `release/<major>.<minor>`.
- Tags on `main` branch should increase monotonic. It's forbidden to create tags in sequence like: `0.2.0` -> `0.2.1` -> `0.3.0` -> `0.3.1` -> `0.2.2`. Start a release branch `release/0.2` from tag `0.2.1` and implement required logic. Mark the commit in the release branch as `0.2.2` and release it.
- Use `cherry-pick` mechanisms for transferring changes between `main` branch and supported release branches. So, make `cherry-pick` of `0.2.2` commit from `release/0.2` branch into `main` and deliver it as `0.3.2` for instance.

Recap: Every time commits structure in the project should look as a tree.

### Releasing new distributions flow
1. Create a `feature` branch from `main` or release one.
2. Make corresponding changes. Don't be afraid to run `tox -e format` and `tox` sometimes during development.
3. Run `tox -e doc`.
4. Examine generated documentation.
5. Squash all commits into one and rebase your changes on the actual state of the target branch.
6. Write what you have done in `CHANGELOG.md` file into the corresponding section. Don't forget to actualize the `VERSION` of these changes in `py_bootstrap/__init__.py` file.
7. Examine diff before merging, clean it from accidentally committed garbage.
8. Run `tox -e format` on ready for merging commit. 
9. Run `tox` of ready for merging commit. Ensure that the command passed successfully.
10. Merge your `feature` branch into target one: `main` or one of `release`.
11. Mark the commit by tag according to the version from `CHANGELOG.md` file.
12. Prepare a distribution from the tag. Run `tox -e build`. Make final checks with generated archive. Ensure it is installed properly.
13. Publish the archive in Test PyPI. Run `tox -e upload -- dist/ak_py_bootstrap-<version>.tar.gz`. Ensure that the distribution is installed properly from Test PyPI. Prepare a temporary environment and run `pip install --extra-index-url=https://test.pypi.org/simple/ ak-py-bootstrap`.
14. Publish the archive in main PyPI. Run `export PYPI_REPOSITORY_ALIAS=pypi` for switching uploading to main PyPI and repeat uploading via `tox -e upload -- ...`. Ensure that the distribution is installed properly from PyPI. Prepare a temporary environment and run `pip install ak-py-bootstrap`.

Use this flow for releasing distributions from release branches.
