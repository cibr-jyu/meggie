echo "Setting up the env.."
export PYTHONPATH=/usr/lib/python3.9/site-packages
if [ -d ".meggie-env" ]; then
  echo "Skipping env creation as already exists."
else
  echo "Creating venv.."
  python -m venv .meggie-env
  ./.meggie-env/bin/python -m pip install -e .
  ./.meggie-env/bin/python -m pip install PyQt5.sip
fi
bash
