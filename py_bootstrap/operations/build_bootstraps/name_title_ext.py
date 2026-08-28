__all__ = ("BuildBootstrapNameTitleOperationExt",)

import logging
import typing as t
from functools import cached_property

from .base import BuildBootstrapOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser


logger = logging.getLogger(__name__)


class BuildBootstrapNameTitleOperationExt(BuildBootstrapOperation):
    cli_argument_name_help: str = "Specifies name of generated entity."
    cli_argument_name_required: bool = True
    cli_argument_title_help: str = (
        "Specifies custom title if present "
        "or will be computed from the other CLI arguments."
    )

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser"):
        super().prepare_cli_parser(parser=parser)
        parser.add_argument(
            "--name",
            dest="op_build_name",
            type=cls.validate_cli_argument_name,
            required=cls.cli_argument_name_required,
            help=cls.cli_argument_name_help,
        )
        parser.add_argument(
            "--title",
            dest="op_build_title",
            type=cls.validate_cli_argument_title,
            default="",
            help=cls.cli_argument_title_help,
        )

    @classmethod
    def validate_cli_argument_name(cls, value: str) -> str:
        return value

    @classmethod
    def validate_cli_argument_title(cls, value: str) -> str:
        return value

    def build_context(self) -> dict[str, str]:
        ctx = super().build_context()
        ctx["name"] = self.cli_argument_name
        ctx["title"] = self.cli_argument_title
        return ctx

    @property
    def cli_argument_name(self) -> str:
        return self.cli_namespace.op_build_name

    @cached_property
    def cli_argument_title(self) -> str:
        title = self.cli_namespace.op_build_title
        if title:
            return title
        return self.cli_argument_name.title()
