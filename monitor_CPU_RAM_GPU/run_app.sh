#!/bin/bash
set -e
cd "$(dirname "$(readlink -f "$0")")"

if [ -f ./appvenv/bin/activate ]; then
    source ./appvenv/bin/activate
else
    echo "Не найден venv: $(pwd)/appvenv/bin/activate" >&2
    exit 1
fi

export DISPLAY="${DISPLAY:-:0}"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"

exec python main.py "$@"
