import requests


def generate_image(prompt: str, negative_prompt: str, num_inference_steps: int, save_path: str):
    url = "http://127.0.0.1:8000/generate_image/"

    # Define the payload
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "num_inference_steps": num_inference_steps
    }

    try:
        # Send a POST request to the server
        response = requests.post(url, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Write the content of the response (image) to a file
            with open(save_path, "wb") as file:
                file.write(response.content)

            return f"Image saved to {save_path}"
        else:
            return f"Failed to generate image. Status code: {response.status_code}\n{response.json()}"
    except Exception as e:
        return f"An error occurred: {e}"


def transcribe(audio_file):
    # The URL of the FastAPI server
    url = "http://127.0.0.1:8000/transcribe/"

    # Path to the audio file you want to transcribe
    audio_file_path = audio_file

    # Open the audio file in binary mode
    with open(audio_file_path, "rb") as audio_file:
        # Create a dictionary with the file data
        files = {"file": audio_file}

        # Make a POST request to the server
        response = requests.post(url, files=files)
        if response.status_code == 200:
            transcribed_text = response.text
            return transcribed_text
        else:
            raise Exception(f"Error: {response.status_code} - {response.json().get('detail')}")


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
    text=transcribe(audio_file="audio.mp3")

    result = generate_image(prompt="A nice young girl with black eyes ",negative_prompt="",num_inference_steps=56, save_path="oko.png")
    print(result)

    text_to_translate = "To run the model we need to specify a pre-trained model file and a tokenizer for the text data"
    target_language = "spa_Latn"
    translated_text = translate(text_to_translate, target_language)
    print(f"Translated text: {translated_text}")

