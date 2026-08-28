__all__ = ("BuildBootstrapPythonNamesOperationExt",)

import logging
import re
import typing as t
from argparse import ArgumentTypeError
from functools import cached_property

from .base import BuildBootstrapOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser


logger = logging.getLogger(__name__)


class BuildBootstrapPythonNamesOperationExt(BuildBootstrapOperation):
    cli_argument_python_name_help: str = (
        "Specifies python name of generated entity. Should be valid python name."
    )
    cli_argument_python_upper_name_help: str = (
        "Specifies custom puthon name in UPPER_CASE if present "
        "or will be computed from the --python-name."
    )
    cli_argument_python_class_name_help: str = (
        "Specifies custom puthon name in PascalCase if present "
        "or will be computed from the --python-name."
    )
    cli_argument_hyphen_name_help: str = (
        "Specifies custom hyphen name in kebab-case if present "
        "or will be computed from the --python-name."
    )
    cli_argument_title_help: str = (
        "Specifies custom title in 'Title Case' if present "
        "or will be computed from --python-name."
    )

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser"):
        super().prepare_cli_parser(parser=parser)
        parser.add_argument(
            "--python-name",
            dest="op_build_python_name",
            type=cls.validate_cli_argument_python_name,
            required=True,
            help=cls.cli_argument_python_name_help,
        )
        parser.add_argument(
            "--python-upper-name",
            dest="op_build_python_upper_name",
            type=cls.validate_cli_argument_python_upper_name,
            default="",
            help=cls.cli_argument_python_upper_name_help,
        )
        parser.add_argument(
            "--python-class-name",
            dest="op_build_python_class_name",
            type=cls.validate_cli_argument_python_class_name,
            default="",
            help=cls.cli_argument_python_class_name_help,
        )
        parser.add_argument(
            "--hyphen-name",
            dest="op_build_hyphen_name",
            type=cls.validate_cli_argument_hyphen_name,
            default="",
            help=cls.cli_argument_hyphen_name_help,
        )
        parser.add_argument(
            "--title",
            dest="op_build_title",
            type=cls.validate_cli_argument_title,
            default="",
            help=cls.cli_argument_title_help,
        )

    @classmethod
    def validate_cli_argument_python_name(cls, value: str) -> str:
        if not re.match(r"^[a-z][a-z0-9_]*[a-z0-9]$", value):
            raise ArgumentTypeError("Invalid --python-name CLI argument value provided")
        return value

    @classmethod
    def validate_cli_argument_python_upper_name(cls, value: str) -> str:
        if not value:
            return ""

        if not re.match(r"^[A-Z][A-Z0-9_]*[A-Z0-9]$", value):
            raise ArgumentTypeError(
                "Invalid --python-upper-name CLI argument value provided"
            )
        return value

    @classmethod
    def validate_cli_argument_python_class_name(cls, value: str) -> str:
        if not value:
            return ""

        if not re.match(r"^[A-Z][a-zA-Z0-9]+$", value):
            raise ArgumentTypeError(
                "Invalid --python-class-name CLI argument value provided"
            )
        return value

    @classmethod
    def validate_cli_argument_hyphen_name(cls, value: str) -> str:
        if not value:
            return ""

        if not re.match(r"^[a-z][a-z0-9-]*[a-z0-9]$", value):
            raise ArgumentTypeError("Invalid --hyphen-name CLI argument value provided")
        return value

    @classmethod
    def validate_cli_argument_title(cls, value: str) -> str:
        if not value:
            return ""

        if not re.match(r"^([A-Z][a-z0-9]* ?)+$", value):
            raise ArgumentTypeError("Invalid --title CLI argument value provided")
        return value.strip()

    def build_context(self) -> dict[str, str]:
        ctx = super().build_context()
        ctx["python_name"] = self.cli_argument_python_name
        ctx["upper_name"] = self.cli_argument_python_upper_name
        ctx["class_name"] = self.cli_argument_python_class_name
        ctx["hyphen_name"] = self.cli_argument_hyphen_name
        ctx["title"] = self.cli_argument_title
        return ctx

    @property
    def cli_argument_python_name(self) -> str:
        return self.cli_namespace.op_build_python_name

    @cached_property
    def python_name_parts(self) -> list[str]:
        return self.cli_argument_python_name.split("_")

    @cached_property
    def cli_argument_python_upper_name(self) -> str:
        value = self.cli_namespace.op_build_python_upper_name
        if value:
            return value
        return "_".join([i.upper() for i in self.python_name_parts])

    @cached_property
    def cli_argument_python_class_name(self) -> str:
        value = self.cli_namespace.op_build_python_class_name
        if value:
            return value
        return "".join([i.title() for i in self.python_name_parts])

    @cached_property
    def cli_argument_hyphen_name(self) -> str:
        value = self.cli_namespace.op_build_python_upper_name
        if value:
            return value
        return "-".join(self.python_name_parts)

    @cached_property
    def cli_argument_title(self) -> str:
        value = self.cli_namespace.op_build_title
        if value:
            return value
        return " ".join([i.title() for i in self.python_name_parts])
