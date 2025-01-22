import requests
from typing import List

def lemmatize_sentences(sentences: List[str],lang, url="http://127.0.0.1:8000/lemmatize") -> List[List[str]]:
    payload = {"sentences": sentences,
               'lang': lang}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data.get("lemmatized_sentences", [])
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the server: {e}")
        return []


def detect_language(text, url='http://127.0.0.1:8000/detect_language'):
    """
    Sends text to the language detection server and returns the detected language code and confidence score.

    Parameters:
    - text (str): The text to analyze for language detection.
    - url (str): The URL of the language detection endpoint.

    Returns:
    - dict: A dictionary containing 'language_code' and 'confidence'.

    Raises:
    - requests.HTTPError: If the server returns an unsuccessful status code.
    """
    payload = {'text': text}
    response = requests.post(url, json=payload)

    # Raise an exception for bad status codes
    response.raise_for_status()

    # Parse the JSON response
    data = response.json()
    return {
        'language_code': data['language_code'],
        'confidence': data['confidence']
    }

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


def transcribe(file_path, language):
    # The URL of the FastAPI server
    url = "http://127.0.0.1:8000/transcribe/"
    data = {'language': language,
            'file_path': file_path
            }

    # Path to the audio file you want to transcribe
    audio_file_path = file_path

    # Open the audio file in binary mode
    with open(audio_file_path, "rb") as audio_file:
        # Create a dictionary with the file data
        files = {"file": audio_file}

        # Make a POST request to the server
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            transcribed_text = response.json()
            return transcribed_text
        else:
            raise Exception(f"Error: {response.status_code} - {response.json().get('detail')}")


def translate(text: str, source_language: str, target_language: str) -> str:
    url = "http://127.0.0.1:8000/translate"
    payload = {
        "text": text,
        "source_language": source_language,
        "target_language": target_language
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        translated_text = response.json().get("translated_text")
        return translated_text
    else:
        raise Exception(f"Error: {response.status_code} - {response.json().get('detail')}")

def tts_melo(text: str, lang: str, output: str):
    url = "http://127.0.0.1:8000/tts_melo"
    payload = {
        "text": text,
        "lang": lang,
        "output_path": output
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("file saved in "+ output)
        return output
    else:
        raise Exception(f"Error: {response.status_code} - {response.json().get('detail')}")




if __name__ == "__main__":
    text_to_lemmatize = [']第1課はやくいきましょうわかりましたどこへ']
    lem = lemmatize_sentences(text_to_lemmatize, lang='ja')


    text_to_translate = "To run the model we need to specify a pre-trained model file and a tokenizer for the text data"
    source_language = 'eng_Latn'
    target_language = "fra_Latn"
    translated_text = translate(text_to_translate, source_language, target_language)

    result = detect_language("Detected language")
    language_code = result['language_code']
    confidence = result['confidence']
    print(f"Detected language: {language_code} with confidence {confidence}")




    text = transcribe(file_path="audio_file.wav", language='pl')


    tts_melo("I do not have a dream",lang="en", output="dream.wav")
    tts_melo("私には夢があります", lang="jp", output="dream_jp.wav")

    sentences_fr = [
        "Les chauves-souris rayées s'accrochent à leurs pattes pour mieux s'en sortir",
        "Elle courait et sautait dans le parc",
        "Ils étudient la linguistique depuis des années"
    ]
    lemmatized_fr = lemmatize_sentences(sentences_fr, lang='fr')






    '''
    result = generate_image(prompt="A nice young girl with black eyes ", negative_prompt="", num_inference_steps=30,
                            save_path="oko1.png")
    result = generate_image(prompt="A nice young girl with white eyes ", negative_prompt="", num_inference_steps=30,
                            save_path="oko2.png")
    '''