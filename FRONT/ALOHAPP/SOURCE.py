from ENGINE.API_BIGAI_CLIENT import transcribe, detect_language, lemmatize_sentences
from WORD import WORD_Abstract, WORD_Japanese
from sudachipy import tokenizer
from sudachipy import dictionary
from ordered_set import OrderedSet
import pickle
import spacy_stanza
import pykakasi
from pydub import AudioSegment
from pathlib import Path
import os
import re

def get_all_paths_in_one_source(path, extension = '.pkl'):

    if not extension.startswith('.'):
        extension = '.' + extension
    all_files = os.listdir(path)
    filtered_files = [file for file in all_files if file.endswith(extension)]

    return filtered_files



class SOURCE:
    source_type = ['AUDIO', 'DECKS', 'EXEL', 'PIC', 'TATOEBA', 'TEXT', 'VIDEO']
    user_type = ['BOOK', 'SELFLEARNING', 'DECK', 'TATOEBA', 'NETFLIX', 'YT', 'TEXT', 'PIC', 'VIDEO', 'FREQDICT',
                 'EXAMS']

    def __init__(self, source_type, user_type, name, lang, path, part=-1):
        if source_type not in self.source_type:
            raise ValueError(f"Invalid source type '{source_type}'. Allowed source_type are: {self.source_type}")
        self.source_type = source_type
        if user_type not in self.user_type:
            raise ValueError(f"Invalid user type '{user_type}'. Allowed user_type are: {self.user_type}")
        self.user_type = user_type
        self.path = path
        self.name = name
        self.lang = lang
        self.part = part
        self.words = set()
        self.n_grams = set()
        self.sentences = set()

        if source_type=='AUDIO' and user_type=='BOOK':
            if part == -1:
                self.parts = sorted(get_all_paths_in_one_source(path,extension='.mp3'))
            else:
                self.parts = sorted(get_all_paths_in_one_source(path,extension='.mp3'))
                self.parts = [self.parts[part]]

            tokenizer_obj = dictionary.Dictionary().create()
            mode = tokenizer.Tokenizer.SplitMode.A
            kks = pykakasi.kakasi()
            for part in self.parts:
                text_seg = transcribe(file_path=self.path+'/'+part, language=self.lang)
                audio = AudioSegment.from_file(self.path+'/'+part)

                for segment in text_seg['segments']:
                    segment['audio'] = audio[segment['start'] * 1000:segment['end'] * 1000]
                    segment['text_lemma_spacy'] = lemmatize_sentences([segment['text']],lang=self.lang)[0]
                    if self.lang == 'ja':
                        tokens = tokenizer_obj.tokenize(segment['text'], mode)
                        segment['text_lemma_suda'] = {token.dictionary_form()  for token in tokens}
                        segment['text_lemma_pos'] = {token.part_of_speech() for token in tokens}

                        for word in segment['text_lemma_suda']:
                            result = kks.convert(word)
                            for item in result:
                                self.words.add(WORD_Japanese(text=item['orig'],language=self.lang,part_of_speech='verb',orginal=item['orig'],hiragana=item['hira'],katakana=item['kana'],hepburn=item['hepburn'],kunrei=item['kunrei'],passport=item['passport']))
                                print(f"Original: {item['orig']}, Rōmaji: {item['hepburn']}")


so = SOURCE(source_type='AUDIO', user_type='BOOK', name='ASSIMIL', lang='ja',
                                               path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/JA/SELF_LEARNING/ASSIMIL',
                                               part=-1)
oko=4
with open("my_object.pkl", "wb") as file:  # 'wb' means write binary
    pickle.dump(so, file)
oko=6
with open("my_object.pkl", "rb") as file:  # 'rb' means read binary
    loaded_object = pickle.load(file)
oko=7
