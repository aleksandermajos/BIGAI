import pandas as pd
path = "../../DATA/WORDS/"
import os


def load_en():
    en = pd.read_excel(path+'EN/1000WORDSENGLISH.xlsx')
    en.WORD = en.WORD.str.replace('\d+', '')
    en = en[en["WORD"].str.contains("rank") == False]

    return en

def load_pl():
    pl = pd.read_excel(path+'PL/1000WORDSPOLISH.xlsx')
    pl.WORD = pl.WORD.str.replace('\d+', '')
    pl = pl[pl["WORD"].str.contains("rank") == False]

    return pl

def load_ru():
    ru = pd.read_excel(path+'RU/1000WORDSRUS.xlsx')
    ru.WORD = ru.WORD.str.replace('\d+', '')
    ru = ru[ru["WORD"].str.contains("rank") == False]

    return ru

def load_de():
    de = pd.read_excel(path+'DE/1000WORDSGERMAN.xlsx')
    de.WORD = de.WORD.str.replace('\d+', '')
    de = de[de["WORD"].str.contains("rank") == False]

    return de

def load_es():
    print(os.getcwd())
    full_path = path+'ES/1000WORDSSPANISH.xlsx'
    print(full_path)
    es = pd.read_excel(full_path)
    es.WORD = es.WORD.str.replace('\d+', '')
    es = es[es["WORD"].str.contains("rank") == False]

    return es

def load_fr():
    print(os.getcwd())
    fr = pd.read_excel(path+'FR/1000WORDSFRENCH.xlsx')
    fr.WORD = fr.WORD.str.replace('\d+', '')
    fr = fr[fr["WORD"].str.contains("rank") == False]

    return fr


