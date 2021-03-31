#!/usr/bin/env bash

set -ex

export PYTHONPATH=${PYTHONPATH}:${APP_DIR}

function start_server {
  python main.py migrate
  python main.py runserver
}

case "$1" in
    "run-server" ) start_server ;;
    "bash" ) bash ;;
    "python" ) python ;;
    *) bash ;;
esac