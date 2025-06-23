__all__ = ("BuildOperation",)

import logging
import typing as t

from py_bootstrap.operations import BaseBuildBootstrapOperation

if t.TYPE_CHECKING:
    ...

logger = logging.getLogger(__name__)

DESCRIPTION = "Test bootstrap template"


class BuildOperation(BaseBuildBootstrapOperation):
    cli_description = DESCRIPTION
    cli_argument_name_help = "The name of the test project"
    entry_point_path = __file__
