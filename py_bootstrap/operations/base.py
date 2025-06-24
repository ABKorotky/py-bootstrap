__all__ = ("BaseBootstrapsOperation",)

import logging
import typing as t
from importlib import import_module
from importlib.metadata import entry_points

from py_bootstrap.base.operations import BaseCliOperation

if t.TYPE_CHECKING:
    from types import ModuleType


logger = logging.getLogger(__name__)


class BaseBootstrapsOperation(BaseCliOperation):
    entry_point_module_name = "__entry_point__"

    @classmethod
    def find_bootstraps(cls) -> t.Iterator[tuple[str, "ModuleType"]]:
        for package_entry_point in entry_points(group="py_bootstrap_templates"):
            # EntryPoint(
            #   name='ingots',
            #   value='ingots.py_bootstrap.templates',
            #   group='py_bootstrap_templates')
            try:
                package_templates_module = package_entry_point.load()
            except ImportError as err:
                logger.exception(
                    "%r. package importing error: %r. entry_point: %r.",
                    cls,
                    err,
                    package_entry_point,
                )
                continue

            for template_dir in package_templates_module.ENABLED_TEMPLATES:
                import_path = (
                    f"{package_entry_point.value}.{template_dir}"
                    f".{cls.entry_point_module_name}"
                )
                try:
                    entry_point_module = import_module(import_path)
                    yield template_dir, entry_point_module
                except ImportError as err:
                    logger.exception(
                        "%r. bootstrap importing error: %r. path: %r.",
                        cls,
                        err,
                        import_path,
                    )
