__all__ = ("RegisterBootstrapOperation",)

import logging
import os
import typing as t
from functools import cached_property
from shutil import copyfile

from .base import BaseBootstrapOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser


logger = logging.getLogger(__name__)


class RegisterBootstrapOperation(BaseBootstrapOperation):
    cli_description = "Register an user bootstrap."

    excluded_directories: list[str] = ["__pycache__"]
    excluded_file_extensions: list[str] = ["pyo", "pyc"]

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
        super().prepare_cli_parser(parser=parser, prefix=prefix)
        parser.add_argument(
            "--source",
            dest="source_dir",
            type=str,
            default="",
            help=(
                "Specifies the source directory with metadata and bootstrap templates."
                " Current directory by default."
            ),
        )
        parser.add_argument(
            "-y",
            "--override",
            dest="is_override_mode",
            action="store_true",
            default=False,
            help=(
                "Override existing bootstrap with the same name if it exists."
                " By default, it will not override."
            ),
        )

    @cached_property
    def source_path(self) -> str:
        if not self._cli_namespace.source_dir:
            return os.getcwd()
        return os.path.join(os.getcwd(), self._cli_namespace.source_dir)

    @property
    def is_override_mode(self) -> bool:
        return self._cli_namespace.is_override_mode

    def run(self):
        # TODO. add some validations before registering.
        self.create_bootstrap_dir()
        self.populate_bootstrap_dir()

    def create_bootstrap_dir(self):
        try:
            os.makedirs(self.bootstrap_path, exist_ok=self.is_override_mode)
        except OSError as err:
            logger.error(
                "Unable the create the %r directory. Error: %r.",
                self.bootstrap_path,
                err,
            )
            raise Exception("Creating bootstrap directory") from err

    def populate_bootstrap_dir(self):
        logger.debug(
            "Fill %r directory from %r.",
            self.bootstrap_path,
            self.source_path,
        )
        for root_path, dirs_names, files_names in os.walk(self.source_path):
            logger.debug("Process %r source root.", root_path)
            rel_path = os.path.normpath(
                os.path.relpath(root_path, start=self.bootstrap_path)
            )
            destination_base_path = os.path.join(self.bootstrap_path, rel_path)

            for dir_name in dirs_names:
                if not self.check_directory_for_uploading(dir_name=dir_name):
                    logger.debug(
                        "Directory %s/%s is skipped from uploading.",
                        root_path,
                        dir_name,
                    )
                    continue

                try:
                    self.generate_directory(
                        destination_base_path=destination_base_path,
                        dir_name=dir_name,
                    )
                except Exception as err:
                    logger.warning(
                        "Unable to generate %r/%r directory. Error: %r.",
                        root_path,
                        dir_name,
                        err,
                    )
                else:
                    logger.debug(
                        "Directory %s/%s is generated successfully.",
                        root_path,
                        dir_name,
                    )

            for full_file_name in files_names:
                file_name, file_ext = os.path.splitext(full_file_name)
                if not self.check_file_for_uploading(
                    file_name=file_name, file_ext=file_ext
                ):
                    logger.debug(
                        "File %s/%s is skipped from uploading.",
                        root_path,
                        full_file_name,
                    )
                    continue

                try:
                    self.upload_file(
                        source_base_path=root_path,
                        destination_base_path=destination_base_path,
                        file_name=full_file_name,
                    )
                except Exception as err:
                    logger.warning(
                        "Unable to upload %r/%r file. Error: %r.",
                        root_path,
                        full_file_name,
                        err,
                    )
                else:
                    logger.debug(
                        "File %s/%s is uploaded successfully.",
                        root_path,
                        full_file_name,
                    )

    def check_directory_for_uploading(self, dir_name: str) -> bool:
        return dir_name not in self.excluded_directories

    def generate_directory(self, destination_base_path: str, dir_name: str):
        destination_path = os.path.join(destination_base_path, dir_name)
        try:
            os.makedirs(destination_path)
        except FileExistsError:
            ...
        else:
            logger.info("Directory %r is created.", destination_path)

    def check_file_for_uploading(self, file_name: str, file_ext: str) -> bool:
        return file_ext not in self.excluded_file_extensions

    def upload_file(
        self, source_base_path: str, destination_base_path: str, file_name: str
    ):
        source_path = os.path.join(source_base_path, file_name)
        destination_path = os.path.join(destination_base_path, file_name)
        copyfile(source_path, destination_path)
        logger.info(
            "File is copied from %s to %s.", source_path, destination_path
        )
