@echo off
cd ..

if [ -d "./.venv" ]; then
  echo Virtual environment already exists. Skipping creation.
else
  echo Creating virtual environment...
  python -m venv .venv
  .venv\Scripts\activate.bat
  .venv/bin/pip install --upgrade pip
  .venv/bin/pip install -r requirements.txt
fi

python rava.py

cd commandline