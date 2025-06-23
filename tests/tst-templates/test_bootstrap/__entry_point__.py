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
    ...

logger = logging.getLogger(__name__)

DESCRIPTION = "Provides bootstrapping for test python project"


class BuildOperation(BaseBuildBootstrapOperation):
    cli_description = "Generates a test skeleton of python project"
    cli_argument_name_help = "The name of the test project"
    entry_point_path = __file__


class ExportOperation(BaseExportBootstrapOperation):
    cli_description = "Exports a python project test bootstrap template"
    entry_point_path = __file__
