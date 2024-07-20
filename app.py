#!/usr/bin/env python3

from flask import Flask, Response, url_for
from twilio.twiml.voice_response import VoiceResponse
from yt_dlp import YoutubeDL

YDL_OPTS = {
    "format": "best",
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    "postprocessors": [
        {  # Extract audio using ffmpeg
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "10",  # WORST QUALITY
        }
    ],
}

app = Flask(__name__)


# def get_song(search: str) -> str:
#     # Download with yt-dlp
#     url = ["https://youtu.be/CzJbz9qSsd0?si=hhPlTJO39mo44gLv"]
#     with YoutubeDL(YDL_OPTS) as ydl:
#         error_code = ydl.download(url)
#
#     return "test"


@app.route("/answer", methods=["GET", "POST"])
def answer():
    response = VoiceResponse()
    response.play(url_for("static", filename="cheerleader.mp3"))

    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
