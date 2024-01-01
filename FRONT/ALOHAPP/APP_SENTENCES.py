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
import itertools
from functools import partial
import platform
from thefuzz import fuzz

from ENGINE.ALOHAPP_USER_FILES_WORDS import load_de, load_es, load_fr
from ENGINE.ALOHAPP_GIVE_WORDS import give_words
from ENGINE.ALOHAPP_UPGRADE_USER_FILES import upgrade_words_pass_act
from ENGINE.ALOHAPP_LOAD_PICS import get_pictures
from ENGINE.ALOHAPP_OPENAI_CHATGPT import ChatGPT
from ENGINE.ALOHAPP_REC_MIC_PYAUDIO import Mic_Recorder
from ENGINE.STT_WHISPER import WhisperModel
from ENGINE.TTS_DE_SILERO import TTS_DE
from ENGINE.TTS_EN_SILERO import TTS_EN
from ENGINE.TTS_ES_SILERO import TTS_ES
from ENGINE.TTS_FR_SILERO import TTS_FR
from ENGINE.TTS_SSML_SILERO import prepare_ssml, add_space_between_words

rec_path = "../../DATA/ALOHA/PHRASES/SPEAKING/"

words_number = 10
sen_number_pass = 8
sen_number_act = 8

main_language= 'DE'
whisper_model = ''
words_buttons = ''

simil_edge = 90
new_words_percentage = 100


#user_words_dictionary_es = load_es()
#user_words_dictionary_fr = load_fr()
user_words_dictionary_de = load_de()


chat_bot = ChatGPT()


def main(page: ft.Page):
    page.title = "SENTENCES"

    def mode_pas_act_changed(e):
        main_language = Controls_column.controls[13].value
        if e.control.value == True:
            words_number = Controls_column.controls[7].value
            words_number = float(words_number)
            words_number = int(words_number)

            if main_language =='DE':words_fin, words_pos = give_words(user_words_dictionary_de,
                                                                      words_number=words_number,
                                                                      sen_number=sen_number_pass,
                                                                      lang='DE',
                                                                      new_percentage=new_words_percentage,
                                                                      active=e.control.value)
            if main_language =='ES':words_fin, words_pos = give_words(user_words_dictionary_es,
                                                                      words_number=words_number,
                                                                      sen_number=sen_number_pass,
                                                                      lang='ES',
                                                                      new_percentage=new_words_percentage,
                                                                      active=e.control.value)
            if main_language =='FR':words_fin, words_pos = give_words(user_words_dictionary_fr,
                                                                      words_number=words_number,
                                                                      sen_number=sen_number_pass,
                                                                      lang='FR',
                                                                      new_percentage=new_words_percentage,
                                                                      active=e.control.value)

            wb = generate_words_buttons((words_fin))
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
            sentences_column.controls.clear()
            sentences_trans_column.controls.clear()
            sentences_pictures_column.controls.clear()

            slowo = words_container.content.controls[0].text


            control_switch = your_sentences_container.content.controls[0].controls[0].value
            if control_switch == False:
                row = ft.Row(
                    [your_sentences_container, your_explanations_container, sentences_trans_container,
                     sentences_pictures_container,
                     words_container], expand=True)
                page.controls[0] = row

                slowo = words_container.content.controls[0].text

                page.update()
            else:
                row = ft.Row(
                    [Controls_column_container,your_sentences_container, your_explanations_container, sentences_trans_container,
                     sentences_pictures_container,
                     words_container], expand=True)
                page.controls[0] = row
                page.update()
        else:
            words_number = Controls_column.controls[7].value
            words_number = float(words_number)
            words_number = int(words_number)
            if main_language == 'DE': words_fin, words_pos = give_words(user_words_dictionary_de,
                                                                        words_number=words_number,
                                                                        sen_number=sen_number_pass,
                                                                        lang='DE',
                                                                        new_percentage=new_words_percentage,
                                                                        active=e.control.value)
            if main_language == 'ES': words_fin, words_pos = give_words(user_words_dictionary_es,
                                                                        words_number=words_number,
                                                                        sen_number=sen_number_pass,
                                                                        lang='ES',
                                                                        new_percentage=new_words_percentage,
                                                                        active=e.control.value)
            if main_language == 'FR': words_fin, words_pos = give_words(user_words_dictionary_fr,
                                                                        words_number=words_number,
                                                                        sen_number=sen_number_pass,
                                                                        lang='FR',
                                                                        new_percentage=new_words_percentage,
                                                                        active=e.control.value)

            wb = generate_words_buttons((words_fin))
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
            sentences_column.controls.clear()
            sentences_trans_column.controls.clear()
            sentences_pictures_column.controls.clear()

            control_switch = your_sentences_container.content.controls[0].controls[0].value
            if control_switch == False:
                row = ft.Row(
                    [your_sentences_container, sentences_container, sentences_trans_container, sentences_pictures_container,
                     words_container], expand=True)
                page.controls[0] = row
                page.update()
            else:
                row = ft.Row(
                    [Controls_column_container,your_sentences_container, sentences_container, sentences_trans_container,
                     sentences_pictures_container,
                     words_container], expand=True)
                page.controls[0] = row
                page.update()


    def mode_control_changed(e):
        if e.control.value == True:
            row = ft.Row(
                [Controls_column_container,your_sentences_container, sentences_container, sentences_trans_container, sentences_pictures_container,
                 words_container], expand=True)
            page.controls[0] = row
            page.update()
        else:
            row = ft.Row(
                [your_sentences_container, sentences_container, sentences_trans_container, sentences_pictures_container,
                 words_container], expand=True)
            page.controls[0] = row
            page.update()


    def slider_speech_changed(e):
        pass
    def slider_words_number(e):
        main_language = Controls_column.controls[13].value
        words_number = Controls_column.controls[7].value
        words_number = float(words_number)
        words_number = int(words_number)
        if main_language=='DE': words_fin, words_pos = give_words(user_words_dictionary_de, words_number=words_number, sen_number=sen_number_pass,lang='DE', new_percentage=new_words_percentage)
        if main_language == 'ES': words_fin, words_pos = give_words(user_words_dictionary_es, words_number=words_number,
                                                                    sen_number=sen_number_pass,
                                                                    lang='ES',
                                                                    new_percentage=new_words_percentage)
        if main_language == 'FR': words_fin, words_pos = give_words(user_words_dictionary_fr, words_number=words_number,
                                                                    sen_number=sen_number_pass,
                                                                    lang='FR',
                                                                    new_percentage=new_words_percentage)

        wb = generate_words_buttons((words_fin))
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
        sentences_column.controls.clear()
        sentences_trans_column.controls.clear()
        row = ft.Row(
            [Controls_column_container, your_sentences_container, sentences_container, sentences_trans_container,
             sentences_pictures_container,
             words_container], expand=True)
        page.controls[0] = row
        page.update()
    def slider_sent_pas(e):
        pass
    def slider_sent_act(e):
        pass



    def generate_words_buttons(list_of_words):
        list_of_buttons = []
        for word in list_of_words:
            list_of_buttons.append(ft.ElevatedButton(word, on_click=give_sentences))
        return list_of_buttons

    def give_sentences(e):
        word = e.control.text
        global current_word
        current_word = word
        give_sentences_impl(word)

    def give_n_sentences(sentences, words_list, number=25,lang='DE'):
        if lang =='DE': sen_lemma_1000_list = user_words_dictionary_de['sen_de_lemma_1000']["LEMMA"].values.tolist()
        if lang == 'ES': sen_lemma_1000_list = user_words_dictionary_es['sen_es_lemma_1000']["LEMMA"].values.tolist()
        if lang == 'FR': sen_lemma_1000_list = user_words_dictionary_fr['sen_fr_lemma_1000']["LEMMA"].values.tolist()

        word_freq_list = []
 
        for n in range(len(words_list)):
            word_freq_list.append([])

        pos = 0
        for lemma_sen in sen_lemma_1000_list:
            lemma_sen = lemma_sen.replace(' ','')
            lemma_words = lemma_sen.split(",")
            pos_word = 0
            for word in words_list:
                if (word in lemma_words):
                    word_freq_list[pos_word].append(pos)
                pos_word = pos_word+1
            pos = pos+1

        results = []
        times = 0
        for pos_sen in range(len(sen_lemma_1000_list)):
            for word in word_freq_list:
                if (pos_sen in word):
                    times = times+1
            results.append(times)
            times = 0

        true_indexes = []
        desired = len(word_freq_list)
        for nu in range(len(word_freq_list)):
            indexes  = [i for i, x in enumerate(results) if x == desired]
            if len(indexes)>0: true_indexes.append(indexes)
            desired = desired -1

        true_indexes = list(itertools.chain(*true_indexes))
        sentences_list = sentences["SENTENCE"].values.tolist()

        #all_sen_used = user_words_time_dictionary['sen_de_1000_time_read']
        #all_sen_used = all_sen_used.values.tolist()
        #all_sen_used = list(itertools.chain(*all_sen_used))
        #n = 2
        #del all_sen_used[0]
        #del all_sen_used[n - 1::n]


        last_result =[]
        last_indexes=[]

        for num_sen in range(len(true_indexes)):
            index_of_sen = true_indexes[num_sen]
            last_result.append(sentences_list[index_of_sen])
            last_indexes.append(index_of_sen)
            if len(last_result) == number: break


        return last_result, last_indexes

    def give_n_translations(sent_pos,number,lang='DE'):
        results =[]
        if lang =='DE': sen_en_1000_list = user_words_dictionary_de['sen_de_en_1000']["TRANSLATION"].values.tolist()
        if lang == 'ES': sen_en_1000_list = user_words_dictionary_es['sen_es_en_1000']["TRANSLATION"].values.tolist()
        if lang == 'FR': sen_en_1000_list = user_words_dictionary_fr['sen_fr_en_1000']["TRANSLATION"].values.tolist()

        for nu in range(number):
            tran_pos = sent_pos[nu]
            translation = sen_en_1000_list[tran_pos]
            results.append(translation)
        return results


    def give_sentences_impl(word):
        if switch_button_pas_act.value == False:
            number = int(Controls_column.controls[9].value)
        else:
            number = int(Controls_column.controls[11].value)

        main_language = Controls_column.controls[13].value
        sentences_column.controls.clear()
        sentences_trans_column.controls.clear()
        sentences_pictures_column.controls.clear()
        if main_language=="DE": sentences, sent_pos = give_n_sentences(user_words_dictionary_de['sen_de_1000'], [word], number=number,lang=main_language)
        if main_language == "ES": sentences, sent_pos = give_n_sentences(user_words_dictionary_es['sen_es_1000'],
                                                                         [word], number=number,lang=main_language)
        if main_language == "FR": sentences, sent_pos = give_n_sentences(user_words_dictionary_fr['sen_fr_1000'],
                                                                         [word], number=number,lang=main_language)

        #upgrade_sen_time_read(sentences,user_words_time_dictionary)
        for nu in range(len(sentences)):
            text_field = ft.TextField(
                label=word,
                multiline=True,
                label_style=ft.TextStyle(color=ft.colors.GREEN),
                color=ft.colors.GREEN,
                value=sentences[nu],
                on_focus=text_on_focus,
                data=sentences[nu],
        )
            if main_language=="DE": play_icon = ft.IconButton(icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=play_clicked_de,data=sentences[nu])
            if main_language == "ES": play_icon = ft.IconButton(icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED,
                                                                on_click=play_clicked_es, data=sentences[nu])
            if main_language == "FR": play_icon = ft.IconButton(icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED,
                                                                on_click=play_clicked_fr, data=sentences[nu])
            sentences_column.controls.append(text_field)
            sentences_column.controls.append(play_icon)

        page.update()

        translations = give_n_translations(sent_pos,len(sentences),lang=main_language)
        for nu in range(len(sentences)):
            text_field = ft.TextField(
                label=word,
                multiline=True,
                label_style=ft.TextStyle(color=ft.colors.GREEN),
                color=ft.colors.GREEN,
                value=translations[nu],
                on_focus=text_on_focus,
                data=sentences[nu],
        )
            play_icon = ft.IconButton(icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=play_clicked_en,data=translations[nu])
            sentences_trans_column.controls.append(text_field)
            sentences_trans_column.controls.append(play_icon)



        page.update()




    def play_clicked_de(e):
        #upgrade_words_time_listen(e.control.data,user_words_dictionary,user_words_time_dictionary)
        #upgrade_sen_time_listen(e.control.data,user_words_time_dictionary)
        time = Controls_column.controls[1].value
        value = float(time)
        speech_spaces = int(value)
        tts_de = TTS_DE()
        text =e.control.data
        text = prepare_ssml(text)
        if speech_spaces != 0: text = add_space_between_words(text,speech_spaces)
        tts_de.create_and_save(text)

    def play_clicked_es(e):
        #upgrade_words_time_listen(e.control.data,user_words_dictionary,user_words_time_dictionary)
        #upgrade_sen_time_listen(e.control.data,user_words_time_dictionary)
        time = Controls_column.controls[1].value
        value = float(time)
        speech_spaces = int(value)
        tts_es = TTS_ES()
        text =e.control.data
        text = prepare_ssml(text)
        if speech_spaces != 0: text = add_space_between_words(text,speech_spaces)
        tts_es.create_and_save(text)

    def play_clicked_fr(e):
        #upgrade_words_time_listen(e.control.data,user_words_dictionary,user_words_time_dictionary)
        #upgrade_sen_time_listen(e.control.data,user_words_time_dictionary)
        time = Controls_column.controls[1].value
        value = float(time)
        speech_spaces = int(value)
        tts_fr = TTS_FR()
        text =e.control.data
        text = prepare_ssml(text)
        if speech_spaces != 0: text = add_space_between_words(text,speech_spaces)
        tts_fr.create_and_save(text)


    def play_clicked_en(e):
        time = Controls_column.controls[1].value
        value = float(time)
        speech_spaces = int(value)
        tts_en = TTS_EN()
        text =e.control.data
        text = prepare_ssml(text)
        if speech_spaces != 0: text = add_space_between_words(text,speech_spaces)
        tts_en.create_and_save(text)

    def text_on_focus(e):
        sentences_pictures_column.controls.clear()
        pictures = get_pictures(e.control.data)
        for pic in pictures:
            pics_field = ft.Image(
                src=pic,
                width=300,
                height=300,
                fit=ft.ImageFit.FILL,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            )

            sentences_pictures_column.controls.append(pics_field)
        page.update()


    def rec_button_clicked(e):
        mic_recorder = Mic_Recorder(length=6,path=rec_path, file='flet.wav')
        mic_recorder.record()
        wm.transcribe_file(path=mic_recorder.path, file='flet.wav')
        wm.last_transcribe = wm.last_transcribe.replace('.', '')
        for nu in range(1):
            text_field = ft.TextField(
                label='YOUR SENTENCE',
                multiline=True,
                label_style=ft.TextStyle(color=ft.colors.YELLOW),
                color=ft.colors.YELLOW,
                value=wm.last_transcribe,
        )
            if wm.options['language'] == 'german': play_icon = ft.IconButton(icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=play_clicked_de, data=wm.last_transcribe)
            if wm.options['language'] == 'spanish': play_icon = ft.IconButton(
                icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=play_clicked_es, data=wm.last_transcribe)
            if wm.options['language'] == 'french': play_icon = ft.IconButton(
                icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=play_clicked_fr, data=wm.last_transcribe)
            your_sentences_column.controls.insert(1,text_field)
            your_sentences_column.controls.insert(2, play_icon)

            max_num_of_elements_in_your_sentences_column = sen_number_pass * 2 + 1
            how_many_elements = len(your_sentences_column.controls)
            if how_many_elements > max_num_of_elements_in_your_sentences_column:
                del your_sentences_column.controls[how_many_elements - 1]
                del your_sentences_column.controls[how_many_elements - 2]

        if len(sentences_column.controls) >0:
            your_sentence = your_sentences_column.controls[2].data
            best_match =''
            best_percent = 0
            index = 0
            best_index = 0
            for sentence in sentences_column.controls:
                if isinstance(sentence, flet_core.icon_button.IconButton):
                    if fuzz.ratio(str(sentence.data), your_sentence) > best_percent:
                        best_match = str(sentence.data)
                        best_percent = fuzz.ratio(str(sentence.data), your_sentence)
                        best_index = index
                index = index + 1

            sentence = best_match

            oko = fuzz.ratio(sentence, your_sentence)
            if switch_button_pas_act.value == False: simil_edge=90
            if switch_button_pas_act.value == True: simil_edge = 85

            if wm.options['language'] == 'french': simil_edge = 70



            if oko > simil_edge:
                #upgrade_sen_time_repeat(sentence,user_words_time_dictionary)
                your_sentences_column.controls[1].label = "GREAT-->"+str(oko)
                del sentences_column.controls[best_index]
                del sentences_column.controls[best_index-1]
                del sentences_trans_column.controls[best_index]
                del sentences_trans_column.controls[best_index-1]
                #upgrade_words_time_repeat(sentence,user_words_dictionary,user_words_time_dictionary)
                if len(your_explanations_column.controls) > 0: your_explanations_column.controls.clear()
            else:
                text = 'Give me explanation where I make mistake in a sentence :' + your_sentence + ' comparing to: ' + sentence + 'Explanation in English and German language'
                bot_text = chat_bot.talk(text)
                text_field = ft.TextField(
                    label='YOUR EXPLANATION',
                    multiline=True,
                    label_style=ft.TextStyle(color=ft.colors.YELLOW),
                    color=ft.colors.YELLOW,
                    value=sentence + bot_text,
                )
                if len(your_explanations_column.controls) > 0: your_explanations_column.controls.clear()
                your_explanations_column.controls.append(text_field)


        if len(sentences_column.controls) == 0:
            upgrade_words_pass_act(sen_number_pass, current_word, user_words_dictionary_de, switch_button_pas_act.value)
            if current_word != '':
                indx_to_del = 0
                words_buttons = page.controls[0].controls[len(page.controls[0].controls)-1].content.controls
                for indx in range(len(words_buttons)):
                    if words_buttons[indx].text == current_word:
                        indx_to_del = indx
                del words_buttons[indx_to_del]
                your_sentences_column.controls.clear()

                rb = FilledButton("REC", style=ButtonStyle(shape=CircleBorder(), padding=10),on_click=rec_button_clicked)

                sbpa=Switch(label="PAS/ACT MODE", on_change=mode_pas_act_changed)

                sbc=Switch(label="CONTROL MODE", on_change=mode_control_changed)

                row_your_sentences = ft.Row([sbc, sbpa, rb])
                your_sentences_column.controls.append(row_your_sentences)


        page.update()

    def language_changed(e):
        if isinstance(e, str):
            ml = e
            if ml == 'DE':
                words_fin, words_pos = give_words(user_words_dictionary_de, words_number=words_number,
                                                  sen_number=sen_number_pass,
                                                  lang=ml,
                                                  new_percentage=new_words_percentage)

                os = platform.system()
                if os == 'Darwin':
                    wm = WhisperModel(size='small', lang='german')
                if os == 'Windows' or os == 'Linux':
                    wm = WhisperModel(size='medium', lang='german')
            if ml == 'ES':
                words_fin, words_pos = give_words(user_words_dictionary_es, words_number=words_number,
                                                  sen_number=sen_number_pass,
                                                  lang=ml,
                                                  new_percentage=new_words_percentage)
                os = platform.system()
                if os == 'Darwin':
                    wm = WhisperModel(size='small', lang='spanish')
                if os == 'Windows' or os == 'Linux':
                    wm = WhisperModel(size='medium', lang='spanish')

            if ml == 'FR':
                words_fin, words_pos = give_words(user_words_dictionary_fr, words_number=words_number,
                                                  sen_number=sen_number_pass,
                                                  lang=ml,
                                                  new_percentage=new_words_percentage)
                os = platform.system()
                if os == 'Darwin':
                    wm = WhisperModel(size='small', lang='french')
                if os == 'Windows' or os == 'Linux':
                    wm = WhisperModel(size='medium', lang='french')


            global main_language
            main_language = ml
            global whisper_model
            whisper_model = wm
            global words_buttons
            wb = generate_words_buttons((words_fin))
            words_buttons = wb


            return wm, wb
        else:
            ml = e.data
            page.update()
            language_changed(ml)





    Controls_column = ft.Column([], )
    Controls_column.scroll = ft.ScrollMode.AUTO
    Controls_column_container = ft.Container(
        Controls_column,
        expand=True,
        margin=10,
        padding=10,
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        alignment=ft.alignment.top_center,
    )

    Controls_column.controls.append(Text("SPACE BETWEEN WORDS"))
    Controls_column.controls.append(
        Slider(min=0, max=2, divisions=2, value=0, label="{value}s", on_change=slider_speech_changed))
    Controls_column.controls.append(Text("SPEED OF SPEECH"))
    Controls_column.controls.append(
        Slider(min=0, max=100, divisions=10, value=50, label="{value}%", on_change=slider_speech_changed))
    Controls_column.controls.append(Text("PITCH OF SPEECH"))
    Controls_column.controls.append(
        Slider(min=0, max=100, divisions=10, value=50, label="{value}%", on_change=slider_speech_changed))
    Controls_column.controls.append(Text("WORDS_NUMBER"))
    Controls_column.controls.append(Slider(min=1, max=100, divisions=100, value=words_number, label="{value}  WORDS",
                                           on_change=slider_words_number))
    Controls_column.controls.append(Text("SENTENCES PASSIVE"))
    Controls_column.controls.append(
        Slider(min=1, max=25, divisions=25, value=sen_number_pass, label="{value}  SENTENCES ON PASSIVE",
               on_change=slider_sent_pas))
    Controls_column.controls.append(Text("SENTENCES ACTIVE"))
    Controls_column.controls.append(
        Slider(min=1, max=20, divisions=20, value=sen_number_act, label="{value} SENTENCES ON ACTIVE",
               on_change=slider_sent_act))
    Controls_column.controls.append(Text("MAIN LANGUAGE"))
    Controls_column.controls.append(ft.Dropdown(
        label="MAIN LANGUAGE",
        hint_text="Choose your language to learn?",
        on_change=language_changed,
        options=[
            ft.dropdown.Option("DE"),
            ft.dropdown.Option("ES"),
            ft.dropdown.Option("FR"),
        ],
        autofocus=True,
    ))

    check_box_de = ft.Checkbox(label="DE")
    check_box_fr = ft.Checkbox(label="ES")
    check_box_es = ft.Checkbox(label="FR")
    row_controls_column = ft.Row([check_box_de, check_box_fr, check_box_es])
    Controls_column.controls.append(Text("HELPER LANGUAGES"))
    Controls_column.controls.append(row_controls_column)

    Controls_column.controls[13].value = Controls_column.controls[13].options[0].key
    global main_language
    ml = Controls_column.controls[13].value
    main_language = ml
    global whisper_model
    global words_buttons
    wm, wb = language_changed(ml)
    whisper_model = wm
    words_buttons = wb

    switch_button_pas_act = Switch(label="P/A M", on_change=mode_pas_act_changed)
    switch_button_control = Switch(label="CO M", on_change=mode_control_changed)


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


    sentences_column = ft.Column([],)
    sentences_column.scroll = ft.ScrollMode.AUTO
    sentences_container = ft.Container(
        sentences_column,
        expand=True,
        margin=10,
        padding=10,
        bgcolor=ft.colors.AMBER_100,
        border_radius=10,
        alignment=ft.alignment.top_center,
    )

    sentences_trans_column = ft.Column([], )
    sentences_trans_column.scroll = ft.ScrollMode.AUTO
    sentences_trans_container = ft.Container(
        sentences_trans_column,
        expand=True,
        margin=10,
        padding=10,
        bgcolor=ft.colors.AMBER_100,
        border_radius=10,
        alignment=ft.alignment.top_center,
    )

    sentences_pictures_column = ft.Column([], )
    sentences_pictures_column.scroll = ft.ScrollMode.AUTO
    sentences_pictures_container = ft.Container(
        sentences_pictures_column,
        expand=True,
        margin=10,
        padding=10,
        bgcolor=ft.colors.AMBER_100,
        border_radius=10,
        alignment=ft.alignment.top_center,
    )

    your_sentences_column = ft.Column([], )
    your_sentences_column.scroll = ft.ScrollMode.AUTO
    your_sentences_container = ft.Container(
        your_sentences_column,
        expand=True,
        margin=10,
        padding=10,
        bgcolor=ft.colors.CYAN_500,
        border_radius=10,
        alignment=ft.alignment.top_center,
    )

    rec_button = FilledButton("REC",style=ButtonStyle(shape=CircleBorder(), padding=10),on_click=rec_button_clicked)



    row_your_sentences = ft.Row([switch_button_control,switch_button_pas_act,rec_button])
    your_sentences_column.controls.append(row_your_sentences)

    your_explanations_column = ft.Column([], )
    your_explanations_column.scroll = ft.ScrollMode.AUTO
    your_explanations_container = ft.Container(
        your_explanations_column,
        expand=True,
        margin=10,
        padding=10,
        bgcolor=ft.colors.CYAN_500,
        border_radius=10,
        alignment=ft.alignment.top_center,
    )





    row = ft.Row([your_sentences_container, sentences_container, sentences_trans_container,sentences_pictures_container, words_container], expand=True)
    page.add(row)
    page.theme_mode = ft.ThemeMode.DARK

ft.app(target=main)