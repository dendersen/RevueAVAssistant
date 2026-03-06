cd ..

if [ -d "./.venv" ]; then
  echo Virtual environment already exists. Skipping creation.
  source .venv/bin/activate
else
  echo Creating virtual environment...
  python -m venv .venv
  source .venv/bin/activate
  .venv/bin/pip install --upgrade pip
  .venv/bin/pip install -r requirements.txt
fi

python rava.py

cd commandline