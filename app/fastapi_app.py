from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import whisper
import tempfile
import os

app = FastAPI()

@app.post("/api/transcribe_api")
async def transcribe_api(
    audio: UploadFile = File(...),
    language: str = Form(...),
    model: str = Form(default="small")
):
    try:
        if model not in ["tiny", "base", "small", "medium", "large"]:
            return JSONResponse({"error": "Invalid model"}, status_code=400)

        whisper_model = whisper.load_model(model)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(await audio.read())
            tmp_path = tmp.name

        result = whisper_model.transcribe(tmp_path, language=language)
        os.remove(tmp_path)

        return {
            "model": model,
            "language": language,
            "transcription": result["text"]
        }

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
