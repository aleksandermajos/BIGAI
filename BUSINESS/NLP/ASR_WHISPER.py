import os
import torch
import whisper
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import re
from BUSINESS.NLP.FILES_OPS import get_all_names

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
lang = 'Spanish'
learning_path = '../DATA/PHRASES/LEARNING/'+lang

class WhisperModel():
        def __init__(self,size='small', lang='polish'):
            #processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
            #self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2")
            self.model = whisper.load_model(size)
            self.options = dict(language=lang, beam_size=5, best_of=5)
            self.transcribe_options = dict(task="transcribe", **self.options)
            self.translate_options = dict(task="translate", **self.options)
            self.last_transcribe =""
            self.last_translate =""
            self.full_input_path =''
            self.full_output_path=''


        def transcribe_file(self,path,file):
            filename, file_extension = os.path.splitext(file)
            full_input_path = path + '/' + file
            self.full_input_path = full_input_path
            transcription = self.model.transcribe(full_input_path, **self.transcribe_options)["text"]
            print(transcription)
            full_output_path = path + '/' + transcription + file_extension
            full_output_path = re.sub("[$@&!?]", "", full_output_path)
            self.full_output_path = full_output_path
            isExist = os.path.exists(full_output_path)
            if not isExist:
                os.rename(full_input_path, full_output_path)
            self.last_transcribe = transcription


        def translate_file(self):
            full_input_path = self.full_output_path
            translation = self.model.transcribe(full_input_path, **self.translate_options)["text"]
            print(translation)
            self.last_translate = translation


        def transcribe_all_in_dir(self,path,fe ='.wav'):
            list_of_files = get_all_names(path)
            for name in list_of_files:
                filename, file_extension = os.path.splitext(name)
                contains_digit = any(map(str.isdigit, filename))
                if file_extension == fe and contains_digit:
                    full_input_path = path + '/' + name
                    transcription = self.model.transcribe(full_input_path, **self.transcribe_options)["text"]
                    translation = self.model.transcribe(full_input_path, **self.translate_options)["text"]
                    print(transcription)
                    print(translation)
                    full_output_path = path + '/' + transcription + file_extension
                    full_output_path = re.sub("[$@&!?]", "", full_output_path)
                    isFileExist = os.path.isfile(full_output_path)
                    if isFileExist==False:
                        os.rename(full_input_path, full_output_path)
                    self.last_transcribe = transcription
                    self.last_translate = translation
            return transcription

