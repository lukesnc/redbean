# redbean

Source code for the Redbean Project.

## Info

This project uses [Twilio](https://www.twilio.com/en-us) to handle phone calls. A Twilio Voice number will need to be set up with the webhook pointing to this applcation.

## Setup

You will need to install `ngrok` and `ffmpeg` via your system's package manager. Afterwards, configure/authenticate to ngrok.

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
