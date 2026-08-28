__all__ = ("OperationsTestHelper",)

import contextlib
import io
import shutil
import typing as t
from contextlib import suppress
from unittest import TestCase

from py_bootstrap.scripts.bootstrap import main

if t.TYPE_CHECKING:
    ...


class OperationsTestHelper(TestCase):
    destination_dir = "tst-destination-dir"

    def tearDown(self):
        shutil.rmtree(self.destination_dir, ignore_errors=True)

    def run_main(
        self,
        cli_args: t.Optional[list[str]] = None,
        is_supress_system_exit: bool = True,
    ) -> str:
        mock_stdout = io.StringIO()
        with contextlib.redirect_stdout(mock_stdout):
            if is_supress_system_exit:
                with suppress(SystemExit):
                    main(cli_args=cli_args)
            else:
                main(cli_args=cli_args)

        return mock_stdout.getvalue()
