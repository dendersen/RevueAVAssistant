@echo off
cd ..

IF EXIST "./.venv" (
    echo Virtual environment already exists. Skipping creation.
) ELSE (
    echo Creating virtual environment...
    python -m venv .venv
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r requirements.txt
)

.venv/bin/python rava.py

cd commandline