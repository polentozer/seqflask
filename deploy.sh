#!/bin/bash

if [ -d "env" ]
then
    . env/bin/activate
    pip install -r requirements.txt
    python3 wsgi.py
else
    python3 -m venv env
    . env/bin/activate
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    python3 wsgi.py
fi
