import itertools
from APP.DATA_OP.UPGRADE_USER_FILES import upgrade_words_time_read, upgrade_words_time_listen, upgrade_words_time_repeat

def give_words(user_words_dictionary, user_words_time_dictionary,start, stop):
    de = user_words_dictionary['de']
    de_fin = de[['WORD']].iloc[start:stop]
    de_fin = de_fin.values.tolist()
    de_fin = list(itertools.chain(*de_fin))
    positions = []
    for i in range(start ,stop):
        positions.append(i)
    #upgrade_words_time_read(positions, user_words_time_dictionary, key='read')
    return de_fin, positions

def give_words_read_balanced(user_words_time_dictionary,words_number, new_percentage=100):
    new_words = int(words_number*new_percentage/100)
    old_words = words_number - new_words

    words = user_words_time_dictionary['de_time_read']
    words = words.values.tolist()

    if new_percentage==100:
        result =[]
        positions =[]
        index=0
        for cur_word in words:
            if isinstance(cur_word[1], float):
                result.append(cur_word[0])
                positions.append(index)
            index = index + 1
            if len(result)==new_words: break


    #upgrade_words_time_read(positions, user_words_time_dictionary, key='read')
    return result, positions

def give_words(user_words_dictionary, words_number, sen_number,lang='DE', new_percentage=100, active=False):
    new_words = int(words_number*new_percentage/100)
    old_words = words_number - new_words
    result =[]
    positions=[]

    if lang=='DE':words = user_words_dictionary['de']['WORD']
    if lang == 'ES': words = user_words_dictionary['es']['WORD']
    if lang == 'FR': words = user_words_dictionary['fr']['WORD']

    words = words.values.tolist()


    if active==False:
        if lang=='DE': passive = user_words_dictionary['de']['PASSIVE']
        if lang == 'ES': passive = user_words_dictionary['es']['PASSIVE']
        if lang == 'FR': passive = user_words_dictionary['fr']['PASSIVE']

        passive = passive.values.tolist()

        for indx in range(len(words)):
            if passive[indx] < sen_number:
                result.append(words[indx])
                positions.append(indx)
            if len(result) == words_number: break


    else:
        if lang=='DE':active = user_words_dictionary['de']['ACTIVE']
        if lang == 'ES': active = user_words_dictionary['es']['ACTIVE']
        if lang == 'FR': active = user_words_dictionary['fr']['ACTIVE']

        active = active.values.tolist()

        for indx in range(len(words)):
            if active[indx] < sen_number:
                result.append(words[indx])
                positions.append(indx)
            if len(result) == words_number: break




    return result, positions

def give_words_conv(user_words_dictionary, words_number, word_times, lang='DE'):
    result =[]
    positions=[]

    if lang=='DE':words = user_words_dictionary['de']['WORD']
    if lang == 'ES': words = user_words_dictionary['es']['WORD']
    if lang == 'FR': words = user_words_dictionary['fr']['WORD']

    words = words.values.tolist()



    if lang=='DE': conv = user_words_dictionary['de']['CONV']
    if lang == 'ES': conv = user_words_dictionary['es']['CONV']
    if lang == 'FR': conv = user_words_dictionary['fr']['CONV']

    conv = conv.values.tolist()

    for indx in range(len(words)):
        if conv[indx] < word_times:
            result.append(words[indx])
            positions.append(indx)
        if len(result) == words_number: break


    return result, positions