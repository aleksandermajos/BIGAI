import pandas as pd

df_deu = pd.read_csv("deu_sentences.tsv",sep='\t')
df_deu.columns = ['ID', 'language', 'text']
df_deu = df_deu.drop(['ID'], axis=1)
df_fra = pd.read_csv("fra_sentences.tsv",sep='\t')
df_fra.columns = ['ID', 'language', 'text']
df_fra = df_fra.drop(['ID'], axis=1)
df_pol = pd.read_csv("pol_sentences.tsv",sep='\t')
df_pol.columns = ['ID', 'language', 'text']
df_pol = df_pol.drop(['ID'], axis=1)
df_spa = pd.read_csv("spa_sentences.tsv",sep='\t')
df_spa.columns = ['ID', 'language', 'text']
df_spa = df_spa.drop(['ID'], axis=1)

df_concat = pd.concat([df_deu[0:1000], df_fra[0:1000], df_pol[0:1000], df_spa[0:1000]], ignore_index=True)
df_concat.to_csv("data_lang.csv", index=False)
