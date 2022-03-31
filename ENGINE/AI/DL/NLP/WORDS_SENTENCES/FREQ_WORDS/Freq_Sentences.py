import os
import re
import random
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from os import fspath
import pandas as pd
import requests
from bs4 import BeautifulSoup

dirty_words = pd.read_csv('ES.csv')
for i in range(len(dirty_words.index)-1):
    print(i)
    word = dirty_words.loc[i,'WORD']
    '''
    word = word.replace(" ", "")
    if len(word) < 2:
        continue
    '''
    request = "https://context.reverso.net/translation/spanish-english/"+word
    req = requests.get(request, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(req.text, 'html.parser')
    sentences = [x.text.strip() for x in soup.find_all('span', {'class':'text'}) if '\n' in x.text]
    if len(sentences) < 1:
        continue
    sentences_target = sentences[0::2]
    sorted_target = sorted(sentences_target, key=len)
    dirty_words.loc[i,'SEN_A']=sorted_target[0]
    dirty_words.loc[i,'SEN_A_TRAN']=sentences[sentences.index(sorted_target[0])+1]
    dirty_words.loc[i,'SEN_B']=sorted_target[1]
    dirty_words.loc[i,'SEN_B_TRAN']=sentences[sentences.index(sorted_target[1])+1]
    dirty_words.loc[i,'SEN_C']=sorted_target[2]
    dirty_words.loc[i,'SEN_C_TRAN']=sentences[sentences.index(sorted_target[2])+1]
dirty_words.to_csv('ES.csv')
