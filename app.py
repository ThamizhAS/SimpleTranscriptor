from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import whisper, tempfile, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_OPTIONS = ["tiny", "base", "small", "medium", "large"]

@app.post("/transcribe_api")
async def transcribe_api(
    audio: UploadFile = File(...),
    language: str = Form(...),
    model: str = Form(default="small")
):
    try:
        if model not in MODEL_OPTIONS:
            return JSONResponse({"error": f"Invalid model '{model}'"}, status_code=400)

        whisper_model = whisper.load_model(model)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(await audio.read())
            tmp_path = tmp.name

        result = whisper_model.transcribe(tmp_path, language=language)
        os.remove(tmp_path)

        return JSONResponse({
            "model": model,
            "language": language,
            "transcription": result["text"]
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
