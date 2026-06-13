from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()


GROQ_API_KEY= os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)


def get_response(text: str) -> str:
    """Send text to Groq and return text response."""
    from groq import Groq
    
    client = Groq()
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text},
        ]
    )
    return completion.choices[0].message.content