import pandas as pd
from PIL import Image
path = "../DATA/PIC/SENTENCES_DE_1000_V1_PIC/"

def get_pictures(sentence):
    pictures =[]

    for i in range(1,5):
        try:
            full_path = path+sentence+'_'+str(i)+'.png'
            img_PIL = Image.open(full_path)
            pictures.append(full_path)
        finally:
            print('No picture on :' +full_path)
    return pictures






