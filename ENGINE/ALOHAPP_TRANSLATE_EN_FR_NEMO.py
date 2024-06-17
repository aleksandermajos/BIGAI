import nemo.collections.nlp as nemo_nlp


class Translate_EN_FR_NEMO():

    def __init__(self):
        self.model = nemo_nlp.models.machine_translation.MTEncDecModel.from_pretrained(
            model_name="nmt_en_fr_transformer24x6")

    def translate(self,text):
        fr =  self.model.TRANSLATE_NLLB([text], source_lang="en", target_lang="fr")
        return fr[0]