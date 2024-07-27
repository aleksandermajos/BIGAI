from dataclasses import dataclass
from typing import NamedTuple

class SOURCE(object):
    source_type = ['AUDIO', 'DECKS', 'EXEL', 'PIC', 'TATOEBA', 'TEXT', 'VIDEO']
    user_type = ['BOOK', 'SELFLEARNING', 'DECK', 'TATOEBA','NETFLIX', 'YT', 'TEXT','PIC', 'VIDEO', 'FREQDICT']
    part = 0
    language = ''
    words = []
    def __init__(self, source_type,user_type,part, language):
        self.source_type = source_type
        self.user_type = user_type
        self.part = part
        self.language = language
        if self.source_type not in SOURCE.source_type:
            print(f'Source type {self.source_type} not supported')

    def Extract_Words(self):
        pass


freq_dict_de = SOURCE(source_type='TEXT', user_type='FREQDICT', part=0, language='de')
oko=7