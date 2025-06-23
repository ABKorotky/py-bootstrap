__all__ = ("BootstrapsDispatcher",)

import logging
import typing as t

from .base import BaseBootstrapsOperation
from .build_bootstrap import BuildBootstrapsDispatcherOperation
from .list_bootstraps import ListBootstrapsOperation
from .register_bootstrap import RegisterBootstrapOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser

logger = logging.getLogger(__name__)


class BootstrapsDispatcher(BaseBootstrapsOperation):
    cli_description = "Bootstrapping Python projects management tool."

    op_list_cls = ListBootstrapsOperation
    op_build_cls = BuildBootstrapsDispatcherOperation
    op_register_cls = RegisterBootstrapOperation

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
        subparsers = parser.add_subparsers(
            title="Bootstraps management operations",
            dest="operation",
            required=True,
        )
        list_parser = subparsers.add_parser(
            "list",
            description=cls.op_list_cls.cli_description,
            help=cls.op_list_cls.cli_description,
        )
        cls.op_list_cls.prepare_cli_parser(parser=list_parser, prefix="list")

        build_parser = subparsers.add_parser(
            "build",
            description=cls.op_build_cls.cli_description,
            help=cls.op_build_cls.cli_description,
        )
        cls.op_build_cls.prepare_cli_parser(parser=build_parser, prefix="build")

        register_parser = subparsers.add_parser(
            "register",
            description=cls.op_register_cls.cli_description,
            help=cls.op_register_cls.cli_description,
        )
        cls.op_register_cls.prepare_cli_parser(
            parser=register_parser, prefix="register"
        )

    def run(self):
        operation_name = self.cli_namespace.operation
        operation: "BaseBootstrapsOperation"
        match operation_name:
            case "list":
                operation = self.op_list_cls()
            case "build":
                operation = self.op_build_cls()
            case "register":
                operation = self.op_register_cls()
            case _:
                logger.error("r. unknown operation: %s", operation_name)
                raise ValueError(f"Unknown operation {operation_name}")

        operation.set_cli_namespace(self.cli_namespace)
        operation.run()
