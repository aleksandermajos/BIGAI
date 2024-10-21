def get_lang_name_to_tts_melo(short):
    if short == 'en': return 'english'
    if short == 'de': return 'german'
    if short == 'fr': return 'french'
    if short == 'es': return 'spanish'
    if short == 'it': return 'italian'

def get_lang_name_to_nllb(lang):
    if lang == "jp": return 'jpn_Jpan'
    if lang == "en": return 'eng_Latn'
    if lang == "es": return 'spa_Latn'
    if lang == "fr": return 'fra_Latn'
    if lang == "de": return 'deu_Latn'
    if lang == "zh": return 'zho_Hans'
    if lang == "ko": return 'kor_Hang'