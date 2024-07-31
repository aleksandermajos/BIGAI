from ENGINE.API_BIGAI_CLIENT import transcribe, tts_melo
import pickle
import spacy_stanza
from pydub import AudioSegment
from openai import OpenAI
from playsound import playsound
import os
from pathlib import Path
import pathlib





class SOURCE(object):
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
        if self.source_type not in SOURCE.source_type:
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



p = Path.cwd()
path_data = str(p.home())+'/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/DE/LITTLE_PRINCE/'
path_data = Path(path_data)
files = [f for f in path_data.iterdir() if f.is_file()]

for chapter_path in files:
    file_name = chapter_path.name
    path_str = str(chapter_path)
    print(file_name)
    current_chapter = SOURCE(name=file_name,path = path_str, source_type='AUDIO', user_type='BOOK', language='de')
    result = current_chapter.populate_text()
    with open(path_str+'.pkl', 'wb') as file:
        pickle.dump(result, file)

'''
path =r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/DE/LITTLE_PRINCE/03 Der Kleine Prinz - Kapitel 1.mp3'
LITTLEPRINCE_AUDIO_BOOK_PART1_DE = SOURCE(name='LITTLEPRINCE_AUDIO_BOOK_PART1_DE',path = path, source_type='AUDIO', user_type='BOOK', part=1, language='de')
pick = LITTLEPRINCE_AUDIO_BOOK_PART1_DE.populate_text()
with open('my_pick.pkl', 'wb') as file:
    # Step 4: Use pickle.dump() to serialize and save the dictionary
    pickle.dump(pick, file)
oko=5
'''