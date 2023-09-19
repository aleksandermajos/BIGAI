from GENERATE_SENTENCES import generate_sentences_from_words


key_list = ["de",'es','fr']

for key in key_list:
    for dif in range(2,8):
        generate_sentences_from_words(num_sent=10,dif=dif,key=key)