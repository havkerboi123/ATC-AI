import os
import json
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI(title="Local AI ATC Mock Server")

@app.post("/process")
async def process(
    audio: UploadFile = File(...),
    data: str = Form(default="{}")
):
    print("\n" + "="*50)
    print("Received request at /process")
    print(f"Audio Filename: {audio.filename}")
    print(f"Audio Content-Type: {audio.content_type}")
    
    # Parse and cleanly print telemetry JSON data
    try:
        telemetry = json.loads(data)
        print("Parsed Telemetry:")
        print(json.dumps(telemetry, indent=4))
    except Exception as e:
        print(f"Error parsing telemetry JSON: {e}")
        print(f"Raw data: {data}")
    print("="*50 + "\n")
    
    # Locate a mock response audio file
    possible_paths = [
        "test.wav",
        "../test.wav",
        "pilot_request.wav",
        "../pilot_request.wav",
        "ATC-AI/test.wav",
        "ATC-AI/pilot_request.wav"
    ]
    
    response_file = None
    for p in possible_paths:
        if os.path.exists(p):
            response_file = p
            break
            
    if response_file:
        print(f"Returning mock audio file from: {os.path.abspath(response_file)}")
        return FileResponse(response_file, media_type="audio/wav")
    else:
        print("Error: Could not find test.wav or pilot_request.wav mock files.")
        return JSONResponse(
            status_code=404,
            content={"detail": "Mock audio file (test.wav or pilot_request.wav) not found on server."}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("local_server:app", host="127.0.0.1", port=8000, reload=True)
