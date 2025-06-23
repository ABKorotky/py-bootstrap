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

DESCRIPTION = "Provides operations for Bootstraps"


class BuildOperation(BaseBuildBootstrapOperation):
    cli_description = "Generates a skeleton of a new Bootstrap"
    cli_argument_name_help = "Specifies name of the bootstrap"
    cli_argument_description_help = "Specifies description of the bootstrap"
    entry_point_path = __file__

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
        super().prepare_cli_parser(parser, prefix)

    def build_context(self) -> dict[str, str]:
        context = super().build_context()
        return context


class ExportOperation(BaseExportBootstrapOperation):
    cli_description = "Exports a Bootstrap's template files"
    entry_point_path = __file__
