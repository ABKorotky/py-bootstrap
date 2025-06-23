__all__ = ("ListBootstrapsOperation",)

import logging
import typing as t

from .base import BaseBootstrapsOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser
    from types import ModuleType


logger = logging.getLogger(__name__)


class ListBootstrapsOperation(BaseBootstrapsOperation):
    cli_description = (
        "Finds and prints the list of available bootstraps"
        " with brief description."
    )

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""): ...

    def run(self):
        for name, entry_point_module in self.find_bootstraps():
            self.process_bootstrap_entry_point(
                name=name, module=entry_point_module
            )

    def process_bootstrap_entry_point(self, name: str, module: "ModuleType"):
        try:
            print(f"{name}: {module.DESCRIPTION}")
        except Exception as err:
            logger.warning(
                "%r. failed to print description for %r: %s.", self, name, err
            )
            return
