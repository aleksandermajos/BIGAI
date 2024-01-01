import itertools
from ENGINE.ALOHAPP_UPGRADE_USER_FILES import upgrade_words_time_read, upgrade_words_time_listen, upgrade_words_time_repeat

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

def give_words(user_words_dictionary, words_number, sen_number,lang='de', new_percentage=100, active=False):
    new_words = int(words_number*new_percentage/100)
    old_words = words_number - new_words
    result =[]
    positions=[]

    if lang=='de':words = user_words_dictionary['de']['WORD']
    if lang == 'es': words = user_words_dictionary['es']['WORD']
    if lang == 'fr': words = user_words_dictionary['fr']['WORD']

    words = words.values.tolist()


    if active==False:
        if lang=='de': passive = user_words_dictionary['de']['PASSIVE']
        if lang == 'es': passive = user_words_dictionary['es']['PASSIVE']
        if lang == 'fr': passive = user_words_dictionary['fr']['PASSIVE']

        passive = passive.values.tolist()

        for indx in range(len(words)):
            if passive[indx] < sen_number:
                result.append(words[indx])
                positions.append(indx)
            if len(result) == words_number: break


    else:
        if lang=='de':active = user_words_dictionary['de']['ACTIVE']
        if lang == 'es': active = user_words_dictionary['es']['ACTIVE']
        if lang == 'fr': active = user_words_dictionary['fr']['ACTIVE']

        active = active.values.tolist()

        for indx in range(len(words)):
            if active[indx] < sen_number:
                result.append(words[indx])
                positions.append(indx)
            if len(result) == words_number: break




    return result, positions

def give_words_conv(user_words_dictionary, words_number, word_times, lang='de'):
    result =[]
    positions=[]

    if lang=='de':words = user_words_dictionary['de']['WORD']
    if lang == 'es': words = user_words_dictionary['es']['WORD']
    if lang == 'fr': words = user_words_dictionary['fr']['WORD']
    if lang == 'it': words = user_words_dictionary['it']['WORD']
    if lang == 'pt': words = user_words_dictionary['pt']['WORD']
    if lang == 'ro': words = user_words_dictionary['ro']['WORD']
    if lang == 'ca': words = user_words_dictionary['ca']['WORD']
    if lang == 'pl': words = user_words_dictionary['pl']['WORD']
    if lang == 'en': words = user_words_dictionary['en']['WORD']
    if lang == 'ko': words = user_words_dictionary['ko']['WORD']
    if lang == 'ja': words = user_words_dictionary['ja']['WORD']
    if lang == 'ar': words = user_words_dictionary['ar']['WORD']
    if lang == 'ru': words = user_words_dictionary['ru']['WORD']
    if lang == 'zh': words = user_words_dictionary['zh']['WORD']
    if lang == 'tr': words = user_words_dictionary['tr']['WORD']
    if lang == 'sv': words = user_words_dictionary['sv']['WORD']
    if lang == 'da': words = user_words_dictionary['da']['WORD']
    if lang == 'nl': words = user_words_dictionary['nl']['WORD']
    if lang == 'fa': words = user_words_dictionary['fa']['WORD']
    if lang == 'he': words = user_words_dictionary['he']['WORD']

    words = words.values.tolist()



    if lang=='de': conv = user_words_dictionary['de']['CONV']
    if lang == 'es': conv = user_words_dictionary['es']['CONV']
    if lang == 'fr': conv = user_words_dictionary['fr']['CONV']
    if lang == 'it': conv = user_words_dictionary['it']['CONV']
    if lang == 'pt': conv = user_words_dictionary['pt']['CONV']
    if lang == 'ro': conv = user_words_dictionary['ro']['CONV']
    if lang == 'ca': conv = user_words_dictionary['ca']['CONV']
    if lang == 'pl': conv = user_words_dictionary['pl']['CONV']
    if lang == 'en': conv = user_words_dictionary['en']['CONV']
    if lang == 'ko': conv = user_words_dictionary['ko']['CONV']
    if lang == 'ja': conv = user_words_dictionary['ja']['CONV']
    if lang == 'ar': conv = user_words_dictionary['ar']['CONV']
    if lang == 'ru': conv = user_words_dictionary['ru']['CONV']
    if lang == 'zh': conv = user_words_dictionary['zh']['CONV']
    if lang == 'tr': conv = user_words_dictionary['tr']['CONV']
    if lang == 'sv': conv = user_words_dictionary['sv']['CONV']
    if lang == 'da': conv = user_words_dictionary['da']['CONV']
    if lang == 'nl': conv = user_words_dictionary['nl']['CONV']
    if lang == 'fa': conv = user_words_dictionary['fa']['CONV']
    if lang == 'he': conv = user_words_dictionary['he']['CONV']

    conv = conv.values.tolist()

    for indx in range(len(words)):
        if conv[indx] < word_times:
            result.append(words[indx])
            positions.append(indx)
        if len(result) == words_number: break


    return result, positions