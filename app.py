#!/usr/bin/env python3

from flask import Flask, url_for
from twilio.twiml.voice_response import VoiceResponse
from yt_dlp import YoutubeDL

app = Flask(__name__)


def download_song(search_term: str) -> str | None:
    # Get first search result from Youtube
    print(f'searching YouTube for "{search_term}"')
    ydl_opts = {
        "default_search": "ytsearch",  # Search on YouTube
        "quiet": True,  # Suppress logging
    }
    with YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(search_term, download=False)

    videos = search_results.get("entries", [])
    if not videos:
        print("no search results found")
        return None

    url = videos[0]["webpage_url"]

    # Download first result
    ydl_opts = {
        "format": "best",
        "restrictfilenames": True,
        # "paths": {"home": "static"},
        "outtmpl": "static/song",
        "postprocessors": [
            {  # Extract and convert audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "10",  # 10 = worst
            }
        ],
    }

    with YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([url])

    if error_code != 0:
        return None

    # TODO: the song will always overwrite to this location for now
    # in the future we could have different filenames and cache them
    # in the static/ dir
    return "song.mp3"


@app.route("/answer", methods=["GET", "POST"])
def answer():
    print("taking incoming call...")
    response = VoiceResponse()

    # Get voice command

    search = "ric flair drip"

    # Fetch desired song
    filename = download_song(search)

    # Serve song
    print("playing song...")
    response.play(url_for("static", filename=filename))

    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
