import contextlib
import io
import os
import shutil
import typing as t
from argparse import Namespace
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

import tests as tst_package
from py_bootstrap.operations.register_bootstrap import (
    RegisterBootstrapOperation,
)

if t.TYPE_CHECKING:
    ...


class TstOperation(RegisterBootstrapOperation):
    package = tst_package
    templates_dir_name = "tst-templates"


class ListBootstrapsOperationTestCase(TestCase):
    tst_cls = TstOperation
    tst_obj: TstOperation

    source_path: "Path"

    def setUp(self):
        self.source_path = Path(tst_package.__file__).parent
        self.tst_obj = self.tst_cls()

    def tearDown(self):
        shutil.rmtree(self.tst_obj.bootstrap_path, ignore_errors=True)

    def test_run(self):
        source_path = self.source_path / "tst-templates/test_bootstrap"
        namespace = Namespace(
            source_path=source_path,
            bootstrap_name="test_bootstrap_copy",
            upload_confirmation=True,
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)

        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            self.tst_obj.run()

        output = mock_stdout.getvalue()
        assert not output

        destination_path = self.tst_obj.bootstrap_path
        assert os.path.exists(destination_path)

        assert os.path.isdir(os.path.join(destination_path, "some-dir"))
        assert os.path.isfile(
            os.path.join(destination_path, "some-dir", "copied-file.txt")
        )

        assert os.path.isdir(
            os.path.join(destination_path, "{underscored_name}")
        )
        assert os.path.isfile(
            os.path.join(
                destination_path,
                "{underscored_name}",
                "generated-file.txt.tmpl",
            )
        )

        assert os.path.isfile(os.path.join(destination_path, "some-file.txt"))
        assert os.path.isfile(
            os.path.join(
                destination_path, f"{self.tst_obj.entry_point_module_name}.py"
            )
        )

    def test_run_override(self):
        source_path = self.source_path / "tst-templates/test_bootstrap"
        namespace = Namespace(
            source_path=source_path,
            bootstrap_name="test_bootstrap_copy",
            upload_confirmation=True,
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)

        os.makedirs(self.tst_obj.bootstrap_path, exist_ok=True)
        os.mknod(self.tst_obj.bootstrap_path / "some-old-file.txt")

        self.tst_obj.run()

        destination_path = self.tst_obj.bootstrap_path
        assert os.path.exists(destination_path)

        assert not os.path.isfile(
            os.path.join(destination_path, "some-old--file.txt")
        )

    def test_run_interactive_no(self):
        source_path = self.source_path / "tst-templates/test_bootstrap"
        namespace = Namespace(
            source_path=source_path,
            bootstrap_name="test_bootstrap_copy",
            upload_confirmation=False,
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)

        mock_stdout = io.StringIO()
        with (
            contextlib.redirect_stdout(mock_stdout),
            patch("builtins.input", Mock(return_value="N")),
        ):
            self.tst_obj.run()

        output = mock_stdout.getvalue()
        assert not output

        destination_path = self.tst_obj.bootstrap_path
        assert not os.path.exists(destination_path)

    def test_run_wrong_entry_point_file(self):
        source_path = self.source_path / "tst-templates/test_wrong_entry_point"
        namespace = Namespace(
            source_path=source_path,
            bootstrap_name="test_bootstrap_copy",
            upload_confirmation=True,
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)

        with self.assertRaises(Exception) as err_cm:
            self.tst_obj.run()

        assert (
            str(err_cm.exception)
            == "BuildOperation class is missed in entry-point file"
        )

    def test_run_missed_entry_point_file(self):
        source_path = self.source_path / "tst-templates/test_missed_entry_point"
        namespace = Namespace(
            source_path=source_path,
            bootstrap_name="test_bootstrap_copy",
            upload_confirmation=True,
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)

        with self.assertRaises(Exception) as err_cm:
            self.tst_obj.run()

        assert str(err_cm.exception) == "entry-point file is missed"
