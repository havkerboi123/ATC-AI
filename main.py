# main.py
import os
import uuid
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from agent.voice import get_text, get_speech
from agent.process_response import get_response

app = FastAPI()

@app.post("/process")
async def process(audio: UploadFile = File(...)):
    # Save uploaded file temporarily
    ext = audio.filename.split(".")[-1]
    input_path = f"/tmp/{uuid.uuid4()}.{ext}"
    output_path = f"/tmp/{uuid.uuid4()}.wav"

    with open(input_path, "wb") as f:
        f.write(await audio.read())

    # STT → LLM → TTS
    result = get_text(input_path)
    text = result["text"]

    response_text = get_response(text)

    get_speech(response_text, output_path)

    # Cleanup input
    os.remove(input_path)

    return FileResponse(output_path, media_type="audio/wav", filename="response.wav")