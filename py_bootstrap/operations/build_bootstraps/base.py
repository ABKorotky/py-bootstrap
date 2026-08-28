__all__ = (
    "BuildBootstrapOperation",
    "BuildDescriptor",
)

import logging
import sys
import typing as t
from datetime import datetime

from py_bootstrap.files_processors import GenerateFilesProcessor

from ..base import (
    BaseDescriptor,
    DescriptorOperationExt,
    DestinationPathOperationExt,
)

if t.TYPE_CHECKING:
    from argparse import ArgumentParser


logger = logging.getLogger(__name__)


class BuildBootstrapOperation(
    DestinationPathOperationExt, DescriptorOperationExt["BuildDescriptor"]
):
    cli_description = "Generates something from a given bootstrap"

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser"): ...

    _context: dict[str, str]

    def run(self):
        self._context = self.build_context()
        logger.debug("%r. prepared context: %r.", self, self._context)
        super().run()
        self.populate_destination_dir()

    def build_context(self) -> dict[str, str]:
        now = datetime.now()
        return {
            "empty": "",
            "date_today": now.strftime("%Y-%m-%d"),
            "date_year": str(now.year),
            "python_major": str(sys.version_info.major),
            "python_minor": str(sys.version_info.minor),
        }

    def populate_destination_dir(self):
        processor = GenerateFilesProcessor()
        processor.set_source_path(path=self._descriptor.templates_path)
        processor.set_destination_path(path=self.cli_destination_path)
        if self._dry_run:
            processor.set_dry_run_mode()
        processor.set_context(value=self._context)
        processor.run()


class BuildDescriptor(BaseDescriptor):
    op_build_cls = BuildBootstrapOperation
