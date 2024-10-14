import os
import platform
from typing import List, Tuple
from TIMELINE import Timeline
from WORDUSE import WordUse
from SOURCE import SOURCE
os_name = platform.system()


class USER:
    def __init__(self, native, langs, words_pd=15, time_pd=60, old_new=80):
        self.native = native
        self.langs = langs
        self.words_pd = words_pd
        self.time_pd = time_pd
        self.old_new = old_new
        self.sources: List[SOURCE] = []
        if os_name == 'Darwin':
            self.sources.append(SOURCE(source_type='AUDIO',user_type='BOOK',name='ASSIMIL',lang=self.langs[0][0],path=r'/Users/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/'+self.langs[0][0].upper()+'/SELF_LEARNING/ASSIMIL'))
        elif os_name == 'Linux':
            self.sources.append(SOURCE(source_type='AUDIO', user_type='BOOK', name='ASSIMIL', lang=self.langs[0][0],
                                       path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/'+self.langs[0][0].upper()+'/SELF_LEARNING/ASSIMIL'))
        self.new_user = True

    words: List[Tuple[Timeline, WordUse]] = []



    def Update_Sources(self):
        pass

    def Get_Progress(self):
        pass

    def Generate_Decks(self):
        pass

    def Popoulate_Audio(self):
        pass

    def Popoulate_Pics(self):
        pass