from dataclasses import dataclass
from typing import NamedTuple
from ENGINE.API_BIGAI_CLIENT import transcribe, tts_melo

class SOURCE(object):
    source_type = ['AUDIO', 'DECKS', 'EXEL', 'PIC', 'TATOEBA', 'TEXT', 'VIDEO']
    user_type = ['BOOK', 'SELFLEARNING', 'DECK', 'TATOEBA','NETFLIX', 'YT', 'TEXT','PIC', 'VIDEO', 'FREQDICT']
    part = 0
    language = ''

    words_text = []
    n_grams_text = []
    sentences_text = []

    words_audio = []
    n_grams_audio = []
    sentences_audio = []

    pics = []
    videos = []
    def __init__(self, name ,source_type,user_type,part, language):
        self.name = name
        self.source_type = source_type
        self.user_type = user_type
        self.part = part
        self.language = language
        if self.source_type not in SOURCE.source_type:
            print(f'Source type {self.source_type} not supported')

    def populate_words_text(self):
        pass

    def populate_n_gram_text(self):
        pass

    def populate_sentences_text(self):
        pass



    def populate_words_audio(self):
        pass

    def populate_n_grams_audio(self):
        pass

    def populate_sentences_audio(self):
        pass

    def populate_pics(self):
        pass

    def populate_videos(self):
        pass







LP_AUDIO_BOOK_PART1_DE = SOURCE(name='LP',source_type='AUDIO', user_type='BOOK', part=1, language='de')
oko=7