#!/usr/bin/env python3

from urllib.parse import unquote

from flask import Flask, url_for, request
from twilio.twiml.voice_response import Start, Stop, VoiceResponse
from yt_dlp import YoutubeDL

app = Flask(__name__)


def download_song(search_term: str) -> str | None:
    # Get first search result from Youtube
    print(f"searching YouTube for {search_term}")
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
        "format": "m4a/bestaudio/best",
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


@app.route("/handle-transcribe", methods=["POST"])
def handle_transcribe():
    data = request.get_data().decode("utf-8")
    parsed = {d.split("=")[0]: d.split("=")[1] for d in data.split("&")}
    if parsed["TranscriptionEvent"] != "transcription-content":
        return "", 200

    # Extract words from data
    content = unquote(parsed["TranscriptionData"])
    print(content)
    words = content.split(",")[0].split(":")[1]
    words = words.strip().lower()

    # Filter unnecessary words
    filtered = words.replace("play ", "")

    # Download song during <Pause>
    download_song(filtered)
    return "", 200


@app.route("/answer", methods=["GET", "POST"])
def answer():
    response = VoiceResponse()
    response.say("just say play followed by the song name")

    # Do voice search
    start = Start()
    start.transcription(
        name="Voice search",
        profanity_filter=False,
        track="inbound_track",
        enable_automatic_punctuation=False,
        status_callback_url="https://clever-pigeon-integral.ngrok-free.app/handle-transcribe",
    )
    response.append(start)
    response.pause(5)
    stop = Stop()
    stop.transcription(name="Voice search")

    # Wait for song to finish download then start playing
    response.say("loading")
    response.pause(20)
    response.play(url_for("static", filename="song.mp3"))

    # Restart
    response.redirect(
        "https://clever-pigeon-integral.ngrok-free.app/answer", method="GET"
    )

    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
