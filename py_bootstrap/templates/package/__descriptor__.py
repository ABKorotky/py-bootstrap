__all__ = ("Descriptor",)

import logging
import re
import typing as t
from argparse import ArgumentTypeError
from functools import cached_property
from pathlib import Path

from py_bootstrap.operations import (
    BuildBootstrapDescriptionOperationExt,
    BuildBootstrapPythonNamesOperationExt,
)
from py_bootstrap.operations import Descriptor as _Descriptor
from py_bootstrap.operations import ExportBootstrapOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser, Namespace

logger = logging.getLogger(__name__)


class BuildOperation(
    BuildBootstrapPythonNamesOperationExt,
    BuildBootstrapDescriptionOperationExt,
):
    cli_description = "Generates a skeleton of a Python Application"

    cli_argument_author_help = "Specifies author's first and last names."
    cli_argument_author_email_help = (
        "Specifies author's email. Should be valid email address."
    )
    cli_argument_repo_help = (
        "Specifies a repository URL for the package. Should be a valid URL."
    )
    cli_argument_pypi_name_help = (
        "Specifies custom PyPI name if present "
        "or will be computed from the other CLI arguments."
        "Should contain lowercase letters, digits and hyphens only."
    )

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser"):
        super().prepare_cli_parser(parser=parser)
        parser.add_argument(
            "--author",
            dest="op_build_author",
            type=str,
            required=True,
            help=cls.cli_argument_author_help,
        )
        parser.add_argument(
            "--author-email",
            dest="op_build_author_email",
            type=cls.validate_cli_argument_author_email,
            required=True,
            help=cls.cli_argument_author_email_help,
        )
        parser.add_argument(
            "--repo",
            dest="op_build_repo",
            type=cls.validate_cli_argument_repo,
            default="",
            help=cls.cli_argument_repo_help,
        )
        parser.add_argument(
            "--pypi-name",
            dest="op_build_pypi_name",
            type=cls.validate_cli_argument_pypi_name,
            default="",
            help=cls.cli_argument_pypi_name_help,
        )

    @classmethod
    def validate_cli_argument_name(cls, value: str) -> str:
        if not re.match(r"^[a-z][a-z0-9-]+$", value):
            raise ArgumentTypeError("Invalid --cli-name CLI argument value provided")
        return value

    @classmethod
    def validate_cli_argument_author_email(cls, value: str) -> str:
        if not re.match(r"^\w[\w+.]+\w@[\w.]+$", value):
            raise ArgumentTypeError(
                "Invalid --author-email CLI argument value provided"
            )
        return value

    @classmethod
    def validate_cli_argument_repo(cls, value: str) -> str:
        if not re.match(r"^https?://\w+[\w.]+/.*$", value):
            raise ArgumentTypeError("Invalid --repo CLI argument value provided")
        return value

    @classmethod
    def validate_cli_argument_pypi_name(cls, value: str) -> str:
        if not re.match(r"^[a-z][a-z0-9-]*[a-z0-9]$", value):
            raise ArgumentTypeError("Invalid --pypi-name CLI argument value provided")
        return value

    def validate_cli_namespace(self, namespace: "Namespace"):
        criteria = any(
            [
                namespace.op_build_name,
                namespace.op_build_python_name,
            ]
        )
        if not criteria:
            logger.error("%r. one of criteria: name, python_name.", self)
            raise ValueError(
                "Malformed CLI arguments, neither name nor python_name provided."
            )

    @cached_property
    def cli_argument_python_name(self) -> str:
        python_name = super().cli_argument_pytho_name
        if python_name:
            return python_name
        return self.cli_argument_name

    def build_context(self) -> dict[str, str]:
        context = super().build_context()
        context["author"] = self.cli_argument_author
        context["author_email"] = self.cli_argument_author_email
        context["repo"] = self.cli_argument_repo
        context["pypi_name"] = self.cli_argument_pypi_name
        return context

    @property
    def cli_argument_author(self) -> str:
        return self.cli_namespace.op_build_author

    @property
    def cli_argument_author_email(self) -> str:
        return self.cli_namespace.op_build_author_email

    @property
    def cli_argument_repo(self) -> str:
        return self.cli_namespace.op_build_repo

    @cached_property
    def cli_argument_pypi_name(self) -> str:
        value = self.cli_namespace.op_build_pypi_name
        if value:
            return value
        return "-".join(self.python_name_parts)


class ExportOperation(ExportBootstrapOperation):
    cli_description = "Exports a Python's Application template files"


_CLI_HELP = """Provides two operations:
    - a builder for generating skeletons of Python Package.
    - an exporter of Python Package template files.
"""


class Descriptor(_Descriptor):
    cli_description = "Python Packages bootstrapping"
    cli_help = _CLI_HELP
    templates_path = Path(__file__).parent
    op_build_cls = BuildOperation
    op_export_cls = ExportOperation
