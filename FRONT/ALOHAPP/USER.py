import platform
from typing import List, Set
from datetime import datetime
from WORDUSE import WordUse
from WORD import WORD
from SOURCE import SOURCE
from ENGINE.API_BIGAI_CLIENT import *
os_name = platform.system()



class USER:
    def __init__(self, native, langs, words_pd=15, time_pd=60, old_new=80):
        self.native = native
        self.langs = langs
        self.words_past: List[List[WordUse]] = [[] for _ in range(len(self.langs))]
        self.words_present: List[Set[str]] = []
        self.words_future: List[Set[str]] = []
        self.prompt_present: ''

        self.words_pd = words_pd
        self.time_pd = time_pd
        self.old_new = old_new
        self.sources: List[SOURCE] = []
        if os_name == 'Darwin':
            self.sources.append(SOURCE(source_type='AUDIO',user_type='BOOK',name='ASSIMIL',lang=self.langs[0][0],path=r'/Users/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/'+self.langs[0][0].upper()+'/SELF_LEARNING/ASSIMIL'))
        elif os_name == 'Linux':
            for lang in self.langs:
                self.sources.append(SOURCE(source_type='AUDIO', user_type='BOOK', name='BLONDYNA', lang=lang[0],
                                       path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/'+lang[0].upper()+'/SELF_LEARNING/BLONDYNA',part=0))
                self.sources.append(SOURCE(source_type='TEXT', user_type='FREQDICT', name='FREQDICT'+lang[0].upper(), lang=lang[0],
                                       path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/TEXT/FREQ_DICT_WORDS/' +
                                            lang[0].upper()))


    def Update_Words_Past(self,my_sentences, bot_sentences):
        for my_sentence in my_sentences:
            lang = detect_language(my_sentence)
            lang = lang['language_code']

            lemmatized = lemmatize_sentences([my_sentence], lang=lang)
            for word in lemmatized[0]:
                part_number = 0
                for part in self.sources[1].words_in_parts:
                    if word in part:
                        WORD_INSTANCE = WORD(word,lang,part_number)
                        WORDUSE_INSTANCE = WordUse(WORD_INSTANCE)
                        WORDUSE_INSTANCE.Say.append(datetime.now())
                        part_number = 0
                    else: part_number += 1



    def Update_Words_Present(self):
        for lang in self.langs:
            for source in self.sources:
                if lang[0] ==source.lang:
                    self.words_present = self.sources[0].get_words_from_n_parts(start=0, end=2)


    def Update_Words_Future(self):
        pass

    def Create_Prompt_From_Words_Present(self, lang='fr'):
        self.prompt_present = ', '.join(self.words_present)



    def Get_Progress(self):
        pass

    def Generate_Decks(self):
        pass

    def Popoulate_Audio(self):
        pass

    def Popoulate_Pics(self):
        pass