import typing as t

from .helpers import OperationsTestHelper

if t.TYPE_CHECKING:
    ...


class BuildBootstrapsTestCase(OperationsTestHelper):

    def test_build_help(self):
        output = self.run_main(cli_args=["build", "--help"])
        assert "usage: bootstrap build" in output
        assert "Generates something from a given bootstrap" in output
        assert "-h, --help" in output
        assert "--dest" in output
        assert "--dry-run" in output
        assert "Found bootstraps" in output
        assert "package" in output
        assert "bootstrap" in output

    def test_build_package_help(self):
        output = self.run_main(cli_args=["build", "package", "--help"])
        assert "usage: bootstrap build package" in output
        assert "Generates something from a given bootstrap" in output
        assert "-h, --help" in output

    def test_build_bootstrap_help(self):
        output = self.run_main(cli_args=["build", "bootstrap", "--help"])
        assert "usage: bootstrap build bootstrap" in output
        assert "Generates something from a given bootstrap" in output
        assert "-h, --help" in output

    def test_build_package(self):
        output = self.run_main(
            cli_args=["build", "package"], is_supress_system_exit=False
        )

    def test_build_bootstrap(self):
        output = self.run_main(
            cli_args=["build", "bootstrap"], is_supress_system_exit=False
        )
