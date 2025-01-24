from sudachipy import tokenizer
from sudachipy import dictionary

# Initialize the tokenizer
tokenizer_obj = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.C  # "C" mode for keeping compound words intact

def get_unique_lemmas(sentence):
    # Tokenize and lemmatize
    tokens = tokenizer_obj.tokenize(sentence, mode)
    # Extract dictionary forms and filter duplicates
    unique_lemmas = {token.dictionary_form() for token in tokens}
    return unique_lemmas

# Input sentence
sentence = "第2課ピカソ展見ましたか?何を?ピカソ展まだです。"

# Get unique dictionary forms
unique_words = get_unique_lemmas(sentence)

# Print unique words
print(unique_words)