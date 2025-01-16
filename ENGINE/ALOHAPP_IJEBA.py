import jieba

# Sample Chinese sentences
sentences = [
    "我喜欢学习自然语言处理。",
    "自然语言处理是人工智能的一个分支。",
    "我正在学习用Python进行自然语言处理。"
]

# Combine sentences into a single text
text = ' '.join(sentences)

# Segment the text into words
words = jieba.lcut(text)

# Convert the list of words into a set to get unique words
unique_words = set(words)

# Display the unique words
for word in unique_words:
    print(word)
