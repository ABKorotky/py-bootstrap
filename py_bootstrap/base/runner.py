__all__ = ("BaseOperationsRunner",)

import logging
import typing as t
from argparse import ArgumentParser

if t.TYPE_CHECKING:
    from argparse import Namespace
from py_bootstrap.base.operation import BaseCliOperation

logger = logging.getLogger(__name__)


class BaseOperationsRunner:
    cli_prog: t.ClassVar[str]
    operation_cls: t.ClassVar[type["BaseCliOperation"]]

    _cli_args: t.Optional[list[str]] = None

    def set_cli_args(self, cli_args: list[str]):
        self._cli_args = cli_args

    def run(self):
        logger.info("%r. start.", self)
        parser = self.build_cli_parser()
        self.prepare_cli_parser(parser=parser)
        self.operation_cls.prepare_cli_parser(parser=parser)
        namespace = self.parse_cli_args(parser=parser)

        self.configure_logging(namespace=namespace)
        logger.debug("%r. CLI namespace: %r.", self, namespace)

        operation = self.operation_cls()
        logger.debug("%r. created operation: %r.", namespace, operation)
        operation.set_cli_namespace(namespace=namespace)
        if namespace.runner_dry_run:
            operation.set_dry_run_mode()

        logger.debug("%r. running operation: %r.", self, operation)
        operation.run()
        logger.info("%r. done.", self)

    def build_cli_parser(self) -> "ArgumentParser":
        params = self.get_cli_parser_creating_parameters()
        logger.debug("CLI parser creating parameters: %r.", params)
        return ArgumentParser(**params)

    def get_cli_parser_creating_parameters(self) -> dict:
        return {
            "prog": self.cli_prog,
            "description": self.operation_cls.cli_description,
        }

    def prepare_cli_parser(self, parser: "ArgumentParser"):
        parser.add_argument(
            "-v",
            "--verbose",
            dest="runner_verbosity",
            action="count",
            default=0,
            help=(
                "Specifies logging level. -v is INFO, -vv is DEBUG. "
                "WARNING by default."
            ),
        )
        parser.add_argument(
            "--dry-run",
            dest="runner_dry_run",
            action="store_true",
            help="Enables dry-run mode for the action.",
        )

    def parse_cli_args(self, parser: "ArgumentParser") -> "Namespace":
        logger.debug("CLI arguments: %r.", self._cli_args)
        namespace, unparsed_args = parser.parse_known_args(self._cli_args)
        logger.debug(
            "parsed CLI arguments: %r. unparsed: %r.", namespace, unparsed_args
        )
        return namespace

    def configure_logging(self, namespace: "Namespace"):
        level = logging.WARNING

        v = namespace.runner_verbosity
        if v == 1:
            level = logging.INFO
        elif v >= 2:
            level = logging.DEBUG

        logging.root.setLevel(level=level)
