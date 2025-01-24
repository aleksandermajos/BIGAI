import fugashi

tagger = fugashi.Tagger()
sentence = '第2課ピカソ展見ましたか?何を?ピカソ展まだです。'
lemmatized = [word.feature.lemma or word.surface for word in tagger(sentence)]
print(lemmatized)