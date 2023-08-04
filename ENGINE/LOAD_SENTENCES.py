import pandas as pd
path = "../DATA/PHRASES/GENERATING/GPT/"


def load_de_gpt():
    sen_de_1000 = pd.read_excel(path+'DE/SENTENCES_DE_1000_V1.xlsx')
    sen_de_1000_raw = pd.read_excel(path+'DE/SENTENCES_DE_1000_V1_RAW.xlsx')
    sen_de_en_1000 = pd.read_excel(path+'DE/SENTENCES_DE_EN_1000_V1.xlsx')
    sen_de_en_lemma_1000 = pd.read_excel(path + 'DE/SENTENCES_DE_EN_LEMMA_1000_V1.xlsx')
    sen_de_lemma_1000 = pd.read_excel(path+'DE/SENTENCES_DE_LEMMA_1000_V1.xlsx')
    return sen_de_1000, sen_de_1000_raw, sen_de_en_1000, sen_de_en_lemma_1000, sen_de_lemma_1000

    return de



