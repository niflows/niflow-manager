import os
from pathlib import Path
import pytest
from click.testing import CliRunner
from .. import main

GIT_AUTHOR = "Test Author"
GIT_EMAIL = "unreal3214@fake2182.tld"


@pytest.mark.parametrize(
    "directory, organization, workflow, override, target, abort",
    [
        (None, "org", "wf", None, ".", True),
        (".", "org", "wf", None, ".", True),
        (None, "org", "wf", "y", ".", False),
        (".", "org", "wf", "y", ".", False),
        ("niflow-org-wf", "org", "wf", None, "niflow-org-wf", False),
        ("org-wf", "org", "wf", None, "niflow-org-wf", False),
        ("ow", "org", "wf", "", "niflow-org-wf", False),
        ("ow", "org", "wf", "y", "niflow-org-wf", False),
        ("ow", "org", "wf", "n", "niflow-ow", False),
    ],
)
def test_init_path_selection(
    directory, organization, workflow, override, target, abort
):
    runner = CliRunner()

    args = ["init"]
    inputs = []

    orig_path = Path(directory or ".")
    targ_path = Path(target)

    if directory is not None:
        args.append(directory)

    # Non-standard paths prompt user input
    if orig_path.name not in (
        f"niflow-{organization}-{workflow}",
        f"{organization}-{workflow}",
    ):
        inputs.extend([organization, workflow])
        if override is not None:
            inputs.append(override)

    with runner.isolated_filesystem():
        result = runner.invoke(main, args, "\n".join(inputs))

        if abort:
            assert result.exit_code != 0
            assert not (targ_path / ".git").exists()
        else:
            assert result.exit_code == 0

            assert targ_path.exists()
            assert (targ_path / ".git").exists()


def test_init_unknown_language():
    runner = CliRunner()
    args = ["init", "niflow-org-wf", "--language", "unsupportedlanguage"]
    with runner.isolated_filesystem():
        result = runner.invoke(main, args, None)
        assert result.exit_code != 0
        assert "Unknown language" in result.exception.args[0]


@pytest.mark.parametrize("gitconfig", [os.devnull, "tmp_gitconfig"])
def test_init_python(gitconfig):
    runner = CliRunner()

    args = ["init", "niflow-org-wf", "--language", "python"]

    with runner.isolated_filesystem():
        inputs = None
        if gitconfig != os.devnull:
            config_path = Path(gitconfig)
            config_path.write_text(
                f"[user]\n\temail = {GIT_EMAIL}\n\tname = {GIT_AUTHOR}"
            )
            gitconfig = str(config_path.absolute())
        else:
            inputs = "\n".join([GIT_AUTHOR, GIT_EMAIL])

        result = runner.invoke(main, args, inputs, env={"GIT_CONFIG": gitconfig})

        assert result.exit_code == 0

    if gitconfig == os.devnull:
        assert "Enter package author name: " in result.stdout
        assert "Enter package author email: " in result.stdout
    else:
        assert "Enter package author name: " not in result.stdout
        assert "Enter package author email: " not in result.stdout


def test_init_python_bidsapp():
    runner = CliRunner()

    args = ["init", "niflow-org-bidsapp", "--language", "python", "--bids", "1.0"]

    with runner.isolated_filesystem():
        config_path = Path("tmp_gitconfig")
        config_path.write_text(f"[user]\n\temail = {GIT_EMAIL}\n\tname = {GIT_AUTHOR}")
        gitconfig = str(config_path.absolute())

        result = runner.invoke(main, args, None, env={"GIT_CONFIG": gitconfig})

        assert "pybids" in Path("niflow-org-bidsapp/package/setup.cfg").read_text()

    assert result.exit_code == 0


@pytest.mark.parametrize("language", [None, "base"])
def test_init_bidsapp(language):
    runner = CliRunner()

    args = ["init", "niflow-org-bidsapp", "--bids", "1.0"]
    if language is not None:
        args.extend(["--language", language])

    with runner.isolated_filesystem():
        config_path = Path("tmp_gitconfig")
        config_path.write_text(f"[user]\n\temail = {GIT_EMAIL}\n\tname = {GIT_AUTHOR}")
        gitconfig = str(config_path.absolute())

        result = runner.invoke(main, args, None, env={"GIT_CONFIG": gitconfig})

    assert result.exit_code != 0
    if language is None:
        assert "language-specific" in result.exception.args[0]
    else:
        assert "No BIDS App template" in result.exception.args[0]
