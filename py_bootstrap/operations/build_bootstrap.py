__all__ = (
    "BuildBootstrapsDispatcherOperation",
    "BaseBuildBootstrapOperation",
)

import logging
import os
import re
import typing as t
from datetime import datetime
from functools import cached_property
from pathlib import Path

from py_bootstrap import PY_VERSION
from py_bootstrap.files_processors import GenerateFilesProcessor

from .base import BaseBootstrapsOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser


logger = logging.getLogger(__name__)


class BuildBootstrapsDispatcherOperation(BaseBootstrapsOperation):
    cli_description = "Generates a skeleton of something from given bootstrap."

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
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

        subparsers = parser.add_subparsers(
            title="Found bootstraps", dest="bootstrap", required=True
        )
        # prepare parsers for templates
        for name, entry_point_module in cls.find_bootstraps():
            template_parser = subparsers.add_parser(
                name,
                description=entry_point_module.BuildOperation.cli_description,
                help=entry_point_module.BuildOperation.cli_description,
            )
            entry_point_module.BuildOperation.prepare_cli_parser(
                parser=template_parser, prefix=name
            )

    def run(self):
        bootstrap_name = self.cli_namespace.bootstrap
        entry_points_modules_map = dict(self.find_bootstraps())

        entry_point_module = entry_points_modules_map[bootstrap_name]

        try:
            operation: "BaseBuildBootstrapOperation" = (
                entry_point_module.BuildOperation()
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


class BaseBuildBootstrapOperation(BaseBootstrapsOperation):
    entry_point_path: t.ClassVar[str]
    cli_argument_name_help: t.ClassVar[str]
    cli_argument_description_help: t.ClassVar[str]

    _context: dict[str, str]

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
        parser.add_argument(
            "--name",
            dest="name",
            type=cls.validate_cli_argument_name,
            required=True,
            help=cls.cli_argument_name_help,
        )
        parser.add_argument(
            "--description",
            dest="description",
            type=str,
            required=True,
            help=cls.cli_argument_description_help,
        )

    @classmethod
    def validate_cli_argument_name(cls, value: str) -> str:
        if not re.match(r"^[a-z0-9-]+$", value):
            raise ValueError(
                "The name can only contain alphanumeric characters and hyphens."
            )
        return value

    @cached_property
    def bootstrap_path(self) -> "Path":
        return Path(self.entry_point_path).parent

    @cached_property
    def destination_path(self) -> "Path":
        if self.cli_namespace.destination_dir:
            return Path(os.getcwd(), self._cli_namespace.destination_dir)
        return Path.cwd()

    def run(self):
        self._context = self.build_context()
        self.create_destination_dir()
        self.populate_destination_dir()

    def build_context(self) -> dict[str, str]:
        name = self.cli_namespace.name.strip()
        name_parts: list[str] = name.split("-")

        underscored_name = "_".join(name_parts)
        upper_name = "_".join(i.upper() for i in name_parts)
        class_name = "".join(i.title() for i in name_parts)
        title = " ".join(i.title() for i in name_parts)

        now = datetime.now()
        return {
            "name": name,
            "underscored_name": underscored_name,
            "upper_name": upper_name,
            "class_name": class_name,
            "title": title,
            "description": self.cli_namespace.description.strip(),
            "empty": "",
            "date_today": now.strftime("%Y-%m-%d"),
            "date_year": str(now.year),
            "python_major": str(PY_VERSION[0]),
            "python_minor": str(PY_VERSION[1]),
        }

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
        processor = GenerateFilesProcessor()
        processor.set_source_path(source_path=self.bootstrap_path)
        processor.set_destination_path(destination_path=self.destination_path)
        processor.set_context(value=self._context)
        processor.set_entry_point_file_name(
            value=f"{self.entry_point_module_name}.py"
        )
        processor.run()
