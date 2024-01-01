from pywhispercpp.model import Model
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"DATA/ALOHA/PHRASES/SPEAKING/"

model = Model('large', language="en", n_threads=6)
par = model.get_params()
par2 = model.get_params_schema()
langs = model.available_languages()
segments = model.transcribe(path+'jfk.wav', speed_up=True)
for segment in segments:
    print(segment.text)