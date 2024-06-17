def get_lang_name_to_tts_melo(lang):
    if lang == "jp": return 'JP','JP'
    if lang == "en": return 'EN','EN-BR'
    if lang == "es": return 'ES','ES'
    if lang == "fr": return 'FR','FR'
    if lang == "de": return 'DE','DE'
    if lang == "zh": return 'ZH','ZH'
    if lang == "ko": return 'KR','KR'

def get_lang_name_to_nllb(lang):
    if lang == "jp": return 'jpn_Jpan'
    if lang == "en": return 'eng_Latn'
    if lang == "es": return 'spa_Latn'
    if lang == "fr": return 'fra_Latn'
    if lang == "de": return 'deu_Latn'
    if lang == "zh": return 'zho_Hans'
    if lang == "ko": return 'kor_Hang'