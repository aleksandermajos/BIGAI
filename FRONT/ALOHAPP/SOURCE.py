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
        text = transcribe(file_path=self.path, language='de')
        oko=5

    def populate_audio(self):
        pass
'''
text=transcribe(file_path=path, language='de')
'''
path =r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/DE/LITTLE_PRINCE/03 Der Kleine Prinz - Kapitel 1.mp3'
LITTLEPRINCE_AUDIO_BOOK_PART1_DE = SOURCE(name='LITTLEPRINCE_AUDIO_BOOK_PART1_DE',path = path, source_type='AUDIO', user_type='BOOK', part=1, language='de')
LITTLEPRINCE_AUDIO_BOOK_PART1_DE.populate_text()
oko=6