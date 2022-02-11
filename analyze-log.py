import json
import os
import shlex
import sys


def main():
    output, headers = {}, None
    for line in read():
        toks = parse(line)
        if toks:
            if toks[0] in ('gcc',):
                p, d = parse_compile_log(toks)
                if p:
                    output[p] = d
                    output[p]['headers'] = headers = []
                else:
                    headers = None
            elif set(toks[0]) == {'.'}:
                h = parse_header_log(toks)
                if h:
                    headers.append(h)
    print(json.dumps(output, indent=2, sort_keys=True))


def parse_compile_log(toks):
    src, defs, incs = None, {}, {}
    for t in toks:
        if t.endswith('.c'):
            src = fix_path(t)
        if t.startswith('-D'):
            path = fix_path(t[2:])
            defs[path] = None
        if t.startswith('-I'):
            path = fix_path(t[2:])
            incs[path] = None
    return src, {'defines': sorted(defs), 'includes': list(incs)}


def parse_header_log(toks):
    path = fix_path(toks[1])
    return None if os.path.isabs(path) else path


def fix_path(path):
    root = os.path.abspath(sys.argv[1])
    path = os.path.join(root, path)
    path = os.path.normpath(path)
    return os.path.relpath(path, root) if path.startswith(root) else path


def parse(line):
    try:
        return shlex.split(line)
    except ValueError:
        return None


def read():
    for line in sys.stdin:
        line = line.rstrip('\n')
        while line.endswith('\\'):
            l1 = line.rstrip('\\')
            l2 = next(sys.stdin).rstrip('\n')
            line = l1 + l2
        yield line


if __name__ == '__main__':
    main()
