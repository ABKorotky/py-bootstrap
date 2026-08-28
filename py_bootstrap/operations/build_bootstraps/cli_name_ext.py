__all__ = ("BuildBootstrapCliNameOperationExt",)

import logging
import re
import typing as t
from argparse import ArgumentTypeError
from functools import cached_property

from .base import BuildBootstrapOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser


logger = logging.getLogger(__name__)


class BuildBootstrapCliNameOperationExt(BuildBootstrapOperation):
    cli_argument_cli_name_help: str = (
        "Specifies CLI name of generated entity."
        "Should contain alphanumeric characters and hyphens only."
    )
    cli_argument_cli_name_required: bool = True

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser"):
        super().prepare_cli_parser(parser=parser)
        parser.add_argument(
            "--cli-name",
            dest="op_build_cli_name",
            type=cls.validate_cli_argument_cli_name,
            required=cls.cli_argument_cli_name_required,
            help=cls.cli_argument_cli_name_help,
        )

    @classmethod
    def validate_cli_argument_cli_name(cls, value: str) -> str:
        if not re.match(r"^[a-z][a-z0-9-]*[a-z0-9]$", value):
            raise ArgumentTypeError("Invalid --cli-name CLI argument value provided")
        return value

    def build_context(self) -> dict[str, str]:
        ctx = super().build_context()
        ctx["cli_name"] = self.cli_argument_cli_name
        return ctx

    @property
    def cli_argument_cli_name(self) -> str:
        return self.cli_namespace.op_build_cli_name

    @cached_property
    def cli_name_parts(self) -> list[str]:
        return self.cli_argument_cli_name.split("-")
