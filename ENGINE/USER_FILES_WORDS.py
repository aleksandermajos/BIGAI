import pandas as pd
path = "../../DATA/ALOHAPP/USER/"
import os
cwd = os.getcwd()


def load_de():
    de = pd.read_excel(path + 'DE/1000WORDSGERMAN.xlsx')
    de.WORD = de.WORD.str.replace('\d+', '')
    de = de[de["WORD"].str.contains("rank") == False]
    sen_de_1000 = pd.read_excel(path+'DE/SENTENCES_DE_1000_V1.xlsx')
    sen_de_1000_raw = pd.read_excel(path+'DE/SENTENCES_DE_1000_V1_RAW.xlsx')
    sen_de_en_1000 = pd.read_excel(path+'DE/SENTENCES_DE_EN_1000_V1.xlsx')
    sen_de_en_lemma_1000 = pd.read_excel(path + 'DE/SENTENCES_DE_EN_LEMMA_1000_V1.xlsx')
    sen_de_lemma_1000 = pd.read_excel(path+'DE/SENTENCES_DE_LEMMA_1000_V1.xlsx')

    user_dictionary = {"de": de, "sen_de_1000": sen_de_1000, "sen_de_1000_raw": sen_de_1000_raw, "sen_de_en_1000": sen_de_en_1000,"sen_de_en_lemma_1000": sen_de_en_lemma_1000,"sen_de_lemma_1000": sen_de_lemma_1000}
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
    sen_es_1000 = pd.read_excel(path+'ES/SENTENCES_ES_1000_V1.xlsx')
    #sen_es_1000_raw = pd.read_excel(path+'ES/SENTENCES_ES_1000_V1_RAW.xlsx')
    sen_es_en_1000 = pd.read_excel(path+'ES/SENTENCES_ES_EN_1000_V1.xlsx')
    sen_es_en_lemma_1000 = pd.read_excel(path + 'ES/SENTENCES_ES_EN_LEMMA_1000_V1.xlsx')
    sen_es_lemma_1000 = pd.read_excel(path+'ES/SENTENCES_ES_LEMMA_1000_V1.xlsx')

    user_dictionary = {"es": es, "sen_es_1000": sen_es_1000, "sen_es_en_1000": sen_es_en_1000,"sen_es_en_lemma_1000": sen_es_en_lemma_1000,"sen_es_lemma_1000": sen_es_lemma_1000}
    return user_dictionary

def load_fr():
    fr = pd.read_excel(path + 'FR/1000WORDSFRENCH.xlsx')
    fr.WORD = fr.WORD.str.replace('\d+', '')
    fr = fr[fr["WORD"].str.contains("rank") == False]
    sen_fr_1000 = pd.read_excel(path+'FR/SENTENCES_FR_1000_V1.xlsx')
    #sen_es_1000_raw = pd.read_excel(path+'ES/SENTENCES_ES_1000_V1_RAW.xlsx')
    sen_fr_en_1000 = pd.read_excel(path+'FR/SENTENCES_FR_EN_1000_V1.xlsx')
    sen_fr_en_lemma_1000 = pd.read_excel(path + 'FR/SENTENCES_FR_EN_LEMMA_1000_V1.xlsx')
    sen_fr_lemma_1000 = pd.read_excel(path+'FR/SENTENCES_FR_LEMMA_1000_V1.xlsx')

    user_dictionary = {"fr": fr, "sen_fr_1000": sen_fr_1000, "sen_fr_en_1000": sen_fr_en_1000,"sen_fr_en_lemma_1000": sen_fr_en_lemma_1000,"sen_fr_lemma_1000": sen_fr_lemma_1000}
    return user_dictionary

