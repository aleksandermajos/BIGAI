from playsound import playsound
from ENGINE.KEY_OPENAI import provide_key
from openai import OpenAI
import os
key=provide_key()
client = OpenAI(api_key=key)
from pydub import AudioSegment



def generate_and_play(text, voice, path=''):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    if path == '':
        response.stream_to_file("oko.mp3")
        '''
        audio = AudioSegment.from_mp3("oko.mp3")
        silence = AudioSegment.silent(duration=1000)
        output = audio + silence + audio
        output.export("oko.mp3", format="mp3")
        '''


        playsound('oko.mp3')
        os.remove('oko.mp3')
    else:
        response.stream_to_file(path)
        playsound(path)
