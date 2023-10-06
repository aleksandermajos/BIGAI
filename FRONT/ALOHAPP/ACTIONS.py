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
'''
from ENGINE.TTS_DE_SILERO import TTS_DE
from ENGINE.TTS_FR_SILERO import TTS_FR
from ENGINE.TTS_ES_SILERO import TTS_ES
'''
from ENGINE.SILERO_SSML import prepare_ssml

from ENGINE.TTS_ELEVENLABS_API import generate_and_play
from ENGINE.UPGRADE_USER_FILES import upgrade_words_conv

from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
rec_path = path_beginning+"DATA/ALOHAPP/PHRASES/SPEAKING/"


def rec_button_clicked(e):

    voice = 'Bella'

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
    if e.page.main_language=='de':
        '''
        tts_de = TTS_DE()
        last_transcibe = prepare_ssml(whisper_model.last_transcribe)
        tts_de.create_and_save(last_transcibe)
        
        generate_and_play(text=whisper_model.last_transcribe, voice=voice)
        '''
    if e.page.main_language=='fr':
        '''
        tts_fr = TTS_FR()
        last_transcibe = prepare_ssml(whisper_model.last_transcribe)
        tts_fr.create_and_save(last_transcibe)
        
        generate_and_play(text=whisper_model.last_transcribe, voice=voice)
        '''
    if e.page.main_language=='es':
        '''
        tts_es = TTS_ES()
        last_transcibe = prepare_ssml(whisper_model.last_transcribe)
        tts_es.create_and_save(last_transcibe)
        
        generate_and_play(text=whisper_model.last_transcribe, voice=voice)
        '''

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
        if e.page.main_language=='de': upgrade_words_conv('de',how_many_times,e.page.repeat_words_full[real_indx_to_del], e.page.user_words_dictionary_de)
        if e.page.main_language == 'fr': upgrade_words_conv('fr',how_many_times, e.page.repeat_words_full[real_indx_to_del],
                                                            e.page.user_words_dictionary_fr)
        if e.page.main_language == 'es': upgrade_words_conv('es',how_many_times, e.page.repeat_words_full[real_indx_to_del],
                                                            e.page.user_words_dictionary_es)
        if how_many_times >= e.page.repeat_table_full[i]:
            button_index = real_indx_to_del_list.index(i)
            button_index = indx_to_del[button_index]
            buttons_to_del.append(button_index)

    num_of_buttons = len(e.page.words_buttons)
    for i in buttons_to_del:
        if i< len(e.page.words_buttons):
            del e.page.words_buttons[i]


    if e.page.main_language=='de': bot_text = e.page.chat_bot.talk(whisper_model.last_transcribe+'Geben Sie Ihre Antwort in nur einem Satz auf Deutsch')
    if e.page.main_language == 'fr': bot_text = e.page.chat_bot.talk(
        whisper_model.last_transcribe + 'Donnez-moi la réponse en 3 phrases en français')
    if e.page.main_language == 'es': bot_text = e.page.chat_bot.talk(
        whisper_model.last_transcribe + 'Dame la respuesta en 3 frases en español')
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
    if e.page.main_language=='de':
        '''
        tts_de = TTS_DE()
        bot_text = prepare_ssml(bot_text)
        tts_de.create_and_save(bot_text)
        '''
        generate_and_play(text=bot_text, voice=voice)
    if e.page.main_language=='fr':
        '''
        tts_fr = TTS_FR()
        bot_text = prepare_ssml(bot_text)
        tts_fr.create_and_save(bot_text)
        '''
        generate_and_play(text=bot_text, voice=voice)
    if e.page.main_language=='es':
        '''
        tts_es = TTS_ES()
        bot_text = prepare_ssml(bot_text)
        tts_es.create_and_save(bot_text)
        '''
        generate_and_play(text=bot_text, voice=voice)


def mode_control_changed(e):
    pass