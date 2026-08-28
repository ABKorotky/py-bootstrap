__all__ = ("Descriptor",)

import logging
import typing as t
from pathlib import Path

from py_bootstrap.operations import (
    BuildBootstrapCliNameOperationExt,
)
from py_bootstrap.operations import Descriptor as _Descriptor
from py_bootstrap.operations import ExportBootstrapOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser


logger = logging.getLogger(__name__)


class BuildOperation(BuildBootstrapCliNameOperationExt):
    cli_description = ""
    cli_argument_name_help = "Specifies name of the bootstrap"
    cli_argument_cli_name_help = "Specifies CLI name of the bootstrap"

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser"):
        super().prepare_cli_parser(parser=parser)

    def build_context(self) -> dict[str, str]:
        context = super().build_context()
        return context


class ExportOperation(ExportBootstrapOperation):
    cli_description = "Export bootstrap operation"


class Descriptor(_Descriptor):
    cli_description = "Generates files for integration with Bootstrap"
    templates_path = Path(__file__).parent
    op_build_cls = BuildOperation
    op_export_cls = ExportOperation
