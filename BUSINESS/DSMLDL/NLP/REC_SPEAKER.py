import soundcard as sc
import soundfile as sf
import os

class Sound_recorder():

    def __init__(self,length=5,path="DATA/PHRASES/LEARNING/GERMAN/",file='rec_sound.wav'):
        print(os.getcwd())
        self.OUTPUT_FILE_NAME = path+file
        self.SAMPLE_RATE = 48000  # [Hz]. sampling rate.
        self.RECORD_SEC = length  # [sec]. duration recording audio.

    def record(self,length=5):
        print('Start recording')
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=self.SAMPLE_RATE) as mic:
            data = mic.record(numframes=self.SAMPLE_RATE * length)
            sf.write(file=self.OUTPUT_FILE_NAME, data=data[:, 0], samplerate=self.SAMPLE_RATE)
