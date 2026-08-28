__all__ = ("ListBootstraps",)

import logging
import typing as t

from .base import BaseCliOperation
from .operations import BOOTSTRAPS_FINDER

if t.TYPE_CHECKING:
    from argparse import ArgumentParser

    from .operations import Descriptor


logger = logging.getLogger(__name__)


class ListBootstraps(BaseCliOperation):
    cli_description = "Prints brief info for every found bootstrap"

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser"): ...

    def run(self):
        for name, descriptor in BOOTSTRAPS_FINDER.list():
            try:
                self.process_bootstrap_descriptor(name=name, descriptor=descriptor)
            except Exception as err:
                logger.warning(
                    "%r. failed to print description for %r: %s.",
                    self,
                    name,
                    err,
                )

    def process_bootstrap_descriptor(self, name: str, descriptor: type["Descriptor"]):
        print(f"{name}:")
        print(f"    {descriptor.cli_description}.")
        print(f"    Build operation: {descriptor.op_build_cls}.")
        print(f"    Export operation: {descriptor.op_export_cls}.")
