__all__ = ("main",)

import typing as t

from py_bootstrap.base.operations import BaseOperationsRunner
from py_bootstrap.operations import BootstrapsDispatcher

if t.TYPE_CHECKING:
    ...


class BootstrapsRunner(BaseOperationsRunner):
    cli_prog = "bootstrap"
    operation_cls = BootstrapsDispatcher


def main(cli_args: t.Optional[list[str]] = None):
    entrypoint = BootstrapsRunner()

    if cli_args is not None:
        entrypoint.set_cli_args(cli_args)

    entrypoint.run()


if __name__ == "__main__":
    main()
