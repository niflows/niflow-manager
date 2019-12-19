import sys
import click
from pathlib import Path
import subprocess as sp
from .. import __version__
from .init import init
from .test import testkraken_specs, testkraken_run
from .build import docker_image


@click.group()
@click.version_option(__version__)
def main():
    pass


main.command()(init)


@main.command()
@click.argument("workflow_path", type=click.Path(), default=".")
def install(workflow_path):
    print(f"installing {workflow_path}")
    sp.check_call([sys.executable, "-m", "pip", "install", f"{workflow_path}"])


@main.command()
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


@click.argument("workflow_path", type=click.Path(), default=".")
@click.option(
    "-w",
    "--working-dir",
    type=click.Path(),
    help="Working directory, default is a temporary directory.",
)
@main.command()
def build(workflow_path, working_dir=None):
    print("build", workflow_path)
    docker_image(workflow_path=workflow_path, working_dir=working_dir)
