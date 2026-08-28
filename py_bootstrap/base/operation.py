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

    _dry_run: bool = False

    def set_dry_run_mode(self):
        self._dry_run = True
        logger.debug("%r. sry-run mode is set.", self)

    def log_dry_run_action(self, action: str, **kwargs):
        logger.warning("%r. dry-run mode. %s.", self, action, **kwargs)

    def run(self):
        raise NotImplementedError(f"{self.__class__}.run")


class BaseCliOperation(BaseOperation):
    cli_description: t.ClassVar[str]
    cli_help: str = ""

    @classmethod
    def prepare_cli_parser(cls, parser: "ArgumentParser"):
        raise NotImplementedError(f"{cls.__name__}.prepare_cli_parser")

    _cli_namespace: "Namespace"

    @property
    def cli_namespace(self) -> "Namespace":
        return self._cli_namespace

    def set_cli_namespace(self, namespace: "Namespace"):
        self.validate_cli_namespace(namespace=namespace)
        self._cli_namespace = namespace

    def validate_cli_namespace(self, namespace: "Namespace"): ...
