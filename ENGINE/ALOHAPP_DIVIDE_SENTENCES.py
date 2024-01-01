import pandas as pd
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"DATA/ALOHA/PHRASES/GENERATING/GPT/"


def divide_raw(key='de',dif=1):

    dif=dif*1000
    Sentences = pd.read_excel(path+key.upper()+'/'+'SENTENCES_'+key.upper()+'_'+str(dif)+'_V1_RAW.xlsx')
    sentences_list = Sentences["Sentences"].values.tolist()

    orginal = []
    translation = []

    for sentence in sentences_list:
        x = sentence.split('(')
        org = x[0]
        if len(org)<2:
            print("OHO")
        if len(x)==2 and len(org)>2:
            if org[0:1].isnumeric(): org = org[3:]
            org = org.replace(".", "")
            if len(org)>1:
                if org[-1].isspace(): org = org[:-1]
            orginal.append(org)
            tran = x[1]
            tran = tran.replace(")", "")
            tran = tran.replace(".", "")
            translation.append(tran)

    df_sentence = pd.DataFrame(orginal,columns =['SENTENCE'])
    df_sentence.to_excel(path+key.upper()+'/'+'SENTENCES_'+key.upper()+'_'+str(dif)+'_V1.xlsx', index=False)
    df_translation = pd.DataFrame(translation,columns =['TRANSLATION'])
    df_translation.to_excel(path+key.upper()+'/'+'SENTENCES_'+key.upper()+'_'+'EN_'+str(dif)+'_V1.xlsx', index=False)
    '''
    df_all = pd.concat([df_sentence, df_translation], axis=1)
    df_all.to_excel("SENTENCES_DIV_EXTRA.xlsx", index=False)
    '''
"""
divide_raw(key='de',dif=7)
"""