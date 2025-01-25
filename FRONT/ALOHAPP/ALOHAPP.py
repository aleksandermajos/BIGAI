import flet as ft
from FRONT.ALOHAPP.CONTAINERS import generate_words_buttons,create_words_container, create_conversation_container, create_helper_container
from ENGINE.ALOHAPP_STT_VOICE_ASSISTANT import VoiceAssistant
import pickle
from USER import USER


def main(page: ft.Page):
    page.title = "ALOHAPP"

    page.user = USER(native='pl',langs=['ja'],langs_priority=['ja'])
    with open("data.pkl", "wb") as file:  # 'wb' means write in binary mode
        pickle.dump(page.user, file)

    page.user.hmt = 4

    page.user.Update_Words_Present(source_name='ASSIMIL',source_lang='ja',start=0,end=0)
    page.user.Create_Prompt_From_Words_Present()

    page.words_buttons = generate_words_buttons(list(page.user.words_present))
    page.words_column ,page.words_container = create_words_container(page.words_buttons)
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