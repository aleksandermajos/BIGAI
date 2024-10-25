import platform
from typing import List, Set
from WORDUSE import WordUse
from SOURCE import SOURCE
from ENGINE.API_BIGAI_CLIENT import *
os_name = platform.system()



class USER:
    def __init__(self, native, langs, words_pd=15, time_pd=60, old_new=80):
        self.native = native
        self.langs = langs
        self.words_past: List[List[WordUse]] = [[] for _ in range(len(self.langs)+1)]
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
            self.sources.append(SOURCE(source_type='AUDIO', user_type='BOOK', name='ASSIMIL', lang=self.langs[0][0],
                                       path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/'+self.langs[0][0].upper()+'/SELF_LEARNING/ASSIMIL'))
            self.sources.append(SOURCE(source_type='TEXT', user_type='FREQDICT', name='FREQDICT'+self.langs[0][0].upper(), lang=self.langs[0][0],
                                       path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/TEXT/FREQ_DICT_WORDS/' +
                                            self.langs[0][0].upper()))


    def Update_Words_Past(self,my_sentences, bot_sentences):
        for my_sentence in my_sentences:
            lang = detect_language(my_sentence)
            lang = lang['language_code']
            list_of_lang = [tuple_[0] for tuple_ in self.langs]
            position = list_of_lang.index(lang)
            if position:
                pass
            else:
                pass
            if lang==self.native:
                pass


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