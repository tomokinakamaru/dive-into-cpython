from json import load
from os.path import dirname
from sys import stdin


def main():
    print('#!/bin/sh')
    print('set -eu')
    print('cd cpython')
    print('rm -rf .astdump')
    print('mkdir .astdump')
    print('echo "*" > .astdump/.gitignore')
    for path, dct in load(stdin).items():
        dump(path, dct['define'], dct['include'])


def dump(path, define, include):
    out = f'.astdump/{path}.json'
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
    print(' '.join(mkdir))
    print(' '.join(clang))


if __name__ == '__main__':
    main()
