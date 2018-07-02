#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE="$DIR/../"

echo "Installing dependencies..."
pip install -r $BASE/requirements.txt -t $BASE/lib/

echo "Done"