import typing as t
from argparse import ArgumentParser, Namespace
from unittest import TestCase

from py_bootstrap.base.operations import (
    BaseCliOperation,
    BaseOperation,
)

if t.TYPE_CHECKING:
    ...


class BaseOperationTestCase(TestCase):
    tst_cls = BaseOperation

    def setUp(self):
        self.tst_obj = self.tst_cls()

    def test_run(self):
        with self.assertRaises(NotImplementedError):
            self.tst_obj.run()


class BaseCliOperationTestCase(BaseOperationTestCase):
    tst_cls = BaseCliOperation
    tst_obj: BaseCliOperation

    def test_prepare_cli_parser(self):
        with self.assertRaises(NotImplementedError):
            self.tst_cls.prepare_cli_parser(ArgumentParser())

    def test_set_cli_namespace(self):
        namespace = Namespace()
        self.tst_obj.set_cli_namespace(namespace=namespace)
        assert self.tst_obj._cli_namespace == namespace
