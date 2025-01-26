import webrtcvad
import numpy as np
import collections
from openai import OpenAI
from ENGINE.PYAUDIO_DEVICES import find_mic_id
from ENGINE.TTS_OPENAI import generate_and_play
from ENGINE.API_BIGAI_CLIENT import *
from ENGINE.ALOHAPP_TEXT_GEN import generate_text, generate_sugestion
from FRONT.ALOHAPP.CONTAINERS import delete_rows_words_buttons
from groq import Groq
from cerebras.cloud.sdk import Cerebras
import google.generativeai as genai
from scipy.io.wavfile import write
import pyaudio
from sudachipy import dictionary
import pykakasi
import json
import flet as ft
import os

import platform
os_name = platform.system()


class VoiceAssistant:
    def __init__(self,main_page,stt='whisper',tts='melo',text_gen='openai'):
        self.main_page = main_page
        if stt == 'whisper':
            self.stt = 'whisper'

        if tts == 'melo':
            self.tts = 'melo'
        if tts == 'openai':
            self.tts = 'openai'
            self.tts_voice = "alloy"



        if text_gen == 'openai':
            self.text_gen = 'openai'
            from ENGINE.KEY_OPENAI import provide_key
            key = provide_key()
            self.client_openai = OpenAI(api_key=key)

        if text_gen == 'google':
            self.text_gen = 'google'
            from ENGINE.KEY_GOOGLE import provide_key
            key = provide_key()
            self.client_google = genai
            self.client_google.configure(api_key=key)
            self.google_model = self.client_google.GenerativeModel("gemini-2.0-flash-exp")

        if text_gen == 'cerebras':
            self.text_gen = 'cerebras'
            from ENGINE.KEY_CEREBRAS import provide_key
            key = provide_key()
            self.client_cerebras = Cerebras(api_key=key,)

        if text_gen == 'groq':
            self.text_gen = 'groq'
            from ENGINE.KEY_GROQ import provide_key
            self.client_groq = Groq(
                api_key=provide_key()
            )
            self.welcome = True


        if text_gen == 'ollama':
            self.text_gen = 'ollama'


        self.context = ''
        self.great = False
        self.my_sentences = []
        self.my_sentences_languages = []
        self.bot_sentences = []
        self.bot_sugestions = []
        self.main_language = self.main_page.user.langs[0]
        self.tokenizer_obj = dictionary.Dictionary().create()
        self.kks = pykakasi.kakasi()



        # WebRTC VAD setup
        self.vad = webrtcvad.Vad(0)  # Aggressiveness from 0 to 3

        # Audio recording parameters
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000  # Sample rate
        self.FRAME_DURATION_MS = 30  # Duration of each frame in milliseconds
        self.CHUNK = int(self.RATE * self.FRAME_DURATION_MS / 1000)  # Number of samples per frame

        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()

    def process_audio(self, buffer):
        print("Processing audio for transcription...")
        # Convert the buffer to a single byte string
        audio_data = b''.join(buffer)

        # Convert byte string to numpy array
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        write(os.getcwd()+'/audio_file.wav',self.RATE, audio_np)
        print(len(audio_np))



        print(os.getcwd())
        if self.stt == 'whisper':
            print("Transcribing audio...")
            if os_name == 'Darwin':
                text = transcribe(file_path=os.getcwd()+'/audio_file.wav', language='zz')
            if os_name == 'Linux':
                try:
                    text = transcribe(file_path=os.getcwd()+'/audio_file.wav', language='zz')
                    text = text['segments'][0]['text']
                except IndexError:
                    print("Error: No transcription segments found. Please try speaking more clearly or check your microphone.")
                    text = 'transcribe error'
                    print(text)

            print(text)

        lang_of_my_sentence = detect_language(text)
        lang_of_my_sentence = lang_of_my_sentence['language_code']
        if lang_of_my_sentence in self.main_page.user.langs:
            self.great = True
            self.my_sentences.append(text)
            self.my_sentences_languages.append(lang_of_my_sentence)







        if lang_of_my_sentence != self.main_language:
            self.great = False
            if self.stt == 'whisper':
                print("Transcribing audio.!")
                if os_name == 'Darwin':
                    text_ll = transcribe(file_path=os.getcwd()+'/audio_file.wav', language=self.main_language)
                if os_name == 'Linux':
                    text_ll = transcribe(file_path=os.getcwd()+'/audio_file.wav', language=self.main_language)
                    try:
                        text_ll = text_ll['segments'][0]['text']
                    except IndexError:
                        print("Error: No transcription segments found. Please try speaking more clearly or check your microphone.")
                        text_ll = 'ok'
        else: text_ll = ''





        if self.great == True:
            text_field = ft.TextField(
                label='YOUR SENTENCE ORGINAL',
                multiline=True,
                label_style=ft.TextStyle(color=ft.colors.GREEN_800),
                color=ft.colors.GREEN_800,
                value=text,
                icon=ft.icons.EMOJI_EMOTIONS
            )
        else:
            text_field = ft.TextField(
                label='YOUR SENTENCE ORGINAL',
                multiline=True,
                label_style=ft.TextStyle(color=ft.colors.YELLOW),
                color=ft.colors.YELLOW,
                value=text,
                icon=ft.icons.EMOJI_EMOTIONS
            )




        if len(self.main_page.conversation_column.controls) > 3:
            magic_row = self.main_page.conversation_column.controls[0]
            self.main_page.conversation_column.controls.clear()
            self.main_page.conversation_column.controls.append(magic_row)

        if len(text_ll) > 0:
            above = ''
            below = ''
            tokens = self.tokenizer_obj.tokenize(text_ll)
            words = [token.surface() for token in tokens]
            for word in words:
                result = self.kks.convert(word)
                for item in result:
                    above += ' '+ item['hira']+' '
                    below += ' '+ item['hepburn']+' '

            if lang_of_my_sentence != self.main_language:
                text_field_ll = ft.TextField(
                    label='YOUR SENTENCE IN TARGET LANGUAGE',
                    multiline=True,
                    label_style=ft.TextStyle(color=ft.colors.YELLOW),
                    color=ft.colors.YELLOW,
                    value=f"{above}\n{text_ll}\n{below}",
                    icon=ft.icons.EMOJI_EMOTIONS,
                    text_style=ft.TextStyle(size=20, color=ft.colors.WHITE)
                )
                self.main_page.conversation_column.controls.append(text_field_ll)



        self.main_page.conversation_column.controls.append(text_field)
        self.main_page.update()

        if lang_of_my_sentence != self.main_language:
            if self.tts == 'melo':
                tts_melo(text_ll, lang=self.main_language, output="example.wav")
            if self.tts == 'openai':
                generate_and_play(text_ll,voice=self.tts_voice)


        bot_reply = generate_text(self, text)
        response_bot_json = json.loads(bot_reply)
        bot_reply = response_bot_json["japanese"]
        bot_reply_translated = response_bot_json["english"]
        print(bot_reply)
        print(bot_reply_translated)

        if bot_reply == '':
            source_language = 'eng_Latn'
            target_language = 'jpn_Jpan'
            bot_reply = translate(bot_reply_translated, source_language, target_language)



        above = ''
        below = ''
        tokens = self.tokenizer_obj.tokenize(bot_reply)
        words = [token.surface() for token in tokens]
        for word in words:
            result = self.kks.convert(word)
            for item in result:
                above += ' ' + item['hira'] + ' '
                below += ' ' + item['hepburn'] + ' '
        self.bot_sentences.append(bot_reply)
        text_field = ft.TextField(
            label='BOT REPLY',
            multiline=True,
            label_style=ft.TextStyle(color=ft.colors.BLACK),
            color=ft.colors.BLACK,
            value=f"{above}\n{bot_reply}\n{below}"

        )

        text_field_translated = ft.TextField(
            label='BOT REPLY TRANSLATED',
            multiline=True,
            label_style=ft.TextStyle(color=ft.colors.BLACK),
            color=ft.colors.BLACK,
            value=bot_reply_translated

        )

        bot_sugestions = generate_sugestion(self, bot_reply)
        response_bot_json = json.loads(bot_sugestions)
        bot_reply_sugestions = response_bot_json["japanese"]
        bot_reply_sugestions_translated = response_bot_json["english"]
        print(bot_reply_sugestions)
        print(bot_reply_sugestions_translated)
        if bot_reply_sugestions == '':
            source_language = 'eng_Latn'
            target_language = 'jpn_Jpan'
            bot_reply_sugestions = translate(bot_reply_sugestions_translated, source_language, target_language)

        above = ''
        below = ''
        tokens = self.tokenizer_obj.tokenize(bot_reply_sugestions)
        words = [token.surface() for token in tokens]
        for word in words:
            result = self.kks.convert(word)
            for item in result:
                above += ' ' + item['hira'] + ' '
                below += ' ' + item['hepburn'] + ' '
        self.bot_sugestions.append(bot_reply_sugestions)
        text_field_su = ft.TextField(
            label='BOT REPLY SUGESTIONS',
            multiline=True,
            label_style=ft.TextStyle(color=ft.colors.BLACK),
            color=ft.colors.YELLOW,
            value=f"{above}\n{bot_reply_sugestions}\n{below}\n{bot_reply_sugestions_translated}"

        )

        self.main_page.helper_column.controls.append(text_field_su)
        self.main_page.conversation_column.controls.append(text_field)
        self.main_page.conversation_column.controls.append(text_field_translated)
        self.context += "user:"+text+'.'
        self.context += "assistant:"+bot_reply+'.'
        self.last_bot_reply = bot_reply
        self.main_page.update()


        if len(self.main_page.helper_column.controls) > 3:
            magic_row = self.main_page.helper_column.controls[0]
            self.main_page.helper_column.controls.clear()
            self.main_page.helper_column.controls.append(magic_row)

        '''
        if lang_of_my_sentence in self.main_page.user.langs:
           known_words =  self.main_page.user.Update_Words_Past(my_sentences=self.my_sentences,my_sentences_languages=self.my_sentences_languages, bot_sentences=self.bot_sentences)
           if known_words:
               self.main_page.words_buttons = delete_words_buttons(page=self.main_page, known_words=known_words)
               self.main_page.update()
        '''

        if self.tts == 'melo':
            tts_melo(bot_reply, lang=self.main_language, output="example.wav")
        if self.tts == 'openai':
            generate_and_play(bot_reply,voice=self.tts_voice)


    def record_and_transcribe(self):
        stream = self.audio.open(format=self.FORMAT,
                                 channels=self.CHANNELS,
                                 rate=self.RATE,
                                 input=True,
                                 frames_per_buffer=self.CHUNK,
                                 input_device_index=find_mic_id())

        num_padding_frames = int(400 / self.FRAME_DURATION_MS)  # 400ms padding
        ring_buffer = collections.deque(maxlen=num_padding_frames)
        triggered = False
        frames = []

        print("Listening...")
        try:
            while True:
                try:
                    data = stream.read(self.CHUNK, exception_on_overflow=False)
                    if len(data) != self.CHUNK * 2:
                        continue

                    active = self.vad.is_speech(data, self.RATE)
                    if not triggered:
                        ring_buffer.append((data, active))
                        num_voiced = len([f for f, speech in ring_buffer if speech])
                        if num_voiced > 0.9 * ring_buffer.maxlen:
                            triggered = True
                            frames.extend([f for f, s in ring_buffer])
                            ring_buffer.clear()
                            print("Voice detected, recording...")
                    else:
                        frames.append(data)
                        ring_buffer.append((data, active))
                        num_unvoiced = len([f for f, speech in ring_buffer if not speech])
                        if num_unvoiced > 0.9 * ring_buffer.maxlen:
                            print("End of speech detected, processing audio...")
                            self.process_audio(frames)
                            frames = []
                            triggered = False

                except Exception as e:
                    print(f"Error: {e}")
                    break
        finally:
            stream.stop_stream()
            stream.close()
