#!/bin/sh

python -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

exit
