__all__ = ("Descriptor",)

import logging
import typing as t
from pathlib import Path

from py_bootstrap.operations import BuildBootstrapOperation
from py_bootstrap.operations import Descriptor as _Descriptor

if t.TYPE_CHECKING:
    ...


logger = logging.getLogger(__name__)


class BuildOperation(BuildBootstrapOperation):
    cli_argument_name_help = "Specifies name of the test project"
    cli_argument_description_help = "Specifies description of the test project"


class Descriptor(_Descriptor):
    cli_description = "Provides a test bootstrap for preparing test skeletons"
    templates_path = Path(__file__).parent
    op_build_cls = BuildOperation
