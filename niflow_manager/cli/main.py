import click
from pathlib import Path
import subprocess as sp
from .. import __version__
from .init import init
from .test import testkraken_specs, testkraken_run


@click.group()
@click.version_option(__version__)
def main():
    pass


main.command()(init)


@main.command()
def install():
    print("install command not yet implemented")


@main.command()
@click.argument('workflow_path', type=click.Path(), default='.')
@click.option('-w', '--working-dir', type=click.Path(),
              help="Working directory, default is a temporary directory.")

def test(workflow_path, working_dir=None):
    print(f'testing {workflow_path}')
    testkraken_specs(workflow_path=Path(workflow_path))
    testkraken_run(workflow_path=workflow_path, working_dir=working_dir)



@main.command()
def build():
    print("build command not yet implemented")
