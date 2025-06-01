__all__ = ("ListBootstrapsOperation",)

import logging
import os
import typing as t

from .base import BaseBootstrapsOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser


logger = logging.getLogger(__name__)


class ListBootstrapsOperation(BaseBootstrapsOperation):
    cli_description = "Prints the list of available bootstraps."

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""): ...

    def run(self):
        templates_path = os.path.join(
            self.package_path, self.templates_dir_name
        )
        logger.debug("%r. directory with templates: %r.", self, templates_path)
        for name in os.listdir(templates_path):
            logger.debug("%r. found item: %r.", self, name)
            item_path = os.path.join(templates_path, name)
            self.process_item(name=name, item_path=item_path)

    def process_item(self, name: str, item_path: str):
        if not os.path.isdir(item_path):
            return
        if name.startswith("__"):
            return
        if name.startswith("."):
            return

        try:
            metadata_module = self.load_bootstrap_metadata(name=name)
        except Exception:
            return

        try:
            print(f"{name}: {metadata_module.DESCRIPTION}")
        except Exception as err:
            logger.warning(
                "%r. failed to print description for %r: %s.", self, name, err
            )
            return
