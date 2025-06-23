import typing as t
from argparse import ArgumentParser
from unittest import TestCase

from py_bootstrap.base.operations import (
    BaseCliOperation,
    BaseOperationsRunner,
    BaseRecursiveOperationsContainer,
)

if t.TYPE_CHECKING:
    ...


class TstOperation(BaseCliOperation):
    cli_description = "Test operation"
    is_run: bool = False

    @classmethod
    def prepare_cli_parser(cls, parser: ArgumentParser, prefix: str = ""):
        parser.add_argument("--test-arg", help="A test argument.")

    def run(self):
        self.is_run = True


class TstNestedTwoContainer(BaseRecursiveOperationsContainer):
    cli_description = "Test nested two operations dispatcher"
    operations_classes_map = {
        "test": TstOperation,
    }


class TstNestedOneContainer(BaseRecursiveOperationsContainer):
    cli_description = "Test nested one operations dispatcher"
    operations_classes_map = {
        "nested-two": TstNestedTwoContainer,
        "test": TstOperation,
    }


class TstRootDispatcher(BaseRecursiveOperationsContainer):
    cli_description = "Test root operations dispatcher"
    operations_classes_map = {
        "nested-one": TstNestedOneContainer,
    }


class TstOperationsRunner(BaseOperationsRunner):
    cli_prog = "test"
    operation_cls = TstRootDispatcher


class BaseOperationsRunnerTestCase(TestCase):
    tst_cls = TstOperationsRunner
    tst_obj: TstOperationsRunner

    def setUp(self):
        self.tst_obj = self.tst_cls()

    def test_run_basic_flow(self):
        self.tst_obj.set_cli_args(
            ["nested-one", "nested-two", "test", "--test-arg=value"]
        )
        self.tst_obj.run()
        assert isinstance(self.tst_obj._operation, TstRootDispatcher)
        assert isinstance(
            self.tst_obj._operation._operation, TstNestedOneContainer
        )
        assert isinstance(
            self.tst_obj._operation._operation._operation,
            TstNestedTwoContainer,
        )
        assert isinstance(
            self.tst_obj._operation._operation._operation._operation,
            TstOperation,
        )
        tst_operation = self.tst_obj._operation._operation._operation._operation
        assert tst_operation._cli_namespace.test_arg == "value"
        assert tst_operation.is_run

    def test_run_undefined_operation(self):
        self.tst_obj.set_cli_args(
            ["nested-one", "nested-two", "wrong", "--test-arg=value"]
        )
        with self.assertRaises(SystemExit) as err_ctx:
            self.tst_obj.run()

        assert err_ctx.exception.code == 2
