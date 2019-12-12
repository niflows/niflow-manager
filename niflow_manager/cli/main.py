import click
import subprocess as sp
from .. import __version__
from .init import init


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
    #path, full_name, organization, workflow = normalize_path(name)
    print(f'testing {workflow_path}')
    #path.mkdir(parents=True, exist_ok=True)
    if working_dir:
        sp.run(['testkraken', str(workflow_path), "-w", working_dir], check=True)
    else:
        sp.run(['testkraken', str(workflow_path)], check=True)



@main.command()
def build():
    print("build command not yet implemented")
