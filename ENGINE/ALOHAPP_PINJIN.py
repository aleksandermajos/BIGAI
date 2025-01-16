from pypinyin import pinyin, Style

# Sample list of unique Chinese words
unique_words = ["学习", "自然语言处理", "人工智能"]

# Convert each word to pinyin
for word in unique_words:
    pinyin_representation = pinyin(word, style=Style.TONE3)
    # Flatten the list of lists and join syllables
    pinyin_flat = ''.join([item for sublist in pinyin_representation for item in sublist])
    print(f"Original: {word}, Pinyin: {pinyin_flat}")