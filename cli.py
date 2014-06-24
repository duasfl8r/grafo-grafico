# -*- encoding: utf-8 -*-

"""
Command-line interface for grafo-grafico.

Usage:
    cli.py [options] generate <configfile>
    cli.py [options] flush

Options:
    -o <FILE>, --output=<FILE>          saves output on a file
    -f <FORMAT>, --format=<FORMAT>      output format: png or gv [default: gv]
"""

import os
import sys

from docopt import docopt

from settings import VERSION, LOGFILE
from graph_generator import make_graph

CONFIG = None

def output(message, filename):
    """
    Redirects output on `message` or to whatever file
    `filename` points to. If `filename` is `None`, redirects it to STDOUT.

    Arguments:

    - message: a string
    - filename: a string containing a filename
    """

    if filename is None:
        output_file = sys.stdout
        close_output = lambda _: True
    else:
        output_file = open(filename, 'w')
        close_output = lambda f: f.close()

    output_file.write(message)
    close_output(output_file)

def flush():
    """
    Removes the log file if it exists.
    """

    if os.path.isfile(LOGFILE):
        os.remove(LOGFILE)

def generate(args):
    """
    Generates the graph.
    """

    graph = make_graph(CONFIG)

    if args['--format'] == 'gv':
        output(graph.graphviz(), args['--output'])
    elif args['--format'] == 'png':
        if not args['--output']:
            sys.stderr.write('Please, use the --output option to define the output file.\n')
            exit(-1)
        else:
            graph.save_png(args['--output'])
    else:
        sys.stderr.write('Unknown format: {0}'.format(args['--format']))

if __name__ == '__main__':
    args = docopt(__doc__, version=VERSION)

    # Evaluates the configuration file set on docopt's ``args`` as a
    # python script, and returns the ``CONFIG`` object that is
    # (hopefully) set in it.
    if args['<configfile>']:
        config_filename = args['<configfile>']
        with open(config_filename) as config_file:
            config_source = config_file.read()
        config_module = compile(config_source, config_filename, 'exec')
        eval(config_module)

    if args['generate']:
        generate(args)
    elif args['flush']:
        flush()
