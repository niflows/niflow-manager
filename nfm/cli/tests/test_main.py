import pytest
from click.testing import CliRunner
from .. import main


@pytest.mark.parametrize("option", ["--help", "--version"])
def test_utility_options(option):
    runner = CliRunner()
    result = runner.invoke(main, [option])
    assert result.exit_code == 0


@pytest.mark.parametrize("command", ["test", "install"])
def test_unimplemented(command):
    runner = CliRunner()
    result = runner.invoke(main, [command])
    assert result.exit_code == 0
    assert "not yet implemented" in result.stdout
