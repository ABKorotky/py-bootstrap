__all__ = (
    "ExportBootstrapOperation",
    "ExportDescriptor",
)

import logging
import typing as t

from py_bootstrap.files_processors import CopyFilesProcessor

from ..base import (
    BaseDescriptor,
    DescriptorOperationExt,
    DestinationPathOperationExt,
)

if t.TYPE_CHECKING:
    from argparse import ArgumentParser


logger = logging.getLogger(__name__)


class ExportBootstrapOperation(
    DestinationPathOperationExt,
    DescriptorOperationExt["ExportDescriptor"],
):
    cli_description = "Exports template files from a given bootstrap"

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser"): ...

    def run(self):
        super().run()
        self.populate_destination_dir()

    def populate_destination_dir(self):
        processor = CopyFilesProcessor()
        processor.set_source_path(path=self._descriptor.templates_path)
        processor.set_destination_path(path=self.cli_destination_path)
        if self._dry_run:
            processor.set_dry_run_mode()
        processor.run()


class ExportDescriptor(BaseDescriptor):
    op_export_cls = ExportBootstrapOperation
