import pandas as pd
import requests

def load_words():
    words = pd.read_excel('JAPANESE_N5.xlsx')
    return words


def save_words(df):
    df.to_excel('JAPANESE_N5_DIV.xlsx')


def rem_digits(df):
    df['WORD'] = df['WORD'].str.replace('\d+', '')
    return df

def rem_dot(df):
    df['WORD'] = df['WORD'].str.replace('.', '')
    return df

def rem_xa0(df):
    df['WORD'] = df['WORD'].str.replace('\xa0', ',')
    return df

def rem_double_coma(df):
    df['WORD'] = df['WORD'].str.replace(',,', ',')
    return df

def rem_slash(df):
    df['WORD'] = df['WORD'].str.replace('-', '')
    return df


words = load_words()
words = rem_digits(words)
words = rem_dot(words)
words = rem_xa0(words)
words = rem_double_coma(words)
words = rem_slash(words)
save_words(words)

#words[['WORD', 'KANA', 'MEANING']] = words['WORD'].str.split(',', expand=True)
oko=5