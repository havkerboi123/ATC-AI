# main.py
import os
import uuid
import json
import tempfile
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from agent.voice import get_text, get_speech
from agent.process_response import get_response

app = FastAPI()

@app.post("/process")
async def process(
    audio: UploadFile = File(...),
    data: str = Form(default="{}")
):
    # Save uploaded file temporarily
    ext = audio.filename.split(".")[-1]
    temp_dir = tempfile.gettempdir()
    input_path = os.path.join(temp_dir, f"{uuid.uuid4()}.{ext}")
    output_path = os.path.join(temp_dir, f"{uuid.uuid4()}.wav")

    with open(input_path, "wb") as f:
        f.write(await audio.read())

    # STT → LLM → TTS
    result = get_text(input_path)
    text = result["text"]

    try:
        telemetry = json.loads(data)
    except Exception as e:
        print(f"Failed to parse telemetry JSON: {e}")
        telemetry = None

    response_text = get_response(text, telemetry)

    get_speech(response_text, output_path)

    # Cleanup input
    os.remove(input_path)

    return FileResponse(output_path, media_type="audio/wav", filename="response.wav")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)