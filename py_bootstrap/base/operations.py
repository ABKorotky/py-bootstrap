__all__ = (
    "BaseOperation",
    "BaseCliOperation",
    "BaseOperationsDispatcher",
    "BaseOperationsRunner",
)

import logging
import typing as t
from argparse import ArgumentParser

if t.TYPE_CHECKING:
    from argparse import Namespace

logger = logging.getLogger(__name__)


class BaseOperation:
    def run(self):
        raise NotImplementedError(f"{self.__class__}.run")


class BaseCliOperation(BaseOperation):
    cli_description: t.ClassVar[str]

    _cli_namespace: "Namespace"

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
        raise NotImplementedError(f"{cls.__name__}.prepare_cli_parser")

    def set_cli_namespace(self, namespace: "Namespace"):
        self._cli_namespace = namespace


class BaseOperationsDispatcher(BaseCliOperation):

    operations_classes_map: t.ClassVar[dict[str, type["BaseCliOperation"]]] = {}

    _cli_parent_prefix: str = ""
    _operation: "BaseCliOperation"

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser", prefix: str = ""):
        dest = f"__operation__{prefix}" if prefix else "__operation"
        subparsers = parser.add_subparsers(
            title="Registered operations", dest=dest, required=True
        )
        for (
            cli_name,
            operation_cls,
        ) in cls.operations_classes_map.items():
            subparser = subparsers.add_parser(
                cli_name, help=operation_cls.cli_description
            )
            dest_name = cli_name.replace("-", "_")
            operation_prefix = f"{prefix}__{dest_name}" if prefix else dest_name
            logger.debug("%r. prepare CLI parser from: %r.", cls, operation_cls)
            operation_cls.prepare_cli_parser(
                parser=subparser, prefix=operation_prefix
            )

    def run(self):
        operation_attr_name = (
            f"__operation__{self._cli_parent_prefix}"
            if self._cli_parent_prefix
            else "__operation"
        )
        cli_name = getattr(self._cli_namespace, operation_attr_name)

        operation_cls = self.operations_classes_map[cli_name]
        logger.debug("%r. found operation class: %r.", self, operation_cls)

        operation = operation_cls()
        self._operation = operation

        operation.set_cli_namespace(namespace=self._cli_namespace)

        if isinstance(operation, BaseOperationsDispatcher):
            dest_name = cli_name.replace("-", "_")
            prefix = (
                f"{self._cli_parent_prefix}__{dest_name}"
                if self._cli_parent_prefix
                else dest_name
            )
            operation.set_cli_parent_prefix(prefix=prefix)

        operation.run()

    def set_cli_parent_prefix(self, prefix: str):
        self._cli_parent_prefix = prefix


class BaseOperationsRunner:
    cli_prog: t.ClassVar[str]
    operation_cls: t.ClassVar[type["BaseCliOperation"]]

    _cli_args: t.Optional[list[str]] = None
    _operation: "BaseCliOperation"

    def set_cli_args(self, cli_args: list[str]):
        self._cli_args = cli_args

    def run(self):
        parser = self.build_cli_parser()
        self.operation_cls.prepare_cli_parser(parser=parser)
        namespace = self.parse_cli_args(parser=parser)

        operation = self.operation_cls()
        self._operation = operation

        operation.set_cli_namespace(namespace=namespace)
        logger.debug("%r. running operation: %r.", self, operation)
        operation.run()

    def build_cli_parser(self) -> "ArgumentParser":
        params = self.get_cli_parser_creating_parameters()
        logger.debug("CLI parser creating parameters: %r.", params)
        return ArgumentParser(**params)

    def get_cli_parser_creating_parameters(self) -> dict:
        return {
            "prog": self.cli_prog,
            "description": self.operation_cls.cli_description,
        }

    def parse_cli_args(self, parser: "ArgumentParser") -> "Namespace":
        logger.debug("CLI arguments: %r.", self._cli_args)
        namespace, unparsed_args = parser.parse_known_args(self._cli_args)
        logger.debug(
            "parsed CLI arguments: %r. unparsed: %r.", namespace, unparsed_args
        )
        return namespace
