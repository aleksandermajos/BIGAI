import fasttext
import os
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/MODELS/TEXT/fasttext'
path = path_beginning+"/"

# Load the pre-trained model
model = fasttext.load_model(path+"lid.176.bin")


def Detect_language(text):
    predictions = model.predict(text, k=1)  # Top 1 prediction
    language_code = predictions[0][0].replace("__label__", "")
    confidence = predictions[1][0]
    print(f"Detected language: {language_code} with confidence {confidence}")
    return language_code