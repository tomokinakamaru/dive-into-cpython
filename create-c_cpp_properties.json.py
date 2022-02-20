import json
import os
import sys


def main():
    root = sys.argv[1]
    defines, include_path = set(), set()
    for defs, incs in read():
        defines.update(defs)
        for i in incs:
            if os.path.isabs(i):
                include_path.add(i)
            else:
                if os.path.exists(os.path.join(root, i)):
                    p = os.path.join('${workspaceFolder}', i)
                    p = os.path.normpath(p)
                    include_path.add(p)
    settings = {
        'configurations': [{
            'name': 'Generated',
            'cStandard': 'c99',
            'defines': sorted(defines),
            'includePath': sorted(include_path),
        }],
        'version': 4
    }
    print(json.dumps(settings, indent=4))


def read():
    for src, dct in json.load(sys.stdin).items():
        yield dct['defines'], dct['includes']


if __name__ == '__main__':
    main()
