# redbean

Source code for the Redbean Project.

## Setup

Start by installing via system package manager: `ngrok ffmpeg`

You will need to authenticate to ngrok after installing it.

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
