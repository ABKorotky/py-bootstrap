# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from importlib.metadata import version as _dist_version

sys.path.insert(0, os.path.abspath(".."))

# -- Project information ----------------------------------------------------------

project = "Py Bootstrap"
author = "Aliaksandr Karotki"
copyright = f"2025, {author}"

# Derived from the installed distribution (setuptools-scm resolves it from the
# latest git tag). `release` is the full version, `version` the short X.Y.
release = _dist_version("ak-py-bootstrap")
version = ".".join(release.split(".")[:2])

# -- General configuration ------------------------------------------------------

extensions: list[str] = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_rtd_theme",
    "myst_parser",
    "sphinxarg.ext",
]

templates_path: list[str] = ["_templates"]
exclude_patterns: list[str] = [
    "build",
    "releasing/*",  # maintainer docs, not part of the published site
    "Thumbs.db",
    ".DS_Store",
]

# Markdown (MyST) sources alongside reStructuredText.
myst_enable_extensions = ["colon_fence", "deflist"]
myst_heading_anchors = 3

autodoc_typehints = "description"
autodoc_member_order = "bysource"
# Document each object once, at its definition site. Without this, apidoc's
# automodule on a package __init__ honours its `__all__` and re-documents
# re-exported names (e.g. BaseCliOperation), which then makes short
# cross-references to them ambiguous.
autodoc_default_options = {"ignore-module-all": True}

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

# -- HTML output --------------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path: list[str] = ["static"]
html_title = f"{project} {release}"
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}
