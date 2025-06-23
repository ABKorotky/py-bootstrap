import contextlib
import io
import os
import shutil
import typing as t
from argparse import Namespace
from unittest import TestCase

import tests as tst_package
from py_bootstrap.operations import (
    BaseBuildBootstrapOperation,
)

if t.TYPE_CHECKING:
    ...


class TstOperation(BaseBuildBootstrapOperation):
    package = tst_package
    templates_dir_name = "tst-templates"
    entry_point_path = os.path.join(
        os.path.dirname(tst_package.__file__),
        templates_dir_name,
        "test_bootstrap",
        f"{BaseBuildBootstrapOperation.entry_point_module_name}.py",
    )


class BaseBuildBootstrapOperationTestCase(TestCase):

    tst_cls = TstOperation
    tst_obj: TstOperation

    def setUp(self):
        self.tst_obj = self.tst_cls()

    def tearDown(self):
        shutil.rmtree(
            os.path.join(os.getcwd(), "test-destination"), ignore_errors=True
        )

    def test_run(self):
        namespace = Namespace(
            destination_dir="test-destination",
            name="test-name",
            description="Test project description",
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)

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

        assert os.path.isdir(os.path.join(destination_path, "test_name"))
        assert os.path.isfile(
            os.path.join(destination_path, "test_name", "generated-file.txt")
        )

        assert os.path.isfile(os.path.join(destination_path, "some-file.txt"))
        assert not os.path.isfile(
            os.path.join(
                destination_path, f"{self.tst_obj.entry_point_module_name}.py"
            )
        )

    def test_run_on_existed_directory(self):
        namespace = Namespace(
            destination_dir="test-destination",
            name="test",
            description="Test project description",
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)

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
            name="test",
            description="Test project description",
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)

        os.mknod("test-destination")
        with self.assertRaises(Exception) as err_ctx:
            self.tst_obj.run()
        os.remove("test-destination")

        assert err_ctx.exception.args == ("Creating destination directory",)
