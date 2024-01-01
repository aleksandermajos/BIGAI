import flet as ft
from ENGINE.ALOHAPP_OPENAI_CHATGPT import ChatGPT
from FRONT.ALOHAPP.CONTAINERS import create_ocr_container


def main(page: ft.Page):
    page.title = "OCR"
    langs = ['ar','de','en','es','fr','it','jp','ko','pl','po','ru','zh']
    page.main_language = 'de'
    tts = ['silero','ellabs','playht']
    api_hub = ['edenai','together']
    params = {
        "langs": langs,
        "tts": tts,
        'api_hub': api_hub,
        'words_number': 15,
        'word_times' : 4,
        'repeat_word' : 4
    }
    page.chat_bot = ChatGPT()
    page.ocr_column, page.ocr_container = create_ocr_container()

    row = ft.Row(
        [page.ocr_container], expand=True)
    page.add(row)
    page.theme_mode = ft.ThemeMode.DARK


ft.app(target=main)