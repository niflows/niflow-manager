#!/usr/bin/env python3
from pathlib import Path
import subprocess as sp
import click


@click.argument('name', type=click.Path(), default='.')
@click.option('--language', help='Language for new niflow')
def init(name, language):
    path = Path(name).absolute()

    # Do not validate/modify current directory
    if name != '.':
        name_parts = path.name.split('-')
        if name_parts[0] != 'niflow':
            name_parts.insert(0, 'niflow')
        new_name = '-'.join(name_parts)
        if len(name_parts) < 3:
            click.echo(click.style("WARNING: ", fg='red'), nl=False)
            click.confirm(f"Workflow {new_name} may not have an organization. Continue?",
                          abort=True)
        path = path.with_name('-'.join(name_parts))

    click.echo(f'Initializing workflow: {path.name} in {path.parent}')
    path.mkdir(parents=True, exist_ok=True)
    sp.run(['git', '-C', str(path), 'init'], check=True)
