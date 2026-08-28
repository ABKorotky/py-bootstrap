__all__ = ("BuildBootstrapsDispatcherOperation",)

import logging
import typing as t

from ..base import BaseBootstrapsDispatcherOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser

    from .base import BuildBootstrapOperation, BuildDescriptor


logger = logging.getLogger(__name__)


class BuildBootstrapsDispatcherOperation(
    BaseBootstrapsDispatcherOperation["BuildDescriptor", "BuildBootstrapOperation"]
):
    cli_description = "Generates a skeleton of something from a given bootstrap."

    @classmethod
    def get_cli_subparser_description(cls, descriptor: type["BuildDescriptor"]) -> str:
        return descriptor.op_build_cls.cli_description

    @classmethod
    def get_cli_subparser_help(cls, descriptor: type["BuildDescriptor"]) -> str:
        return descriptor.op_build_cls.cli_help

    @classmethod
    def prepare_cli_subparser(
        cls, subparser: "ArgumentParser", descriptor: type["BuildDescriptor"]
    ):
        descriptor.op_build_cls.prepare_cli_parser(parser=subparser)

    def create_operation(
        self, descriptor: type["BuildDescriptor"]
    ) -> "BuildBootstrapOperation":
        return descriptor.op_build_cls()
