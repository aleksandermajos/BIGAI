import argparse
import flet as ft
from ENGINE.ALOHAPP_USER_FILES_WORDS import load_de, load_es, load_fr, load_it, load_pt, load_ro, load_ca, load_en, load_pl, load_ja, load_ko
from ENGINE.ALOHAPP_USER_FILES_WORDS import load_ar, load_ru, load_zh, load_tr, load_sv, load_da, load_nl, load_fa, load_he
from FRONT.ALOHAPP.CONTAINERS import generate_words_buttons,create_words_container, create_conversation_container
from ENGINE.ALOHAPP_GIVE_WORDS import give_words_conv
from ENGINE.ALOHAPP_OPENAI_CHATGPT import ChatGPT
from ENGINE.ALOHAPP_STT_WHISPER_LIVE import Whisper_live
import spacy_stanza
import sounddevice as sd


def main(page: ft.Page):
    page.main_language = 'ja'
    print(sd.query_devices())



    page.title = "CONVERSATIONS_AI"
    langs = ['de','en','es','fr','it','pl','pt','ca','ro','ar','ja','ko','ru','zh','tr','sv','nl','da', 'fa','he']
    tts = ['silero','ellabs','playht']
    api_hub = ['edenai']
    params = {
        "langs": langs,
        "tts": tts,
        'api_hub': api_hub,
        'words_number': 15,
        'word_times' : 4,
        'repeat_word' : 4
    }
    parser = argparse.ArgumentParser(description="", allow_abbrev=True)
    # Positional args
    parser.add_argument('-m', '--model', default='small', type=str, help="Whisper.cpp model, default to %(default)s")
    parser.add_argument('-ind', '--input_device', type=int, default=None,
                        help=f'Id of The input device (aka microphone)\n'
                             f'available devices {Whisper_live.available_devices()}')
    parser.add_argument('-st', '--silence_threshold', default=16,
                        help=f"he duration of silence after which the inference will be running, default to %(default)s")
    parser.add_argument('-bd', '--block_duration', default=30,
                        help=f"minimum time audio updates in ms, default to %(default)s")

    args = parser.parse_args()




    page.chat_bot = ChatGPT()

    if page.main_language == 'de': page.user_words_dictionary = load_de()
    if page.main_language == 'es': page.user_words_dictionary = load_es()
    if page.main_language == 'fr': page.user_words_dictionary = load_fr()
    if page.main_language == 'it': page.user_words_dictionary = load_it()
    if page.main_language == 'pt': page.user_words_dictionary = load_pt()
    if page.main_language == 'ro': page.user_words_dictionary = load_ro()
    if page.main_language == 'ca': page.user_words_dictionary = load_ca()
    if page.main_language == 'pl': page.user_words_dictionary = load_pl()
    if page.main_language == 'en': page.user_words_dictionary = load_en()
    if page.main_language == 'ko': page.user_words_dictionary = load_ko()
    if page.main_language == 'ja': page.user_words_dictionary = load_ja()
    if page.main_language == 'ar': page.user_words_dictionary = load_ar()
    if page.main_language == 'ru': page.user_words_dictionary = load_ru()
    if page.main_language == 'zh': page.user_words_dictionary = load_zh()
    if page.main_language == 'tr': page.user_words_dictionary = load_tr()
    if page.main_language == 'sv': page.user_words_dictionary = load_sv()
    if page.main_language == 'nl': page.user_words_dictionary = load_nl()
    if page.main_language == 'da': page.user_words_dictionary = load_da()
    if page.main_language == 'fa': page.user_words_dictionary = load_fa()
    if page.main_language == 'he': page.user_words_dictionary = load_he()

    page.lemma = spacy_stanza.load_pipeline(page.main_language)
    words_fin, words_pos = give_words_conv(page.user_words_dictionary,
                                           words_number=params['words_number'],
                                           word_times=params['word_times'],
                                           lang=page.main_language
                                           )

    page.words_buttons = generate_words_buttons((words_fin))
    page.words_column, page.words_container = create_words_container(page.words_buttons)
    page.conversation_column, page.conversation_container = create_conversation_container()
    page.repeat_table = [params['repeat_word']] * params['words_number']
    page.repeat_table_full = [params['repeat_word']] * params['words_number']
    page.repeat_words_full = words_fin


    row = ft.Row(
        [page.conversation_container, page.words_container], expand=True)
    page.add(row)
    page.theme_mode = ft.ThemeMode.DARK

    my_assistant = Whisper_live(main_page=page,
                                language=page.main_language,
                                model=args.model,
                                input_device=3,
                                silence_threshold=args.silence_threshold,
                                block_duration=args.block_duration,
                                commands_callback=print)
    my_assistant.start()

ft.app(target=main)
