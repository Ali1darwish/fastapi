import time
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pytubefix import YouTube
import os
import tempfile
import threading

app = FastAPI()

def remove_file_later(path: str, delay: int = 50):
    time.sleep(delay)
    if os.path.exists(path):
        os.remove(path)

@app.get("/download")
def download_audio(url: str):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_audio_only()
        
        # ملف مؤقت
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, "temp.mp3")
        
        # تحميل الملف مؤقتًا
        stream.download(filename="temp.mp3", output_path=temp_dir)
        
        # تشغيل thread لحذف الملف بعد فترة
        threading.Thread(target=remove_file_later, args=(temp_file_path, 60), daemon=True).start()
        
        # ارسال الملف للمستخدم
        return FileResponse(
            temp_file_path,
            media_type="audio/mpeg",
            filename="temp.mp3"
        )

    except Exception as e:
        return {"error": str(e)}
