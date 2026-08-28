__all__ = ("Descriptor",)

import logging
import typing as t
from pathlib import Path

from py_bootstrap.operations import BuildBootstrapOperation as _BuildBootstrapOperation
from py_bootstrap.operations import Descriptor as _Descriptor
from py_bootstrap.operations import (
    ExportBootstrapOperation as _ExportBootstrapOperation,
)

if t.TYPE_CHECKING:
    from argparse import ArgumentParser

logger = logging.getLogger(__name__)


class BuildOperation(_BuildBootstrapOperation):
    cli_description = ""

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
        super().prepare_cli_parser(parser)
        parser.add_argument(
            "--package-name",
            dest="package_name",
            type=str,
            default=".",
            help="Specifies package_name of generated entity. '.' by default.",
        )

    def build_context(self) -> dict[str, str]:
        context = super().build_context()
        context["package_name"] = self.cli_args.package_name
        return context


class ExportBootstrapOperation(_ExportBootstrapOperation):
    cli_description = "Exports templates from dev-tox bootstrap"


class Descriptor(_Descriptor):
    cli_description = "Provides a bootstrap for tox-based automations"
    templates_path = Path(__file__).parent
    op_build_cls = BuildOperation
    op_export_cls = ExportBootstrapOperation
