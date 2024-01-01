from openai import OpenAI
from playsound import playsound
import os
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"DATA/ALOHA/"
cwd = os.getcwd()
f = open(path+"account.txt", "r")
client = OpenAI(api_key=f.read())

def generate_and_play(text, voice):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    response.stream_to_file("oko.mp3")
    playsound('oko.mp3')



