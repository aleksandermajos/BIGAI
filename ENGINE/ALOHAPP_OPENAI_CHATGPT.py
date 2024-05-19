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



class ChatGPT():
    def __init__(self):
        self.client = OpenAI(api_key=key)
    def talk(self, text):
        completion = self.client.chat.completions.create(model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "user", "content": text}
        ])

        return completion.choices[0].message.content

