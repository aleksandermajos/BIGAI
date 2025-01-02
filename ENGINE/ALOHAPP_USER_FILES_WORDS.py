import pandas as pd
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'

path = path_beginning+"DATA/ALOHAPP/USER/"



def load_de():
    de = pd.read_excel(path + 'DE/1000WORDSGERMAN.xlsx')
    de.WORD = de.WORD.str.replace('\d+', '')
    de = de[de["WORD"].str.contains("rank") == False]
    """
    sen_de_1000 = pd.read_excel(path+'DE/SENTENCES_DE_1000_V1.xlsx')
    sen_de_1000_raw = pd.read_excel(path+'DE/SENTENCES_DE_1000_V1_RAW.xlsx')
    sen_de_en_1000 = pd.read_excel(path+'DE/SENTENCES_DE_EN_1000_V1.xlsx')
    sen_de_en_lemma_1000 = pd.read_excel(path + 'DE/SENTENCES_DE_EN_LEMMA_1000_V1.xlsx')
    sen_de_lemma_1000 = pd.read_excel(path+'DE/SENTENCES_DE_LEMMA_1000_V1.xlsx')
    """
    user_dictionary = {"de": de}
    return user_dictionary

def load_de_time():
    de_time_listened = pd.read_excel(path + 'DE/1000WORDSGERMAN_TIME_LISTENED.xlsx')
    de_time_listened.WORD = de_time_listened.WORD.str.replace('\d+', '')
    de_time_listened = de_time_listened[de_time_listened["WORD"].str.contains("rank") == False]

    de_time_read = pd.read_excel(path + 'DE/1000WORDSGERMAN_TIME_READ.xlsx')
    de_time_read.WORD = de_time_read.WORD.str.replace('\d+', '')
    de_time_read = de_time_read[de_time_read["WORD"].str.contains("rank") == False]

    de_time_repeat = pd.read_excel(path + 'DE/1000WORDSGERMAN_TIME_REPEAT.xlsx')
    de_time_repeat.WORD = de_time_repeat.WORD.str.replace('\d+', '')
    de_time_repeat = de_time_repeat[de_time_repeat["WORD"].str.contains("rank") == False]

    sen_de_1000_time_listened = pd.read_excel(path + 'DE/SENTENCES_DE_1000_V1_TIME_LISTENED.xlsx')
    sen_de_1000_time_listened.SENTENCE = sen_de_1000_time_listened.SENTENCE.str.replace('\d+', '')
    sen_de_1000_time_listened = sen_de_1000_time_listened[sen_de_1000_time_listened["SENTENCE"].str.contains("rank") == False]

    sen_de_1000_time_read = pd.read_excel(path + 'DE/SENTENCES_DE_1000_V1_TIME_READ.xlsx')
    sen_de_1000_time_read.SENTENCE = sen_de_1000_time_read.SENTENCE.str.replace('\d+', '')
    sen_de_1000_time_read = sen_de_1000_time_read[sen_de_1000_time_read["SENTENCE"].str.contains("rank") == False]

    sen_de_1000_time_repeat = pd.read_excel(path + 'DE/SENTENCES_DE_1000_V1_TIME_REPEAT.xlsx')
    sen_de_1000_time_repeat.SENTENCE = sen_de_1000_time_repeat.SENTENCE.str.replace('\d+', '')
    sen_de_1000_time_repeat = sen_de_1000_time_repeat[sen_de_1000_time_repeat["SENTENCE"].str.contains("rank") == False]

    user_dictionary_time = {"de_time_listened": de_time_listened, "de_time_read": de_time_read, "de_time_repeat": de_time_repeat, 'sen_de_1000_time_listened': sen_de_1000_time_listened, 'sen_de_1000_time_read': sen_de_1000_time_read, 'sen_de_1000_time_repeat': sen_de_1000_time_repeat}
    return user_dictionary_time

def save_de(user_words_dictionary,key='de'):
    if key == 'de': user_words_dictionary['de'].to_excel(path + 'DE/1000WORDSGERMAN.xlsx', index=False)
    if key == 'fr': user_words_dictionary['fr'].to_excel(path + 'FR/1000WORDSFRENCH.xlsx', index=False)
    if key == 'es': user_words_dictionary['es'].to_excel(path + 'ES/1000WORDSSPANISH.xlsx', index=False)
    if key == 'it': user_words_dictionary['it'].to_excel(path + 'IT/1000WORDSJAPANESE.xlsx', index=False)
    if key == 'pt': user_words_dictionary['pt'].to_excel(path + 'PT/1000WORDSPORTUGUESE.xlsx', index=False)
    if key == 'ro': user_words_dictionary['ro'].to_excel(path + 'RO/1000WORDSROMANIAN.xlsx', index=False)

def save_de_time(user_words_time_dictionary,key='de_time_listened'):
    if key == 'de_time_listened': user_words_time_dictionary['de_time_listened'].to_excel(path + 'DE/1000WORDSGERMAN_TIME_LISTENED.xlsx', index=False)
    if key == 'de_time_read': user_words_time_dictionary['de_time_read'].to_excel(path + 'DE/1000WORDSGERMAN_TIME_READ.xlsx', index=False)
    if key == 'de_time_repeat': user_words_time_dictionary['de_time_repeat'].to_excel(path + 'DE/1000WORDSGERMAN_TIME_REPEAT.xlsx', index=False)

    if key == 'sen_de_1000_time_listened': user_words_time_dictionary['sen_de_1000_time_listened'].to_excel(path + 'DE/SENTENCES_DE_1000_V1_TIME_LISTENED.xlsx', index=False)
    if key == 'sen_de_1000_time_read': user_words_time_dictionary['sen_de_1000_time_read'].to_excel(path + 'DE/SENTENCES_DE_1000_V1_TIME_READ.xlsx', index=False)
    if key == 'sen_de_1000_time_repeat': user_words_time_dictionary['sen_de_1000_time_repeat'].to_excel(path + 'DE/SENTENCES_DE_1000_V1_TIME_REPEAT.xlsx', index=False)

def load_es():
    es = pd.read_excel(path + 'ES/1000WORDSSPANISH.xlsx')
    es.WORD = es.WORD.str.replace('\d+', '')
    es = es[es["WORD"].str.contains("rank") == False]
    #sen_es_1000 = pd.read_excel(path+'ES/SENTENCES_ES_1000_V1.xlsx')
    #sen_es_1000_raw = pd.read_excel(path+'ES/SENTENCES_ES_1000_V1_RAW.xlsx')
    #sen_es_en_1000 = pd.read_excel(path+'ES/SENTENCES_ES_EN_1000_V1.xlsx')
    #sen_es_en_lemma_1000 = pd.read_excel(path + 'ES/SENTENCES_ES_EN_LEMMA_1000_V1.xlsx')
    #sen_es_lemma_1000 = pd.read_excel(path+'ES/SENTENCES_ES_LEMMA_1000_V1.xlsx')

    user_dictionary = {"es": es}
    return user_dictionary

def load_fr():
    fr = pd.read_excel(path + 'FR/1000WORDSFRENCH.xlsx')
    fr.WORD = fr.WORD.str.replace('\d+', '')
    fr = fr[fr["WORD"].str.contains("rank") == False]
    #sen_fr_1000 = pd.read_excel(path+'FR/SENTENCES_FR_1000_V1.xlsx')
    #sen_es_1000_raw = pd.read_excel(path+'ES/SENTENCES_ES_1000_V1_RAW.xlsx')
    #sen_fr_en_1000 = pd.read_excel(path+'FR/SENTENCES_FR_EN_1000_V1.xlsx')
    #sen_fr_en_lemma_1000 = pd.read_excel(path + 'FR/SENTENCES_FR_EN_LEMMA_1000_V1.xlsx')
    #sen_fr_lemma_1000 = pd.read_excel(path+'FR/SENTENCES_FR_LEMMA_1000_V1.xlsx')

    user_dictionary = {"fr": fr}
    return user_dictionary
def load_it():
    it = pd.read_excel(path + 'IT/1000WORDSJAPANESE.xlsx')
    it.WORD = it.WORD.str.replace('\d+', '')
    it = it[it["WORD"].str.contains("rank") == False]

    user_dictionary = {"it": it}
    return user_dictionary
def load_pt():
    pt = pd.read_excel(path + 'PT/1000WORDSPORTUGUESE.xlsx')
    pt.WORD = pt.WORD.str.replace('\d+', '')
    pt = pt[pt["WORD"].str.contains("rank") == False]

    user_dictionary = {"pt": pt}
    return user_dictionary
def load_ro():
    ro = pd.read_excel(path + 'RO/1000WORDSROMANIAN.xlsx')
    ro.WORD = ro.WORD.str.replace('\d+', '')
    ro = ro[ro["WORD"].str.contains("rank") == False]

    user_dictionary = {"ro": ro}
    return user_dictionary
def load_ca():
    ca = pd.read_excel(path + 'CA/1000WORDSCATALAN.xlsx')
    ca.WORD = ca.WORD.str.replace('\d+', '')
    ca = ca[ca["WORD"].str.contains("rank") == False]

    user_dictionary = {"ca": ca}
    return user_dictionary
def load_pl():
    pl = pd.read_excel(path + 'PL/1000WORDSPOLISH.xlsx')
    pl.WORD = pl.WORD.str.replace('\d+', '')
    pl = pl[pl["WORD"].str.contains("rank") == False]

    user_dictionary = {"pl": pl}
    return user_dictionary
def load_en():
    en = pd.read_excel(path + 'EN/1000WORDSENGLISH.xlsx')
    en.WORD = en.WORD.str.replace('\d+', '')
    en = en[en["WORD"].str.contains("rank") == False]

    user_dictionary = {"en": en}
    return user_dictionary
def load_ja():
    ja = pd.read_excel(path + 'JA/1000WORDSJAPANESE.xlsx')
    ja.WORD = ja.WORD.str.replace('\d+', '')
    ja = ja[ja["WORD"].str.contains("rank") == False]

    user_dictionary = {"ja": ja}
    return user_dictionary
def load_ko():
    ko = pd.read_excel(path + 'KO/1000WORDSKOREAN.xlsx')
    ko.WORD = ko.WORD.str.replace('\d+', '')
    ko = ko[ko["WORD"].str.contains("rank") == False]

    user_dictionary = {"ko": ko}
    return user_dictionary
def load_ar():
    ar = pd.read_excel(path + 'AR/1000WORDSARABIC.xlsx')
    ar.WORD = ar.WORD.str.replace('\d+', '')
    ar = ar[ar["WORD"].str.contains("rank") == False]

    user_dictionary = {"ar": ar}
    return user_dictionary
def load_ru():
    ru = pd.read_excel(path + 'RU/1000WORDSRUSSIAN.xlsx')
    ru.WORD = ru.WORD.str.replace('\d+', '')
    ru = ru[ru["WORD"].str.contains("rank") == False]

    user_dictionary = {"ru": ru}
    return user_dictionary
def load_zh():
    zh = pd.read_excel(path + 'ZH/1000WORDSCHINESE.xlsx')
    zh.WORD = zh.WORD.str.replace('\d+', '')
    zh = zh[zh["WORD"].str.contains("rank") == False]

    user_dictionary = {"zh": zh}
    return user_dictionary
def load_tr():
    tr = pd.read_excel(path + 'TR/1000WORDSTURKISCH.xlsx')
    tr.WORD = tr.WORD.str.replace('\d+', '')
    tr = tr[tr["WORD"].str.contains("rank") == False]

    user_dictionary = {"tr": tr}
    return user_dictionary
def load_sv():
    sv = pd.read_excel(path + 'SV/1000WORDSSWEDISH.xlsx')
    sv.WORD = sv.WORD.str.replace('\d+', '')
    sv = sv[sv["WORD"].str.contains("rank") == False]

    user_dictionary = {"sv": sv}
    return user_dictionary
def load_nl():
    nl = pd.read_excel(path + 'NL/1000WORDSDUTCH.xlsx')
    nl.WORD = nl.WORD.str.replace('\d+', '')
    nl = nl[nl["WORD"].str.contains("rank") == False]

    user_dictionary = {"nl": nl}
    return user_dictionary
def load_da():
    da = pd.read_excel(path + 'DA/1000WORDSDANISCH.xlsx')
    da.WORD = da.WORD.str.replace('\d+', '')
    da = da[da["WORD"].str.contains("rank") == False]

    user_dictionary = {"da": da}
    return user_dictionary
def load_fa():
    fa = pd.read_excel(path + 'FA/1000WORDSFARSI.xlsx')
    fa.WORD = fa.WORD.str.replace('\d+', '')
    fa = fa[fa["WORD"].str.contains("rank") == False]

    user_dictionary = {"fa": fa}
    return user_dictionary
def load_he():
    he = pd.read_excel(path + 'HE/1000WORDSHEBREW.xlsx')
    he.WORD = he.WORD.str.replace('\d+', '')
    he = he[he["WORD"].str.contains("rank") == False]

    user_dictionary = {"he": he}
    return user_dictionary

