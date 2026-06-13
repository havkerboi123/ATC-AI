import os
import requests
import wave
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
load_dotenv()


GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
XAI_API_KEY=os.getenv("XAI_API_KEY")

#We use the xAI speech to text api here
def get_text(audio_path: str) -> dict:
    """Speech-to-text using xAI. Accepts .wav or .mp3"""
    ext = audio_path.split(".")[-1]
    mime = "audio/wav" if ext == "wav" else "audio/mpeg"
    
    with open(audio_path, "rb") as f:
        response = requests.post(
            "https://api.x.ai/v1/stt",
            headers={"Authorization": f"Bearer {os.environ['XAI_API_KEY']}"},
            files={"file": (audio_path, f, mime)},
            data=[
                ("format", "true"),
                ("language", "en"),
            ],
        )
    response.raise_for_status()
    return response.json()

#We use gemini's tts api for text to speech here
def get_speech(text: str, output_path: str = "out.wav") -> str:
    """Text-to-speech using Gemini. Returns path to saved .wav file"""
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-3.1-flash-tts-preview",
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
                )
            ),
        ),
    )

    pcm = response.candidates[0].content.parts[0].inline_data.data
    with wave.open(output_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(pcm)

    return output_path