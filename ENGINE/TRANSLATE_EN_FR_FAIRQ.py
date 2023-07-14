import torch

class Translate_EN_FR():

    def __init__(self):
        self.model = torch.hub.load('pytorch/fairseq', 'transformer.wmt14.en-fr', tokenizer='moses', bpe='subword_nmt')
    def translate(self,text):
        fr = self.model.translate(text, beam=5)
        return fr