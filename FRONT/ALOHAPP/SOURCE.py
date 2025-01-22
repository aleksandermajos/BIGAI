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




class SOURCE_USE:
    source_type = ['AUDIO', 'DECKS', 'EXEL', 'PIC', 'TATOEBA', 'TEXT', 'VIDEO']
    user_type = ['BOOK', 'SELFLEARNING', 'DECK', 'TATOEBA','NETFLIX', 'YT', 'TEXT','PIC', 'VIDEO', 'FREQDICT', 'EXAMS']

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

        if source_type=='AUDIO' and user_type=='BOOK':
            if part == -1:
                self.parts = sorted(get_all_paths_in_one_source(path))
            else:
                self.parts = sorted(get_all_paths_in_one_source(path))
                self.parts = [self.parts[part]]

            kks = pykakasi.kakasi()
            words_in_parts = []
            hira_in_parts = []
            hip = []
            hepburn_in_parts = []
            heip = []
            for part in self.parts:
                wip = get_words_from_one_pickle(path=path+'/'+part,lang=self.lang)
                words_in_parts.append(wip)
                element = 0
                for word in wip:
                    print(element)
                    element = element + 1
                    result = (
                        kks.convert(word))
                    for item in result:
                        hip.append(item['hira'])
                        heip.append(item['hepburn'])
                        print(word+'-'+ item['hira']+'-'+ item['hepburn'])
                hira_in_parts.append(hip)
                hepburn_in_parts.append(heip)
            self.words_in_parts = words_in_parts
            self.hira_in_parts = hira_in_parts
            self.hepburn_in_parts = hepburn_in_parts
            self.all_words = set().union(*self.words_in_parts)

        if source_type=='TEXT' and user_type=='FREQDICT':
            self.parts = sorted(get_all_paths_in_one_source(path,extension='xlsx'))
            self.words_in_parts = []
            for part in self.parts:
                self.words_in_parts.append(get_words_from_one_freq_dict(path+'/'+part))
            self.all_words = set().union(*self.words_in_parts)

        if source_type=='TEXT' and user_type=='EXAMS':
            self.parts = sorted(get_all_paths_in_one_source(path,extension='xlsx'))
            self.words_in_parts = []
            for part in self.parts:
                self.words_in_parts.append(get_words_from_one_exam_jlpt_words(path+'/'+part))
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


    def __init__(self, name, path, source_type,user_type, lang):
        self.name = name
        self.path = path
        self.source_type = source_type
        self.user_type = user_type
        self.language = lang
        if self.source_type not in SOURCE_CREATE.source_type:
            print(f'Source type {self.source_type} not supported')



    def populate_text(self,lemma):
        lemma = lemma
        text = transcribe(file_path=self.path, language=self.language)

        tokenizer_obj = dictionary.Dictionary().create()
        audio = AudioSegment.from_file(self.path)
        for segment in text['segments']:
            if self.language=='ja':

                tokens = tokenizer_obj.tokenize(segment['text'])
                #segment['text_lemma'] = tokens
                # Extract words
                words = [token.surface() for token in tokens]
                unwanted_elements = ['。', '?', '.','_',' ',', ',',']
                words = [item for item in words if item not in unwanted_elements]
                # Get unique words
                unique_words = set(words)
                segment['words_lemma_suda'] = [item for item in unique_words]


            else:
                lem = lemma(segment['text'])
                segment_audio = audio[segment['start']*1000:segment['end']*1000]
                #segment_audio.export(segment['text']+".mp3", format="mp3")
                segment['text_audio'] = segment_audio
                lem_text = []
                for token in lem:
                    lem_text.append(str(token.lemma_))
                unwanted_elements = ['。', '?', '.', '_', ' ', ', ', ',']
                filtered_lem_text= [item for item in lem_text if item not in unwanted_elements]
                segment['text_lemma'] = filtered_lem_text


                for word in segment['words']:
                    lem = lemma(word['word'])
                    lem_word = ''
                    for token in lem:
                        lem_word = (str(token.lemma_))
                    word['word_lemma'] = lem_word
        return text

    def create_pickle(self, path, source_type, user_type, language):
        '''
        p = Path.cwd()
        path_data = str(
            p.home()) + path
        '''
        path_data = Path(path)
        files = [f for f in path_data.iterdir() if f.is_file()]

        lemma = spacy_stanza.load_pipeline(self.language)
        for chapter_path in files:
            file_name = chapter_path.name
            path_str = str(chapter_path)
            current_chapter = SOURCE_CREATE(name=file_name, path=path_str, source_type=source_type, user_type=user_type, lang=language)
            result = current_chapter.populate_text(lemma)

            with open(path_str + '.pkl', 'wb') as file:
                pickle.dump(result, file)

        return load_my_pickle(path)


def load_my_pickle(path):
        with open(path, 'rb') as file:
            loaded_dict = pickle.load(file)
        return loaded_dict

def get_words_from_one_pickle(path,lang):
    data = load_my_pickle(path)
    words_list = []
    for current_segment in data['segments']:
        words_list.extend(current_segment['words_lemma_suda'])
        '''
        for word in current_segment['words']:

            result = detect_language(word['word'])
            language_code = result['language_code']
            if language_code == lang:
                words_gathered.add(word['word_lemma'])
        '''

    words_gathered = set(words_list)


    remove_punctuations = {',', '.', '?', '!', ';', ':','...','%'}
    words_gathered.difference_update(remove_punctuations)
    pattern = re.compile(r'\d')
    words_gathered = {s for s in words_gathered if not pattern.search(s)}
    return words_gathered

def get_words_from_one_freq_dict(path):
    import pandas as pd
    df = pd.read_excel(path, engine='openpyxl')
    words = df['WORD'].reset_index(drop=True).dropna()
    words_gathered = OrderedSet(words)

    remove_punctuations = {',', '.', '?', '!', ';', ':','...','%'}
    words_gathered.difference_update(remove_punctuations)

    pattern = re.compile(r'\d')
    words_gathered = OrderedSet([pattern.sub('', word) for word in words_gathered])

    return words_gathered

def get_words_from_one_exam_jlpt_words(path):
    import pandas as pd
    df = pd.read_excel(path, engine='openpyxl')
    words = df['Kana'].reset_index(drop=True).dropna()
    words_gathered = OrderedSet(words)

    remove_punctuations = {',', '.', '?', '!', ';', ':','...','%'}
    words_gathered.difference_update(remove_punctuations)

    pattern = re.compile(r'\d')
    words_gathered = OrderedSet([pattern.sub('', word) for word in words_gathered])

    return words_gathered




def get_list_of_sources_in_language(path, language):
    pass
'''
path =r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/JA/SELF_LEARNING/ASSIMIL'
ASS_JA = SOURCE_CREATE(name='ASS_JA',path = path, source_type='AUDIO', user_type='BOOK', lang='ja')
pick = ASS_JA.create_pickle(path=path, source_type='AUDIO', user_type='BOOK', language='ja')
with open('my_pick.pkl', 'wb') as file:
    # Step 4: Use pickle.dump() to serialize and save the dictionary
    pickle.dump(pick, file)
oko=5
'''