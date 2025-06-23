__all__ = ("BaseOperationsRunner",)

import logging
import typing as t
from argparse import ArgumentParser

if t.TYPE_CHECKING:
    from argparse import Namespace
from .base import BaseCliOperation

logger = logging.getLogger(__name__)


class BaseOperationsRunner:
    cli_prog: t.ClassVar[str]
    operation_cls: t.ClassVar[type["BaseCliOperation"]]

    _cli_args: t.Optional[list[str]] = None
    _operation: "BaseCliOperation"

    def set_cli_args(self, cli_args: list[str]):
        self._cli_args = cli_args

    def run(self):
        parser = self.build_cli_parser()
        self.operation_cls.prepare_cli_parser(parser=parser)
        namespace = self.parse_cli_args(parser=parser)

        operation = self.operation_cls()
        self._operation = operation

        operation.set_cli_namespace(namespace=namespace)
        logger.debug("%r. running operation: %r.", self, operation)
        operation.run()

    def build_cli_parser(self) -> "ArgumentParser":
        params = self.get_cli_parser_creating_parameters()
        logger.debug("CLI parser creating parameters: %r.", params)
        return ArgumentParser(**params)

    def get_cli_parser_creating_parameters(self) -> dict:
        return {
            "prog": self.cli_prog,
            "description": self.operation_cls.cli_description,
        }

    def parse_cli_args(self, parser: "ArgumentParser") -> "Namespace":
        logger.debug("CLI arguments: %r.", self._cli_args)
        namespace, unparsed_args = parser.parse_known_args(self._cli_args)
        logger.debug(
            "parsed CLI arguments: %r. unparsed: %r.", namespace, unparsed_args
        )
        return namespace
