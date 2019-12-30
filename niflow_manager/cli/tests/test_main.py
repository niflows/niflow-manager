import pytest
from click.testing import CliRunner
from pathlib import Path
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


def test_init_build_python():
    """ initilize a niflow for python and build a container using the default spec"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        res_init = runner.invoke(
            main, ["init", "--language", "python", "wf"], "\n".join(["org", "wf", "y"])
        )
        niflow_path = Path.cwd() / "niflow-org-wf"
        spec_path = niflow_path / "spec.yml"
        assert res_init.exit_code == 0
        assert spec_path.exists()

        # uncommenting the spec file
        with spec_path.open() as f:
            spec_orig = f.readlines()
        with spec_path.open(mode="w") as f:
            for line in spec_orig:
                f.write(line[1:])

        res_build = runner.invoke(main, ["build", str(niflow_path)])
        assert res_build.exit_code == 0
