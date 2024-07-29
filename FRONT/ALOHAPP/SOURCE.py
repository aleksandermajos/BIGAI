from ENGINE.API_BIGAI_CLIENT import transcribe, tts_melo
import stanza
import spacy_stanza
from pydub import AudioSegment
import math


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

    def populate_words_text(self):
        pass

    def __init__(self, name, path, source_type,user_type,part, language):
        self.name = name
        self.path = path
        self.source_type = source_type
        self.user_type = user_type
        self.part = part
        self.language = language
        if self.source_type not in SOURCE.source_type:
            print(f'Source type {self.source_type} not supported')



    def populate_text(self):
        lemma = spacy_stanza.load_pipeline("de")
        text = transcribe(file_path=self.path, language='de')
        audio = AudioSegment.from_file(self.path)
        for segment in text['segments']:
            lem = lemma(segment['text'])
            segment_audio = audio[segment['start']*1000:segment['end']*1000]
            segment_audio.export(segment['text']+".mp3", format="mp3")
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
        oko=5





        oko=5

    def populate_audio(self):
        pass

path =r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/DE/LITTLE_PRINCE/03 Der Kleine Prinz - Kapitel 1.mp3'
LITTLEPRINCE_AUDIO_BOOK_PART1_DE = SOURCE(name='LITTLEPRINCE_AUDIO_BOOK_PART1_DE',path = path, source_type='AUDIO', user_type='BOOK', part=1, language='de')
LITTLEPRINCE_AUDIO_BOOK_PART1_DE.populate_text()
oko=6