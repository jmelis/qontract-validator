import copy
import json
import re
import sys

import click
import json
import jsonpointer


class CyclicRefError(RuntimeError):
    pass


class InvalidRef(RuntimeError):
    pass


def unpack(bundle):
    return {
        path: datafile
        for (path, datafile) in bundle
    }


def load(datafiles_bundle_path):
    datafiles_bundle = json.load(open(datafiles_bundle_path))
    return unpack(datafiles_bundle)


def split_ref(ref):
    m = re.match(r'([^#]+)?(?:#(.*))?', ref)

    path = None if m.group(1) == '' else m.group(1)
    ptr = None if m.group(2) == '' else m.group(2)

    if path is None and ptr is None:
        raise InvalidRef()

    return (path, ptr)


def dereference(bundle, datafile_path, obj, parent=None, key_index=None):
    if isinstance(obj, dict):
        if parent is not None and \
                key_index is not None and \
                '$ref' in obj:

            path, ptr = split_ref(obj['$ref'])

            if path is not None:
                target = copy.deepcopy(bundle[path])

                if ptr is not None:
                    target = jsonpointer.resolve_pointer(target, ptr)
            else:
                target = copy.deepcopy(bundle[datafile_path])
                target = jsonpointer.resolve_pointer(target, ptr)

            dereference(bundle, datafile_path, target)

            override = copy.deepcopy(obj)
            override.pop('$ref')

            if isinstance(target, dict):
                target.update(override)

            parent[key_index] = target
        else:
            for key, item in obj.items():
                dereference(bundle, datafile_path, item, obj, key)
    elif isinstance(obj, list):
        for key_index, item in enumerate(obj):
            dereference(bundle, datafile_path, item, obj, key_index)


def resolve(bundle):
    new_bundle = copy.deepcopy(bundle)
    for datafile_path, datafile in new_bundle.items():
        try:
            dereference(new_bundle, datafile_path, datafile)
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
    bundle = resolve(source_bundle)
    sys.stdout.write(json.dumps(bundle, indent=4) + "\n")
