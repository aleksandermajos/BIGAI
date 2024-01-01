import stanza
import spacy_stanza
import pandas as pd
Sentences_FR_1000 = pd.read_excel('SENTENCES_FR_1000_V1.xlsx')
#Sentences_ES_EN_1000 = pd.read_excel('SENTENCES_ES_EN_1000_V1.xlsx')
Sentences_FR_1000_list = Sentences_FR_1000["SENTENCE"].values.tolist()
#Sentences_ES_EN_1000_list = Sentences_ES_EN_1000["TRANSLATION"].values.tolist()



# Download the stanza model if necessary
#stanza.download("de")
#stanza.download('es')
#stanza.download('fr')
#stanza.download('en')

# Initialize the pipeline
#nlp_de = spacy_stanza.load_pipeline("de")
#nlp_en = spacy_stanza.load_pipeline('en')
nlp_es = spacy_stanza.load_pipeline('es')
nlp_fr = spacy_stanza.load_pipeline('fr')

sentences =[]
lemmas = []
oko=0
for sen_fr in Sentences_FR_1000_list:
    doc = nlp_fr(sen_fr)
    for token in doc:
        lemmas.append(token.lemma_)
    delimiter = ', '
    lemma = delimiter.join(lemmas)
    sentences.append(lemma)
    lemmas.clear()
    print(oko)
    oko = oko+1
df_lemma = pd.DataFrame(sentences,columns =['LEMMA'])
df_lemma.to_excel("SENTENCES_FR_LEMMA_1000_V1.xlsx", index=False)
oko=3




