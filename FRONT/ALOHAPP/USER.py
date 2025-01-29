import platform
from typing import List, Set
from datetime import datetime
from ENGINE.API_BIGAI_CLIENT import *
from SOURCE import *
from WORD import *
os_name = platform.system()



class USER:
    def __init__(self, native, langs, langs_priority,hmt=2, words_pd=25, time_pd=60, old_new=80):
        self.native = native
        self.langs = langs
        self.langs_priority = langs_priority
        self.words_past: List[Set[WORD_Abstract]] = [set() for _ in range(len(langs))]
        self.words_present: List[Set[WORD_Abstract]] = [set() for _ in range(len(langs))]
        self.words_future: List[Set[WORD_Abstract]] = [set() for _ in range(len(langs))]
        self.prompt_present: ''

        self.words_pd = words_pd
        self.time_pd = time_pd
        self.old_new = old_new
        self.hmt = hmt
        self.sources: List[SOURCE] = []
        if os_name == 'Darwin':
            self.sources.append(SOURCE(source_type='AUDIO', user_type='BOOK', name='ASSIMIL', lang=self.langs[0][0], path=r'/Users/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/' + self.langs[0][0].upper() + '/SELF_LEARNING/ASSIMIL'))
        elif os_name == 'Linux':
            for lang in self.langs:
                self.sources.append(SOURCE(source_type='AUDIO', user_type='BOOK', name='ASSIMIL', lang=lang, native=native,
                                               path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/' + lang.upper() + '/SELF_LEARNING/ASSIMIL',
                                               part=-1))


    def Update_Words_Present(self,source_name,source_lang,start,end):
        for source in self.sources:
            if source.lang == source_lang and source.name == source_name:
                self.words_present = source.get_words_from_n_parts(start=start, end=end)


    def Upadete_Full_Words_Present(self,source_name,source_lang,start,end):
        for source in self.sources:
            if source.lang == source_lang and source.name == source_name:
                self.full_words_present = source.get_words_from_n_parts(start=start, end=end)



    def Update_Words_Future(self):
        pass

    def Create_Prompt_From_Words_Present(self, lang='ja'):
        self.prompt_present = ', '.join(self.words_present)



    def Get_Progress(self):
        pass

    def Generate_Decks(self):
        pass

    def Popoulate_Audio(self):
        pass

    def Popoulate_Pics(self):
        pass