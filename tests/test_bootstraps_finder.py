import typing as t
from importlib.metadata import EntryPoint
from unittest import TestCase

from py_bootstrap.operations.bootstraps_finder import FindBootstrapsOperation
from tests import tst_templates
from tests.tst_templates.tst_bootstrap.__descriptor__ import Descriptor

if t.TYPE_CHECKING:
    ...


class TstFindBootstrapsOperation(FindBootstrapsOperation):
    def get_bootstraps_entry_points(self) -> t.Iterable["EntryPoint"]:
        return [EntryPoint("test", tst_templates.__package__, "py_bootstrap_templates")]


class BootstrapsFinderTestCase(TestCase):
    tst_obj: TstFindBootstrapsOperation

    def setUp(self):
        self.tst_obj = TstFindBootstrapsOperation()

    def test_run(self):
        tst_res = list(self.tst_obj.list())
        assert len(tst_res) >= 1, len(tst_res)

        for name, descriptor in tst_res:
            assert name in ("tst_bootstrap",)
            if name == "tst_bootstrap":
                assert descriptor == Descriptor
