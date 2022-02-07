from json import dumps
from json import load
from os import walk
from os.path import join


def main():
    c_files = list(find_c_files())
    with open('build.json') as f:
        for path in load(f):
            c_files.remove(path)

    data = {
        'files.exclude': {
            '**/*.o': True,
            '**/*.a': True,
            '.azure-pipelines': True,
            '.github': True,
            'build': True
        }
    }
    for f in c_files:
        data['files.exclude'][f] = True
    print(dumps(data, indent=4))



def find_c_files():
    cpython = 'cpython'
    for path, _, files in walk(cpython):
        for f in files:
            if f.endswith('.c'):
                yield join(path, f)[len(cpython)+1:]


if __name__ == '__main__':
    main()
