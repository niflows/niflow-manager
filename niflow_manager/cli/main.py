import click

from .. import __version__
from .init import init
from .install import install
from .build import build
from .test import test


@click.group()
@click.version_option(__version__)
def main():
    pass


main.command()(init)

main.command()(install)

main.command()(build)

main.command()(test)
