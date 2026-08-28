__all__ = ("MainDispatcherOperation",)

import logging
import typing as t

from .base import BaseCliOperation
from .list_bootstraps import ListBootstraps
from .operations import (
    BuildBootstrapsDispatcherOperation,
    ExportBootstrapsDispatcherOperation,
)

if t.TYPE_CHECKING:
    from argparse import ArgumentParser


logger = logging.getLogger(__name__)


class MainDispatcherOperation(BaseCliOperation):
    cli_description = "Bootstrap your's Python projects!"

    op_list_cls = ListBootstraps
    op_build_cls = BuildBootstrapsDispatcherOperation
    op_export_cls = ExportBootstrapsDispatcherOperation

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser"):
        subparsers = parser.add_subparsers(
            title="Operations",
            dest="main_operation_name",
            required=True,
        )
        list_parser = subparsers.add_parser(
            "list",
            description=cls.op_list_cls.cli_description,
            help=cls.op_list_cls.cli_description,
        )
        cls.op_list_cls.prepare_cli_parser(parser=list_parser)

        build_parser = subparsers.add_parser(
            "build",
            description=cls.op_build_cls.cli_description,
            help=cls.op_build_cls.cli_description,
        )
        cls.op_build_cls.prepare_cli_parser(parser=build_parser)

        export_parser = subparsers.add_parser(
            "export",
            description=cls.op_export_cls.cli_description,
            help=cls.op_export_cls.cli_description,
        )
        cls.op_export_cls.prepare_cli_parser(parser=export_parser)

    def run(self):
        operation_name = self.cli_namespace.main_operation_name
        operation: "BaseCliOperation"
        match operation_name:
            case "list":
                operation = self.op_list_cls()
            case "build":
                operation = self.op_build_cls()
            case "export":
                operation = self.op_export_cls()
            case _:
                logger.error("%r. unknown operation: %s", self, operation_name)
                raise ValueError(f"Unknown {operation_name} operation")

        operation.set_cli_namespace(namespace=self.cli_namespace)

        if self._dry_run:
            operation.set_dry_run_mode()

        operation.run()
