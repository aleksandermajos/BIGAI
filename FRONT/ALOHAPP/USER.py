import platform
from typing import Set
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

    def prepare_words(self,lang):
        index = self.langs.index(lang)
        self.words_present[index] = Update_Words_Present(self,lang)
        self.prompt_present[index] = Create_Prompt_From_Words_Present(self,lang)
        self.words_future[index] = Update_Words_Future(self,lang)
