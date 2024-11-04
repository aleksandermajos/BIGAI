import datetime
from typing import List
from WORD import WORD

class WordUse:
    def __init__(self, word: WORD):
        self.word = word
        self.Write: List[datetime] = []
        self.Rewrite: List[datetime] = []
        self.Read: List[datetime] = []
        self.Hear: List[datetime] = []
        self.Repeat: List[datetime] = []
        self.Say: List[datetime] = []


