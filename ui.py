import streamlit as st
import requests

st.title("🎧 Whisper Transcriber (Web + API)")

tab1, tab2 = st.tabs(["🌐 Web App", "🌀 API Guide"])

LANGUAGES = ["en", "ta", "hi", "ml", "te"]
MODELS = ["tiny", "base", "small", "medium", "large"]

API_URL = "https://your-api-service.onrender.com/transcribe_api"  # Replace with actual URL

with tab1:
    lang = st.selectbox("Select Language", LANGUAGES, index=1)
    model = st.selectbox("Select Whisper Model", MODELS, index=2)
    file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "m4a"])

    if file and st.button("Transcribe"):
        st.info("Uploading and transcribing...")
        files = {"audio": file.getvalue()}
        response = requests.post(
            API_URL,
            files={"audio": (file.name, file, "audio/mpeg")},
            data={"language": lang, "model": model}
        )

        if response.status_code == 200:
            st.success("✅ Transcription Complete")
            st.write(response.json()["transcription"])
        else:
            st.error("❌ Error: " + response.text)

with tab2:
    st.markdown("### API Example (cURL)")
    st.code(f"""
curl -X POST {API_URL} \\
  -F "audio=@your_audio.mp3" \\
  -F "language=ta" \\
  -F "model=small"
""", language="bash")
