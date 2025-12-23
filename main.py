import re
import time
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pytubefix import YouTube
import os
import tempfile

app = FastAPI()

def clean_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name)

@app.get("/download")
def download_audio(url: str):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_audio_only()
        
        # تنظيف اسم الملف من الحروف الممنوعة
        safe_title = clean_filename(yt.title) + ".mp3"

        # ملف مؤقت
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, safe_title)

        stream.download(filename=safe_title, output_path=temp_dir)

        return FileResponse(
            temp_file_path,
            media_type="audio/mpeg",
            filename=safe_title,
        )

    except Exception as e:
        return {"error": str(e)}
