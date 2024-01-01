import pandas as pd
from datetime import datetime
import itertools
from ENGINE.ALOHAPP_USER_FILES_WORDS import save_de_time, save_de


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

def upgrade_words_conv(lang,num_sentences, word, user_words_dictionary):
    if lang=='de': all_words = user_words_dictionary['de']
    if lang == 'fr': all_words = user_words_dictionary['fr']
    if lang == 'es': all_words = user_words_dictionary['es']
    if lang == 'it': all_words = user_words_dictionary['it']
    if lang == 'pt': all_words = user_words_dictionary['pt']
    if lang == 'ro': all_words = user_words_dictionary['ro']
    if lang == 'ca': all_words = user_words_dictionary['ca']
    if lang == 'pl': all_words = user_words_dictionary['pl']
    if lang == 'en': all_words = user_words_dictionary['en']
    if lang == 'ko': all_words = user_words_dictionary['ko']
    if lang == 'ja': all_words = user_words_dictionary['ja']
    if lang == 'ar': all_words = user_words_dictionary['ar']
    if lang == 'ru': all_words = user_words_dictionary['ru']
    if lang == 'zh': all_words = user_words_dictionary['zh']
    if lang == 'tr': all_words = user_words_dictionary['tr']
    if lang == 'sv': all_words = user_words_dictionary['sv']
    if lang == 'nl': all_words = user_words_dictionary['nl']
    if lang == 'da': all_words = user_words_dictionary['da']
    all_words = all_words.values.tolist()


    for word_pass_act in all_words:
        if word_pass_act[0] == word:
            word_pass_act[3] = num_sentences
            break


    if lang=='de': columns = user_words_dictionary['de'].columns
    if lang == 'fr': columns = user_words_dictionary['fr'].columns
    if lang == 'es': columns = user_words_dictionary['es'].columns
    if lang == 'it': columns = user_words_dictionary['it'].columns
    if lang == 'it': columns = user_words_dictionary['it'].columns
    if lang == 'ro': columns = user_words_dictionary['ro'].columns
    if lang == 'ca': columns = user_words_dictionary['ca'].columns
    if lang == 'pl': columns = user_words_dictionary['pl'].columns
    if lang == 'en': columns = user_words_dictionary['en'].columns
    if lang == 'ja': columns = user_words_dictionary['ja'].columns
    if lang == 'ko': columns = user_words_dictionary['ko'].columns
    if lang == 'ar': columns = user_words_dictionary['ar'].columns
    if lang == 'ru': columns = user_words_dictionary['ru'].columns
    if lang == 'zh': columns = user_words_dictionary['zh'].columns
    if lang == 'tr': columns = user_words_dictionary['tr'].columns
    if lang == 'sv': columns = user_words_dictionary['sv'].columns
    if lang == 'nl': columns = user_words_dictionary['nl'].columns
    if lang == 'da': columns = user_words_dictionary['da'].columns


    df = pd.DataFrame(all_words, columns=columns)
    df = df.fillna(0)
    df = df.astype({'PASSIVE': 'int'})
    df = df.astype({'ACTIVE': 'int'})
    df = df.astype({'CONV': 'int'})

    if lang == 'de':
        user_words_dictionary['de'] = df
        save_de(user_words_dictionary,key='de')
    if lang == 'fr':
        user_words_dictionary['fr'] = df
        save_de(user_words_dictionary,key='fr')
    if lang == 'es':
        user_words_dictionary['es'] = df
        save_de(user_words_dictionary,key='es')
    if lang == 'it':
        user_words_dictionary['it'] = df
        save_de(user_words_dictionary,key='it')
    if lang == 'pt':
        user_words_dictionary['pt'] = df
        save_de(user_words_dictionary,key='pt')
    if lang == 'ro':
        user_words_dictionary['ro'] = df
        save_de(user_words_dictionary,key='ro')
    if lang == 'ca':
        user_words_dictionary['ca'] = df
        save_de(user_words_dictionary,key='ca')
    if lang == 'pl':
        user_words_dictionary['pl'] = df
        save_de(user_words_dictionary,key='pl')
    if lang == 'en':
        user_words_dictionary['en'] = df
        save_de(user_words_dictionary,key='en')
    if lang == 'ja':
        user_words_dictionary['ja'] = df
        save_de(user_words_dictionary,key='ja')
    if lang == 'ko':
        user_words_dictionary['ko'] = df
        save_de(user_words_dictionary,key='ko')
    if lang == 'ar':
        user_words_dictionary['ar'] = df
        save_de(user_words_dictionary,key='ar')
    if lang == 'ru':
        user_words_dictionary['ru'] = df
        save_de(user_words_dictionary,key='ru')
    if lang == 'zh':
        user_words_dictionary['zh'] = df
        save_de(user_words_dictionary,key='zh')
    if lang == 'tr':
        user_words_dictionary['tr'] = df
        save_de(user_words_dictionary,key='tr')
    if lang == 'sv':
        user_words_dictionary['sv'] = df
        save_de(user_words_dictionary,key='sv')
    if lang == 'nl':
        user_words_dictionary['nl'] = df
        save_de(user_words_dictionary,key='nl')
    if lang == 'da':
        user_words_dictionary['da'] = df
        save_de(user_words_dictionary,key='da')










