#!/bin/sh
set -eu

script_dir=$(cd "$(dirname "$0")" && pwd -P)

python_path=$script_dir

cpython_ast=$script_dir/cpython.ast

PYTHONPATH="$python_path" CPYTHON_AST="$cpython_ast" python3 "$@"
