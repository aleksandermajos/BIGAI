import pykakasi

# Initialize pykakasi
kks = pykakasi.kakasi()

# Sample list of unique Japanese words
unique_words = ["見ました", "ピカソ展", "何を", "まだです"]

# Transliterate each word and display the original and its rōmaji equivalent
for word in unique_words:
    result = kks.convert(word)
    for item in result:
        print(f"Original: {item['orig']}, Rōmaji: {item['hepburn']}")

import cutlet

# Initialize cutlet
katsu = cutlet.Cutlet()

# Sample list of unique Japanese words
unique_words = ["見ました", "ピカソ展", "何を", "まだです"]
print('BREAK')
# Transliterate each word and display the original and its rōmaji equivalent
for word in unique_words:
    romaji = katsu.romaji(word)
    print(f"Original: {word}, Rōmaji: {romaji}")