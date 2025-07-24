from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import whisper
import tempfile
import requests
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcribe-file")
async def transcribe_file(
    language: str = Form(...),
    model: str = Form(...),
    audio: UploadFile = File(...)
):
    try:
        model_instance = whisper.load_model(model)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(await audio.read())
            tmp_path = tmp.name

        result = model_instance.transcribe(tmp_path, language=language)
        os.remove(tmp_path)
        return {"success": True, "text": result["text"]}

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@app.post("/transcribe-url")
async def transcribe_url(
    audio_url: str = Form(...),
    language: str = Form(...),
    model: str = Form(...)
):
    try:
        response = requests.get(audio_url)
        if response.status_code != 200:
            return JSONResponse(status_code=400, content={"success": False, "error": "Failed to download audio file."})

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name

        model_instance = whisper.load_model(model)
        result = model_instance.transcribe(tmp_path, language=language)
        os.remove(tmp_path)
        return {"success": True, "text": result["text"]}

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})
