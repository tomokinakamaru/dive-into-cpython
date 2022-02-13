from json import load
from os import environ
from os import walk
from os.path import isdir
from os.path import join
from os.path import normpath


def scan(func):
    run(func, environ.get('CPYTHON_AST'))


def run(func, path):
    (run_all if isdir(path) else run_one)(func, path)


def run_all(func, path):
    for root, _, files in walk(path):
        for f in files:
            if f.endswith('.json'):
                run_one(func, join(root, f))


def run_one(func, path):
    with open(path) as f:
        visit(func, load(f), [], Position())


def visit(func, node, stack, pos):
    pos.update(node)
    func(node, stack, pos)
    stack.append(node)
    for n in node.get('inner', ()):
        visit(func, n, stack, pos)
    stack.pop()


def has(dct, key):
    d = dct
    for k in key:
        if k in d:
            d = d[k]
        else:
            return False
    return True


def get(dct, key):
    d = dct
    for k in key[:-1]:
        d = d.get(k, {})
    return d.get(key[-1])


def set(dct, key, val):
    d = dct
    for k in key[:-1]:
        d = d.setdefault(k, {})
    d[key[-1]] = val


class Position(object):
    def __init__(self):
        self.gen = 0
        self.dct = {}
        self.cache = {}
        for k in POS_KEYS:
            set(self.dct, k, (0, '?'))

    def __str__(self):
        return f'{self.file}:{self.line}'

    def update(self, node):
        self.gen += 1
        for k in POS_KEYS:
            if has(node, k):
                set(self.dct, k, (self.gen, get(node, k)))

    def get(self, *keys):
        return sorted(
            (get(self.dct, k) for k in keys),
            key=lambda x: -x[0]
        )[0][1]

    def set(self, key, val):
        set(self.dct, key, val)

    @property
    def file(self):
        return normpath(self.get(
            LOC_FILE, RNG_FILE,
            LOC_EXP_FILE, RNG_EXP_FILE,
            LOC_SPL_FILE, RNG_SPL_FILE
        ))

    @property
    def line(self):
        return self.get(
            LOC_LINE, RNG_LINE,
            LOC_EXP_LINE, RNG_EXP_LINE,
            LOC_SPL_LINE, RNG_SPL_LINE
        )


LOC = 'loc',

RNG = 'range', 'begin'

EXP = 'expansionLoc',

SPL = 'spellingLoc',

FILE = 'file',

LINE = 'line',

LOC_EXP = LOC + EXP

RNG_EXP = RNG + EXP

LOC_SPL = LOC + SPL

RNG_SPL = RNG + SPL

LOC_FILE = LOC + FILE

RNG_FILE = RNG + FILE

LOC_EXP_FILE = LOC_EXP + FILE

RNG_EXP_FILE = RNG_EXP + FILE

LOC_SPL_FILE = LOC_SPL + FILE

RNG_SPL_FILE = RNG_SPL + FILE

LOC_LINE = LOC + LINE

RNG_LINE = RNG + LINE

LOC_EXP_LINE = LOC_EXP + LINE

RNG_EXP_LINE = RNG_EXP + LINE

LOC_SPL_LINE = LOC_SPL + LINE

RNG_SPL_LINE = RNG_SPL + LINE

POS_KEYS = (
    LOC_FILE, RNG_FILE,
    LOC_EXP_FILE, RNG_EXP_FILE,
    LOC_SPL_FILE, RNG_SPL_FILE,
    LOC_LINE, RNG_LINE,
    LOC_EXP_LINE, RNG_EXP_LINE,
    LOC_SPL_LINE, RNG_SPL_LINE
)
