import platform
from typing import List, Set
from datetime import datetime
from ENGINE.API_BIGAI_CLIENT import *
from SOURCE import *
from WORD import *
os_name = platform.system()



class USER:
    def __init__(self, native, langs, langs_priority,hmt=2, words_pd=25, time_pd=60, old_new=80, name='ALEX_ASSIMIL'):
        self.native = native
        self.langs = langs
        self.langs_priority = langs_priority
        self.words_past: List[Set[WORD_Abstract]] = [set() for _ in range(len(langs))]
        self.words_present: List[Set[WORD_Abstract]] = [set() for _ in range(len(langs))]
        self.words_future: List[Set[WORD_Abstract]] = [set() for _ in range(len(langs))]
        self.prompt_present: List[str] = ['' for _ in range(len(langs))]
        self.sources: List[Set[SOURCE]] = [set() for _ in range(len(langs))]

        self.words_pd = words_pd
        self.time_pd = time_pd
        self.old_new = old_new
        self.hmt = hmt

        for lang in self.langs:
            index = self.langs.index(lang)
            self.sources[index].add(SOURCE(source_type='AUDIO', user_type='BOOK', name='ASSIMIL', lang=lang, native=native,
                       path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/' + lang.upper() + '/SELF_LEARNING/ASSIMIL',
                       part=-1))


    def Update_Words_Present(self,source_name,source_lang,start,end):
        for source_set in self.sources:
                for source in source_set:
                    if source.name == source_name and source.lang == source_lang:
                        WORDS = source.get_words_from_n_parts(start=start, end=end)
                        index = self.langs.index(source_lang)
                        self.words_present[index].update(WORDS)

    def Upadete_Full_Words_Present(self,source_name,source_lang,start,end):
        for source in self.sources:
            if source.lang == source_lang and source.name == source_name:
                self.full_words_present = source.get_words_from_n_parts(start=start, end=end)



    def Update_Words_Future(self):
        pass

    def Create_Prompt_From_Words_Present(self, lang='ja'):
        index = self.langs.index(lang)
        self.prompt_present[index] = self.words_present[index]
        self.prompt_present[index] = ','.join(word.original for word in self.prompt_present[index])

    def Get_Progress(self):
        pass

    def Generate_Decks(self):
        pass

    def Popoulate_Audio(self):
        pass

    def Popoulate_Pics(self):
        pass