import openai

class ChatGPT():
    def __init__(self):
        f = open("/Users/aleksander/PycharmProjects/OPENAI/account.txt", "r")
        openai.api_key = f.read()
    def talk(self, text):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": text}
            ]
        )
        return completion
