import openai

from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"DATA/ALOHAPP/"

import os
cwd = os.getcwd()


class ChatGPT():
    def __init__(self):
        f = open(path+"account.txt", "r")
        openai.api_key = f.read()
    def talk(self, text):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": text}
            ]
        )
        return completion.choices[0].message.content
