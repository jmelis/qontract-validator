import copy
import json
import sys

import click


class CyclicRefError(RuntimeError):
    pass


def unpack(bundle):
    return {
        path: datafile
        for (path, datafile) in bundle
    }


def load(datafiles_bundle_path):
    datafiles_bundle = json.load(open(datafiles_bundle_path))
    return unpack(datafiles_bundle)


def dereference(bundle, obj, parent=None, key_index=None):
    if isinstance(obj, dict):
        if parent is not None and \
                key_index is not None and \
                '$ref' in obj:

            target = copy.deepcopy(bundle[obj['$ref']])
            dereference(bundle, target)

            override = copy.deepcopy(obj)
            override.pop('$ref')

            target.update(override)

            parent[key_index] = target
        else:
            for key, item in obj.items():
                dereference(bundle, item, obj, key)
    elif isinstance(obj, list):
        for key_index, item in enumerate(obj):
            dereference(bundle, item, obj, key_index)


def compile(bundle):
    new_bundle = copy.deepcopy(bundle)
    for path, datafile in new_bundle.items():
        try:
            dereference(new_bundle, datafile)
        except RuntimeError as e:
            if 'maximum recursion' in str(e):
                raise CyclicRefError()
            else:
                raise e

    return new_bundle


@click.command()
@click.option('--bundle', 'bundle_path', required=True, help='bundle file')
def main(bundle_path):
    source_bundle = load(bundle_path)
    bundle = compile(source_bundle)
    sys.stdout.write(json.dumps(bundle, indent=4) + "\n")
