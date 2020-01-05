#!/usr/bin/env python3
import subprocess as sp
import sys
import click


@click.argument("workflow_path", type=click.Path(), default=".")
def install(workflow_path):
    print(f"installing {workflow_path}")
    sp.check_call([sys.executable, "-m", "pip", "install", f"{workflow_path}/package"])
