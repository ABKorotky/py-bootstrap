import typing as t

from .helpers import OperationsTestHelper

if t.TYPE_CHECKING:
    ...


class MainDispatcherOperationTestCase(OperationsTestHelper):

    def test_help(self):
        output = self.run_main(cli_args=["--help"])
        assert "usage: bootstrap" in output
        assert "Bootstraps your Python projects!" in output
        assert "-h, --help" in output
        assert "-v, --verbose" in output
        assert "Operations" in output
        assert "list" in output
        assert "build" in output
        assert "export" in output
