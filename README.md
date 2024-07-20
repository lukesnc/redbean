# redbean

Source code for the Redbean Project.

## Setup

You will need to install `ngrok` via your system's package manager. After authenticating, start ngrok with:

```bash
./scripts/ngrok-start.sh
```

Create a Python virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Start the app with:

```bash
flask run
```
