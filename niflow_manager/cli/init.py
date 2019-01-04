#!/usr/bin/env python3
from pkg_resources import resource_filename as pkgr_fn
from pathlib import Path
import subprocess as sp
import click

from ..util.git import git_variables
from ..util.fsutil import copytree


def normalize_path(name):
    path = Path(name).absolute()
    full_name = path.name

    # Accept organization-workflow format and normalize to niflow-organization-workflow
    if name != '.' and not full_name.startswith('niflow-'):
        full_name = 'niflow-' + full_name
        path = path.with_name(full_name)

    # Make guesses as to organization and workflow name
    if full_name.startswith('niflow-'):
        name_parts = full_name.split('-', 2)[1:]
    else:
        name_parts = full_name.split('-', 1)

    if len(name_parts) == 2:
        # Normal name, do not prompt
        organization, workflow = name_parts
    else:
        # Ambiguous, ask for input
        organization = click.prompt("Organization name")
        workflow = click.prompt("Workflow name", default=name_parts[0])
        full_name = '-'.join(['niflow', organization, workflow])
        if name != '.':
            if click.confirm(f'Update path to {full_name}?', default=True):
                path = path.with_name(full_name)
        else:
            click.confirm(f'Niflow name "{full_name}" does not match directory "{path.name}". '
                          'Proceed anyway?', abort=True)

    return path, full_name, organization, workflow


@click.argument('name', type=click.Path(), default='.')
@click.option('--language', help='Language for new niflow')
def init(name, language):
    path, full_name, organization, workflow = normalize_path(name)

    click.echo(f'Initializing workflow: {path.name} in {path.parent}')
    path.mkdir(parents=True, exist_ok=True)
    sp.run(['git', '-C', str(path), 'init'], check=True)

    try:
        git_vars = git_variables(path, 'user.name', 'user.email')
    except KeyError:
        username = click.prompt("Enter package author name")
        email = click.prompt("Enter package author email")
    else:
        username = git_vars['user.name']
        email = git_vars['user.email']

    mapping = {
        'USERNAME': username,
        'USEREMAIL': email,
        'ORGANIZATION': organization,
        'WORKFLOW': workflow,
        'FULLNAME': full_name,
        }

    copytree(pkgr_fn('niflow_manager', 'data/templates/base'), path, mapping=mapping)

    if language is not None:
        language_dir = Path(pkgr_fn('niflow_manager', f'data/templates/{language}'))
        try:
            copytree(language_dir, path, mapping=mapping)
        except FileNotFoundError:
            raise ValueError(f"Unknown language: {language}")
