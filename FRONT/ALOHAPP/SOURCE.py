from ENGINE.API_BIGAI_CLIENT import transcribe, lemmatize_sentences
from ENGINE.ALOHAPP_TEXT_GEN import generate_pos_tran
from openai import OpenAI
from WORD import WORD_Japanese
from sudachipy import tokenizer
from sudachipy import dictionary
import pickle
import pykakasi
from pydub import AudioSegment
import os
import json


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

    def __init__(self, source_type, user_type, name, lang, path, part=-1, text_gen='openai'):
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

        if text_gen == 'openai':
            self.text_gen = 'openai'
            from ENGINE.KEY_OPENAI import provide_key
            key = provide_key()
            self.client_openai = OpenAI(api_key=key)

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
                                self.words.add(WORD_Japanese(text=item['orig'],language=self.lang,original=item['orig'],hiragana=item['hira'],katakana=item['kana'],hepburn=item['hepburn'],kunrei=item['kunrei'],passport=item['passport']))
                                print(f"Original: {item['orig']}, Rōmaji: {item['hepburn']}")
                        bot_reply = generate_pos_tran(self,words=self.words,lang=self.lang, target_lang='en')
                        bot_reply_json = json.loads(bot_reply)

                        if isinstance(bot_reply_json, dict) and 'words' in bot_reply_json:
                            print("'words' exists in bot_reply_json")
                        else:
                            print("'words' does not exist")
                            while not (isinstance(bot_reply_json, dict) and 'words' in bot_reply_json):
                                bot_reply = generate_pos_tran(self, words=self.words, lang=self.lang, target_lang='en')
                                bot_reply_json = json.loads(bot_reply)

                        for word in self.words:
                            for item in bot_reply_json['words']:
                                if item['original'] == word['original']:
                                    word['part_of_speech'] = item['part_of_speech']
                                    word['translate'] = item['translate']
            self.client_openai = None






