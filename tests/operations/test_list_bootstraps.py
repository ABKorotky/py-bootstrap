import contextlib
import io
import typing as t
from argparse import Namespace
from importlib.metadata import EntryPoint
from unittest import TestCase
from unittest.mock import Mock, patch

import tests.tst_templates as tst_package
from py_bootstrap.operations import base as base_module
from py_bootstrap.operations.list_bootstraps import ListBootstrapsOperation

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
        mock_entry_point = Mock(
            return_value=[
                EntryPoint(
                    "test", tst_package.__package__, "py_bootstrap_templates"
                )
            ]
        )
        with (
            patch.object(base_module, "entry_points", mock_entry_point),
            contextlib.redirect_stdout(mock_stdout),
        ):
            self.tst_obj.run()

        output = mock_stdout.getvalue()
        """
        test_bootstrap: Test bootstrap template
        """
        assert "test_bootstrap" in output
