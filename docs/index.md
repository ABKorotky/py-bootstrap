# Py Bootstrap

It's the simplest and lightweight tool which uses only built-in python features for working with strings and files.
Generates ready-for-development skeletons for Python projects.

Provides several scaffolds for pure python projects.

So, have an idea about new Python project? Don't hesitate, don't waste time for preparing and configuring development tools.
Just install this tool, generate a skeleton and start implementing your dreams!

```console
$ python3.14 -m venv .venv
$ source .venv/bin/activate
$ pip install ak-py-bootstrap
$ bootstrap list
application: Provides bootstrapping for Python Applications
package: Provides bootstrapping for Python Packages
...
$ bootstrap build application --name=demo-app --description="The demo application"
...
$ tox -e format
$ tox
...
$ git init
$ git add .
$ git commit -m "Prepare the project for developing, configure development tools. Good luck!"
```

Also, this tool is [pluginable](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/).
You can develop and ship your own bootstraps according to your needs and preferences.

## Where to go next

- {doc}`installation` and {doc}`quickstart` — get running in a few minutes.
- {doc}`guides/index` — task recipes: generate a project, write / export /
  register a bootstrap, ship bootstraps as a plugin.
- {doc}`concepts/index` — how bootstraps, operations, and templates fit together.
- {doc}`reference/index` — the `bootstrap` CLI and the Python API.
- {doc}`contributing`, {doc}`versioning`, {doc}`changelog`.

```{toctree}
:hidden:
:caption: Getting started

installation
quickstart
```

```{toctree}
:hidden:
:caption: Guides

guides/index
```

```{toctree}
:hidden:
:caption: Concepts

concepts/index
```

```{toctree}
:hidden:
:caption: Reference

reference/index
```

```{toctree}
:hidden:
:caption: Project

contributing
versioning
changelog
authors
```
