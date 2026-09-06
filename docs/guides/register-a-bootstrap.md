# Register a bootstrap

A new bootstrap must be registered with the tool before it can be used.

```console
$ bootstrap register --help
usage: bootstrap register [-h] --name BOOTSTRAP_NAME --source SOURCE_PATH [-y]

options:
  --name BOOTSTRAP_NAME
                        Name for the registered bootstrap.
  --source SOURCE_PATH  Directory containing the bootstrap (metadata + templates).
                        Current directory by default.
  -y, --yes-upload      Do not prompt for confirmation.
```

Register the directory you built or exported:

```console
$ bootstrap register --name=demo --source=demo-bootstrap
```

Confirm when prompted (or pass `-y` to skip the prompt). Then check it:

```console
$ bootstrap list
...
demo: The demo bootstrap
```

The registered bootstrap is now usable like any built-in:

```console
$ bootstrap build demo --help
```

```{warning}
Registration is deliberately unopinionated and **overwrites** an existing
bootstrap of the same name. That makes iterating on a bootstrap fast, but it is
also easy to clobber one you meant to keep. You own the choice of name.
```

## See also

- {doc}`write-a-bootstrap`, {doc}`export-and-modify-a-bootstrap`
- {doc}`distribute-bootstraps-as-a-plugin` — share bootstraps without manual
  registration.
