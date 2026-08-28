__all__ = ("main", "build_parser")

import logging
import typing as t

from py_bootstrap.base import BaseOperationsRunner
from py_bootstrap.main_dispatcher import MainDispatcherOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser


logging.basicConfig(
    level=logging.WARNING, format="β %(levelname)s %(message)s - %(name)s"
)


class BootstrapsRunner(BaseOperationsRunner):
    cli_prog = "bootstrap"
    operation_cls = MainDispatcherOperation


def build_parser() -> "ArgumentParser":
    """Return the fully populated ``bootstrap`` CLI parser.

    Used by the Sphinx ``sphinx-argparse`` extension to render the CLI reference,
    and handy for tests. Building the parser has no side effects.
    """
    runner = BootstrapsRunner()
    parser = runner.build_cli_parser()
    runner.operation_cls.prepare_cli_parser(parser=parser)
    return parser


def main(cli_args: t.Optional[list[str]] = None):
    entrypoint = BootstrapsRunner()

    if cli_args is not None:
        entrypoint.set_cli_args(cli_args)

    entrypoint.run()


if __name__ == "__main__":
    main()
