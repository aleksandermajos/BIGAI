import spacy

nlp = spacy.blank("ja")
doc = nlp('第2課ピカソ展見ましたか?何を?ピカソ展まだです。')

# Extract lemma and simplify
lemmatized = []
for token in doc:
    if token.lemma_ not in ['ます', 'た']:  # Ignore auxiliary markers
        lemmatized.append(token.lemma_)
print(lemmatized)