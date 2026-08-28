__all__ = ("BuildBootstrapDescriptionOperationExt",)

import logging
import typing as t

from .base import BuildBootstrapOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser


logger = logging.getLogger(__name__)


class BuildBootstrapDescriptionOperationExt(BuildBootstrapOperation):
    cli_argument_description_help: str = "Specifies description of generated entity."
    cli_argument_description_required = True

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser"):
        super().prepare_cli_parser(parser)
        parser.add_argument(
            "--description",
            dest="op_build_description",
            type=cls.validate_cli_argument_description,
            required=cls.cli_argument_description_required,
            help=cls.cli_argument_description_help,
        )

    @classmethod
    def validate_cli_argument_description(cls, value: str) -> str:
        return value

    def build_context(self) -> dict[str, str]:
        ctx = super().build_context()
        ctx["description"] = self.cli_argument_description
        return ctx

    @property
    def cli_argument_description(self) -> str:
        return self.cli_namespace.op_build_description
