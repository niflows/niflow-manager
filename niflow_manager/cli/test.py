#!/usr/bin/env python3
import subprocess as sp
import yaml
from pathlib import Path
import click


def testkraken_specs(workflow_path):
    """reading spec.yml and creating testkraken yml file"""
    with (workflow_path / "spec.yml").open() as f:
        params = yaml.safe_load(f)

    # everything what is in test, should be added
    params_tkraken = params["test"]
    fixed_envs_tkraken = params_tkraken.get("fixed_env", [])
    # required_env from the build part should be one of the fixed_env
    fixed_envs_tkraken.append(params["build"]["required_env"])
    params_tkraken["fixed_env"] = fixed_envs_tkraken

    if params.get("post_build", None):
        params_tkraken["post_build"] = params["post_build"]
    else:
        # if post build not provided, it will use he default one that installs niflow-manager
        # and the package (after coping it first)
        params_tkraken["post_build"] = {}
        params_tkraken["post_build"]["copy"] = [".", "/nfm"]
        params_tkraken["post_build"]["miniconda"] = {
            "pip_install": ["niflow-manager", "/nfm/package/"]
        }

    with (workflow_path / "testkraken_spec.yml").open("w") as f:
        yaml.dump(params_tkraken, f, default_flow_style=False, sort_keys=False)


def testkraken_run(workflow_path, working_dir=None):
    if working_dir:
        sp.run(["testkraken", workflow_path, "-w", working_dir], check=True)
    else:
        sp.run(["testkraken", workflow_path], check=True)


@click.argument("workflow_path", type=click.Path(), default=".")
@click.option(
    "-w",
    "--working-dir",
    type=click.Path(),
    help="Working directory, default is a temporary directory.",
)
def test(workflow_path, working_dir=None):
    print(f"testing {workflow_path}")
    testkraken_specs(workflow_path=Path(workflow_path))
    testkraken_run(workflow_path=workflow_path, working_dir=working_dir)
