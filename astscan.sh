#!/bin/sh
set -eu

script_path=$0

if [ -h "$script_path" ]; then
    script_path=$(ls -ld "$script_path" | sed 's/.* -> //')
fi

script_dir=$(cd "$(dirname "$script_path")" && pwd -P)

PYTHONPATH="$script_dir" CPYTHON_AST="$script_dir/cpython.ast" python3 "$@"
