__all__ = (
    "DestinationPathOperationExt",
    "DescriptorOperationExt",
    "BaseDescriptor",
    "BaseBootstrapsDispatcherOperation",
)

import logging
import os
import typing as t

from py_bootstrap.base import BaseCliOperation

from .bootstraps_finder import BOOTSTRAPS_FINDER

if t.TYPE_CHECKING:
    from argparse import ArgumentParser
    from pathlib import Path


logger = logging.getLogger(__name__)


class DestinationPathOperationExt(BaseCliOperation):

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser"):
        parser.add_argument(
            "--dest",
            dest="destination_path",
            default=".",
            type=cls.validate_cli_argument_destination_dir,
            help="Specifies the destination directory. Current directory by default.",
        )

    @classmethod
    def validate_cli_argument_destination_dir(cls, value: str) -> "Path":
        path = Path(os.getcwd())

        if value:
            path = path / value

        if not path.exists():
            return path

        if path.is_dir():
            return path

        import argparse

        raise argparse.ArgumentTypeError(f"--dest={value} is not a valid directory")

    @property
    def cli_destination_path(self) -> "Path":
        return self.cli_namespace.destination_path

    def run(self):
        if self._dry_run:
            self.log_dry_run_action(
                action="destination directory is created: %r"
                % self.cli_destination_path
            )
            return

        self.create_destination_dir()

    def create_destination_dir(self):
        try:
            os.makedirs(self.cli_destination_path, exist_ok=True)
            logger.info(
                "%r. destination directory is created: %r.",
                self,
                self.cli_destination_path,
            )
        except OSError as err:
            logger.error(
                "unable the create the %r directory. Error: %r.",
                self.cli_destination_path,
                err,
            )
            raise err


class BaseDescriptor:
    cli_description: t.ClassVar[str]
    cli_help: str = ""
    templates_path: t.ClassVar["Path"]


DescriptorTypeVar = t.TypeVar("DescriptorTypeVar", bound="BaseDescriptor")


class DescriptorOperationExt(BaseCliOperation, t.Generic[DescriptorTypeVar]):
    _descriptor: type[DescriptorTypeVar]

    def set_descriptor(self, descriptor: type[DescriptorTypeVar]) -> None:
        self._descriptor = descriptor


OperationTypeVar = t.TypeVar("OperationTypeVar", bound="DescriptorOperationExt")


class BaseBootstrapsDispatcherOperation(
    BaseCliOperation, t.Generic[DescriptorTypeVar, OperationTypeVar]
):

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser"):
        subparsers = parser.add_subparsers(
            title="Found bootstraps", dest="bootstrap_name", required=True
        )
        for name, descriptor in BOOTSTRAPS_FINDER.list():
            cli_description = cls.get_cli_subparser_description(descriptor=descriptor)
            cli_help = cls.get_cli_subparser_help(descriptor=descriptor)
            subparser = subparsers.add_parser(
                name,
                description=cli_description,
                help=cli_help,
            )
            cls.prepare_cli_subparser(subparser=subparser, descriptor=descriptor)

    @classmethod
    def get_cli_subparser_description(cls, descriptor: type[DescriptorTypeVar]) -> str:
        raise NotImplementedError(f"{cls.__name__}.get_cli_subparser_description")

    @classmethod
    def get_cli_subparser_help(cls, descriptor: type[DescriptorTypeVar]) -> str:
        raise NotImplementedError(f"{cls.__name__}.get_cli_subparser_help")

    @classmethod
    def prepare_cli_subparser(
        cls, subparser: "ArgumentParser", descriptor: type[DescriptorTypeVar]
    ):
        raise NotImplementedError(f"{cls.__name__}.prepare_cli_subparser")

    @property
    def cli_bootstrap_name(self) -> str:
        return self.cli_namespace.bootstrap_name

    def run(self):
        descriptor = BOOTSTRAPS_FINDER.get(name=self.cli_bootstrap_name)
        operation = self.create_operation(descriptor=descriptor)
        operation.set_cli_namespace(namespace=self.cli_namespace)
        if self._dry_run:
            operation.set_dry_run_mode()
        operation.set_descriptor(descriptor=descriptor)
        operation.run()

    def create_operation(self, descriptor: type[DescriptorTypeVar]) -> OperationTypeVar:
        raise NotImplementedError(f"{self.__class__}.create_operation")
