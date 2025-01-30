def get_lang_name_to_tts_melo(short):
    if short == 'en': return 'EN'
    if short == 'fr': return 'FR'
    if short == 'es': return 'ES'
    if short == 'it': return 'IT'
    if short == 'zh': return 'ZH'
    if short == 'ja': return 'JA'
    if short == 'ko': return 'KR'

def get_speaker_name_to_tts_melo(short):
    if short == 'EN': return 'EN-BR'
    if short == 'FR': return 'FR'
    if short == 'ES': return 'ES'
    if short == 'IT': return 'IT'
    if short == 'ZH': return 'ZH'
    if short == 'JA': return 'JA'
    if short == 'KR': return 'KR'

def get_lang_name_to_tts_kokoro(short):
    if short == 'ja': return 'Japanese'
    if short == 'zh': return 'Mandarin Chinese'

def get_speaker_name_to_tts_kokoro(short):
    if short == 'ja': return 'jf_alpha'
    if short == 'zh': return 'zm_yunjian'


def get_lang_name_to_nllb(lang):
    if lang == 'pl': return 'pol_Latn'
    if lang == "jp": return 'jpn_Jpan'
    if lang == "ja": return 'jpn_Jpan'
    if lang == "en": return 'eng_Latn'
    if lang == "English": return 'eng_Latn'
    if lang == "es": return 'spa_Latn'
    if lang == "fr": return 'fra_Latn'
    if lang == "French": return 'fra_Latn'
    if lang == "de": return 'deu_Latn'
    if lang == "zh": return 'zho_Hans'
    if lang == "ko": return 'kor_Hang'
