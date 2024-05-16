import requests

# The URL of the FastAPI server
url = "http://127.0.0.1:8000/transcribe/"

# Path to the audio file you want to transcribe
audio_file_path = "example.wav"

# Open the audio file in binary mode
with open(audio_file_path, "rb") as audio_file:
    # Create a dictionary with the file data
    files = {"file": audio_file}

    # Make a POST request to the server
    response = requests.post(url, files=files)
    print(response.text)

# Check if the request was successful
if response.status_code == 200:
    # Get the transcription from the response
    transcription = response.json().get("transcription")
    print("Transcription:", transcription)
else:
    print("Error:", response.status_code, response.text)