import contextlib
import io
import typing as t
from argparse import Namespace
from unittest import TestCase

from list_bootstraps import ListBootstrapsOperation

if t.TYPE_CHECKING:
    ...


class ListBootstrapsOperationTestCase(TestCase):
    tst_cls = ListBootstrapsOperation
    tst_obj: ListBootstrapsOperation

    def setUp(self):
        self.tst_obj = self.tst_cls()

    def test_run(self):
        namespace = Namespace()
        self.tst_obj.set_cli_namespace(namespace=namespace)

        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            self.tst_obj.run()

        output = mock_stdout.getvalue()
        """
        test_bootstrap: Test bootstrap template
        """
        assert "package" in output
        assert "bootstrap" in output
