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
    data: str = Form(...)
):
    # Save uploaded file temporarily
    ext = audio.filename.split(".")[-1]
    temp_dir = tempfile.gettempdir()
    input_path = os.path.join(temp_dir, f"{uuid.uuid4()}.{ext}")
    output_path = os.path.join(temp_dir, f"{uuid.uuid4()}.wav")

    print("\n" + "="*60)
    print("Received request at local /process")
    print(f"Audio file: {audio.filename}")

    with open(input_path, "wb") as f:
        f.write(await audio.read())

    # STT → LLM → TTS
    result = get_text(input_path)
    text = result["text"]
    print(f"Transcribed Text: '{text}'")

    try:
        telemetry = json.loads(data)
        print(f"Parsed Telemetry from Client: {json.dumps(telemetry, indent=4)}")
    except Exception as e:
        print(f"Failed to parse telemetry JSON: {e}")
        print(f"Raw data string: {data}")
        telemetry = None

    response_text = get_response(text, telemetry)
    print(f"Groq Response Text: '{response_text}'")
    print("="*60 + "\n")

    get_speech(response_text, output_path)

    # Cleanup input
    os.remove(input_path)

    return FileResponse(output_path, media_type="audio/wav", filename="response.wav")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
