import platform
from typing import List, Set
from datetime import datetime
from WORDUSE import WordUse
from WORD import WORD
from SOURCE import SOURCE
from ENGINE.API_BIGAI_CLIENT import *
os_name = platform.system()



class USER:
    def __init__(self, native, langs, langs_priority,hmt=2, words_pd=25, time_pd=60, old_new=80):
        self.native = native
        self.langs = langs
        self.langs_priority = langs_priority
        self.words_past: List[List[WordUse]] = [[] for _ in range(len(self.langs))]
        self.words_present: List[Set[str]] = []
        self.words_future: List[Set[str]] = []
        self.prompt_present: ''

        self.words_pd = words_pd
        self.time_pd = time_pd
        self.old_new = old_new
        self.hmt = hmt
        self.sources: List[SOURCE] = []
        if os_name == 'Darwin':
            self.sources.append(SOURCE(source_type='AUDIO',user_type='BOOK',name='ASSIMIL',lang=self.langs[0][0],path=r'/Users/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/'+self.langs[0][0].upper()+'/SELF_LEARNING/ASSIMIL'))
        elif os_name == 'Linux':
            for lang in self.langs:
                self.sources.append(
                    SOURCE(source_type='TEXT', user_type='FREQDICT', name='FREQDICT' + lang.upper(), lang=lang,
                           path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/TEXT/FREQ_DICT_WORDS/' +lang.upper()))
                self.sources.append(SOURCE(source_type='AUDIO', user_type='BOOK', name='BLONDYNA', lang=lang,
                                       path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/'+lang.upper()+'/SELF_LEARNING/BLONDYNA',part=-1))
                self.sources.append(SOURCE(source_type='AUDIO', user_type='BOOK', name='ASSIMIL', lang=lang,
                                           path=r'/home/bigai/PycharmProjects/BIGAI/DATA/ALOHAPP/AUDIO/BOOK/' + lang.upper() + '/SELF_LEARNING/ASSIMIL',
                                           part=-1))



    def Update_Words_Past(self,my_sentences, my_sentences_languages, bot_sentences):
        known_words = []
        lang = my_sentences_languages[-1]
        lang_pos =  self.langs.index(lang)
        curr_sentence = my_sentences[-1]
        lemmatized = lemmatize_sentences([curr_sentence], lang=lang)
        lemmatized_sentence = lemmatized[-1]

        for word in lemmatized_sentence:
            for source in self.sources:
                if source.lang==lang and 'FREQDICT' in source.name:
                    for thousand, part in enumerate(source.words_in_parts):
                        if word in part:
                            Filled = False
                            for curr_word_use in self.words_past[lang_pos]:
                                Filled = False
                                if curr_word_use.word.word==word:
                                    curr_word_use.Say.append(datetime.now())
                                    if len(curr_word_use.Say) == self.hmt:
                                        known_words.append(word)
                                    Filled = True
                                    break
                            if not Filled:
                                get_score = part.items.index(word)+thousand*1000
                                WORD_INSTANCE = WORD(word, lang, get_score)
                                WORDUSE_INSTANCE = WordUse(WORD_INSTANCE)
                                WORDUSE_INSTANCE.Say.append(datetime.now())
                                self.words_past[lang_pos].append(WORDUSE_INSTANCE)
                                break
                            if not self.words_past[lang_pos]:
                                get_score = part.items.index(word) + thousand * 1000
                                WORD_INSTANCE = WORD(word, lang, get_score)
                                WORDUSE_INSTANCE = WordUse(WORD_INSTANCE)
                                WORDUSE_INSTANCE.Say.append(datetime.now())
                                self.words_past[lang_pos].append(WORDUSE_INSTANCE)
                                break
        return known_words




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