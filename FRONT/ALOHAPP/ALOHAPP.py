import flet as ft
from FRONT.ALOHAPP.CONTAINERS import generate_words_buttons,create_words_container, create_conversation_container, create_helper_container
from ENGINE.ALOHAPP_STT_VOICE_ASSISTANT import VoiceAssistant
from USER import USER


def main(page: ft.Page):
    page.title = "ALOHAPP"
    page.Alex_user = USER(native='pl', langs=['fr', 'es'])

    page.words_buttons = generate_words_buttons(list(page.Alex_user.sources[0].words_in_parts[0]))
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