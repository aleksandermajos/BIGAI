from sudachipy import tokenizer
from sudachipy import dictionary

# Initialize the tokenizer
tokenizer_obj = dictionary.Dictionary().create()

# Sample Japanese sentences
text = "第2課ピカソ展見ましたか?何を?ピカソ展まだです。"

# Tokenize the text
tokens = tokenizer_obj.tokenize(text)

# Extract words
words = [token.surface() for token in tokens]

# Get unique words
unique_words = set(words)

# Display the unique words
for word in unique_words:
    print(word)