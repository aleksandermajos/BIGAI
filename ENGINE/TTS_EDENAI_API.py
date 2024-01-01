import requests
import json
import soundfile as sf
import sounddevice as sd
from ENGINE.KEY_EDENAI import provide_key
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"DATA/ALOHA/"
key = provide_key()



def generate_and_play(text, voice):
    url = "https://api.edenai.run/v2/audio/text_to_speech"
    payload = {
        "response_as_dict": True,
        "attributes_as_list": False,
        "show_original_response": False,
        "rate": 0,
        "pitch": 0,
        "volume": 0,
        "sampling_rate": 0,
        "providers": "elevenlabs",
        "language": "de",
        "text": text,
        "option": "FEMALE"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer "+key
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    url = result['elevenlabs']['audio_resource_url']
    r = requests.get(url, allow_redirects=True)
    open(path + 'edenai.wav', 'wb').write(r.content)
    samples, samplerate = sf.read(path + 'edenai.wav')
    sd.play(samples, samplerate)

    return 0