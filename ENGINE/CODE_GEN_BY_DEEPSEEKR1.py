import flet as ft
import speech_recognition as sr
from webrtcvad import Vad
import pyaudio
import threading
import queue

class AudioStream:
    def __init__(self):
        self.r = sr.Recognizer()
        self.vad = Vad(3)  # Aggressiveness level 3 for VAD
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.audio_queue = queue.Queue()
        self.running = True

    def start_stream(self):
        self.stream = self.pa.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=48000,
                                  input=True,
                                  frames_per_buffer=3200,
                                  stream_callback=self.callback)
        self.stream.start()

    def callback(self, in_data, frame_count, time_info, status):
        if not self.running:
            return (None, 0)
        self.audio_queue.put(in_data)
        return (None, 0)

    def process_audio(self):
        while self.running:
            data = self.audio_queue.get()
            if not self.vad.is_speech(data, 48000):
                continue
            # Process speech here with STT
            try:
                text = self.r.recognize_google(self.r.listen(sr.AudioData(data, 48000, 2)))
                print("Recognized:", text)
                # Update Flet window here
                # (This part would be integrated into the Flet UI)
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

    def stop_stream(self):
        self.running = False
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
        self.pa.terminate()

def main(page: ft.Page):
    page.title = "Live Speech to Text"
    text_box = ft.Text(value="Listening...", width=400)
    page.add(text_box)

    audio_stream = AudioStream()
    audio_stream.start_stream()
    process_thread = threading.Thread(target=audio_stream.process_audio)
    process_thread.start()

    def on_disconnect():
        audio_stream.stop_stream()
        process_thread.join()

    page.on_disconnect = on_disconnect

ft.app(target=main)