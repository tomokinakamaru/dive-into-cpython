import json
import os


def scan(func):
    run(func, os.environ.get('CPYTHON_AST'))


def run(func, path):
    f = run_all if os.path.isdir(path) else run_one
    f(func, path)


def run_all(func, path):
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith('.json'):
                run_one(func, os.path.join(root, f))


def run_one(func, path):
    with open(path) as f:
        visit(func, json.load(f), Context())


def visit(func, node, ctx):
    ctx.stack.append(node)
    ctx.pos.update(node)
    func(node, ctx)
    for n in node.get('inner', ()):
        visit(func, n, ctx)
    ctx.stack.pop()


class Context(object):
    def __init__(self):
        self.stack = []
        self.pos = Position()


class Position(object):
    def __init__(self):
        self.data = {}
        self.exp = False
        self.loc = False

    def __str__(self):
        f1, l1 = self.file1, self.line1
        f2, l2 = self.file2, self.line2
        return f'{f1}:{l1};{f2}:{l2}' if f2 else f'{f1}:{l1}'

    @property
    def cpython(self):
        if os.path.isabs(self.file1):
            return False
        f = self.file2
        return not os.path.isabs(f) if f else True

    @property
    def file1(self):
        if self.exp:
            k = LOC_EXP_FILE if self.loc else RNG_EXP_FILE
            return get(self.data, k)
        else:
            k = LOC_FILE if self.loc else RNG_FILE
            return get(self.data, k)

    @property
    def line1(self):
        if self.exp:
            k = LOC_EXP_LINE if self.loc else RNG_EXP_LINE
            return get(self.data, k)
        else:
            k = LOC_LINE if self.loc else RNG_LINE
            return get(self.data, k)

    @property
    def file2(self):
        if self.exp:
            k = LOC_SPL_FILE if self.loc else RNG_SPL_FILE
            return get(self.data, k)
        return None

    @property
    def line2(self):
        if self.exp:
            k = LOC_SPL_LINE if self.loc else RNG_SPL_LINE
            return get(self.data, k)
        return None

    def update(self, node):
        for k in POS_KEYS:
            v = get(node, k)
            if v:
                set(self.data, k, v)
        self.exp = has(node, LOC_EXP) or has(node, RNG_EXP)
        self.loc = has(node, LOC_LINE) or has(node, LOC_EXP_LINE)


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
