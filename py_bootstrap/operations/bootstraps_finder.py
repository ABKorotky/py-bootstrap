__all__ = (
    "FindBootstrapsOperation",
    "BOOTSTRAPS_FINDER",
)

import logging
import typing as t
from importlib import import_module
from importlib.metadata import entry_points

if t.TYPE_CHECKING:
    from importlib.metadata import EntryPoint

    from .descriptors import Descriptor


logger = logging.getLogger(__name__)


class FindBootstrapsOperation:
    entry_point_group_name = "py_bootstrap_templates"
    descriptor_module_name = "__descriptor__"

    _found_descriptors: dict[str, type["Descriptor"]]

    def list(self) -> t.Iterable[tuple[str, type["Descriptor"]]]:
        try:
            return (i for i in self._found_descriptors.items())
        except AttributeError:
            self.prepare_bootstraps_cache()
            return self.list()

    def get(self, name: str) -> type["Descriptor"]:
        try:
            return self._found_descriptors[name]
        except AttributeError:
            self.prepare_bootstraps_cache()
            return self.get(name)

    def prepare_bootstraps_cache(self):
        self._found_descriptors = dict(self.find_bootstraps())

    def find_bootstraps(self) -> t.Iterator[tuple[str, type["Descriptor"]]]:
        # iterates over all pyproject.toml/project.entry-points.py_bootstrap_templates
        for package_entry_point in self.get_bootstraps_entry_points():
            # EntryPoint(
            #   name=<key in project.entry-points.py_bootstrap_templates>,
            #   value=<path to a directory with bootstraps templates>,
            #   group='py_bootstrap_templates'  # or another
            #   )
            try:
                package_templates_module = package_entry_point.load()
            except ImportError as err:
                logger.warning(
                    "%r. package importing error: %r. skip %r entry-point.",
                    self,
                    err,
                    package_entry_point,
                )
                continue

            try:
                enabled_templates = package_templates_module.ENABLED_TEMPLATES
            except AttributeError:
                logger.warning(
                    "%r. wrong package format: ENABLED_TEMPLATES attribute"
                    " is missing. skip %r entry-point-processing.",
                    self,
                    package_entry_point,
                )
                continue

            for name in enabled_templates:
                import_path = (
                    f"{package_entry_point.value}.{name}"
                    f".{self.descriptor_module_name}"
                )
                try:
                    descriptor_module = import_module(import_path)
                    logger.debug(
                        "%r. found descriptor in %r for %r.",
                        self,
                        import_path,
                        package_entry_point,
                    )
                    descriptor = descriptor_module.Descriptor
                    yield name, descriptor
                except ImportError as err:
                    logger.warning(
                        "%r. bootstrap importing error %r for %r.",
                        self,
                        err,
                        package_entry_point,
                    )
                except AttributeError as err:
                    logger.warning(
                        "%r. invalid bootstrap descriptor module structure: %s.",
                        self,
                        err,
                    )

    def get_bootstraps_entry_points(self) -> t.Iterable["EntryPoint"]:
        return (i for i in entry_points(group=self.entry_point_group_name))


BOOTSTRAPS_FINDER = FindBootstrapsOperation()
