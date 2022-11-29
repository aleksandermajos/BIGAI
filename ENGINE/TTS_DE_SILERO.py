import torch

class TTS_DE():

    def __init__(self,speaker='eva_k'):
        self.device = torch.device('cuda')
        self.local_file = 'model_de_silero.pt'
        self.model = torch.package.PackageImporter(self.local_file).load_pickle("tts_models", "model")
        self.model.to(self.device)
        self.sample_rate = 48000
        self.speaker=speaker

    def create_and_save(self,text,):
        audio_paths = self.model.save_wav(text=text,
                             speaker=self.speaker,
                             sample_rate=self.sample_rate)