from FRONT.ALOHAPP.CONTAINERS import *
from ENGINE.ALOHAPP_STT_VOICE_ASSISTANT import VoiceAssistant
from SOURCE import *
from WORD import *
from USER import *


def main(page: ft.Page):
    page.title = "ALOHAPP"

    page.lang = 'ja'

    page.user = USER(native='en',langs=['ja','zh'],langs_priority=[10,8])
    with open("USER_ALEX_ASSIMIL_EXP.pkl", "wb") as file:  # 'wb' means write in binary mode
        pickle.dump(page.user, file)

    with open("USER_ALEX_ASSIMIL.pkl", 'rb') as file:  # 'rb' mode is for reading in binary
        page.user = pickle.load(file)

    page.user.prepare_words(lang=page.lang)

    page.rows_full_words_button = generate_full_words_buttons_rows(user=page.user,lang=page.lang)
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