#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd)"
export PYTHONPATH=$DIR:$PYTHONPATH
python -m tc_badges.cli "$@"