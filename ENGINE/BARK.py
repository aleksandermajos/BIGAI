from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio

# download and load all models
preload_models()

# generate audio from text
text_prompt = """
Jak ciepła i cicha jest
noc sierpniowa ,
w którą listki leciutko,
wiatr muska.
Drzewa szumią cicho -
jakby od niechcenia.
A niebo się pyszni
"""
audio_array = generate_audio(text_prompt,history_prompt="v2/pl_speaker_1")
write_wav("pl1.wav", SAMPLE_RATE, audio_array)
audio_array = generate_audio(text_prompt,history_prompt="v2/pl_speaker_2")
write_wav("pl2.wav", SAMPLE_RATE, audio_array)
audio_array = generate_audio(text_prompt,history_prompt="v2/pl_speaker_3")
write_wav("pl3.wav", SAMPLE_RATE, audio_array)

# play text in notebook
Audio(audio_array, rate=SAMPLE_RATE)