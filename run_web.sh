#!/bin/bash

set -eu

pushd web
trap popd 1 2 3 6

if [ ! -d "./venv" ]; then
  python -m venv ./venv
fi

source ./venv/bin/activate
pip install -r requirements.txt

pip install -r requirements.txt
uvicorn --host 0.0.0.0 --port 8080 main:app

popd