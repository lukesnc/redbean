# redbean

Source code for the Redbean Project.

This project uses [Twilio](https://www.twilio.com/en-us) to handle phone calls. A Twilio Voice number will need to be set up with the webhook pointing to this applcation.

## Setup

You will need to install `ngrok` and `ffmpeg` via your system's package manager. Afterwards, authenticate to ngrok via the CLI.

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

## Caller Instructions
1. Call `XXX-XXX-XXXX`
2. Press any button to ignore the Twilio free account prompt (skip this if account is upgraded)
3. After it greets you, say the name of the song or video you want to hear (examples: "porter robinson cheerleader" or "dracula flow 3")
4. Redbean will download the requested media from YouTube then start playing it when it's done
5. When the song is finished it will ask you what you want to hear next (back to Step 3)
