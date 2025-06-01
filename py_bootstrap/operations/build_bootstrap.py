__all__ = ("BuildBootstrapOperation",)

import logging
import os
import typing as t
from functools import cached_property
from shutil import copyfile

from .base import BaseBootstrapOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser


logger = logging.getLogger(__name__)


class BuildBootstrapOperation(BaseBootstrapOperation):
    cli_description = "Generates a skeleton from given bootstrap."
    excluded_directories: list[str] = ["__pycache__"]
    excluded_file_extensions: list[str] = []

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
        super().prepare_cli_parser(parser=parser, prefix=prefix)
        parser.add_argument(
            "--dest",
            dest="destination_dir",
            type=str,
            default="",
            help=(
                "Specifies the destination directory for generating."
                " Current directory by default."
            ),
        )

    @cached_property
    def destination_path(self) -> str:
        if not self._cli_namespace.destination_dir:
            return os.getcwd()
        return os.path.join(os.getcwd(), self._cli_namespace.destination_dir)

    def run(self):
        self.validate_context()
        self.prepare_context()
        self.create_destination_dir()
        self.populate_destination_dir()

    def validate_context(self):
        try:
            self.metadata_module.validate_context(context=self.context)
        except Exception as err:
            logger.error(
                "Unable to validate context for the %r bootstrap. Error: %r.",
                self.name,
                err,
            )
            raise Exception("Context is invalid") from err

    def prepare_context(self):
        try:
            self.metadata_module.prepare_context(context=self.context)
        except Exception as err:
            logger.error(
                "Unable to prepare context for the %r bootstrap. Error: %r.",
                self.name,
                err,
            )
            raise Exception("Preparing context") from err

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
        logger.debug(
            "Fill %r directory from %r.",
            self.destination_path,
            self.bootstrap_path,
        )
        for root_path, dirs_names, files_names in os.walk(self.bootstrap_path):
            logger.debug("Process %r source root.", root_path)
            rel_path = os.path.normpath(
                os.path.relpath(root_path, start=self.bootstrap_path)
            )
            destination_base_path = os.path.join(
                self.destination_path, rel_path
            )

            for dir_name in dirs_names:
                if not self.check_directory_for_generating(dir_name=dir_name):
                    logger.debug(
                        "Directory %s/%s is skipped from generating.",
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
                if not self.check_file_for_generating(
                    file_name=file_name, file_ext=file_ext
                ):
                    logger.debug(
                        "File %s/%s is skipped from generating.",
                        root_path,
                        file_name,
                    )
                    continue

                try:
                    self.generate_file(
                        source_base_path=root_path,
                        destination_base_path=destination_base_path,
                        file_name=file_name,
                        file_ext=file_ext,
                    )
                except Exception as err:
                    logger.warning(
                        "Unable to generate %r/%r file. Error: %r.",
                        root_path,
                        full_file_name,
                        err,
                    )
                else:
                    logger.debug(
                        "File %s/%s is generated successfully.",
                        root_path,
                        full_file_name,
                    )

    def check_directory_for_generating(self, dir_name: str) -> bool:
        return dir_name not in self.excluded_directories

    def generate_directory(self, destination_base_path: str, dir_name: str):
        destination_path = os.path.join(destination_base_path, dir_name)
        destination_path = self.generate_content_from_template(
            template=destination_path
        )
        try:
            os.makedirs(destination_path)
        except FileExistsError:
            ...
        else:
            logger.info("Directory %r is created.", destination_path)

    def check_file_for_generating(self, file_name: str, file_ext: str) -> bool:
        if file_name.startswith(self.metadata_module_name):
            return False
        return file_ext not in self.excluded_file_extensions

    def generate_file(
        self,
        source_base_path: str,
        destination_base_path: str,
        file_name: str,
        file_ext: str,
    ):
        source_path = os.path.join(source_base_path, file_name + file_ext)
        if file_ext == ".tmpl":
            destination_path = self.generate_content_from_template(
                template=os.path.join(destination_base_path, file_name)
            )
            self.generate_file_from_template(
                source_path=source_path,
                destination_path=destination_path,
            )
        else:
            destination_path = self.generate_content_from_template(
                template=os.path.join(
                    destination_base_path, file_name + file_ext
                )
            )
            self.generate_file_from_copy(
                source_path=source_path, destination_path=destination_path
            )

    def generate_file_from_template(
        self, source_path: str, destination_path: str
    ):
        source_rel_path = os.path.relpath(source_path)
        destination_rel_path = os.path.relpath(destination_path)
        with open(source_path) as fd:
            origin_content = fd.read()
        prepared_content = self.generate_content_from_template(
            template=origin_content
        )
        with open(destination_path, mode="w+") as fd:
            fd.write(prepared_content)
        logger.info(
            "Create %s file from the %s template.",
            destination_rel_path,
            source_rel_path,
        )

    def generate_file_from_copy(self, source_path: str, destination_path: str):
        source_rel_path = os.path.relpath(source_path)
        destination_rel_path = os.path.relpath(destination_path)
        copyfile(source_path, destination_path)
        logger.info(
            "Copy %s file to %s.", source_rel_path, destination_rel_path
        )

    def generate_content_from_template(self, template: str) -> str:
        return template.format(**self.context)
