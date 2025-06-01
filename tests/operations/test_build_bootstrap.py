import contextlib
import io
import os
import shutil
import typing as t
from argparse import Namespace
from unittest import TestCase

import tests as tests_package
from py_bootstrap.operations.build_bootstrap import BuildBootstrapOperation

if t.TYPE_CHECKING:
    ...


class BuildBootstrapsOperationTestCase(TestCase):

    tst_cls = BuildBootstrapOperation
    tst_obj: BuildBootstrapOperation

    def setUp(self):
        self.tst_obj = self.tst_cls()
        self.tst_obj.package = tests_package

    def tearDown(self):
        shutil.rmtree(
            os.path.join(os.getcwd(), "test-destination"), ignore_errors=True
        )

    def test_run(self):
        namespace = Namespace(
            name="test_bootstrap",
            destination_dir="test-destination",
            context_overrides=["key:value"],
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)

        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            self.tst_obj.run()

        output = mock_stdout.getvalue()
        assert not output

        destination_path = self.tst_obj.destination_path
        assert os.path.exists(destination_path)

        assert os.path.isdir(os.path.join(destination_path, "dir"))
        assert os.path.isfile(os.path.join(destination_path, "dir", "file.txt"))

        assert os.path.isfile(os.path.join(destination_path, "some-file.txt"))
        assert os.path.isdir(os.path.join(destination_path, "value.d"))
        assert os.path.isfile(
            os.path.join(destination_path, "value.d", "some-file.txt")
        )

    def test_run_on_existed_directory(self):
        namespace = Namespace(
            name="test_bootstrap",
            destination_dir="test-destination",
            context_overrides=["key:value"],
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

    def test_run_invalid_context(self):
        namespace = Namespace(
            name="test_bootstrap",
            destination_dir="test-destination",
            context_overrides=[],
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)

        with self.assertRaises(Exception) as err_ctx:
            self.tst_obj.run()

        assert err_ctx.exception.args == ("Context is invalid",)

    def test_run_context_prepare_error(self):
        namespace = Namespace(
            name="test_bootstrap",
            destination_dir="test-destination",
            context_overrides=["key:value", "error:1"],
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)

        with self.assertRaises(Exception) as err_ctx:
            self.tst_obj.run()

        assert err_ctx.exception.args == ("Preparing context",)

    def test_run_unable_create_destination_dir(self):
        namespace = Namespace(
            name="test_bootstrap",
            destination_dir="test-destination",
            context_overrides=["key:value"],
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)

        os.mknod("test-destination")
        with self.assertRaises(Exception) as err_ctx:
            self.tst_obj.run()
        os.remove("test-destination")

        assert err_ctx.exception.args == ("Creating destination directory",)


class BuildRealBootstrapOperationTestCase(TestCase):
    tst_cls = BuildBootstrapOperation
    tst_obj: BuildBootstrapOperation

    def setUp(self):
        self.tst_obj = self.tst_cls()

    def tearDown(self):
        shutil.rmtree(
            os.path.join(os.getcwd(), "test-destination"), ignore_errors=True
        )

    def test_build_application(self):
        namespace = Namespace(
            name="application",
            destination_dir="test-destination",
            context_overrides=[
                "name:test-app",
                "description:Test application description",
            ],
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)

        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            self.tst_obj.run()

        output = mock_stdout.getvalue()
        assert not output

        destination_path = self.tst_obj.destination_path
        assert os.path.exists(destination_path)

        assert os.path.isfile(os.path.join(destination_path, ".gitignore"))
        assert os.path.isfile(
            os.path.join(destination_path, ".pre-commit-config.yaml")
        )
        assert os.path.isfile(os.path.join(destination_path, "CHANGELOG.md"))
        assert os.path.isfile(os.path.join(destination_path, "pyproject.toml"))
        assert os.path.isfile(os.path.join(destination_path, "README.md"))
        assert os.path.isfile(
            os.path.join(destination_path, "requirements.txt")
        )
        assert os.path.isfile(
            os.path.join(destination_path, "requirements-dev.txt")
        )

        assert os.path.isdir(os.path.join(destination_path, "docs"))
        assert os.path.isfile(
            os.path.join(destination_path, "docs", "__init__.py")
        )
        assert os.path.isfile(os.path.join(destination_path, "docs", "conf.py"))
        assert os.path.isfile(
            os.path.join(destination_path, "docs", "index.rst")
        )
        assert os.path.isfile(
            os.path.join(destination_path, "docs", "make.bat")
        )
        assert os.path.isfile(
            os.path.join(destination_path, "docs", "Makefile")
        )

        assert os.path.isdir(os.path.join(destination_path, "test_app"))
        assert os.path.isfile(
            os.path.join(destination_path, "test_app", "__init__.py")
        )

        assert os.path.isdir(os.path.join(destination_path, "tests"))
        assert os.path.isfile(
            os.path.join(destination_path, "tests", "__init__.py")
        )
        assert os.path.isfile(
            os.path.join(destination_path, "tests", "test_app.py")
        )

    def test_build_package(self):
        namespace = Namespace(
            name="package",
            destination_dir="test-destination",
            context_overrides=[
                "name:test-pkg",
                "description:Test package description",
                "author:Test Author",
                "author_email:author@mail.loc",
            ],
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)

        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            self.tst_obj.run()

        output = mock_stdout.getvalue()
        assert not output

        destination_path = self.tst_obj.destination_path
        assert os.path.exists(destination_path)

        assert os.path.isfile(os.path.join(destination_path, ".gitignore"))
        assert os.path.isfile(
            os.path.join(destination_path, ".pre-commit-config.yaml")
        )
        assert os.path.isfile(os.path.join(destination_path, "AUTHORS.md"))
        assert os.path.isfile(os.path.join(destination_path, "CHANGELOG.md"))
        assert os.path.isfile(os.path.join(destination_path, "pyproject.toml"))
        assert os.path.isfile(os.path.join(destination_path, "README.md"))
        assert os.path.isfile(
            os.path.join(destination_path, "requirements.txt")
        )
        assert os.path.isfile(
            os.path.join(destination_path, "requirements-dev.txt")
        )

        assert os.path.isdir(os.path.join(destination_path, "docs"))
        assert os.path.isfile(
            os.path.join(destination_path, "docs", "__init__.py")
        )
        assert os.path.isfile(os.path.join(destination_path, "docs", "conf.py"))
        assert os.path.isfile(
            os.path.join(destination_path, "docs", "index.rst")
        )
        assert os.path.isfile(
            os.path.join(destination_path, "docs", "make.bat")
        )
        assert os.path.isfile(
            os.path.join(destination_path, "docs", "Makefile")
        )

        assert os.path.isdir(os.path.join(destination_path, "test_pkg"))
        assert os.path.isfile(
            os.path.join(destination_path, "test_pkg", "__init__.py")
        )

        assert os.path.isdir(os.path.join(destination_path, "tests"))
        assert os.path.isfile(
            os.path.join(destination_path, "tests", "__init__.py")
        )
        assert os.path.isfile(
            os.path.join(destination_path, "tests", "test_package.py")
        )

    def test_build_template(self):
        namespace = Namespace(
            name="template",
            destination_dir="test-destination",
            context_overrides=[],
        )
        self.tst_obj.set_cli_namespace(namespace=namespace)

        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            self.tst_obj.run()

        output = mock_stdout.getvalue()
        assert not output

        destination_path = self.tst_obj.destination_path
        assert os.path.exists(destination_path)

        assert os.path.isfile(os.path.join(destination_path, "__metadata__.py"))
