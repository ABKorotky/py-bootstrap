# Development maintaining entrypoint:
#
#   make              show the target list
#   make check        cs + ann + test + cl-check
#   make release VERSION=0.10.0

SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:

# requires-python = ">=3.13"; `python3` is often older, so be explicit.
PYTHON ?= python3.13
VENV   ?= .venv
BIN    := $(VENV)/bin
PY     := $(BIN)/python
STAMPS := $(VENV)/.stamps

# Release: index alias from ~/.pypirc, and what dist-upload sends.
# Defaults to the real index - `PYPI=testpypi` for a rehearsal.
PYPI ?= pypi
DIST ?= dist/*

PKG := py_bootstrap
SRC := $(PKG) tests tools
DOC_OUT := docs/build

# $(call group,NAME) -> the stamp file standing for "group NAME is installed"
group = $(STAMPS)/group-$(1)


##@ Environment

$(PY):
	$(PYTHON) -m venv $(VENV)
	$(PY) -m pip install --quiet --upgrade pip

# Needs pip >= 25.1 for PEP 735 --group. Re-runs whenever pyproject.toml changes.
$(STAMPS)/group-%: pyproject.toml | $(PY)
	@mkdir -p $(@D)
	$(PY) -m pip install --quiet --group $*
	@touch $@

# The package itself, for tasks that import it.
$(STAMPS)/editable: pyproject.toml | $(PY)
	@mkdir -p $(@D)
	$(PY) -m pip install --quiet --editable .
	@touch $@

.PHONY: deps
deps: $(call group,dev) $(STAMPS)/editable  ## Install every dev dependency into $(VENV)


##@ Code quality

.PHONY: format
format: $(call group,format)  ## Format code with isort and black
	$(BIN)/isort $(SRC)
	$(BIN)/black $(SRC)

.PHONY: cs
cs: $(call group,cs)  ## Check code style (isort, black, flake8)
	$(BIN)/isort --check-only --diff $(SRC)
	$(BIN)/black --check --diff $(SRC)
	$(BIN)/flake8 $(SRC)

.PHONY: ann
ann: $(call group,ann)  ## Check type annotations with mypy
	$(BIN)/mypy $(SRC)

# tox owns the test suite: it builds the package and runs it on every supported
# interpreter, which a single shared virtualenv cannot do. Which interpreters
# those are is declared in tox.ini, pyproject.toml and ci.yml with nothing
# linking them, so confirm they still agree before trusting what the run covered.
.PHONY: test
test: $(call group,tox)  ## Check the supported-Python list, then run the suite on every supported interpreter
	$(PY) tools/check_matrix.py
	$(PY) -m tox $(if $(PY_ENV),-e $(PY_ENV),)

# The `ci` workflow runs exactly these targets, one per job. Keep the two in
# step: a check worth enforcing on GitHub is worth failing locally first.
.PHONY: check
check: cs ann doc test cl-check  ## Run every check the `ci` workflow runs


##@ Documentation

# docs/modules/ is gitignored and regenerated. Read the Docs runs this target
# too, with VENV pointed at its own environment, so the flags live in one place.
.PHONY: apidoc
apidoc: $(call group,doc)  ## Regenerate the API reference stubs in docs/modules/
	rm -rf docs/modules
	$(BIN)/sphinx-apidoc --separate --force --no-toc --module-first --ext-viewcode \
		--output-dir=docs/modules $(PKG)

.PHONY: doc
doc: apidoc $(STAMPS)/editable  ## Build the HTML documentation
	rm -rf $(DOC_OUT)
	$(BIN)/sphinx-build -b html --keep-going docs $(DOC_OUT)


##@ Changelog

.PHONY: cl-check
cl-check: $(call group,changelog)  ## Fail if the branch adds no news fragment
	$(BIN)/towncrier check --compare-with $(if $(AGAINST),$(AGAINST),origin/main)

.PHONY: cl-preview
cl-preview: $(call group,changelog)  ## Preview the collated changelog [VERSION=X.Y.Z]
	$(BIN)/towncrier build --draft --version $(if $(VERSION),$(VERSION),UNRELEASED)


.PHONY: cl-build
cl-build: require-version $(call group,changelog)  ## Collate changelog.d/ into CHANGELOG.md (VERSION=X.Y.Z)
	$(BIN)/towncrier build --version $(VERSION) --yes


##@ Release

.PHONY: cut-tag
cut-tag: $(call group,changelog)  ## Verify, write the CHANGELOG section, commit and tag (VERSION=X.Y.Z)
	$(PY) tools/check_version.py $(VERSION)
	$(PY) tools/check_no_diff.py
	$(BIN)/towncrier build --version $(VERSION) --yes
	git add CHANGELOG.md changelog.d
	git commit --message "Prepare $(VERSION) version"
	git tag v$(VERSION)

# Also usable on its own: check out an old tag and rebuild that version.
.PHONY: dist-build
dist-build: $(call group,dist)  ## Build the distribution and check it installs
	$(PY) tools/check_no_diff.py
	rm -rf dist
	$(PY) -m build
	rm -rf build
	$(PY) tools/smoke.py

.PHONY: dist-upload
dist-upload: $(call group,dist)  ## Upload DIST (default dist/*) to PYPI (default $(PYPI))
	$(BIN)/twine check --strict $(DIST)
	$(BIN)/twine upload --repository=$(PYPI) --verbose $(DIST)

# Prerequisites run left to right and stop at the first failure. Do not add -j.
.PHONY: release
release: cut-tag dist-build dist-upload  ## Cut the tag, build, upload (VERSION=X.Y.Z [PYPI=testpypi])


##@ Housekeeping

.PHONY: clean
clean:  ## Remove build, test and doc artefacts (keeps every virtualenv)
	rm -rf build dist docs/modules $(DOC_OUT) htmlcov .coverage .mypy_cache
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +

.PHONY: venvclean
venvclean: clean  ## Also remove the virtualenvs ($(VENV) and .tox/)
	rm -rf $(VENV) .tox

# Targets are listed in definition order, not sorted: the sections below read as
# the order you actually use them in. `##@ Name` starts a section, `## text`
# after a target's prerequisites documents it.
.PHONY: help
help:  ## Show this help
	@echo "py-bootstrap - make targets:"
	@awk 'BEGIN {FS = ":.*## "} \
		/^##@ / {printf "\n%s\n", substr($$0, 5); next} \
		/^[a-z][a-zA-Z0-9_-]*:.*## / {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo
	@echo "Variables: VERSION, MESSAGE, PYPI, DIST, AGAINST, PYTHON, VENV"
