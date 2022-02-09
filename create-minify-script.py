import json
import os
import sys


def main():
    files = set()
    for src, headers in read():
        files.add(src)
        files.update(headers)

    print('#!/bin/sh')
    print('set -eu')
    print('rm -rf "$2"')
    for f in files:
        print(f'mkdir -p "$2/{os.path.dirname(f)}"')
        print(f'cp "$1/{f}" "$2/{f}"')


def read():
    for src, dct in json.load(sys.stdin).items():
        yield src, dct['headers']


if __name__ == '__main__':
    main()
