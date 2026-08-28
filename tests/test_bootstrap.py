import contextlib
import io
import shutil
import typing as t
from pathlib import Path
from unittest import TestCase

from py_bootstrap.scripts.bootstrap import main

if t.TYPE_CHECKING:
    ...


class MainTestCase(TestCase):
    destination_dir = "tst-destination-dir"

    def tearDown(self):
        shutil.rmtree(self.destination_dir, ignore_errors=True)

    def test_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["--help"])

        output = mock_stdout.getvalue()
        assert "usage: bootstrap [-h]" in output
        assert "Bootstrapping Python projects management tool" in output
        assert "Bootstraps management operations" in output
        assert "{list,build,export}" in output

    def test_list_bootstraps_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["list", "--help"])

        output = mock_stdout.getvalue()
        assert "usage: bootstrap list [-h]" in output
        assert (
            "Finds and prints the list of available bootstraps with brief description"
            in output
        )

    def test_list_bootstraps(self):
        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            main(cli_args=["list"])

        output = mock_stdout.getvalue()
        assert "package" in output

    def test_build_bootstrap_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["build", "--help"])

        output = mock_stdout.getvalue()
        assert "usage: bootstrap build [-h]" in output
        assert "Generates a skeleton of something from given bootstrap" in output
        assert "--dest DESTINATION_DIR" in output
        assert "Found bootstraps" in output
        assert "{package,bootstrap}" in output

    def test_build_bootstrap_bootstrap_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["build", "bootstrap", "--help"])

        output = mock_stdout.getvalue()
        assert "usage: bootstrap build bootstrap [-h]" in output
        assert "Generates a skeleton of a new Bootstrap" in output
        assert "--name NAME" in output
        assert "--description DESCRIPTION" in output

    def test_build_bootstrap_bootstrap(self):
        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            main(
                cli_args=[
                    "build",
                    f"--dest={self.destination_dir}",
                    "bootstrap",
                    "--name=test_bs",
                    "--description=Test bootstrap description",
                ]
            )

        output = mock_stdout.getvalue()
        assert not output

        destination_path = Path() / self.destination_dir
        assert destination_path.is_dir()
        assert (destination_path / "__descriptor__.py").is_file()
        assert (destination_path / "demo-file.txt.tmpl").is_file()

    def test_build_bootstrap_package_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["build", "package", "--help"])

        output = mock_stdout.getvalue()
        assert "usage: bootstrap build package [-h]" in output
        assert "Generates a skeleton of a new Python Package" in output
        assert "--name NAME" in output
        assert "--description DESCRIPTION" in output
        assert "--author AUTHOR" in output
        assert "--author-email AUTHOR_EMAIL" in output
        assert "--repo REPO" in output

    def test_build_bootstrap_package(self):
        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            main(
                cli_args=[
                    "build",
                    f"--dest={self.destination_dir}",
                    "package",
                    "--name=test-pkg",
                    "--description=Test package description",
                    "--author=Test Author",
                    "--author-email=est.author@mail.loc",
                    "--repo=https://localhost/test-pkg",
                ]
            )

        output = mock_stdout.getvalue()
        assert not output

        destination_path = Path() / self.destination_dir
        assert destination_path.is_dir()
        assert not (destination_path / "__descriptor__.py").is_file()
        assert (destination_path / "docs").is_dir()
        assert (destination_path / "docs" / "__init__.py").is_file()
        assert (destination_path / "docs" / "conf.py").is_file()
        assert (destination_path / "docs" / "index.rst").is_file()
        assert (destination_path / "docs" / "make.bat").is_file()
        assert (destination_path / "docs" / "Makefile").is_file()
        assert (destination_path / "test_pkg").is_dir()
        assert (destination_path / "test_pkg" / "__init__.py").is_file()
        assert (destination_path / "tests").is_dir()
        assert (destination_path / "tests" / "__init__.py").is_file()
        assert (destination_path / "tests" / "test_package.py").is_file()
        assert (destination_path / ".gitignore").is_file()
        assert (destination_path / "AUTHORS.md").is_file()
        assert (destination_path / "CHANGELOG.md").is_file()
        assert (destination_path / "pyproject.toml").is_file()
        assert (destination_path / "README.md").is_file()
        assert (destination_path / "requirements.txt").is_file()
        assert (destination_path / "requirements-dev.txt").is_file()
        assert (destination_path / "tox.ini").is_file()

    def test_export_bootstrap_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["export", "--help"])

        output = mock_stdout.getvalue()
        assert "usage: bootstrap export [-h]" in output
        assert "Exports a bootstrap by given name" in output
        assert "--dest DESTINATION_DIR" in output
        assert "Found bootstraps" in output
        assert "{application,package,bootstrap}" in output

    def test_export_bootstrap_bootstrap_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["export", "bootstrap", "--help"])

        output = mock_stdout.getvalue()
        assert "usage: bootstrap export bootstrap [-h]" in output
        assert "Exports a Bootstrap template files" in output

    def test_export_bootstrap_bootstrap(self):
        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            main(
                cli_args=[
                    "export",
                    f"--dest={self.destination_dir}",
                    "bootstrap",
                ]
            )

        output = mock_stdout.getvalue()
        assert not output

        destination_path = Path() / self.destination_dir
        assert destination_path.is_dir()
        assert (destination_path / "__entry_point__.py").is_file()
        assert (destination_path / "__entry_point__.py.tmpl").is_file()
        assert (destination_path / "demo-file.txt.tmpl.tmpl").is_file()

    def test_export_bootstrap_package_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["export", "package", "--help"])

        output = mock_stdout.getvalue()
        assert "usage: bootstrap export package [-h]" in output
        assert "Exports a Python Package's template files" in output

    def test_export_bootstrap_package(self):
        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            main(
                cli_args=[
                    "export",
                    f"--dest={self.destination_dir}",
                    "package",
                ]
            )

        output = mock_stdout.getvalue()
        assert not output

        destination_path = Path() / self.destination_dir
        assert destination_path.is_dir()
        assert (destination_path / "__entry_point__.py").is_file()
        assert (destination_path / "docs").is_dir()
        assert (destination_path / "docs" / "__init__.py").is_file()
        assert (destination_path / "docs" / "conf.py.tmpl").is_file()
        assert (destination_path / "docs" / "index.rst.tmpl").is_file()
        assert (destination_path / "docs" / "make.bat").is_file()
        assert (destination_path / "docs" / "Makefile").is_file()
        assert (destination_path / "{python_name}").is_dir()
        assert (destination_path / "{python_name}" / "__init__.py.tmpl").is_file()
        assert (destination_path / "tests").is_dir()
        assert (destination_path / "tests" / "__init__.py").is_file()
        assert (destination_path / "tests" / "test_package.py.tmpl").is_file()
        assert (destination_path / "{empty}.gitignore.tmpl").is_file()
        assert (destination_path / "AUTHORS.md.tmpl").is_file()
        assert (destination_path / "CHANGELOG.md.tmpl").is_file()
        assert (destination_path / "pyproject.toml.tmpl").is_file()
        assert (destination_path / "README.md.tmpl").is_file()
        assert (destination_path / "requirements.txt").is_file()
        assert (destination_path / "requirements-dev.txt").is_file()
        assert (destination_path / "tox.ini.tmpl").is_file()
