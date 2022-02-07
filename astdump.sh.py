from json import load
from os.path import dirname


def main():
    with open('build.json') as f:
        print('#!/bin/sh')
        print('rm -rf astdump.err')
        print(f'cd cpython || exit 1')
        for path, dct in load(f).items():
            dump(path, dct['define'], dct['include'])


def dump(path, define, include):
    out = f'../astdump/{path}.json'
    err = f'../astdump.err'
    mkdir = ['mkdir', '-p', dirname(out)]
    clang = ['clang', '-Xclang', '-ast-dump=json', '-fsyntax-only', '-Wno-everything']
    for d in define:
        if '=' in d:
            k, v = d.split('=', 1)
            clang.append(f"-D{k}='{v}'")
        else:
            clang.append(f'-D{d}')
    for i in include:
        clang.append(f'-I{i}')
    clang.append(path)
    clang.append('>')
    clang.append(out)
    clang.append('2>>')
    clang.append(err)
    print(' '.join(mkdir))
    print(' '.join(clang))


if __name__ == '__main__':
    main()
