import contextlib
import io
import shutil
import typing as t
from pathlib import Path
from unittest import TestCase

from py_bootstrap.operations.register_bootstrap import (
    RegisterBootstrapOperation,
)
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
        """
        usage: bootstrap [-h] {list,build,export,register} ...
        Bootstrapping Python projects management tool.
        options:
          -h, --help            show this help message and exit
        Bootstraps management operations:
          {list,build,export,register}
            list                Finds and prints the list of available bootstraps with
                                brief description.
            build               Generates a skeleton of something from given
                                bootstrap.
            export              Exports a bootstrap by given name.
            register            Registers a new bootstrap.
        """
        assert "usage: bootstrap [-h]" in output
        assert "Bootstrapping Python projects management tool" in output
        assert "Bootstraps management operations" in output
        assert "{list,build,export,register}" in output

    def test_list_bootstraps_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["list", "--help"])

        output = mock_stdout.getvalue()
        """
        usage: bootstrap list [-h]
        Finds and prints the list of available bootstraps with brief description.
        options:
          -h, --help  show this help message and exit
        """
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

        assert "application" in output
        assert "package" in output

    def test_build_bootstrap_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["build", "--help"])

        output = mock_stdout.getvalue()
        """
        usage: bootstrap build [-h] [--dest DESTINATION_DIR]
                       {application,package,bootstrap} ...
        Generates a skeleton of something from given bootstrap.
        options:
          -h, --help            show this help message and exit
          --dest DESTINATION_DIR
                                Specifies the destination directory for generating.
                                Current directory by default.
        Found bootstraps:
          {application,package,bootstrap}
            application         Generates a skeleton of a new Python Application
            package             Generates a skeleton of a new Python Package
            bootstrap           Generates a skeleton of a new Bootstrap
        """
        assert "usage: bootstrap build [-h]" in output
        assert (
            "Generates a skeleton of something from given bootstrap" in output
        )
        assert "--dest DESTINATION_DIR" in output
        assert "Found bootstraps" in output
        assert "{application,package,bootstrap}" in output

    def test_build_bootstrap_application_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["build", "application", "--help"])

        output = mock_stdout.getvalue()
        """
        usage: bootstrap build application [-h] --name NAME --description DESCRIPTION
                                   [--repo REPO]
        Generates a skeleton of a new Python Application
        options:
          -h, --help            show this help message and exit
          --name NAME           The name of the application
          --description DESCRIPTION
                                Description of the application.
        """
        assert "usage: bootstrap build application [-h]" in output
        assert "Generates a skeleton of a new Python Application" in output
        assert "--name NAME" in output
        assert "--description DESCRIPTION" in output

    def test_build_bootstrap_application(self):
        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            main(
                cli_args=[
                    "build",
                    f"--dest={self.destination_dir}",
                    "application",
                    "--name=test-app",
                    "--description=Test application description",
                ]
            )

        output = mock_stdout.getvalue()
        assert not output

        destination_path = Path() / self.destination_dir
        assert destination_path.is_dir()
        assert not (destination_path / "__entry_point__.py").is_file()
        assert (destination_path / "tests").is_dir()
        assert (destination_path / "tests" / "__init__.py").is_file()
        assert (destination_path / ".gitignore").is_file()
        assert (destination_path / "CHANGELOG.md").is_file()
        assert (destination_path / "pyproject.toml").is_file()
        assert (destination_path / "README.md").is_file()
        assert (destination_path / "requirements.txt").is_file()
        assert (destination_path / "requirements-dev.txt").is_file()
        assert (destination_path / "tox.ini").is_file()

    def test_build_bootstrap_bootstrap_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["build", "bootstrap", "--help"])

        output = mock_stdout.getvalue()
        """
        usage: bootstrap build bootstrap [-h] --name NAME --description DESCRIPTION
        Generates a skeleton of a new Bootstrap
        options:
          -h, --help            show this help message and exit
          --name NAME           Specifies name of the bootstrap
          --description DESCRIPTION
                                Specifies description of the bootstrap
        """
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
                    "--name=test-bs",
                    "--description=Test bootstrap description",
                ]
            )

        output = mock_stdout.getvalue()
        assert not output

        destination_path = Path() / self.destination_dir
        assert destination_path.is_dir()
        assert (destination_path / "__entry_point__.py").is_file()
        assert (destination_path / "demo-file.txt.tmpl").is_file()

    def test_build_bootstrap_package_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["build", "package", "--help"])

        output = mock_stdout.getvalue()
        """
        usage: bootstrap build package [-h] --name NAME --description DESCRIPTION
                               --author AUTHOR --author-email AUTHOR_EMAIL
                               [--repo REPO]
        Generates a skeleton of a new Python Package
        options:
          -h, --help            show this help message and exit
          --name NAME           The name of the package
          --description DESCRIPTION
                                Description of the application.
          --author AUTHOR       Author of the package.
          --author-email AUTHOR_EMAIL
                                Email of the author.
          --repo REPO           Repository URL for the application.
        """
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
        assert not (destination_path / "__entry_point__.py").is_file()
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
        """
        usage: bootstrap export [-h] [--dest DESTINATION_DIR]
                        {application,package,bootstrap} ...
        Exports a bootstrap by given name.
        options:
          -h, --help            show this help message and exit
          --dest DESTINATION_DIR
                                Specifies the destination directory for exporting.
                                Current directory by default.
        Found bootstraps:
          {application,package,bootstrap}
            application         Exports a Python Application's template files
            package             Exports a Python Package's template files
            bootstrap           Exports a Bootstrap's template files
        """
        assert "usage: bootstrap export [-h]" in output
        assert "Exports a bootstrap by given name" in output
        assert "--dest DESTINATION_DIR" in output
        assert "Found bootstraps" in output
        assert "{application,package,bootstrap}" in output

    def test_export_bootstrap_application_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["export", "application", "--help"])

        output = mock_stdout.getvalue()
        """
        usage: bootstrap export application [-h]
        Exports a Python Application's template files
        options:
          -h, --help  show this help message and exit
        """
        assert "usage: bootstrap export application [-h]" in output
        assert "Exports a Python Application's template files" in output

    def test_export_bootstrap_application(self):
        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            main(
                cli_args=[
                    "export",
                    f"--dest={self.destination_dir}",
                    "application",
                ]
            )

        output = mock_stdout.getvalue()
        assert not output

        destination_path = Path() / self.destination_dir
        assert destination_path.is_dir()
        assert (destination_path / "__entry_point__.py").is_file()
        assert (destination_path / "tests").is_dir()
        assert (destination_path / "tests" / "__init__.py").is_file()
        assert (destination_path / "{empty}.gitignore.tmpl").is_file()
        assert (destination_path / "CHANGELOG.md.tmpl").is_file()
        assert (destination_path / "pyproject.toml.tmpl").is_file()
        assert (destination_path / "README.md.tmpl").is_file()
        assert (destination_path / "requirements.txt").is_file()
        assert (destination_path / "requirements-dev.txt").is_file()
        assert (destination_path / "tox.ini.tmpl").is_file()

    def test_export_bootstrap_bootstrap_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["export", "bootstrap", "--help"])

        output = mock_stdout.getvalue()
        """
        usage: bootstrap export bootstrap [-h]
        Exports a Bootstrap's template files
        options:
          -h, --help  show this help message and exit
        """
        assert "usage: bootstrap export bootstrap [-h]" in output
        assert "Exports a Bootstrap's template files" in output

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
        """
        usage: bootstrap export package [-h]
        Exports a Python Package's template files
        options:
          -h, --help  show this help message and exit
        """
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
        assert (
            destination_path / "{python_name}" / "__init__.py.tmpl"
        ).is_file()
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

    def test_register_bootstrap_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["register", "--help"])

        output = mock_stdout.getvalue()
        """
        usage: bootstrap register [-h] --name BOOTSTRAP_NAME --source SOURCE_PATH [-y]
        Registers a new bootstrap.
        options:
          -h, --help            show this help message and exit
          --name BOOTSTRAP_NAME
                        Specifies name of registered bootstrap template.
          --source SOURCE_PATH   Specifies the source directory with metadata and
                        bootstrap templates. Current directory by default.
          -y, --yes-upload      Do not prompt for confirmation.
        """
        assert "usage: bootstrap register [-h]" in output
        assert "Registers a new bootstrap" in output
        assert "--name BOOTSTRAP_NAME" in output
        assert "--source SOURCE_PATH" in output
        assert "-y, --yes-upload" in output

    def test_register_bootstrap(self):
        try:
            mock_stdout = io.StringIO()
            with contextlib.redirect_stdout(mock_stdout):
                main(
                    cli_args=[
                        "register",
                        "--name=test-bootstrap",
                        "--source=tests/tst-register-bootstrap-source",
                        "--yes-upload",
                    ]
                )

            output = mock_stdout.getvalue()
            assert not output

            destination_path = (
                RegisterBootstrapOperation.templates_path / "test-bootstrap"
            )
            assert destination_path.is_dir()
            assert (destination_path / "__entry_point__.py").is_file()
            assert (destination_path / "some-file.txt").is_file()
            assert (destination_path / "some-dir").is_dir()
            assert (destination_path / "some-dir" / "copied-file.txt").is_file()
            assert (destination_path / "{python_name}").is_dir()
            assert (
                destination_path / "{python_name}" / "generated-file.txt.tmpl"
            ).is_file()
        finally:
            shutil.rmtree(
                RegisterBootstrapOperation.templates_path / "test-bootstrap"
            )
