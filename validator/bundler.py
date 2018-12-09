#!/usr/bin/env python2

import os
import re
import sys

import anymarkup
import click
import json


@click.command()
@click.option('--data-root', required=True, help='Data directory')
def main(data_root):
    if data_root[-1] == "/":
        data_root = data_root[:-1]

    datafiles = {}

    for root, dirs, files in os.walk(data_root, topdown=False):
        for name in files:
            if re.search(r'\.(ya?ml|json)$', name):
                path = os.path.join(root, name)
                datafile = path[len(data_root):]

                sys.stderr.write("Processing: {}\n".format(datafile))

                data = anymarkup.parse_file(path, force_types=None)
                datafiles[datafile] = data

    sys.stdout.write(json.dumps(datafiles, indent=4) + "\n")
