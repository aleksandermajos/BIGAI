from APP.DATA_OP.LOAD_WORDS import load_de, load_es, load_fr
import itertools
from OPENAI_CHATGPT import ChatGPT
import pandas as pd
import time


chat_bot = ChatGPT()

def give_words(start, stop,key='de'):
    if key=='de': words = load_de()
    if key=='fr': words = load_fr()
    if key=='es': words = load_es()

    words_fin = words[['WORD']].iloc[start:stop]
    words_fin = words_fin.values.tolist()
    words_fin = list(itertools.chain(*words_fin))
    return words_fin

def give_n_sentences_m_word(words_list,sentences=2,key='de'):
    wo = ''
    for num in range(len(words_list)):
        wo = wo + ' ' + words_list[num]+','
        if key=='de': text = 'Give me '+str(sentences)+' sentences with each word from list of words' + wo+ ' in German language with english translations'
        if key == 'es': text = 'Give me ' + str(
            sentences) + ' sentences with each word from list of words' + wo + ' in Spanish language with english translations'
        if key == 'fr': text = 'Give me ' + str(
            sentences) + ' sentences with each word from list of words' + wo + ' in French language with english translations'
        bot_text = chat_bot.talk(text)
        bot_text_list = bot_text.split("\n")
        bot_text_list = [x for x in bot_text_list if x != '']
    return bot_text_list

def generate_sentences_from_words(num_sent=6,key='es'):
    words = give_words(0,1001,key=key)
    n_sentences = []

    for slice in range(int(len(words)/num_sent)):

        words_slice = words[slice*num_sent:slice*num_sent + num_sent]
        n_sentences = n_sentences+ give_n_sentences_m_word(words_slice,sentences=num_sent,key='es')
        print(slice)
    df = pd.DataFrame(n_sentences,columns =['Sentences'])
    if key=='es': df.to_excel("SENTENCES_ES_1000_V1.xlsx", index=False)
    if key == 'de': df.to_excel("SENTENCES_DE_1000_V1.xlsx", index=False)
    if key == 'fr': df.to_excel("SENTENCES_fr_1000_V1.xlsx", index=False)

    return df

def generate_sentences_from_en(key='es'):
    n_sentences = []
    path = "../../DATA/WORDS/"
    en = pd.read_excel(path+'EN/SENTENCES_EN_1000_V1.xlsx')
    en.TRANSLATION = en.TRANSLATION.str.replace('\d+', '')
    en = en[en["TRANSLATION"].str.contains("rank") == False]
    en_list = en["TRANSLATION"].values.tolist()

    indx=0
    for tran in en_list:
        if key=='de': text = 'Give me translation from sentence "' + tran +'" to german language'
        if key == 'es': text = 'Give me translation from sentence "' + tran + '" to spanish language'
        if key == 'fr': text = 'Give me translation from sentence "' + tran + '" to french language'
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

    return en

generate_sentences_from_en(key='es')



