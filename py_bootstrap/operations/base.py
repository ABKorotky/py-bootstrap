__all__ = (
    "BaseBootstrapsOperation",
    "BaseBootstrapOperation",
)

import logging
import os
import typing as t
from argparse import ArgumentTypeError
from copy import deepcopy
from functools import cached_property
from importlib import import_module

import py_bootstrap as package
from py_bootstrap.base.operations import BaseCliOperation

if t.TYPE_CHECKING:
    from argparse import ArgumentParser
    from types import ModuleType


logger = logging.getLogger(__name__)


class BaseBootstrapsOperation(BaseCliOperation):
    package = package
    templates_dir_name = "templates"
    metadata_module_name = "__metadata__"

    @property
    def package_path(self) -> str:
        return self.package.__path__[0]

    def load_bootstrap_metadata(self, name: str) -> "ModuleType":
        try:
            return import_module(
                f"{self.package.__name__}.{self.templates_dir_name}.{name}"
                f".{self.metadata_module_name}"
            )
        except ImportError as err:
            logger.error(
                "%r. failed to import metadata for %r: %s.", self, name, err
            )
            raise Exception("Loading bootstrap metadata") from err


class BaseBootstrapOperation(BaseBootstrapsOperation):

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
        parser.add_argument(
            "-n",
            "--name",
            dest="name",
            type=str,
            required=True,
            help="Name of the bootstrap.",
        )
        parser.add_argument(
            "-c",
            "--context",
            dest="context_overrides",
            action="append",
            default=[],
            help=(
                "Context overrides in the form of key:value pairs."
                " Can be specified multiple times."
            ),
            type=cls.validate_cli_argument_context,
        )

    @classmethod
    def validate_cli_argument_context(cls, value: str) -> str:
        if ":" not in value:
            raise ArgumentTypeError(
                f"Malformed context value: {value}. Expected format is key:value."
            )
        return value

    @property
    def name(self) -> str:
        return self._cli_namespace.name

    @cached_property
    def bootstrap_path(self) -> str:
        return os.path.join(
            self.package_path, self.templates_dir_name, self.name
        )

    @cached_property
    def metadata_module(self) -> "ModuleType":
        return self.load_bootstrap_metadata(name=self.name)

    @cached_property
    def context(self) -> dict[str, str]:
        ctx = deepcopy(self.metadata_module.CONTEXT)
        for override in self._cli_namespace.context_overrides:
            key, value = override.split(":", 1)
            ctx[key] = value
        return ctx
