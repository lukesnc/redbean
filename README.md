# redbean

Source code for the Redbean Project.

## Setup

You will need to install `ngrok` via your system's package manager. Then authenticate to ngrok.

Create a Python virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

First start ngrok in the background:

```bash
./scripts/ngrok-start.sh
```

Start the app with:

```bash
flask run
```
