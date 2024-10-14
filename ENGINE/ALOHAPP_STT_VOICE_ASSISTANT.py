import webrtcvad
import numpy as np
import collections
from ENGINE.KEY_GROQ import provide_key
from ENGINE.PYAUDIO_DEVICES import find_mic_id
from ENGINE.TTS_OPENAI import generate_and_play
from ENGINE.API_BIGAI_CLIENT import *
from ENGINE.ALOHAPP_LANG_CODES import give_me_lang_code
from groq import Groq
from scipy.io.wavfile import write
import pyaudio
import ollama
import flet as ft
import os
import time
import platform
os_name = platform.system()


class VoiceAssistant:
    def __init__(self,main_page,stt='whisper',tts='openai',text_gen='groq'):
        self.main_page = main_page
        if stt == 'whisper':
            self.stt = 'whisper'

        if tts == 'melo':
            self.tts = 'melo'
        if tts == 'openai':
            self.tts = 'openai'
            self.tts_voice = "alloy"

        if text_gen == 'groq':
            self.text_gen = 'groq'
            self.client_groq = Groq(
                api_key=provide_key()
            )
        if text_gen == 'ollama':
            self.text_gen = 'ollama'


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
        write('audio_file.wav',self.RATE, audio_np)


        print(os.getcwd())
        if self.stt == 'whisper':
            print("Transcribing audio...")
            text = transcribe(file_path=os.getcwd()+'/audio_file.wav', language=self.main_page.user.langs[0][0])
            if os_name == 'Linux':
                text = text['segments'][0]['text']
            print(text)

        text_field = ft.TextField(
            label='YOUR SENTENCE',
            multiline=True,
            label_style=ft.TextStyle(color=ft.colors.YELLOW),
            color=ft.colors.YELLOW,
            value=text,
            icon=ft.icons.EMOJI_EMOTIONS
        )



        if len(self.main_page.conversation_column.controls) > 8:
            magic_row = self.main_page.conversation_column.controls[0]
            self.main_page.conversation_column.controls.clear()
            self.main_page.conversation_column.controls.append(magic_row)



        self.main_page.conversation_column.controls.append(text_field)
        unique_filename = f"oko_{time.time()}.png"
        generate_image(prompt=text, negative_prompt="", num_inference_steps=56,save_path=unique_filename)
        img = ft.Image(src=unique_filename, width=512, height=512)
        self.main_page.conversation_column.controls.append(img)

        self.main_page.update()


        if self.tts == 'melo':
            tts_melo(text, lang=self.main_page.user.langs[0][0], output="example.wav")
        if self.tts == 'openai':
            generate_and_play(text,voice=self.tts_voice)

        if self.text_gen == 'groq':
            chat_completion = self.client_groq.chat.completions.create(
                messages=[
                    {"role": "system", "content": 'You are super assistant.Use only words like you describe a picture.Answer always in '+ give_me_lang_code(self.main_page.user.langs[0][0])+' language and use maximal 3 sentences'},
                    {"role": "user","content": text}
                ],
                model="llama3-70b-8192",
            )
            bot_reply = chat_completion.choices[0].message.content

        if self.text_gen == 'ollama':
            bot_reply = ollama.chat(model='llama3.1:8b', messages=[
                {"role": "system", "content": 'You are super rude and sophisticated assistant answering always in '+ give_me_lang_code(self.main_page.user.langs[0][0])+ ' language in 2 sentences'},
                {'role': 'user','content': text}
            ])
            bot_reply = bot_reply['message']['content']

        print(bot_reply)

        text_field = ft.TextField(
            label='BOT REPLY',
            multiline=True,
            label_style=ft.TextStyle(color=ft.colors.BLACK),
            color=ft.colors.BLACK,
            value=bot_reply

        )
        self.main_page.conversation_column.controls.append(text_field)
        unique_filename = f"oko_{time.time()}.png"
        generate_image(prompt=bot_reply, negative_prompt="", num_inference_steps=56,save_path=unique_filename)
        img = ft.Image(src=unique_filename, width=512, height=512)
        self.main_page.conversation_column.controls.append(img)
        self.main_page.update()

        if self.tts == 'melo':
            tts_melo(bot_reply, lang=self.main_page.user.langs[0][0], output="example.wav")
        if self.tts == 'openai':
            generate_and_play(bot_reply,voice=self.tts_voice)







    def record_and_transcribe(self):
        stream = self.audio.open(format=self.FORMAT,
                                 channels=self.CHANNELS,
                                 rate=self.RATE,
                                 input=True,
                                 frames_per_buffer=self.CHUNK,
                                 input_device_index=find_mic_id())

        num_padding_frames = int(300 / self.FRAME_DURATION_MS)  # 300ms padding
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
