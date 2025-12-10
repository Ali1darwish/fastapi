from pytubefix import YouTube
from pytubefix.cli import on_progress
from fastapi import FastAPI
from fastapi.responses import StreamingResponse


app= FastAPI()
@app.get("/")
def get(url: str):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_audio_only()
        i = stream.download()
        return StreamingResponse(r.iter_content(chunk_size=1024*512), media_type="video/mp4a")
    except Exception as e:
        print(f"An error occurred: {e}")
