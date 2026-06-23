import os
import requests
import pprint

# Define endpoint URL
URL = "http://127.0.0.1:8000/process"

# Find the test.wav file. It could be in the current directory or the parent directory
possible_paths = ["test.wav", "../test.wav", "ATC-AI/test.wav"]
audio_path = None
for p in possible_paths:
    if os.path.exists(p):
        audio_path = p
        break

if not audio_path:
    print("Error: Could not find 'test.wav' in any of these paths:", possible_paths)
    exit(1)

print(f"Found test audio file at: {os.path.abspath(audio_path)}")

# Prepare the file for the multipart form-data request
# The endpoint schema shows the parameter name is 'audio'
files = {
    'audio': ('test.wav', open(audio_path, 'rb'), 'audio/wav')
}

print(f"Sending POST request to {URL}...")
try:
    response = requests.post(URL, files=files)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    
    response.raise_for_status()
    
    content_type = response.headers.get("Content-Type", "")
    print(f"Response Content-Type: {content_type}")
    
    # Check if the response is JSON or binary audio
    if "application/json" in content_type:
        try:
            json_data = response.json()
            print("Response JSON data:")
            pprint.pprint(json_data)
        except Exception as e:
            print(f"Failed to parse JSON: {e}")
            print(f"Raw response preview: {response.text[:200]}")
    else:
        # Assume it's a binary stream/file (e.g., audio/wav or application/octet-stream)
        output_file = "response.wav"
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"Successfully saved response audio to {os.path.abspath(output_file)}")
        print(f"File size: {len(response.content)} bytes")

except requests.exceptions.RequestException as e:
    print(f"HTTP Request failed: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response status: {e.response.status_code}")
        print(f"Response content: {e.response.text}")
