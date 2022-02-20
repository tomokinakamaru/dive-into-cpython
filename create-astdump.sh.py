import json
import os
import sys


def main():
    print('#!/bin/sh')
    print('set -eu')
    print(f'dst="$(pwd)/$2"')
    print(f'rm -rf "$dst"')
    print(f'cd "$1"')
    for n, (src, defs, incs) in enumerate(read()):
        defs = build_defines(defs)
        incs = build_includes(incs)
        print(
            'mkdir', '-p', f'"$dst/{os.path.dirname(src)}"', '&&',
            'clang', '-Xclang', '-ast-dump=json',
            '-fsyntax-only', '-Wno-everything', *defs, *incs,
            src, '>', f'"$dst/{src}.json"', '&'
        )
        if n % 2 == 1:
            print('wait')
    print('wait')


def build_defines(defs):
    for d in defs:
        if '=' in d:
            k, v = d.split('=', 1)
            yield f"-D{k}='{v}'"
        else:
            yield f'-D{d}'


def build_includes(incs):
    for i in incs:
        yield f'-I{i}'


def read():
    for src, dct in json.load(sys.stdin).items():
        yield src, dct['defines'], dct['includes']


if __name__ == '__main__':
    main()
