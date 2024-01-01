from openai import OpenAI
import openai

from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"DATA/ALOHA/"
import os
cwd = os.getcwd()
f = open(path+"account.txt", "r")

client = OpenAI(api_key=openai.api_key)

response = client.audio.speech.create(
    model="tts-1-hd",
    voice="onyx",
    input="Wiecznie śpiewacie na tę samą nutę!"
          "Śpiewacie rozpacz dziką i bezbrzeżną,"
          "Serca przedwczesną goryczą zatrute"
          "I melancholie mglistą a lubieżną,"

)

response.stream_to_file("output.mp3")
