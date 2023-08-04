import flet_core
from flet import (
    FilledButton,
    CircleBorder,
    ButtonStyle,
)
import flet as ft
from flet import (
    Slider,
    Switch,
    Text,
)
from FLET.ACTIONS import rec_button_clicked, mode_control_changed
def generate_words_buttons(list_of_words):
    list_of_buttons = []
    for word in list_of_words:
        list_of_buttons.append(ft.ElevatedButton(word))
    return list_of_buttons


def create_words_container(wb):
    words_column = ft.Column(wb, scroll=ft.ScrollMode.AUTO)
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
    rec_button = FilledButton("REC", style=ButtonStyle(shape=CircleBorder(), padding=10), on_click=rec_button_clicked)
    switch_button_control = Switch(label="CONTROL", on_change=mode_control_changed)
    row_conversation_column = ft.Row([switch_button_control, rec_button])
    conversation_column = ft.Column([],)
    conversation_column.controls.append(row_conversation_column)

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
