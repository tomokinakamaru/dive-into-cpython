from json import dumps
from json import load


def main():
    define, include = read('build.json')
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


def read(path):
    define, include = set(), set()
    with open(path) as f:
        for dct in load(f).values():
            define.update(dct['define'])
            for i in dct['include']:
                if i.startswith('/'):
                    include.add(i)
                else:
                    include.add(f'${{workspaceFolder}}/{i}')
    return list(define), list(include)


if __name__ == '__main__':
    main()
