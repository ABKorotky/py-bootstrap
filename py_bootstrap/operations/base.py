__all__ = ("BaseBootstrapsOperation",)

import logging
import typing as t
from importlib import import_module
from pathlib import Path

import py_bootstrap as package
from py_bootstrap.base.operations import BaseCliOperation

if t.TYPE_CHECKING:
    from types import ModuleType


logger = logging.getLogger(__name__)


class BaseBootstrapsOperation(BaseCliOperation):
    package: "ModuleType" = package
    templates_dir_name = "templates"
    entry_point_module_name = "__entry_point__"

    package_path: "Path"
    templates_path: "Path"

    def __init_subclass__(cls, **kwargs):
        assert cls.package.__file__ is not None
        cls.package_path = Path(cls.package.__file__).parent
        cls.templates_path = cls.package_path.joinpath(cls.templates_dir_name)

    @classmethod
    def import_bootstrap_entry_point(cls, dir_path: "Path") -> "ModuleType":
        venv_rel_path = dir_path.relative_to(cls.package_path.parent)
        import_path = ".".join(
            venv_rel_path.parts + (cls.entry_point_module_name,)
        )
        try:
            return import_module(import_path)
        except ImportError as err:
            logger.error(
                "%r. failed to import entry point by %r: %s.",
                cls,
                import_path,
                err,
            )
            raise Exception(f"Importing {import_path} entry point") from err

    @classmethod
    def find_bootstraps(cls) -> t.Iterator[tuple[str, "ModuleType"]]:
        logger.debug(
            "%r. directory with templates: %r.", cls, cls.templates_path
        )
        for template_dir in cls.templates_path.iterdir():
            if not template_dir.is_dir():
                continue

            logger.debug("%r. found a template: %r.", cls, template_dir)

            name = template_dir.name
            if name.startswith("__") or name.startswith("."):
                continue

            try:
                metadata_module = cls.import_bootstrap_entry_point(
                    dir_path=template_dir
                )
            except Exception:
                continue

            yield name, metadata_module
