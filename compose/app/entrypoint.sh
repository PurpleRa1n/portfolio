#!/usr/bin/env bash

set -ex

function runserver {
  python portfolio/main.py migrate
  python portfolio/main.py runserver
}

case "$1" in
    "runserver" ) runserver ;;
    "bash" ) bash ;;
    "python" ) python ;;
    *) bash ;;
esac