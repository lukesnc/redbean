#!/usr/bin/env python3

import os
from urllib.parse import unquote

import flask
from twilio.twiml.voice_response import Start, Stop, VoiceResponse
from yt_dlp import YoutubeDL


DOMAIN = "https://clever-pigeon-integral.ngrok-free.app"
app = flask.Flask(__name__)
up_next: str | None = None


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
    video_id = url.split("=")[1]

    # Check if video is already downloaded
    filename = f"{video_id}.mp3"
    if os.path.exists(f"static/{filename}"):
        print(f"found cached file static/{filename}")
        return filename

    # Download first result
    ydl_opts = {
        "format": "m4a/bestaudio/best",
        "restrictfilenames": True,
        "paths": {"home": "static"},
        "outtmpl": "%(id)s",
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

    return filename


@app.route("/handle-transcribe", methods=["POST"])
def handle_transcribe():
    data = flask.request.get_data().decode("utf-8")
    parsed = {d.split("=")[0]: d.split("=")[1] for d in data.split("&")}
    if parsed["TranscriptionEvent"] != "transcription-content":
        return "", 200

    # Extract words from data
    content = unquote(parsed["TranscriptionData"])
    print(content)
    words = content.split(",")[0].split(":")[1].lower().replace('"', "").strip()

    # Download song during <Pause> and queue it
    if filename := download_song(words):
        up_next = filename

    return "", 200


@app.route("/answer", methods=["GET", "POST"])
def answer():
    response = VoiceResponse()
    response.say("just say the song or name of you tube video")

    # Do voice search
    start = Start()
    start.transcription(
        name="Voice search",
        profanity_filter=False,
        track="inbound_track",
        enable_automatic_punctuation=False,
        status_callback_url=f"{DOMAIN}/handle-transcribe",
    )
    response.append(start)
    response.pause(5)
    stop = Stop()
    stop.transcription(name="Voice search")
    response.append(stop)

    # Wait for song to finish download then start playing
    response.say("loading")
    response.pause(20)
    response.play(flask.url_for("static", filename=up_next))

    # Restart
    response.redirect(f"{DOMAIN}/answer", method="GET")

    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
