__all__ = ("RegisterBootstrapOperation",)

import logging
import shutil
import typing as t
from argparse import ArgumentTypeError
from functools import cached_property
from pathlib import Path

import py_bootstrap.templates as templates_module
from py_bootstrap.files_processors import CopyFilesProcessor

from .base import BaseBootstrapsOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser


logger = logging.getLogger(__name__)


class RegisterBootstrapOperation(BaseBootstrapsOperation):
    cli_description = "Registers a new bootstrap."
    templates_path = Path(templates_module.__file__).parent

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
        parser.add_argument(
            "--name",
            dest="bootstrap_name",
            type=str,
            required=True,
            help="Specifies name of registered bootstrap template.",
        )
        parser.add_argument(
            "--source",
            dest="source_path",
            type=cls.validate_cli_argument_source_path,
            required=True,
            help=(
                "Specifies a directory with entry-point and other bootstrap files."
                " Current directory by default."
            ),
        )
        parser.add_argument(
            "-y",
            "--yes-upload",
            dest="upload_confirmation",
            action="store_true",
            help="Do not prompt for confirmation.",
        )

    @classmethod
    def validate_cli_argument_source_path(cls, value: str) -> "Path":
        source_path = Path(value)
        if not source_path.is_absolute():
            source_path = Path.cwd() / source_path

        if not source_path.exists():
            raise ArgumentTypeError(f"{source_path} does not exist")

        return source_path

    @cached_property
    def bootstrap_path(self) -> "Path":
        return Path(self.templates_path) / self._cli_namespace.bootstrap_name

    @cached_property
    def source_path(self) -> "Path":
        return self._cli_namespace.source_path

    @cached_property
    def upload_confirmation(self) -> bool:
        return self._cli_namespace.upload_confirmation

    def run(self):
        self.validate_source_dir()

        if not self.upload_confirmation:
            answer = input("Do you want to continue? [y/N] ")
            if answer.lower() != "y":
                return

        self.prepare_bootstrap_dir()
        self.populate_bootstrap_dir()

    def validate_source_dir(self):
        entry_point_path = (
            self.source_path / f"{self.entry_point_module_name}.py"
        )
        if not entry_point_path.exists():
            logger.error(
                "%r. entry-point file is missed. path: %r.",
                self,
                entry_point_path,
            )
            raise Exception("entry-point file is missed")

        content = entry_point_path.read_text()
        if "BuildOperation" not in content:
            logger.error(
                "%r. entry-point file does not contain BuildOperation class.",
                self,
            )
            raise Exception(
                "BuildOperation class is missed in entry-point file"
            )
        if "ExportOperation" not in content:
            logger.error(
                "%r. entry-point file does not contain ExportOperation class.",
                self,
            )
            raise Exception(
                "ExportOperation class is missed in entry-point file"
            )

    def prepare_bootstrap_dir(self):
        if self.bootstrap_path.exists():
            shutil.rmtree(self.bootstrap_path)

        self.bootstrap_path.mkdir()

    def populate_bootstrap_dir(self):
        processor = CopyFilesProcessor()
        processor.set_source_path(source_path=self.source_path)
        processor.set_destination_path(destination_path=self.bootstrap_path)
        processor.run()
