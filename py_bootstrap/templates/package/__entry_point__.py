__all__ = ("BuildOperation",)

import logging
import typing as t

from py_bootstrap.operations import BaseBuildBootstrapOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser

logger = logging.getLogger(__name__)

DESCRIPTION = "Generates a skeleton of Python Package"


class BuildOperation(BaseBuildBootstrapOperation):
    cli_description = DESCRIPTION
    cli_argument_name_help = "The name of the package"
    entry_point_path = __file__

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
        super().prepare_cli_parser(parser, prefix)
        parser.add_argument(
            "--author",
            dest="author",
            type=str,
            required=True,
            help="Author of the package.",
        )
        parser.add_argument(
            "--author-email",
            dest="author_email",
            type=str,
            required=True,
            help="Email of the author.",
        )
        parser.add_argument(
            "--repo",
            dest="repo",
            type=str,
            default="",
            help="Repository URL for the application.",
        )

    def build_context(self) -> dict[str, str]:
        context = super().build_context()

        context["author"] = self.cli_namespace.author
        context["author_email"] = self.cli_namespace.author_email
        context["repo"] = self.cli_namespace.repo

        return context
