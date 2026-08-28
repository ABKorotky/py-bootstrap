__all__ = ("Descriptor",)

import logging
import typing as t
from pathlib import Path

from py_bootstrap.operations import (
    BuildBootstrapDescriptionOperationExt,
    BuildBootstrapNameTitleOperationExt,
)
from py_bootstrap.operations import Descriptor as _Descriptor
from py_bootstrap.operations import ExportBootstrapOperation

if t.TYPE_CHECKING:
    ...


logger = logging.getLogger(__name__)


class BuildOperation(
    BuildBootstrapNameTitleOperationExt, BuildBootstrapDescriptionOperationExt
):
    cli_description = "Generates a skeleton of a new Python Application"


class ExportOperation(ExportBootstrapOperation):
    cli_description = "Exports a Python's Application template files"


_CLI_HELP = """Provides two operations:
    - a builder for generating skeletons of Python Applications.
    - an exporter of Python's Application template files.
"""


class Descriptor(_Descriptor):
    cli_description = "Python Applications bootstrapping"
    cli_help = _CLI_HELP
    templates_path = Path(__file__).parent
    op_build_cls = BuildOperation
    op_export_cls = ExportBootstrapOperation
