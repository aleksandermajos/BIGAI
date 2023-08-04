import pandas as pd
from pathlib import Path

path= "../../DATA/PHRASES/GENERATING/TATOEBA/"

def sentences_pairs(pair: tuple) -> pd.DataFrame:
    lang_A, lang_B = pair
    file_path = path+'EN-DE.tsv'
    file_path_Path = Path(file_path)
    if(file_path_Path.is_file()==True):
        df = pd.read_table(file_path)
        df.columns = [lang_A+' Sentence_ID', lang_A+' Sentence', lang_B+' Sentence_ID', lang_B+' Sentence']
        df = df.convert_dtypes()
    return df

def div_audio() -> bool:
    audio_file_path = path + 'audio.csv'
    audio_file_path_Path = Path(audio_file_path)
    if(audio_file_path_Path.is_file()==True):
        df = pd.read_csv(audio_file_path)
        df.columns=['Text']
        df[['Sentence_id','Audio_id','Username', 'License', 'Attribution_URL']] = df.Text.str.split("\t",expand=True)
        df.drop('Text', inplace=True, axis=1)
        df.to_csv(path+'audio_div.csv',index=False)

def get_audio(sentences: pd.DataFrame):
    audio_file = pd.read_csv(path+'audio_div.csv')
    for ind in sentences.index:
        print(sentences['EN Sentence_ID'][ind], sentences['EN Sentence'][ind],sentences['DE Sentence_ID'][ind], sentences['DE Sentence'][ind])
        if sentences['DE Sentence_ID'][ind] in audio_file.Sentence_id:
            indexes = audio_file.index[audio_file['Sentence_id'] == sentences['DE Sentence_ID'][ind]].tolist()
            print('EXIST')
    oko=5

pair = ('EN', 'DE')
sentences = sentences_pairs(pair)
get_audio(sentences)

