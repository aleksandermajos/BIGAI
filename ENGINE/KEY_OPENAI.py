from openai import OpenAI
from playsound import playsound
import os
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/OPENAI/'
path = path_beginning+""
cwd = os.getcwd()
f = open(path+"account.txt", "r")
key = f.read().strip()
client = OpenAI(api_key=key)

def generate_and_play(text, voice, path=''):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    if path == '':
        response.stream_to_file("oko.mp3")
        playsound('oko.mp3')
        os.remove('oko.mp3')
    else:
        response.stream_to_file(path)
        playsound(path)

def o1_preview():
    response = client.chat.completions.create(
        model="o1-mini",
        messages=[
            {
                "role": "user",
                "content": "Write a bash script that takes a matrix represented as a string with format '[1,2],[3,4],[5,6]' and prints the transpose in the same format."
            }
        ]
    )

    print(response.choices[0].message.content)

o1_preview()
oko=5