__all__ = ("BootstrapsDispatcher",)

import logging
import typing as t

from py_bootstrap.base.operations import BaseOperationsDispatcher

from .build_bootstrap import BuildBootstrapOperation
from .list_bootstraps import ListBootstrapsOperation
from .register_bootstrap import RegisterBootstrapOperation

if t.TYPE_CHECKING:
    ...


logger = logging.getLogger(__name__)


class BootstrapsDispatcher(BaseOperationsDispatcher):
    cli_description = "Bootstrapping Python projects management tool."

    operations_classes_map = {
        "list": ListBootstrapsOperation,
        "build": BuildBootstrapOperation,
        "register": RegisterBootstrapOperation,
    }
