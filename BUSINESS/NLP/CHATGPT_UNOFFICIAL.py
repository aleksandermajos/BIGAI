from pyChatGPT import ChatGPT

class Gadula():
    def __init__(self):
        self.api = ChatGPT(auth_type='google', email='marek.grechuta144@gmail.com', password='password') # auth with google login

    def gada(self,text):
        resp = self.api.send_message(text)
        return resp['message']
