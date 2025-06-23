__all__ = ("BaseRecursiveOperationsContainer",)

import logging
import typing as t
from argparse import ArgumentParser

from .base import BaseCliOperation

if t.TYPE_CHECKING:
    ...

logger = logging.getLogger(__name__)


class BaseRecursiveOperationsContainer(BaseCliOperation):
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
        cli_name = getattr(self.cli_namespace, operation_attr_name)

        operation_cls = self.operations_classes_map[cli_name]
        logger.debug("%r. found operation class: %r.", self, operation_cls)

        operation = operation_cls()
        self._operation = operation

        operation.set_cli_namespace(namespace=self.cli_namespace)

        if isinstance(operation, BaseRecursiveOperationsContainer):
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
