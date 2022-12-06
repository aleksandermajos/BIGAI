from transformers import FSMTForConditionalGeneration, FSMTTokenizer


class Translate():

    def __init__(self):
        mname = "facebook/wmt19-en-de"
        self.tokenizer = FSMTTokenizer.from_pretrained(mname)
        self.model = FSMTForConditionalGeneration.from_pretrained(mname)
    def translate(self,text):
        input_ids = self.tokenizer.encode(text, return_tensors="pt")
        outputs = self.model.generate(input_ids)
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded




