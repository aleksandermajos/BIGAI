import flet as ft
from FRONT.ALOHAPP.CONTAINERS import *
from ENGINE.ALOHAPP_STT_VOICE_ASSISTANT import VoiceAssistant
import pickle
from USER import USER
from SOURCE import *


def main(page: ft.Page):
    page.title = "ALOHAPP"

    lang = 'zh'

    #page.user = USER(native='en',langs=['ja','zh'],langs_priority=['ja','zh'])
    #with open("USER_ALEX_ASSIMIL.pkl", "wb") as file:  # 'wb' means write in binary mode
        #pickle.dump(page.user, file)

    with open("USER_ALEX_ASSIMIL.pkl", 'rb') as file:  # 'rb' mode is for reading in binary
        page.user = pickle.load(file)


    page.user.Update_Words_Present(source_name='ASSIMIL',source_lang=lang,start=0,end=1)
    page.user.Create_Prompt_From_Words_Present(lang=lang)

    page.rows_full_words_button = generate_full_words_buttons_rows(user=page.user,lang=lang)
    page.words_column ,page.words_container = create_words_container(page.rows_full_words_button)

    page.conversation_column ,page.conversation_container = create_conversation_container()
    page.helper_column ,page.helper_container = create_helper_container()


    row = ft.Row(
        [page.conversation_container, page.helper_container, page.words_container], expand=True)
    page.add(row)
    page.theme_mode = ft.ThemeMode.DARK

    va = VoiceAssistant(main_page=page)
    try:
        va.record_and_transcribe()
    finally:
        va.audio.terminate()


ft.app(target=main)