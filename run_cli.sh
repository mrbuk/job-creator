#!/bin/bash

set -eu

pushd cli
trap popd 1 2 3 6

if [ ! -d "./venv" ]; then
  python -m venv ./venv
fi

source ./venv/bin/activate
pip install -r requirements.txt

python job.py $1 $2

popd