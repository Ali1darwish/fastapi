from pytubefix import YouTube
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import requests

app = FastAPI()

@app.get("/audio")
def stream_youtube_audio(url: str):
    try:
        yt = YouTube(url)
        # نجيب أفضل stream للصوت
        stream = yt.streams.get_audio_only()
        audio_url = stream.url  # ده رابط مباشر للصوت على سيرفر YouTube

        # نعمل request ستريم للرابط
        r = requests.get(audio_url, stream=True)
        return StreamingResponse(
            r.iter_content(chunk_size=1024*512),
            media_type="audio/mpeg"
        )

    except Exception as e:
        return {"error": str(e)}
