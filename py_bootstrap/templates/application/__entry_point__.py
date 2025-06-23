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

DESCRIPTION = "Provides bootstrapping for Python Applications"


class BuildOperation(BaseBuildBootstrapOperation):
    cli_description = "Generates a skeleton of a Python Application"
    cli_argument_name_help = "The name of the application"
    entry_point_path = __file__

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
        super().prepare_cli_parser(parser, prefix)
        parser.add_argument(
            "--repo",
            dest="repo",
            type=str,
            default="",
            help="Repository URL for the application.",
        )

    def build_context(self) -> dict[str, str]:
        context = super().build_context()

        context["description"] = self.cli_namespace.description
        context["repo"] = self.cli_namespace.repo

        return context


class ExportOperation(BaseExportBootstrapOperation):
    cli_description = "Exports a Python Application bootstrap template"
    entry_point_path = __file__
