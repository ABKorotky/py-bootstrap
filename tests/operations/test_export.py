import typing as t

from .helpers import OperationsTestHelper

if t.TYPE_CHECKING:
    ...


class ExportBootstrapsTestCase(OperationsTestHelper):

    def test_export_help(self):
        output = self.run_main(cli_args=["export", "--help"])
        assert "usage: bootstrap export" in output
        assert "Exports templates from a given bootstrap" in output
        assert "-h, --help" in output
        assert "--dest" in output
        assert "Found bootstraps" in output
        assert "package" in output
        assert "bootstrap" in output

    def test_export_package_help(self):
        output = self.run_main(cli_args=["export", "package", "--help"])
        assert "usage: bootstrap export package" in output
        assert "Generates something from a given bootstrap" in output
        assert "-h, --help" in output

    def test_export_bootstrap_help(self):
        output = self.run_main(cli_args=["export", "bootstrap", "--help"])
        assert "usage: bootstrap export bootstrap" in output
        assert "Generates something from a given bootstrap" in output
        assert "-h, --help" in output

    def test_export_package(self):
        output = self.run_main(
            cli_args=["export", "package"], is_supress_system_exit=False
        )

    def test_export_bootstrap(self):
        output = self.run_main(
            cli_args=["export", "bootstrap"], is_supress_system_exit=False
        )
