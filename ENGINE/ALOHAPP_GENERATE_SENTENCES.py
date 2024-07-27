from ALOHAPP_LOAD_WORDS import load_de, load_es, load_fr, load_it, load_en, load_pl
import itertools
from ALOHAPP_OPENAI_CHATGPT import ChatGPT
import time
import pandas as pd
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"DATA/ALOHA/PHRASES/GENERATING/GPT/"


chat_bot = ChatGPT()

def give_words(start, stop,dif=1,key='de'):
    if key=='de': words = load_de(dif)
    if key=='fr': words = load_fr(dif)
    if key=='es': words = load_es(dif)
    if key=='it': words = load_it(dif)
    if key=='en': words = load_en(dif)
    if key=='pl': words = load_pl(dif)

    words_fin = words[['WORD']].iloc[start:stop]
    words_fin = words_fin.values.tolist()
    words_fin = list(itertools.chain(*words_fin))
    return words_fin

def give_n_sentences_m_word(words_list,sentences=3,key='de'):
    wo = ''
    fin_list =[]
    for num in range(len(words_list)):
        wo = words_list[num]
        print(wo)
        if key=='de': text = 'Give me '+str(sentences)+' sentences with word ' + wo+ ' in German language with english translations'
        if key == 'es': text = 'Give me ' + str(
            sentences) + ' sentences with word ' + wo + ' in Spanish language with english translations'
        if key == 'fr': text = 'Give me ' + str(
            sentences) + ' sentences with word ' + wo + ' in French language with english translations'
        if key == 'it': text = 'Give me ' + str(
            sentences) + ' sentences with word ' + wo + ' in Italian language with english translations'
        if key == 'en': text = 'Give me ' + str(
            sentences) + ' sentences with word ' + wo + ' in English language with english translations'
        if key == 'pl': text = 'Give me ' + str(
            sentences) + ' sentences with word ' + wo + ' in Polish language with english translations'


        bot_text =''
        while bot_text=='':
            try:
                time.sleep(0.02)
                print(text)
                bot_text = chat_bot.talk(text)
                time.sleep(0.02)
                print(bot_text)
                bot_text_list = bot_text.split("\n")
                bot_text_list = [x for x in bot_text_list if x != '']
                fin_list.append(bot_text_list)
            except:
                time.sleep(0.05)
                bot_text = chat_bot.talk(text)
                print(bot_text)
                bot_text_list = bot_text.split("\n")
                bot_text_list = [x for x in bot_text_list if x != '']
                fin_list.append(bot_text_list)
                print("Something went wrong when calling OPENAI GPT")

    return fin_list

def generate_sentences_from_words(num_sent=2,dif=1,key='de'):
    words = give_words(0,1001,dif=dif,key=key)
    n_sentences = []

    for word in words:
        n_sentences = n_sentences+ give_n_sentences_m_word([word],sentences=num_sent,key=key)
        print(word)

    fin_sentences =[]
    for li in n_sentences:
        for sen in li:
            fin_sentences.append(sen)

    df = pd.DataFrame(fin_sentences,columns =['Sentences'])
    if key == 'de':
        if dif == 1: df.to_excel(path+'DE/'+"SENTENCES_DE_1000_V1_RAW.xlsx", index=False)
        if dif == 2: df.to_excel(path+'DE/'+"SENTENCES_DE_2000_V1_RAW.xlsx", index=False)
        if dif == 3: df.to_excel(path+'DE/'+"SENTENCES_DE_3000_V1_RAW.xlsx", index=False)
        if dif == 4: df.to_excel(path+'DE/'+"SENTENCES_DE_4000_V1_RAW.xlsx", index=False)
        if dif == 5: df.to_excel(path+'DE/'+"SENTENCES_DE_5000_V1_RAW.xlsx", index=False)
        if dif == 6: df.to_excel(path+'DE/'+"SENTENCES_DE_6000_V1_RAW.xlsx", index=False)
        if dif == 7: df.to_excel(path+'DE/'+"SENTENCES_DE_7000_V1_RAW.xlsx", index=False)
        if dif == 8: df.to_excel(path+'DE/'+"SENTENCES_DE_8000_V1_RAW.xlsx", index=False)

    if key=='es':
        if dif==1: df.to_excel("SENTENCES_ES_1000_V1_RAW.xlsx", index=False)
        if dif == 2: df.to_excel("SENTENCES_ES_2000_V1_RAW.xlsx", index=False)
        if dif == 3: df.to_excel("SENTENCES_ES_3000_V1_RAW.xlsx", index=False)
        if dif == 4: df.to_excel("SENTENCES_ES_4000_V1_RAW.xlsx", index=False)
        if dif == 5: df.to_excel("SENTENCES_ES_5000_V1_RAW.xlsx", index=False)
        if dif == 6: df.to_excel("SENTENCES_ES_6000_V1_RAW.xlsx", index=False)
        if dif == 7: df.to_excel("SENTENCES_ES_7000_V1_RAW.xlsx", index=False)
        if dif == 8: df.to_excel("SENTENCES_ES_8000_V1_RAW.xlsx", index=False)

    if key == 'fr':
        if dif==1: df.to_excel("SENTENCES_fr_1000_V1_RAW.xlsx", index=False)
        if dif == 2: df.to_excel("SENTENCES_fr_2000_V1_RAW.xlsx", index=False)
        if dif == 3: df.to_excel("SENTENCES_fr_3000_V1_RAW.xlsx", index=False)
        if dif == 4: df.to_excel("SENTENCES_fr_4000_V1_RAW.xlsx", index=False)
        if dif == 5: df.to_excel("SENTENCES_fr_5000_V1_RAW.xlsx", index=False)
        if dif == 6: df.to_excel("SENTENCES_fr_6000_V1_RAW.xlsx", index=False)
        if dif == 7: df.to_excel("SENTENCES_fr_7000_V1_RAW.xlsx", index=False)
        if dif == 8: df.to_excel("SENTENCES_fr_8000_V1_RAW.xlsx", index=False)

    if key == 'it':
        if dif==1: df.to_excel("SENTENCES_it_1000_V1_RAW.xlsx", index=False)
        if dif == 2: df.to_excel("SENTENCES_it_2000_V1_RAW.xlsx", index=False)
        if dif == 3: df.to_excel("SENTENCES_it_3000_V1_RAW.xlsx", index=False)
        if dif == 4: df.to_excel("SENTENCES_it_4000_V1_RAW.xlsx", index=False)
        if dif == 5: df.to_excel("SENTENCES_it_5000_V1_RAW.xlsx", index=False)
        if dif == 6: df.to_excel("SENTENCES_it_6000_V1_RAW.xlsx", index=False)
        if dif == 7: df.to_excel("SENTENCES_it_7000_V1_RAW.xlsx", index=False)
        if dif == 8: df.to_excel("SENTENCES_it_8000_V1_RAW.xlsx", index=False)

    if key == 'en':
        if dif==1: df.to_excel("SENTENCES_en_1000_V1_RAW.xlsx", index=False)
        if dif == 2: df.to_excel("SENTENCES_en_2000_V1_RAW.xlsx", index=False)
        if dif == 3: df.to_excel("SENTENCES_en_3000_V1_RAW.xlsx", index=False)
        if dif == 4: df.to_excel("SENTENCES_en_4000_V1_RAW.xlsx", index=False)
        if dif == 5: df.to_excel("SENTENCES_en_5000_V1_RAW.xlsx", index=False)
        if dif == 6: df.to_excel("SENTENCES_en_6000_V1_RAW.xlsx", index=False)
        if dif == 7: df.to_excel("SENTENCES_en_7000_V1_RAW.xlsx", index=False)
        if dif == 8: df.to_excel("SENTENCES_en_8000_V1_RAW.xlsx", index=False)

    if key == 'pl':
        if dif==1: df.to_excel("SENTENCES_pl_1000_V1_RAW.xlsx", index=False)
        if dif == 2: df.to_excel("SENTENCES_pl_2000_V1_RAW.xlsx", index=False)
        if dif == 3: df.to_excel("SENTENCES_pl_3000_V1_RAW.xlsx", index=False)
        if dif == 4: df.to_excel("SENTENCES_pl_4000_V1_RAW.xlsx", index=False)
        if dif == 5: df.to_excel("SENTENCES_pl_5000_V1_RAW.xlsx", index=False)
        if dif == 6: df.to_excel("SENTENCES_pl_6000_V1_RAW.xlsx", index=False)
        if dif == 7: df.to_excel("SENTENCES_pl_7000_V1_RAW.xlsx", index=False)
        if dif == 8: df.to_excel("SENTENCES_pl_8000_V1_RAW.xlsx", index=False)

    return df

def generate_sentences_from_en(key='de',dif=1):
    n_sentences = []
    path = "../../DATA/FREQ_DICT_WORDS/"
    if dif ==1: en = pd.read_excel(path+'EN/SENTENCES_EN_1000_V1.xlsx')
    if dif == 2: en = pd.read_excel(path + 'EN/SENTENCES_EN_2000_V1.xlsx')
    if dif == 3: en = pd.read_excel(path + 'EN/SENTENCES_EN_3000_V1.xlsx')
    if dif == 4: en = pd.read_excel(path + 'EN/SENTENCES_EN_4000_V1.xlsx')
    if dif == 5: en = pd.read_excel(path + 'EN/SENTENCES_EN_5000_V1.xlsx')
    if dif == 6: en = pd.read_excel(path + 'EN/SENTENCES_EN_6000_V1.xlsx')
    if dif == 7: en = pd.read_excel(path + 'EN/SENTENCES_EN_7000_V1.xlsx')
    if dif == 8: en = pd.read_excel(path + 'EN/SENTENCES_EN_8000_V1.xlsx')


    en.TRANSLATION = en.TRANSLATION.str.replace('\d+', '')
    en = en[en["TRANSLATION"].str.contains("rank") == False]
    en_list = en["TRANSLATION"].values.tolist()

    indx=0
    for tran in en_list:
        if key == 'de': text = 'Give me translation from sentence "' + tran +'" to german language'
        if key == 'es': text = 'Give me translation from sentence "' + tran + '" to spanish language'
        if key == 'fr': text = 'Give me translation from sentence "' + tran + '" to french language'
        if key == 'it': text = 'Give me translation from sentence "' + tran +'" to italian language'
        if key == 'en': text = 'Give me translation from sentence "' + tran + '" to english language'
        if key == 'pl': text = 'Give me translation from sentence "' + tran + '" to polish language'
        try:
            time.sleep(0.01)
            bot_text = chat_bot.talk(text)
        except:
            time.sleep(0.01)
            bot_text = chat_bot.talk(text)
        indx = indx+1
        bot_text=bot_text.replace("'", "")
        bot_text=bot_text.replace("\"", "")
        bot_text = bot_text.replace(".", "")
        n_sentences.append(bot_text)
        print(indx)
        print(bot_text)
    df = pd.DataFrame(n_sentences, columns=['Sentences'])
    if key == 'es': df.to_excel("SENTENCES_ES_1000_V1.xlsx", index=False)
    if key == 'de': df.to_excel("SENTENCES_DE_1000_V1.xlsx", index=False)
    if key == 'fr': df.to_excel("SENTENCES_fr_1000_V1.xlsx", index=False)
    if key == 'it': df.to_excel("SENTENCES_IT_1000_V1.xlsx", index=False)
    if key == 'en': df.to_excel("SENTENCES_EN_1000_V1.xlsx", index=False)
    if key == 'pl': df.to_excel("SENTENCES_PL_1000_V1.xlsx", index=False)

    return en


generate_sentences_from_words(num_sent=4,dif=2,key='de')
oko=5



