__all__ = (
    "ExportBootstrapsDispatcherOperation",
    "BaseExportBootstrapOperation",
)

import logging
import os
import typing as t
from functools import cached_property
from pathlib import Path

from py_bootstrap.files_processors import CopyFilesProcessor

from .base import BaseBootstrapsOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser


logger = logging.getLogger(__name__)


class ExportBootstrapsDispatcherOperation(BaseBootstrapsOperation):
    cli_description = "Exports a bootstrap by given name."

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
        parser.add_argument(
            "--dest",
            dest="destination_dir",
            type=str,
            default="",
            help=(
                "Specifies the destination directory for exporting."
                " Current directory by default."
            ),
        )

        subparsers = parser.add_subparsers(
            title="Found bootstraps", dest="bootstrap", required=True
        )
        # prepare parsers for templates
        for name, entry_point_module in cls.find_bootstraps():
            template_parser = subparsers.add_parser(
                name,
                description=entry_point_module.ExportOperation.cli_description,
                help=entry_point_module.ExportOperation.cli_description,
            )
            entry_point_module.ExportOperation.prepare_cli_parser(
                parser=template_parser, prefix=name
            )

    def run(self):
        bootstrap_name = self.cli_namespace.bootstrap
        entry_points_modules_map = dict(self.find_bootstraps())

        entry_point_module = entry_points_modules_map[bootstrap_name]

        try:
            operation: "BaseExportBootstrapOperation" = (
                entry_point_module.ExportOperation()
            )
        except AttributeError as err:
            logger.error(
                "%r. metadata does not contain BuildOperation attribute: %r.",
                self,
                entry_point_module,
            )
            raise Exception(
                f"Invalid metadata module for {bootstrap_name}"
            ) from err
        except Exception as err:
            logger.exception(
                "%r. unable to create operation instance from: %r. error: %r.",
                self,
                entry_point_module.Operation,
                err,
            )
            raise Exception(
                f"BuildOperation creation failed for {bootstrap_name}"
            ) from err

        operation.set_cli_namespace(self.cli_namespace)
        operation.run()


class BaseExportBootstrapOperation(BaseBootstrapsOperation):
    entry_point_path: t.ClassVar[str]

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""): ...

    @cached_property
    def bootstrap_path(self) -> "Path":
        return Path(self.entry_point_path).parent

    @cached_property
    def destination_path(self) -> "Path":
        if self.cli_namespace.destination_dir:
            return Path(os.getcwd(), self._cli_namespace.destination_dir)
        return Path.cwd()

    def run(self):
        self.create_destination_dir()
        self.populate_destination_dir()

    def create_destination_dir(self):
        try:
            os.makedirs(self.destination_path, exist_ok=True)
        except OSError as err:
            logger.error(
                "Unable the create the %r directory. Error: %r.",
                self.destination_path,
                err,
            )
            raise Exception("Creating destination directory") from err

    def populate_destination_dir(self):
        processor = CopyFilesProcessor()
        processor.set_source_path(source_path=self.bootstrap_path)
        processor.set_destination_path(destination_path=self.destination_path)
        processor.run()
