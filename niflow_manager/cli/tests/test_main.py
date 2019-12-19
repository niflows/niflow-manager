import pytest
from click.testing import CliRunner
from .. import main


@pytest.mark.parametrize("option", ["--help", "--version"])
def test_utility_options(option):
    runner = CliRunner()
    result = runner.invoke(main, [option])
    assert result.exit_code == 0


@pytest.mark.parametrize("command", ["test", "install", "build"])
def test_commads_help(command):
    runner = CliRunner()
    result = runner.invoke(main, [command, "--help"])
    assert result.exit_code == 0
