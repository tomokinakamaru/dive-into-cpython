from json import dumps
from json import load
from os.path import exists
from os.path import join
from os.path import normpath
from sys import stdin


def main():
    define, include = read()
    data = {
        'configurations': [
            {
                'name': 'Generated from build.log',
                'cStandard': 'c99',
                'includePath': include,
                'defines': define
            }
        ],
        'version': 4
    }
    print(dumps(data, indent=4))


def read():
    define, include = set(), set()
    for dct in load(stdin).values():
        define.update(dct['define'])
        for i in dct['include']:
            if i.startswith('/'):
                include.add(i)
            else:
                if exists(join('cpython', i)):
                    path = normpath(join('${workspaceFolder}', i))
                    include.add(path)
    return sorted(define), sorted(include)


if __name__ == '__main__':
    main()
