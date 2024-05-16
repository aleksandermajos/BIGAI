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


def translate(text: str, target_language: str) -> str:
    url = "http://127.0.0.1:8000/translate"
    payload = {
        "text": text,
        "target_language": target_language
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        translated_text = response.json().get("translated_text")
        return translated_text
    else:
        raise Exception(f"Error: {response.status_code} - {response.json().get('detail')}")

if __name__ == "__main__":
    text_to_translate = "To run the model we need to specify a pre-trained model file and a tokenizer for the text data"
    target_language = "spa_Latn"
    try:
        translated_text = translate(text_to_translate, target_language)
        print(f"Translated text: {translated_text}")
    except Exception as e:
        print(e)
