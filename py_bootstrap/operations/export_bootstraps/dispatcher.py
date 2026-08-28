__all__ = ("ExportBootstrapsDispatcherOperation",)

import logging
import typing as t

from ..base import BaseBootstrapsDispatcherOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser

    from .base import ExportBootstrapOperation, ExportDescriptor


logger = logging.getLogger(__name__)


class ExportBootstrapsDispatcherOperation(
    BaseBootstrapsDispatcherOperation["ExportDescriptor", "ExportBootstrapOperation"]
):
    cli_description = "Generates a skeleton of something from a given bootstrap."

    @classmethod
    def get_cli_subparser_description(cls, descriptor: type["ExportDescriptor"]) -> str:
        return descriptor.op_export_cls.cli_description

    @classmethod
    def get_cli_subparser_help(cls, descriptor: type["ExportDescriptor"]) -> str:
        return descriptor.op_export_cls.cli_help

    @classmethod
    def prepare_cli_subparser(
        cls, subparser: "ArgumentParser", descriptor: type["ExportDescriptor"]
    ):
        descriptor.op_export_cls.prepare_cli_parser(parser=subparser)

    def create_operation(
        self, descriptor: type["ExportDescriptor"]
    ) -> "ExportBootstrapOperation":
        return descriptor.op_export_cls()
