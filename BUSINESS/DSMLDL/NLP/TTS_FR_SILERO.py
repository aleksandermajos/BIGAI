import torch
import os
import simpleaudio as sa

class TTS_FR():

    def __init__(self,speaker='fr_0'):
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = torch.device(DEVICE)
        self.local_file = 'DATA/MODELS/TTS/v3_fr.pt'
        print(os.getcwd())
        self.model = torch.package.PackageImporter(self.local_file).load_pickle("tts_models", "model")
        self.model.to(self.device)
        self.sample_rate = 48000
        self.speaker=speaker

    def create_and_save(self,text):
        audio_paths = self.model.save_wav(text=text,
                             speaker=self.speaker,
                             sample_rate=self.sample_rate)
        filename = audio_paths
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait until sound has finished playing
        os.remove(audio_paths)

