import pickle

path =r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/DE/LITTLE_PRINCE/01 Der Kleine Prinz - Info.mp3.pkl'
with open(path, 'rb') as file:
    loaded_dict = pickle.load(file)


audio = loaded_dict['segments'][3]['text_audio']
audio.export("three.mp3", format="mp3")