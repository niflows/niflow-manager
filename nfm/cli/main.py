import click
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
def test():
    print("test command not yet implemented")
