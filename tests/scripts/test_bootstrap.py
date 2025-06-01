import contextlib
import io
import os
import shutil
import typing as t
from unittest import TestCase

from py_bootstrap.scripts.bootstrap import main

if t.TYPE_CHECKING:
    ...


class MainTestCase(TestCase):
    def test_help(self):
        mock_stdout = io.StringIO()
        with (
            self.assertRaises(SystemExit),
            contextlib.redirect_stdout(mock_stdout),
        ):
            main(cli_args=["--help"])

        output = mock_stdout.getvalue()
        """
        usage: bootstrap [-h] {} ...
        Bootstrapping Python projects management tool.
        options:
          -h, --help  show this help message and exit
        Registered operations:
          {list.build}
          Prints the list of available bootstraps.
          Generates a skeleton from given bootstrap.
        """
        assert "usage: bootstrap [-h]" in output
        assert "Bootstrapping Python projects management tool" in output
        assert "-h, --help" in output
        assert "{list,build}" in output

    def test_list_bootstraps(self):
        mock_stdout = io.StringIO()
        with (contextlib.redirect_stdout(mock_stdout),):
            main(cli_args=["list"])

        output = mock_stdout.getvalue()

        assert "package" in output
        assert (
            "Provides bootstrapping for Python packages based on tox tool"
            in output
        )

    def test_build_bootstrap(self):
        try:
            mock_stdout = io.StringIO()
            with contextlib.redirect_stdout(mock_stdout):
                main(
                    cli_args=[
                        "build",
                        "--name=package",
                        "--dest=test-destination",
                        "--context=name:test-pkg",
                        "--context=description:Test package description",
                        "--context=author:Test Author",
                        "--context=author_email:author@mail.loc",
                    ]
                )

            output = mock_stdout.getvalue()
            assert not output
        finally:
            shutil.rmtree(os.path.join(os.getcwd(), "test-destination"))
