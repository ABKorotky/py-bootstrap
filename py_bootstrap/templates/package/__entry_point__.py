__all__ = (
    "BuildOperation",
    "ExportOperation",
)

import logging
import typing as t

from py_bootstrap.operations import (
    BaseBuildBootstrapOperation,
    BaseExportBootstrapOperation,
)

if t.TYPE_CHECKING:
    from argparse import ArgumentParser

logger = logging.getLogger(__name__)

DESCRIPTION = "Provides operations for Python Packages"


class BuildOperation(BaseBuildBootstrapOperation):
    cli_description = "Generates a skeleton of a new Python Package"
    cli_argument_name_help = "Specifies name of the package"
    cli_argument_description_help = "Specifies description of the package"

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
        super().prepare_cli_parser(parser, prefix)
        parser.add_argument(
            "--author",
            dest="author",
            type=str,
            required=True,
            help="Author of the package.",
        )
        parser.add_argument(
            "--author-email",
            dest="author_email",
            type=str,
            required=True,
            help="Email of the author.",
        )
        parser.add_argument(
            "--repo",
            dest="repo",
            type=str,
            default="",
            help="Repository URL for the application.",
        )

    def build_context(self) -> dict[str, str]:
        context = super().build_context()

        context["author"] = self.cli_namespace.author
        context["author_email"] = self.cli_namespace.author_email
        context["repo"] = self.cli_namespace.repo

        return context


class ExportOperation(BaseExportBootstrapOperation):
    cli_description = "Exports a Python Package's template files"
