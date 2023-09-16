import pandas as pd
from pathlib import Path
import os
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"DATA/ALOHAPP/WORDS/"



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

def load_de(dif=1):
    if dif == 1: de = pd.read_excel(path+'DE/1000WORDSGERMAN.xlsx')
    if dif == 2: de = pd.read_excel(path + 'DE/2000WORDSGERMAN.xlsx')
    if dif == 3: de = pd.read_excel(path + 'DE/3000WORDSGERMAN.xlsx')
    if dif == 4: de = pd.read_excel(path + 'DE/4000WORDSGERMAN.xlsx')
    if dif == 5: de = pd.read_excel(path + 'DE/5000WORDSGERMAN.xlsx')
    if dif == 6: de = pd.read_excel(path + 'DE/6000WORDSGERMAN.xlsx')
    if dif == 7: de = pd.read_excel(path + 'DE/7000WORDSGERMAN.xlsx')
    if dif == 8: de = pd.read_excel(path + 'DE/8000WORDSGERMAN.xlsx')






    de.WORD = de.WORD.str.replace('\d+', '')
    de = de[de["WORD"].str.contains("rank") == False]

    return de

def load_es(dif=1):
    print(os.getcwd())


    if dif==1: full_path = path+'ES/1000WORDSSPANISH.xlsx'
    if dif == 2: full_path = path + 'ES/2000WORDSSPANISH.xlsx'
    if dif == 3: full_path = path + 'ES/3000WORDSSPANISH.xlsx'
    if dif == 4: full_path = path + 'ES/4000WORDSSPANISH.xlsx'
    if dif == 5: full_path = path + 'ES/5000WORDSSPANISH.xlsx'
    if dif == 6: full_path = path + 'ES/6000WORDSSPANISH.xlsx'
    if dif == 7: full_path = path + 'ES/7000WORDSSPANISH.xlsx'
    if dif == 8: full_path = path + 'ES/8000WORDSSPANISH.xlsx'
    print(full_path)
    es = pd.read_excel(full_path)
    es.WORD = es.WORD.str.replace('\d+', '')
    es = es[es["WORD"].str.contains("rank") == False]

    return es

def load_fr(dif=1):
    print(os.getcwd())
    if dif==1:fr = pd.read_excel(path+'FR/1000WORDSFRENCH.xlsx')
    if dif == 2: fr = pd.read_excel(path + 'FR/2000WORDSFRENCH.xlsx')
    if dif == 3: fr = pd.read_excel(path + 'FR/3000WORDSFRENCH.xlsx')
    if dif == 4: fr = pd.read_excel(path + 'FR/4000WORDSFRENCH.xlsx')
    if dif == 5: fr = pd.read_excel(path + 'FR/5000WORDSFRENCH.xlsx')
    if dif == 6: fr = pd.read_excel(path + 'FR/6000WORDSFRENCH.xlsx')
    if dif == 7: fr = pd.read_excel(path + 'FR/7000WORDSFRENCH.xlsx')
    if dif == 8: fr = pd.read_excel(path + 'FR/8000WORDSFRENCH.xlsx')
    fr.WORD = fr.WORD.str.replace('\d+', '')
    fr = fr[fr["WORD"].str.contains("rank") == False]

    return fr


