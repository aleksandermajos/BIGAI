import datetime
from typing import List, Tuple
from TIMELINE import Timeline
from WORDUSE import WordUse
from SOURCE import SOURCE


class USER:
    def __init__(self, native, langs, parts=1, words_pd=15, time_pd=60, old_new=80):
        self.native = native
        self.langs = langs
        self.parts = parts
        self.words_pd = words_pd
        self.time_pd = time_pd
        self.old_new = old_new
        self.sources: List[SOURCE] = []
        self.sources.append(SOURCE(source_type='AUDIO',user_type='BOOK',name='ASSIMIL',lang='fr',path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/FR/SELF_LEARNING/ASSIMIL'))


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