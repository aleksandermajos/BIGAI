import copy


def prepare_ssml(text):
    splitted = text.split()
    splitted.insert(0, '<speak>')
    splitted.insert(len(splitted), '</speak>')
    result = ' '.join(splitted)
    return result


def add_space_between_words(text,sec):
    splitted = text.split()
    spl_copy = copy.deepcopy(splitted)

    extra =0
    for indx in range(len(spl_copy)-1):
        what_inserted = '<break time='+'"'+str(sec)+'s"/>'
        splitted.insert(indx+1+extra, what_inserted)
        extra = extra+1

    result = ' '.join(splitted)
    return result

def add_speed_to_text(text,list_start_stop_strength):
    splitted = text.split()
    extra =0
    for start_stop_strength in list_start_stop_strength:
        if start_stop_strength[2] == 0:
            str='<prosody rate="x-slow">'
        if start_stop_strength[2] == 1:
            str='<prosody rate="slow">'
        if start_stop_strength[2] == 2:
            str='<prosody rate="medium">'
        if start_stop_strength[2] == 3:
            str='<prosody rate="fast">'
        if start_stop_strength[2] == 4:
            str='<prosody rate="x-fast">'
        splitted.insert(start_stop_strength[0] + 1 + extra, str)
        extra = extra +1
        splitted.insert(start_stop_strength[1] + 1 + extra, "</prosody>")
        extra = extra + 1

    result = ' '.join(splitted)
    return result

def add_pitch_to_text(text,list_start_stop_strength):
    splitted = text.split()
    extra =0
    for start_stop_strength in list_start_stop_strength:
        if start_stop_strength[2] == 0:
            str='<prosody pitch="x-low">'
        if start_stop_strength[2] == 1:
            str='<prosody pitch="slow">'
        if start_stop_strength[2] == 2:
            str='<prosody pitch="medium">'
        if start_stop_strength[2] == 3:
            str='<prosody pitch="high">'
        if start_stop_strength[2] == 4:
            str='<prosody pitch="x-high">'
        splitted.insert(start_stop_strength[0] + 1 + extra, str)
        extra = extra +1
        splitted.insert(start_stop_strength[1] + 1 + extra, "</prosody>")
        extra = extra + 1

    result = ' '.join(splitted)
    return result






