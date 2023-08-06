from ENGINE.REC_MIC_PYAUDIO import Mic_Recorder
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
from ENGINE.TTS_DE_SILERO import TTS_DE
from ENGINE.SILERO_SSML import prepare_ssml
from ENGINE.UPGRADE_USER_FILES import upgrade_words_conv

from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
rec_path = path_beginning+"DATA/ALOHAPP/PHRASES/SPEAKING/"




def rec_button_clicked(e):
    if len(e.page.conversation_column.controls) >11:
        magic_row = e.page.conversation_column.controls[0]
        e.page.conversation_column.controls.clear()
        e.page.conversation_column.controls.append(magic_row)
    mic_recorder = Mic_Recorder(length=3,path=rec_path, file='flet.wav')
    mic_recorder.record()
    whisper_model = e.page.whisper_model
    whisper_model.transcribe_file(path=mic_recorder.path, file='flet.wav')
    whisper_model.last_transcribe = whisper_model.last_transcribe.replace('.', '')
    text_field = ft.TextField(
        label='YOUR SENTENCE',
        multiline=True,
        label_style=ft.TextStyle(color=ft.colors.YELLOW),
        color=ft.colors.YELLOW,
        value=whisper_model.last_transcribe,
        icon = ft.icons.EMOJI_EMOTIONS,
        smart_quotes_type = 'smart'
    )
    e.page.conversation_column.controls.append(text_field)
    e.page.update()


    lem = e.page.lemma(whisper_model.last_transcribe)
    indx_to_del = []
    words_buttons = e.page.words_buttons
    for token in lem:
        for indx in range(len(words_buttons)):
            if words_buttons[indx].text in token.lemma_:
                if len(words_buttons[indx].text) != len(token.lemma_):
                    if '|' in token.lemma_:
                        indx_to_del.append(indx)
                        continue
                else:
                    indx_to_del.append(indx)

    real_indx_to_del_list = []
    for indx in indx_to_del:
        element = words_buttons[indx].text
        real_index = e.page.repeat_words_full.index(element)
        real_indx_to_del_list.append(real_index)



    buttons_to_del =[]
    for i in real_indx_to_del_list:
        real_indx_to_del = i
        e.page.repeat_table[i] = e.page.repeat_table[i] - 1
        how_many_times = e.page.repeat_table_full[i]-e.page.repeat_table[i]
        upgrade_words_conv(how_many_times,e.page.repeat_words_full[real_indx_to_del], e.page.user_words_dictionary_de)
        if how_many_times >= e.page.repeat_table_full[i]:
            button_index = real_indx_to_del_list.index(i)
            button_index = indx_to_del[button_index]
            buttons_to_del.append(button_index)

    num_of_buttons = len(e.page.words_buttons)
    for i in buttons_to_del:
        if i< len(e.page.words_buttons):
            del e.page.words_buttons[i]


    bot_text = e.page.chat_bot.talk(whisper_model.last_transcribe+'.Antworten Sie in maximal drei Sätzen auf Deutsch')
    text_field = ft.TextField(
        label='BOT REPLY',
        multiline=True,
        label_style=ft.TextStyle(color=ft.colors.BLACK),
        color=ft.colors.BLACK,
        value=bot_text,
        smart_quotes_type='smart'

    )
    e.page.conversation_column.controls.append(text_field)
    e.page.update()
    tts_de = TTS_DE()
    bot_text = prepare_ssml(bot_text)
    tts_de.create_and_save(bot_text)


def mode_control_changed(e):
    pass