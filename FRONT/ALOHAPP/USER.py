import datetime
from typing import List, Tuple
from TIMELINE import Timeline
from WORDUSE import WordUse
from SOURCE import SOURCE


class USER:
    def __init__(self, native, langs):
        self.native = native
        self.langs = langs

    words: List[Tuple[Timeline, WordUse]] = []
    sources: List[SOURCE] = []

    def Get_Progress(self):
        pass


    def Generate_Decks(self):
        pass

    def Popoulate_Audio(self):
        pass

    def Popoulate_Pics(self):
        pass