import contextlib
import io
import os
import shutil
import typing as t
from argparse import Namespace
from pathlib import Path
from unittest import TestCase

import tests.tst_templates as tst_templates_module
from py_bootstrap.operations import BaseExportBootstrapOperation

if t.TYPE_CHECKING:
    ...


class BaseExportBootstrapOperationTestCase(TestCase):
    tst_cls = BaseExportBootstrapOperation
    tst_obj: BaseExportBootstrapOperation

    templates_path = Path(tst_templates_module.__file__).parent

    def setUp(self):
        self.tst_obj = self.tst_cls()

    def tearDown(self):
        shutil.rmtree(
            os.path.join(os.getcwd(), "test-destination"), ignore_errors=True
        )

    def test_run(self):
        namespace = Namespace(
            destination_dir="test-destination",
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)
        self.tst_obj.set_bootstrap_path(
            path=self.templates_path / "test_bootstrap"
        )

        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            self.tst_obj.run()

        output = mock_stdout.getvalue()
        assert not output

        destination_path = self.tst_obj.destination_path
        assert os.path.exists(destination_path)

        assert os.path.isdir(os.path.join(destination_path, "some-dir"))
        assert os.path.isfile(
            os.path.join(destination_path, "some-dir", "copied-file.txt")
        )

        assert os.path.isdir(os.path.join(destination_path, "{python_name}"))
        assert os.path.isfile(
            os.path.join(
                destination_path,
                "{python_name}",
                "generated-file.txt.tmpl",
            )
        )

        assert os.path.isfile(os.path.join(destination_path, "some-file.txt"))
        assert os.path.isfile(
            os.path.join(
                destination_path, f"{self.tst_obj.entry_point_module_name}.py"
            )
        )

    def test_run_on_existed_directory(self):
        namespace = Namespace(
            destination_dir="test-destination",
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)
        self.tst_obj.set_bootstrap_path(
            path=self.templates_path / "test_bootstrap"
        )

        os.makedirs("test-destination/value.d", exist_ok=True)
        os.mknod("test-destination/dir")
        os.mknod("test-destination/value.d/some-file.txt")

        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            self.tst_obj.run()

        output = mock_stdout.getvalue()
        assert not output

        destination_path = self.tst_obj.destination_path
        assert os.path.exists(destination_path)

        assert os.path.isfile(os.path.join(destination_path, "some-file.txt"))
        assert os.path.isdir(os.path.join(destination_path, "value.d"))
        assert os.path.isfile(
            os.path.join(destination_path, "value.d", "some-file.txt")
        )

    def test_run_unable_create_destination_dir(self):
        namespace = Namespace(
            destination_dir="test-destination",
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)
        self.tst_obj.set_bootstrap_path(
            path=self.templates_path / "test_bootstrap"
        )

        os.mknod("test-destination")
        with self.assertRaises(Exception) as err_ctx:
            self.tst_obj.run()
        os.remove("test-destination")

        assert err_ctx.exception.args == ("Creating destination directory",)
