from json import dumps
from os.path import abspath
from os.path import dirname
from os.path import join
from os.path import realpath
from os.path import relpath
from shlex import split


class Main(object):
    def __init__(self):
        self.entries = {}

    def main(self):
        for line in read('build.log'):
            tokens = parse(line)
            if tokens and tokens[0] == 'gcc':
                self.analyze(tokens)
        print(dumps(self.entries, indent=2,  sort_keys=True))

    def analyze(self, tokens):
        source, define, include = None, [], []
        for t in tokens:
            if t.endswith('.c'):
                source = self.fixpath(t)
            if t.startswith('-D'):
                define.append(t[2:])
            if t.startswith('-I'):
                include.append(self.fixpath(t[2:]))
        if source:
            self.entries[source] = {
                'define': list(set(define)),
                'include': list(set(include))
            }

    @staticmethod
    def fixpath(path):
        p = relpath(join(cpython, path), cpython)
        return path if p.startswith('..') else p


def read(path):
    with open(path) as f:
        for line in f:
            line = line.rstrip('\n')
            while line.endswith('\\'):
                line = line[:-1] + next(f).rstrip('\n')
            yield line


def parse(line):
    try:
        return split(line)
    except ValueError:
        return None


cpython = abspath(join(dirname(realpath(__file__)), 'cpython'))


if __name__ == '__main__':
    Main().main()
