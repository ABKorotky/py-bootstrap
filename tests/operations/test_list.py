import typing as t

from .helpers import OperationsTestHelper

if t.TYPE_CHECKING:
    ...


class ListBootstrapsOperationTestCase(OperationsTestHelper):

    def test_list_help(self):
        output = self.run_main(cli_args=["list", "--help"])
        assert "usage: bootstrap list" in output
        assert "Prints brief info for every found bootstrap" in output
        assert "-h, --help" in output

    def test_list(self):
        output = self.run_main(cli_args=["list"])
        assert "package" in output
        assert "bootstrap" in output
        assert "Build operation" in output
        assert "Export operation" in output
