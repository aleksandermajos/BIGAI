import spacy
nlp = spacy.load("en_core_web_lg")

def get_tokens(text):
    doc = nlp(text)
    res = []
    for w in doc:
        res.append(w.text)
    return res


def get_root(text):
    doc = nlp(text)
    res = ''
    for sent in doc.sents:
        for w in sent:
            if w.dep_ == 'ROOT' or w.dep_ == 'pobj':
                res = w.text
    return res

def get_lemma(text):
    doc = nlp(text)
    res = {}
    for token in doc:
        res[token.text] = token.lemma_
    return res

sen ='this product integrates both libraries for downloading and applying patches'
lemm = get_lemma(sen)
root = get_root(sen)
tokens = get_tokens(sen)
oko=7