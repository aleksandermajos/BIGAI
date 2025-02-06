from ENGINE.API_BIGAI_CLIENT import transcribe, lemmatize_sentences
from ENGINE.ALOHAPP_TEXT_GEN import generate_pos_tran
from openai import OpenAI
from groq import Groq
from cerebras.cloud.sdk import Cerebras
from FRONT.ALOHAPP.WORD import WORD_Chinese
from WORD import WORD_Japanese
from sudachipy import tokenizer
from sudachipy import dictionary
import pickle
import pykakasi
import jieba
from pypinyin import pinyin, Style
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

    def __init__(self, source_type, user_type, name, lang, native, path, part=-1, text_gen='openai'):
        if source_type not in self.source_type:
            raise ValueError(f"Invalid source type '{source_type}'. Allowed source_type are: {self.source_type}")
        self.source_type = source_type
        if user_type not in self.user_type:
            raise ValueError(f"Invalid user type '{user_type}'. Allowed user_type are: {self.user_type}")
        self.user_type = user_type
        self.path = path
        self.name = name
        self.lang = lang
        self.native = native
        self.part = part
        self.words_in_parts = []
        self.source_priority = 5

        if text_gen == 'openai':
            self.text_gen = 'openai'
            from ENGINE.KEY_OPENAI import provide_key
            key = provide_key()
            self.client_openai = OpenAI(api_key=key)

        if text_gen == 'cerebras':
            self.text_gen = 'cerebras'
            from ENGINE.KEY_CEREBRAS import provide_key
            key = provide_key()
            self.client_cerebras = Cerebras(api_key=key, )

        if text_gen == 'groq':
            self.text_gen = 'groq'
            from ENGINE.KEY_GROQ import provide_key
            self.client_groq = Groq(
                api_key=provide_key()
            )
            self.welcome = True

        if text_gen == 'ollama':
            self.text_gen = 'ollama'
            self.ollama_model = 'deepseek-r1:14b'

        if source_type=='AUDIO' and user_type=='BOOK':
            if part == -1:
                self.parts = sorted(get_all_paths_in_one_source(path,extension='.mp3'))
                self.parts_done = sorted(get_all_paths_in_one_source(path,extension='.pkl'))
                pkl_set = {filename.replace('.pkl', '') for filename in self.parts_done}
                missing_files = [filename for filename in self.parts if filename not in pkl_set]
                if len(missing_files) > 0: self.parts = missing_files

            else:
                self.parts = sorted(get_all_paths_in_one_source(path,extension='.mp3'))
                self.parts = [self.parts[part]]
            if self.lang == 'ja':
                tokenizer_obj = dictionary.Dictionary().create()
                mode = tokenizer.Tokenizer.SplitMode.A
                kks = pykakasi.kakasi()

            for part in self.parts:
                print("START OF NEXT PART")
                print(part)
                self.words_in_parts.append(set())
                text_seg = transcribe(file_path=self.path+'/'+part, language=self.lang)
                audio = AudioSegment.from_file(self.path+'/'+part)

                for segment in text_seg['segments']:
                    print("START OF NEXT SEGMENT")
                    segment['audio'] = audio[segment['start'] * 1000:segment['end'] * 1000]
                    segment['text_lemma_spacy'] = lemmatize_sentences([segment['text']],lang=self.lang)[0]


                    if self.lang == 'it':
                        pass

                    if self.lang == 'ja':
                        tokens = tokenizer_obj.tokenize(segment['text'], mode)
                        segment['text_lemma_suda'] = {token.dictionary_form()  for token in tokens}
                        segment['text_lemma_pos'] = {token.part_of_speech() for token in tokens}

                        for word in segment['text_lemma_suda']:
                            result = kks.convert(word)
                            for item in result:
                                self.words_in_parts[-1].add(WORD_Japanese(text=item['orig'],language=self.lang,original=item['orig'],hiragana=item['hira'],katakana=item['kana'],hepburn=item['hepburn'],kunrei=item['kunrei'],passport=item['passport']))
                                #print(f"Original: {item['orig']}, Rōmaji: {item['hepburn']}")


                        while True:
                            try:
                                bot_reply = generate_pos_tran(self, words=self.words_in_parts[-1], lang=self.lang,
                                                              target_lang=self.native)
                                bot_reply_json = json.loads(bot_reply)
                                break  # Exit the loop if parsing is successful
                            except json.JSONDecodeError:
                                # Handle the exception (e.g., wait for new data or log an error)
                                print("Invalid JSON data received. Retrying...")
                                # Update 'received_data' with new data before retrying

                        if isinstance(bot_reply_json, dict) and 'words' in bot_reply_json:
                            print("'words' exists in bot_reply_json")
                        else:
                            print("'words' does not exist")
                            while not (isinstance(bot_reply_json, dict) and 'words' in bot_reply_json):
                                bot_reply = generate_pos_tran(self, words=self.words_in_parts[-1], lang=self.lang, target_lang=self.native)
                                bot_reply_json = json.loads(bot_reply)

                        for word in self.words_in_parts[-1]:
                            for item in bot_reply_json['words']:
                                if isinstance(item['original'], str) and isinstance(word['original'], str):
                                    print("Both are strings.")
                                else:
                                    print("At least one is not a string.")
                                if item['original'] == word['original']:
                                    print("item 'original':")
                                    print(item['original'])
                                    print("word 'original':")
                                    print(word['original'])

                                    word['part_of_speech'] = item['part_of_speech']
                                    print("word 'part_of_speech':")
                                    print(word['part_of_speech'])
                                    print("item 'part_of_speech':")
                                    print(item['part_of_speech'])

                                    word['translate'] = item['translate']
                                    print("word 'translate':")
                                    print(word['translate'])
                                    print("item 'translate':")
                                    print(item['translate'])

                    if self.lang == 'zh':
                        words = segment['text_lemma_spacy']
                        unique_words = set(words)
                        for word in unique_words:

                            pinyin_representation = pinyin(word, style=Style.TONE)
                            # Flatten the list of lists and join syllables
                            pinyin_flat = ''.join([item for sublist in pinyin_representation for item in sublist])
                            self.words_in_parts[-1].add(WORD_Chinese(text=word,language=self.lang,original=word,pinyin=pinyin_flat))
                        bot_reply_json = False
                        while not bot_reply_json:
                            bot_reply = generate_pos_tran(self, words=self.words_in_parts[-1], lang=self.lang,
                                                          target_lang=self.native)
                            try:
                                bot_reply_json = json.loads(bot_reply)
                            except json.JSONDecodeError:
                                print("Invalid JSON received:", bot_reply)
                                break

                        if isinstance(bot_reply_json, dict) and 'words' in bot_reply_json:
                            print("'words' exists in bot_reply_json")
                        else:
                            print("'words' does not exist")
                            while not (isinstance(bot_reply_json, dict) and 'words' in bot_reply_json):
                                bot_reply = generate_pos_tran(self, words=self.words_in_parts[-1], lang=self.lang, target_lang=self.native)
                                bot_reply_json = json.loads(bot_reply)

                        for word in self.words_in_parts[-1]:
                            for item in bot_reply_json['words']:
                                if item['original'] == word['original']:
                                    word['part_of_speech'] = item['part_of_speech']
                                    word['translate'] = item['translate']




                    print("END OF NEXT SEGMENT")
                print("END OF NEXT PART:")
                print(part)
                self.client_openai = None
                with open(self.path + '/' + part + '.pkl', 'wb') as file:  # 'wb' mode is for writing in binary
                    pickle.dump(self, file)

                if text_gen == 'openai':
                    self.text_gen = 'openai'
                    from ENGINE.KEY_OPENAI import provide_key
                    key = provide_key()
                    self.client_openai = OpenAI(api_key=key)

                if text_gen == 'cerebras':
                    self.text_gen = 'cerebras'
                    from ENGINE.KEY_CEREBRAS import provide_key
                    key = provide_key()
                    self.client_cerebras = Cerebras(api_key=key, )

                if text_gen == 'groq':
                    self.text_gen = 'groq'
                    from ENGINE.KEY_GROQ import provide_key
                    self.client_groq = Groq(
                        api_key=provide_key()
                    )
                    self.welcome = True

                if text_gen == 'ollama':
                    self.text_gen = 'ollama'
                    self.ollama_model = 'deepseek-r1:14b'

            self.words_in_all_parts = set()
            for current_set in self.words_in_parts:
                self.words_in_all_parts.update(current_set)

            n = len(self.words_in_parts)
            self.parts_priority = [0] * n

            if text_gen == 'openai':
                self.client_openai = None

            if text_gen == 'groq':
                self.client_groq = None

            if text_gen == 'cerebras':
                self.client_cerebras = None

            if text_gen == 'ollama':
                self.ollama_model = None

    def make_full_words_from_all_parts(self):
        full_words_from_all_parts = set()
        for current_set in self.words_in_parts:
            full_words_from_all_parts.update(current_set)
        self.all_words_from_all_parts = full_words_from_all_parts

    def get_full_words_from_n_parts(self, start, end):
        full_words_from_n_parts = set()
        for current_set in self.words_in_parts[start:end]:
            full_words_from_n_parts.update(current_set)
        return full_words_from_n_parts

    def get_words_from_n_parts(self, start, end):
        words_from_start_end_parts = set()
        for current_set in self.words_in_parts[start:end]:
            words_from_start_end_parts.update(current_set)
        return words_from_start_end_parts









