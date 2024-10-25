
from ENGINE.API_BIGAI_CLIENT import transcribe, tts_melo
import pickle
import spacy_stanza
from pydub import AudioSegment
from pathlib import Path
import os
import re


class SOURCE:
    source_type = ['AUDIO', 'DECKS', 'EXEL', 'PIC', 'TATOEBA', 'TEXT', 'VIDEO']
    user_type = ['BOOK', 'SELFLEARNING', 'DECK', 'TATOEBA','NETFLIX', 'YT', 'TEXT','PIC', 'VIDEO', 'FREQDICT']

    def __init__(self, source_type, user_type, name, lang, path):
        if source_type not in self.source_type:
            raise ValueError(f"Invalid source type '{source_type}'. Allowed source_type are: {self.source_type}")
        self.source_type = source_type
        if user_type not in self.user_type:
            raise ValueError(f"Invalid user type '{user_type}'. Allowed user_type are: {self.user_type}")
        self.user_type = user_type
        self.path = path
        self.name = name
        self.lang = lang

        if source_type=='AUDIO' and user_type=='BOOK':
            self.parts = sorted(get_all_paths_in_one_source(path))
            words_in_parts = []
            for part in self.parts:
                words_in_parts.append(get_words_from_one_pickle(path+'/'+part))
            self.words_in_parts = words_in_parts
            self.all_words = set().union(*self.words_in_parts)

        if source_type=='TEXT' and user_type=='FREQDICT':
            self.parts = sorted(get_all_paths_in_one_source(path,extension='xlsx'))
            self.words_in_parts = []
            for part in self.parts:
                self.words_in_parts.append(get_words_from_one_freq_dict(path+'/'+part))
            self.all_words = set().union(*self.words_in_parts)




    def get_words_from_n_parts(self,start, end):
        if start < 0 or end >= len(self.words_in_parts):
            raise IndexError("Start or end index is out of range.")
        if start > end:
            raise ValueError("Start index cannot be greater than end index.")

            # Initialize an empty set for the union
        result_set = set()

        # Iterate through the specified range and update the result_set
        for i in range(start, end + 1):
            result_set.update(self.words_in_parts[i])

        return result_set






class SOURCE_CREATE(object):
    source_type = ['AUDIO', 'DECKS', 'EXEL', 'PIC', 'TATOEBA', 'TEXT', 'VIDEO']
    user_type = ['BOOK', 'SELFLEARNING', 'DECK', 'TATOEBA','NETFLIX', 'YT', 'TEXT','PIC', 'VIDEO', 'FREQDICT']
    part = 0
    language = ''

    words_text = set()
    n_grams_text = set()
    sentences_text = set()

    words_audio = []
    n_grams_audio = []
    sentences_audio = []

    pics = []
    videos = []


    def __init__(self, name, path, source_type,user_type, language):
        self.name = name
        self.path = path
        self.source_type = source_type
        self.user_type = user_type
        self.language = language
        if self.source_type not in SOURCE_CREATE.source_type:
            print(f'Source type {self.source_type} not supported')



    def populate_text(self):
        lemma = spacy_stanza.load_pipeline(self.language)
        text = transcribe(file_path=self.path, language=self.language)
        audio = AudioSegment.from_file(self.path)
        for segment in text['segments']:
            lem = lemma(segment['text'])
            segment_audio = audio[segment['start']*1000:segment['end']*1000]
            #segment_audio.export(segment['text']+".mp3", format="mp3")
            segment['text_audio'] = segment_audio
            lem_text = []
            for token in lem:
                lem_text.append(str(token.lemma_))
            filtered_lem_text= [item for item in lem_text if '.' not in item and '_' not in item and ' ' not in item and ', ' not in item and ',' not in item]
            segment['text_lemma'] = filtered_lem_text


            for word in segment['words']:
                lem = lemma(word['word'])
                lem_word = ''
                for token in lem:
                    lem_word = (str(token.lemma_))
                word['word_lemma'] = lem_word
        return text

    def create_pickle(self, path, source_type, user_type, language):
        p = Path.cwd()
        path_data = str(
            p.home()) + path
        path_data = Path(path_data)
        files = [f for f in path_data.iterdir() if f.is_file()]

        for chapter_path in files:
            file_name = chapter_path.name
            path_str = str(chapter_path)
            current_chapter = SOURCE_CREATE(name=file_name, path=path_str, source_type=source_type, user_type=user_type, language=language)
            result = current_chapter.populate_text()

            with open(path_str + '.pkl', 'wb') as file:
                pickle.dump(result, file)

        return load_my_pickle(path)


def load_my_pickle(path):
        with open(path, 'rb') as file:
            loaded_dict = pickle.load(file)
        return loaded_dict

def get_words_from_one_pickle(path):
    data = load_my_pickle(path)
    words_gathered = set()
    for current_segment in data['segments']:
        for word in current_segment['words']:
            words_gathered.add(word['word_lemma'])
    remove_punctuations = {',', '.', '?', '!', ';', ':','...','%'}
    words_gathered.difference_update(remove_punctuations)
    pattern = re.compile(r'\d')
    words_gathered = {s for s in words_gathered if not pattern.search(s)}
    return words_gathered

def get_words_from_one_freq_dict(path):
    import pandas as pd
    df = pd.read_excel(path)
    words = df['WORD'].reset_index(drop=True).dropna()
    words_gathered = set(words)
    remove_punctuations = {',', '.', '?', '!', ';', ':','...','%'}
    words_gathered.difference_update(remove_punctuations)
    pattern = re.compile(r'\d')
    words_gathered = {s for s in words_gathered if not pattern.search(s)}
    return words_gathered

def get_all_paths_in_one_source(path, extension = '.pkl'):

    if not extension.startswith('.'):
        extension = '.' + extension
    all_files = os.listdir(path)
    filtered_files = [file for file in all_files if file.endswith(extension)]

    return filtered_files


def get_list_of_sources_in_language(path, language):
    pass
