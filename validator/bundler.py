#!/usr/bin/env python2

import os
import re
import sys

import anymarkup
import json

datadir = sys.argv[1]

if datadir[-1] == "/":
    datadir = datadir[:-1]

datafiles = []

for root, dirs, files in os.walk(datadir, topdown=False):
    for name in files:
        if re.search(r'\.(ya?ml|json)$', name):
            path = os.path.join(root, name)
            datafile = path[len(datadir):]

            sys.stderr.write("Processing: {}\n".format(datafile))

            data = anymarkup.parse_file(path, force_types=None)
            datafiles.append([datafile, data])


print(json.dumps(datafiles, indent=4))
