from flet import (
    FilledButton,
    CircleBorder,
    ButtonStyle,
)
import flet as ft
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)
from ENGINE.ALOHAPP_ACTIONS import pic_button_clicked
from datetime import datetime
import pickle


def pick_files_result(e: FilePickerResultEvent):
    selected_files.value = (
        ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
    )
    selected_files.update()


pick_files_dialog = FilePicker(on_result=pick_files_result)
selected_files = Text()

def generate_full_words_buttons_rows(user,lang):
    index = user.langs.index(lang)
    full_words = user.words_present[index]
    rows = []
    if lang=='ja':
        for word in full_words:
            buttons_row = [
                ft.ElevatedButton(word.text),
                ft.ElevatedButton(word.hepburn),
                ft.ElevatedButton(word.translate),
            ]
            row = Row(controls=buttons_row, wrap=False)
            rows.append(row)
        return rows
    if lang == 'zh':
        for word in full_words:
            buttons_row = [
                ft.ElevatedButton(word.text),
                ft.ElevatedButton(word.pinyin),
                ft.ElevatedButton(word.translate),
            ]
            row = Row(controls=buttons_row, wrap=False)
            rows.append(row)
        return rows



def generate_words_buttons(list_of_words):
    list_of_buttons = []
    for word in list_of_words:
        list_of_buttons.append(ft.ElevatedButton(word))
    return list_of_buttons


def delete_rows_words_buttons(page, known_words, lang):
    rows_words_buttons = page.words_column
    known_words = [item for sublist in known_words for item in sublist]

    index = page.user.langs.index(lang)
    words_present_lang = page.user.words_present[index]

    for word in words_present_lang:
        for known_word in known_words:
            if word.text==known_word:
                word.add_timestamp(datetime.now())
                if word.rfh:
                    print(word.rfh)
                    page.user.words_past[index].add(word)

                    indx_to_del_button = []
                    for word_button in known_words:
                        for indx in range(len(rows_words_buttons.controls)):
                            print(word_button)
                            if rows_words_buttons.controls[indx].controls[0].text == word_button:
                                indx_to_del_button.append(indx)

                    for i in sorted(indx_to_del_button, reverse=True):
                        del rows_words_buttons.controls[i]

                    with open("USER_ALEX_ASSIMIL.pkl", "wb") as file:  # 'wb' means write in binary mode
                        pickle.dump(page.user, file)

    return rows_words_buttons





def create_words_container(wr):
    words_column = ft.Column(wr, scroll=ft.ScrollMode.AUTO)
    words_container = ft.Container(
        words_column,
        margin=10,
        padding=10,
        bgcolor=ft.colors.CYAN_500,
        border_radius=10,
        expand=False,
        alignment=ft.alignment.top_center,
    )
    return words_column, words_container

def create_conversation_container():
    conversation_column = ft.Column([],)
    conversation_column.scroll = ft.ScrollMode.AUTO
    conversation_container = ft.Container(
        conversation_column,
        expand=True,
        margin=10,
        padding=10,
        bgcolor=ft.colors.CYAN_500,
        border_radius=10,
        alignment=ft.alignment.top_center,
    )
    return conversation_column, conversation_container

def create_helper_container():
    helper_column = ft.Column([],)
    helper_column.scroll = ft.ScrollMode.AUTO
    helper_container = ft.Container(
        helper_column,
        expand=True,
        margin=10,
        padding=10,
        bgcolor=ft.colors.CYAN_500,
        border_radius=10,
        alignment=ft.alignment.top_center,
    )
    return helper_column, helper_container