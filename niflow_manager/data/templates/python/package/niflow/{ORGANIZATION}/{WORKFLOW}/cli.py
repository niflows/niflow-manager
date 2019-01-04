# This file provides a user-facing command-line interface (CLI) to your workflow

# A template workflow is provided in workflow.py
# If you change the name there, change the name here, as well.
from .workflow import init_{WORKFLOW}_wf

# The main function is what will be run when niflow-{ORGANIZATION}-{WORKFLOW} is called
# Command-line arguments are available via the sys.argv list, though you may find it easier
# to construct non-trivial command lines using either of the following libraries:
#  * argparse (https://docs.python.org/3/library/argparse.html)
#  * click (https://click.palletsprojects.com)
def main():
    wf = init_{WORKFLOW}_wf()
    wf.run()
