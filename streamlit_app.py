import streamlit as st
import whisper
import tempfile
import os
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html

# ---------------------- Streamlit UI --------------------------

st.title("🎧 Whisper Audio Transcriber")

tab1, tab2 = st.tabs(["🌐 Web App", "🌀 API Guide"])

MODEL_OPTIONS = ["tiny", "base", "small", "medium", "large"]
LANGUAGE_OPTIONS = ["en", "ta", "hi", "ml", "te"]

@st.cache_resource
def load_model(model_name):
    return whisper.load_model(model_name)

with tab1:
    st.markdown("Upload an audio file and select language + model.")

    language = st.selectbox("🗣️ Choose Language", options=LANGUAGE_OPTIONS, index=1)
    model_name = st.selectbox("🧠 Choose Whisper Model", options=MODEL_OPTIONS, index=2)

    uploaded_file = st.file_uploader("🎵 Upload audio file", type=["mp3", "wav", "m4a"])

    if uploaded_file is not None:
        model = load_model(model_name)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        st.info(f"Transcribing with `{model_name}` model and language `{language}`...")

        try:
            result = model.transcribe(tmp_path, language=language)
            st.success("✅ Transcription completed!")
            st.markdown("#### 📝 Transcript:")
            st.write(result["text"])
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            os.remove(tmp_path)

with tab2:
    st.subheader("📡 API (cURL) Usage")
    st.code("""
curl -X POST http://fama.pythonanywhere.com/transcribe_api \\
  -F "audio=@/path/to/audio.mp3" \\
  -F "language=ta" \\
  -F "model=small"
    """, language="bash")
    st.markdown("✅ Supported models: `tiny`, `base`, `small`, `medium`, `large`")

# ---------------------- FastAPI Backend --------------------------

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.post("/transcribe_api")
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

@api.get("/docs", include_in_schema=False)
async def custom_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Whisper API Docs")
