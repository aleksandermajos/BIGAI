import os
import torch
import whisper
import re
from STARTUP.NLP.FILES_OPS import get_all_names

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
lang = 'Spanish'
learning_path = '../DATA/PHRASES/LEARNING/'+lang

class WhisperModel():
        def __init__(self,size='medium', lang='polish'):
            self.model = whisper.load_model(size)
            self.options = dict(language=lang, beam_size=5, best_of=5)
            self.transcribe_options = dict(task="transcribe", **self.options)
            self.translate_options = dict(task="translate", **self.options)
            self.last_transcribe =""
            self.last_translate =""


        def transcribe_file(self,path,file):
            filename, file_extension = os.path.splitext(file)
            full_input_path = path + '/' + file
            transcription = self.model.transcribe(full_input_path, **self.transcribe_options)["text"]
            translation = self.model.transcribe(full_input_path, **self.translate_options)["text"]
            print(transcription)
            print(translation)
            full_output_path = path + '/' + transcription + file_extension
            full_output_path = re.sub("[$@&!?]", "", full_output_path)
            os.rename(full_input_path, full_output_path)
            self.last_transcribe = transcription
            self.last_translate = translation


        def transcribe_all_in_dir(self,path,fe ='.wav'):
            list_of_files = get_all_names(path)
            for name in list_of_files:
                filename, file_extension = os.path.splitext(name)
                if file_extension == fe:
                    full_input_path = path + '/' + name
                    transcription = self.model.transcribe(full_input_path, **self.transcribe_options)["text"]
                    translation = self.model.transcribe(full_input_path, **self.translate_options)["text"]
                    print(transcription)
                    print(translation)
                    full_output_path = path + '/' + transcription + file_extension
                    full_output_path = re.sub("[$@&!?]", "", full_output_path)
                    os.rename(full_input_path, full_output_path)
                    self.last_transcribe = transcription
                    self.last_translate = translation
            return transcription

