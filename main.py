import threading
import subprocess
import uvicorn
from app.fastapi_app import app as fastapi_app

def run_streamlit():
    subprocess.run(["streamlit", "run", "app/streamlit_app.py", "--server.port=8501"])

def run_fastapi():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    threading.Thread(target=run_fastapi).start()
    threading.Thread(target=run_streamlit).start()
