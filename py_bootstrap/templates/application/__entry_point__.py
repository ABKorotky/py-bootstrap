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

DESCRIPTION = "Provides operations for Python Applications"


class BuildOperation(BaseBuildBootstrapOperation):
    cli_description = "Generates a skeleton of a new Python Application"
    cli_argument_name_help = "Specifies name of the application"
    cli_argument_description_help = "Specifies description of the application"

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
        super().prepare_cli_parser(parser, prefix)

    def build_context(self) -> dict[str, str]:
        context = super().build_context()
        return context


class ExportOperation(BaseExportBootstrapOperation):
    cli_description = "Exports a Python Application's template files"
