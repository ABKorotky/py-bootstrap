__all__ = (
    "BaseOperation",
    "BaseCliOperation",
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

    @property
    def cli_namespace(self) -> "Namespace":
        return self._cli_namespace

    def set_cli_namespace(self, namespace: "Namespace"):
        self._cli_namespace = namespace
