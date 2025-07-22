import streamlit as st
import whisper
import tempfile
import os

MODEL_OPTIONS = ["tiny", "base", "small", "medium", "large"]
LANGUAGE_OPTIONS = ["en", "ta", "hi", "ml", "te"]

@st.cache_resource
def load_model(name):
    return whisper.load_model(name)

st.title("🎧 Whisper Audio Transcriber")

language = st.selectbox("Select Language", LANGUAGE_OPTIONS, index=1)
model_name = st.selectbox("Select Model", MODEL_OPTIONS, index=2)
uploaded_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])

if uploaded_file:
    model = load_model(model_name)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info(f"Transcribing in {language} using {model_name}...")
    try:
        result = model.transcribe(tmp_path, language=language)
        st.success("Transcription complete!")
        st.text_area("Transcribed Text", value=result["text"], height=300)
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        os.remove(tmp_path)
