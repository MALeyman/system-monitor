#!/bin/bash
set -e

cd "$(dirname "$(readlink -f "$0")")"

VENV="/home/maksim/develops/python/appvenv"
if [ ! -f "$VENV/bin/activate" ]; then
    echo "Ошибка: не найден venv: $VENV/bin/activate" >&2
    exit 1
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"

export DISPLAY="${DISPLAY:-:0}"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"

if [ ! -f main.py ]; then
    echo "Ошибка: main.py не найден в $(pwd)" >&2
    exit 1
fi

exec python main.py "$@"
