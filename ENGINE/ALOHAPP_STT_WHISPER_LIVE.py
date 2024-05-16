import queue
import time
from typing import Callable
import numpy as np
import sounddevice as sd
import pywhispercpp.constants as constants
import webrtcvad
import logging
from pywhispercpp.model import Model
import flet as ft

from ENGINE.KEY_OPENAI import generate_and_play
from ENGINE.TTS_SILERO_SSML import prepare_ssml
from ENGINE.TTS_SILERO_DE import TTS_DE
from ENGINE.ALOHAPP_UPGRADE_USER_FILES import upgrade_words_conv


class Whisper_live:

    def __init__(self,main_page,
                 language = 'de',
                 model='large-v3-q5_0',
                 input_device: int = None,
                 silence_threshold: int = 8,
                 q_threshold: int = 16,
                 block_duration: int = 30,
                 commands_callback: Callable[[str], None] = None,
                 model_log_level: int = logging.INFO,
                 **model_params):

        """
        :param main_page: main flet page ready to be updated according to tts
        :param model: whisper.cpp model name or a direct path to a`ggml` model
        :param input_device: The input device (aka microphone), keep it None to take the default
        :param silence_threshold: The duration of silence after which the inference will be running
        :param q_threshold: The inference won't be running until the data queue is having at least `q_threshold` elements
        :param block_duration: minimum time audio updates in ms
        :param commands_callback: The callback to run when a command is received
        :param model_log_level: Logging level
        :param model_params: any other parameter to pass to the whsiper.cpp model see ::: pywhispercpp.constants.PARAMS_SCHEMA
        """
        self.main_page = main_page
        self.language = language
        self.input_device = input_device
        self.sample_rate = constants.WHISPER_SAMPLE_RATE  # same as whisper.cpp
        self.channels = 1  # same as whisper.cpp
        self.block_duration = block_duration
        self.block_size = int(self.sample_rate * self.block_duration / 1000)
        self.q = queue.Queue()
        self.vad = webrtcvad.Vad()
        self.silence_threshold = silence_threshold
        self.q_threshold = q_threshold
        self._silence_counter = 0


        self.pwccp_model = Model(model,
                                 language=language,
                                 n_threads=6,
                                 log_level=model_log_level,
                                 print_realtime=False,
                                 print_progress=False,
                                 print_timestamps=False,
                                 single_segment=True,
                                 no_context=True,
                                 **model_params)
        self.commands_callback = commands_callback

    def _audio_callback(self, indata, frames, time, status):
        """
        This is called (from a separate thread) for each audio block.
        """
        if status:
            logging.warning(F"underlying audio stack warning:{status}")

        assert frames == self.block_size
        audio_data = map(lambda x: (x + 1) / 2, indata)  # normalize from [-1,+1] to [0,1]
        audio_data = np.fromiter(audio_data, np.float16)
        audio_data = audio_data.tobytes()
        detection = self.vad.is_speech(audio_data, self.sample_rate)
        if detection:
            self.q.put(indata.copy())
            self._silence_counter = 0
        else:
            if self._silence_counter >= self.silence_threshold:
                if self.q.qsize() > self.q_threshold:
                    self._transcribe_speech()
                    self._silence_counter = 0
            else:
                self._silence_counter += 1

    def _transcribe_speech(self):
        logging.info(f"Speech detected ...")
        audio_data = np.array([])
        while self.q.qsize() > 0:
            # get all the data from the q
            audio_data = np.append(audio_data, self.q.get())
        # Appending zeros to the audio data as a workaround for small audio packets (small commands)
        audio_data = np.concatenate([audio_data, np.zeros((int(self.sample_rate) + 10))])
        # running the inference
        self.pwccp_model.transcribe(audio_data,
                                    new_segment_callback=self._new_segment_callback)
        print('OTO NASZE:')
        print(self.pwccp_model.last_transcribe[0].text)


        text_field = ft.TextField(
            label='YOUR SENTENCE',
            multiline=True,
            label_style=ft.TextStyle(color=ft.colors.YELLOW),
            color=ft.colors.YELLOW,
            value=self.pwccp_model.last_transcribe[0].text,
            icon=ft.icons.EMOJI_EMOTIONS,
            smart_quotes_type='smart'
        )
        if len(self.main_page.conversation_column.controls) > 8:
            magic_row = self.main_page.conversation_column.controls[0]
            self.main_page.conversation_column.controls.clear()
            self.main_page.conversation_column.controls.append(magic_row)



        self.main_page.conversation_column.controls.append(text_field)
        self.main_page.update()

        lem = self.main_page.lemma(self.pwccp_model.last_transcribe[0].text)
        indx_to_del = []
        words_buttons = self.main_page.words_buttons
        for token in lem:
            print(token)
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
            real_index = self.main_page.repeat_words_full.index(element)
            real_indx_to_del_list.append(real_index)

        buttons_to_del = []
        for i in real_indx_to_del_list:
            real_indx_to_del = i
            self.main_page.repeat_table[i] = self.main_page.repeat_table[i] - 1
            how_many_times = self.main_page.repeat_table_full[i] - self.main_page.repeat_table[i]
            upgrade_words_conv(self.main_page.main_language, how_many_times,self.main_page.repeat_words_full[real_indx_to_del], self.main_page.user_words_dictionary)

            if how_many_times >= self.main_page.repeat_table_full[i]:
                button_index = real_indx_to_del_list.index(i)
                button_index = indx_to_del[button_index]
                buttons_to_del.append(button_index)

        num_of_buttons = len(self.main_page.words_buttons)
        for i in buttons_to_del:
            if i < len(self.main_page.words_buttons):
                del self.main_page.words_buttons[i]

        words = ':'

        for word in words_buttons:
            words += word.text + ','
            print(word)

        '''
        speaker = TTS_DE()
        text = self.pwccp_model.last_transcribe[0].text
        text = prepare_ssml(text)
        speaker.generate_and_play(text=text)
'''

        voice = 'nova'
        generate_and_play(text=self.pwccp_model.last_transcribe[0].text, voice=voice)


        if self.main_page.main_language == 'de':
            #bot_text = self.main_page.chat_bot.talk('Auf einen Satz antworten:' + self.pwccp_model.last_transcribe[0].text + 'mit diesen Worten' + words + ' in maximal 85 Zeichen')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+'.Antworten Sie in maximal zwei Sätzen')
        if self.main_page.main_language == 'es':
            #bot_text = self.main_page.chat_bot.talk('Responder a una frase:' + self.pwccp_model.last_transcribe[0].text + 'con estas palabras' + words + ' en un máximo de 85 caracteres')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".Responder en máximo dos oraciones")
        if self.main_page.main_language == 'fr':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".Répondre en deux phrases maximum")
        if self.main_page.main_language == 'it':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".Rispondi al massimo in 2 frasi")
        if self.main_page.main_language == 'pt':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".Responda em no máximo 2 frases")
        if self.main_page.main_language == 'ro':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".Răspunde în maxim 2 propoziții")
        if self.main_page.main_language == 'ca':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".Respon en no més de 2 frases")
        if self.main_page.main_language == 'pl':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".Odpowiedz w maksymalnie 2 zdaniach")
        if self.main_page.main_language == 'en':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".Respond in maximal 2 sentences")
        if self.main_page.main_language == 'ja':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".2 文以内で答えてください")
        if self.main_page.main_language == 'ko':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".2문장 이내로 답변하세요.")
        if self.main_page.main_language == 'ar':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".الإجابة بما لا يزيد عن جملتين")
        if self.main_page.main_language == 'ru':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".Ответ не более чем в 2 предложениях")
        if self.main_page.main_language == 'zh':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".回答不超过2句话")
        if self.main_page.main_language == 'tr':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".En fazla 2 cümleyle")
        if self.main_page.main_language == 'sv':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".Svara i maximalt 2 meningar")
        if self.main_page.main_language == 'nl':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".Reageer in maximaal 2 zinnen")
        if self.main_page.main_language == 'da':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".Svar i maksimalt 2 sætninger")
        if self.main_page.main_language == 'fa':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".حداکثر در 2 جمله پاسخ دهید")
        if self.main_page.main_language == 'he':
            #bot_text = self.main_page.chat_bot.talk('Répondre à une phrase:' + self.pwccp_model.last_transcribe[0].text + 'avec ces mots' + words + ' en 85 caractères maximum')
            bot_text = self.main_page.chat_bot.talk(self.pwccp_model.last_transcribe[0].text+".השב ב-2 משפטים מקסימום")


        text_field = ft.TextField(
            label='BOT REPLY',
            multiline=True,
            label_style=ft.TextStyle(color=ft.colors.BLACK),
            color=ft.colors.BLACK,
            value=bot_text,
            smart_quotes_type='smart'

        )
        self.main_page.conversation_column.controls.append(text_field)
        for indx in range(len(words_buttons)):
            words_buttons[indx].bgcolor = ft.colors.BLACK

        self.main_page.update()

        lem = self.main_page.lemma(bot_text)
        indx_to_change = []
        words_buttons = self.main_page.words_buttons
        for token in lem:
            for indx in range(len(words_buttons)):
                if words_buttons[indx].text in token.lemma_:
                    if len(words_buttons[indx].text) != len(token.lemma_):
                        if '|' in token.lemma_:
                            indx_to_change.append(indx)
                            words_buttons[indx].bgcolor = ft.colors.RED
                            continue
                    else:
                        indx_to_change.append(indx)
                        words_buttons[indx].bgcolor = ft.colors.RED


        self.main_page.update()

        '''
        speaker = TTS_DE()
        text = bot_text
        text = prepare_ssml(text)
        speaker.generate_and_play(text=text)
        '''

        voice = 'onyx'
        generate_and_play(text=bot_text, voice=voice)




    def _new_segment_callback(self, seg):
        if self.commands_callback:
            self.commands_callback(seg[0].text)

    def start(self) -> None:
        """
        Use this function to start the assistant
        :return: None
        """
        logging.info(f"Starting Assistant ...")
        with sd.InputStream(
                device=self.input_device,  # the default input device
                channels=self.channels,
                samplerate=constants.WHISPER_SAMPLE_RATE,
                blocksize=self.block_size,
                callback=self._audio_callback):

            try:
                logging.info(f"Assistant is listening ... (CTRL+C to stop)")
                while True:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                logging.info("Assistant stopped")

    @staticmethod
    def available_devices():
        return sd.query_devices()