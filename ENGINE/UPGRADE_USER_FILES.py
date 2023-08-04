import pandas as pd
from datetime import datetime
import itertools
from APP.DATA_OP.USER_FILES_WORDS import save_de_time, save_de


def upgrade_words_time_read(positions, user_words_time_dictionary, key='read'):
    if key=='read':
        de_time_read = user_words_time_dictionary['de_time_read']
    words = de_time_read.values.tolist()
    for inx in positions:
        element = words[inx]
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if isinstance(element[1], float):
            element[1] = ''
        element[1] = str(element[1]) + ','+dt_string
        words[inx]= element
    if key=='read':
        columns = user_words_time_dictionary['de_time_read'].columns
    df = pd.DataFrame(words, columns = columns)
    if key == 'read':
        user_words_time_dictionary['de_time_read'] = df
    save_de_time(user_words_time_dictionary,key='de_time_read')
    return user_words_time_dictionary

def upgrade_words_time_listen(sentence,user_words_dictionary,user_words_time_dictionary):
    sentences = user_words_dictionary['sen_de_1000']
    sentences = sentences.values.tolist()
    sentences = list(itertools.chain(*sentences))
    if sentence[0] == ' ':
        sentence = sentence[1:]
    index = sentences.index(sentence)
    words = user_words_dictionary['sen_de_lemma_1000']
    words = words.values.tolist()
    words = list(itertools.chain(*words))
    words = words[index]
    extra_words =[]
    words = words.split(',')
    if ('!' in words):
        words.remove(' !')
    if ('?' in words):
        words.remove('?')

    for word in words:
        if ('|' in word):
            extra = word.split('|')
            extra_words = extra
            words = words + extra_words





    de_time_listen = user_words_time_dictionary['de_time_listened']
    copy_of_de_time_listen = de_time_listen.copy()
    copy_of_de_time_listen2 = de_time_listen.copy()
    de_time_listen.drop('TIME', inplace=True, axis=1)
    words_time = de_time_listen.values.tolist()
    words_time = list(itertools.chain(*words_time))

    positions = []
    li=0
    for word in words:
        word = word.replace(' ','')
        if word.find('!') != -1: continue
        if word.find('?') != -1: continue
        if (word in words_time):
            positions.append(words_time.index(word))
        li = li+1

    copy_of_de_time_listen = copy_of_de_time_listen.values.tolist()
    for inx in positions:
        element = copy_of_de_time_listen[inx]
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if isinstance(element[1], float):
            element[1] = ''
        element[1] = str(element[1]) + ','+dt_string
        copy_of_de_time_listen[inx]= element


    columns = copy_of_de_time_listen2.columns
    df = pd.DataFrame(copy_of_de_time_listen, columns=columns)
    user_words_time_dictionary['de_time_listened'] = df

    save_de_time(user_words_time_dictionary,key='de_time_listened')
    return user_words_time_dictionary

def upgrade_words_time_repeat(sentence,user_words_dictionary,user_words_time_dictionary):
    sentences = user_words_dictionary['sen_de_1000']
    sentences = sentences.values.tolist()
    sentences = list(itertools.chain(*sentences))
    index = sentences.index(sentence)
    words = user_words_dictionary['sen_de_lemma_1000']
    words = words.values.tolist()
    words = list(itertools.chain(*words))
    words = words[index]
    words = words.split(',')
    if ('!' in words):
        words.remove(' !')
    if ('?' in words):
        words.remove('?')

    for word in words:
        if ('|' in word):
            extra = word.split('|')
            extra_words = extra
            words = words + extra_words

    de_time_listen = user_words_time_dictionary['de_time_repeat']
    copy_of_de_time_listen = de_time_listen.copy()
    copy_of_de_time_listen2 = de_time_listen.copy()
    de_time_listen.drop('TIME', inplace=True, axis=1)
    words_time = de_time_listen.values.tolist()
    words_time = list(itertools.chain(*words_time))

    positions = []
    li = 0
    for word in words:
        word = word.replace(' ', '')
        if word.find('!') != -1: continue
        if word.find('?') != -1: continue
        if (word in words_time):
            positions.append(words_time.index(word))
        li = li + 1

    copy_of_de_time_listen = copy_of_de_time_listen.values.tolist()
    for inx in positions:
        element = copy_of_de_time_listen[inx]
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if isinstance(element[1], float):
            element[1] = ''
        element[1] = str(element[1]) + ',' + dt_string
        copy_of_de_time_listen[inx] = element

    columns = copy_of_de_time_listen2.columns
    df = pd.DataFrame(copy_of_de_time_listen, columns=columns)
    user_words_time_dictionary['de_time_repeat'] = df

    save_de_time(user_words_time_dictionary,key='de_time_repeat')
    return user_words_time_dictionary

def upgrade_sen_time_read(sentences, user_words_time_dictionary):
    all_sentences = user_words_time_dictionary['sen_de_1000_time_read']
    all_sentences = all_sentences.values.tolist()
    all_sentences = list(itertools.chain(*all_sentences))
    n = 2
    del all_sentences[n - 1::n]

    indexes = []
    for cur_sent in all_sentences:
        for cur_new_sent in sentences:
            if cur_sent == cur_new_sent:
                indexes.append(all_sentences.index(cur_sent))

    all_sentences = user_words_time_dictionary['sen_de_1000_time_read']
    all_sentences = all_sentences.values.tolist()


    for inx in indexes:
        element = all_sentences[inx]
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if isinstance(element[1], float):
            element[1] = ''
        element[1] = str(element[1]) + ',' + dt_string
        all_sentences[inx] = element

    columns = user_words_time_dictionary['sen_de_1000_time_read'].columns
    df = pd.DataFrame(all_sentences, columns=columns)
    user_words_time_dictionary['sen_de_1000_time_read'] = df

    save_de_time(user_words_time_dictionary,key='sen_de_1000_time_read')

def upgrade_sen_time_listen(sentence,user_words_time_dictionary):
    all_sentences = user_words_time_dictionary['sen_de_1000_time_listened']
    all_sentences = all_sentences.values.tolist()
    all_sentences = list(itertools.chain(*all_sentences))
    n = 2
    del all_sentences[n - 1::n]

    indexes = []
    for cur_sent in all_sentences:
        if cur_sent == sentence:
                indexes.append(all_sentences.index(cur_sent))

    all_sentences = user_words_time_dictionary['sen_de_1000_time_listened']
    all_sentences = all_sentences.values.tolist()

    for inx in indexes:
        element = all_sentences[inx]
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if isinstance(element[1], float):
            element[1] = ''
        element[1] = str(element[1]) + ',' + dt_string
        all_sentences[inx] = element

    columns = user_words_time_dictionary['sen_de_1000_time_listened'].columns
    df = pd.DataFrame(all_sentences, columns=columns)
    user_words_time_dictionary['sen_de_1000_time_listened'] = df

    save_de_time(user_words_time_dictionary,key='sen_de_1000_time_listened')

def upgrade_sen_time_repeat(sentence,user_words_time_dictionary):
    all_sentences = user_words_time_dictionary['sen_de_1000_time_repeat']
    all_sentences = all_sentences.values.tolist()
    all_sentences = list(itertools.chain(*all_sentences))
    n = 2
    del all_sentences[n - 1::n]

    indexes = []
    for cur_sent in all_sentences:
        if cur_sent == sentence:
                indexes.append(all_sentences.index(cur_sent))

    all_sentences = user_words_time_dictionary['sen_de_1000_time_repeat']
    all_sentences = all_sentences.values.tolist()

    for inx in indexes:
        element = all_sentences[inx]
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if isinstance(element[1], float):
            element[1] = ''
        element[1] = str(element[1]) + ',' + dt_string
        all_sentences[inx] = element

    columns = user_words_time_dictionary['sen_de_1000_time_repeat'].columns
    df = pd.DataFrame(all_sentences, columns=columns)
    user_words_time_dictionary['sen_de_1000_time_repeat'] = df

    save_de_time(user_words_time_dictionary,key='sen_de_1000_time_repeat')

def upgrade_words_pass_act(num_sentences, word, user_words_dictionary, active):
    all_words = user_words_dictionary['de']
    all_words = all_words.values.tolist()

    if active == False:
        for word_pass_act in all_words:
            if word_pass_act[0] == word:
                word_pass_act[1] = num_sentences
                break
    else:
        for word_pass_act in all_words:
            if word_pass_act[0] == word:
                word_pass_act[2] = num_sentences
                break

    columns = user_words_dictionary['de'].columns
    df = pd.DataFrame(all_words, columns=columns)
    df = df.fillna(0)
    df = df.astype({'PASSIVE': 'int'})
    df = df.astype({'ACTIVE': 'int'})
    user_words_dictionary['de'] = df

    save_de(user_words_dictionary,key='de')

def upgrade_words_conv(num_sentences, word, user_words_dictionary):
    all_words = user_words_dictionary['de']
    all_words = all_words.values.tolist()


    for word_pass_act in all_words:
        if word_pass_act[0] == word:
            word_pass_act[3] = num_sentences
            break


    columns = user_words_dictionary['de'].columns
    df = pd.DataFrame(all_words, columns=columns)
    df = df.fillna(0)
    df = df.astype({'PASSIVE': 'int'})
    df = df.astype({'ACTIVE': 'int'})
    df = df.astype({'CONV': 'int'})

    user_words_dictionary['de'] = df

    save_de(user_words_dictionary,key='de')










