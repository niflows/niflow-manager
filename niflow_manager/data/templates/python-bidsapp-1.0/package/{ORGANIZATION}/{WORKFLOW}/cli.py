# This file provides a user-facing command-line interface (CLI) to your BIDS app
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
import os.path as op
from . import __version__
from .workflow import init_{WORKFLOW}_wf


# This parser includes the options that bids apps are required to accept
# as well as a few additional parameters that are nice
def get_parser():
    """Build parser object"""
    verstr = 'fitlins v{{}}'.format(__version__)

    parser = ArgumentParser(description='Describe your BIDS app here',
                            formatter_class=RawTextHelpFormatter)

    # Arguments as specified by BIDS-Apps
    # required, positional arguments
    # IMPORTANT: they must go directly with the parser object
    parser.add_argument('bids_dir', action='store', type=op.abspath,
                        help='the root folder of a BIDS valid dataset (sub-XXXXX folders should '
                             'be found at the top level in this folder).')
    parser.add_argument('output_dir', action='store', type=op.abspath,
                        help='the output path for the outcomes of preprocessing and visual '
                             'reports')
    parser.add_argument('analysis_level', choices=['run', 'session', 'participant', 'dataset'],
                        help='processing stage to be runa (see BIDS-Apps specification).')

    # optional arguments
    parser.add_argument('-v', '--version', action='version', version=verstr)

    g_bids = parser.add_argument_group('Options for filtering BIDS queries')
    g_bids.add_argument('--participant-label', action='store', nargs='+', default=None,
                        help='one or more participant identifiers (the sub- prefix can be '
                             'removed)')
    g_bids.add_argument('--derivative-label', action='store', type=str,
                        help='execution label to append to derivative directory name')


# The main function is what will be run when niflow-{ORGANIZATION}-{WORKFLOW} is called
# Command-line arguments are available via the sys.argv list, though you should probably
# use the parser object defined above as it already includes the required BIDS app
# paramters. 
def main():
    opts = get_parser().parse_args()
    wf = init_{WORKFLOW}_wf(opts)
    wf.run()
