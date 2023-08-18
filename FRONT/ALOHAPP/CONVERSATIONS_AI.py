import flet as ft
import platform
from ENGINE.USER_FILES_WORDS import load_de, load_es, load_fr
from FRONT.ALOHAPP.CONTAINERS import generate_words_buttons,create_words_container, create_conversation_container
from ENGINE.GIVE_WORDS import give_words_conv
from ENGINE.OPENAI_CHATGPT import ChatGPT
from ENGINE.ASR_WHISPER import WhisperModel
import spacy
import spacy_stanza



def main(page: ft.Page):
    page.title = "CONVERSATIONS_AI"
    main_language = 'ES'



    words_number = 30
    word_times = 4
    repeat_word = 4



    def language_selection(main_language='DE'):
        if main_language == 'DE':
            page.user_words_dictionary_de = load_de()
            words_fin, words_pos = give_words_conv(page.user_words_dictionary_de,
                                                                    words_number=words_number,
                                                                    word_times=word_times,
                                                                    lang='DE'
                                                                   )
            page.lemma = spacy_stanza.load_pipeline("de")
            os = platform.system()
            if os == 'Darwin':
                page.whisper_model = WhisperModel(size='small', lang='german')
            if os == 'Windows' or os == 'Linux':
                page.whisper_model = WhisperModel(size='medium', lang='german')



        if main_language == 'FR':
            page.user_words_dictionary_fr = load_fr()
            words_fin, words_pos = give_words_conv(page.user_words_dictionary_fr,
                                                                    words_number=words_number,
                                                                    word_times=word_times,
                                                                    lang='FR'
                                                                   )
            page.lemma = spacy_stanza.load_pipeline("fr")
            os = platform.system()
            if os == 'Darwin':
                page.whisper_model = WhisperModel(size='small', lang='french')
            if os == 'Windows' or os == 'Linux':
                page.whisper_model = WhisperModel(size='medium', lang='french')

        if main_language == 'ES':
            page.user_words_dictionary_es = load_es()
            words_fin, words_pos = give_words_conv(page.user_words_dictionary_es,
                                                                    words_number=words_number,
                                                                    word_times=word_times,
                                                                    lang='ES'
                                                                   )
            page.lemma = spacy_stanza.load_pipeline("es")
            os = platform.system()
            if os == 'Darwin':
                page.whisper_model = WhisperModel(size='small', lang='spanish')
            if os == 'Windows' or os == 'Linux':
                page.whisper_model = WhisperModel(size='medium', lang='spanish')









        page.chat_bot = ChatGPT()





        page.words_buttons = generate_words_buttons((words_fin))
        page.words_column, page.words_container = create_words_container(page.words_buttons)
        page.conversation_column, page.conversation_container = create_conversation_container()
        page.repeat_table = [repeat_word] * words_number
        page.repeat_table_full = [repeat_word] * words_number
        page.repeat_words_full = words_fin




    language_selection(main_language)
    row = ft.Row(
        [page.conversation_container, page.words_container], expand=True)
    page.add(row)
    page.theme_mode = ft.ThemeMode.DARK

ft.app(target=main)


