import flet as ft
import threading
import queue
import asyncio
import collections
import time
import numpy as np

import webrtcvad
import pyaudio

# -------------------------------------------------------
# A simple STT loop using VAD.
# For demonstration purposes, it simulates recognized text.
# In a real application, replace the simulation with actual
# STT processing (e.g. using faster-whisper or another engine).
# -------------------------------------------------------

class STTVADLoop(threading.Thread):
    def __init__(self, result_queue, running_flag):
        super().__init__()
        self.result_queue = result_queue
        self.running_flag = running_flag  # threading.Event for stopping the loop
        self.sample_rate = 16000
        self.frame_duration_ms = 30  # Frame length in ms
        # Calculate frame size in bytes (16-bit PCM, mono)
        self.frame_size = int(self.sample_rate * self.frame_duration_ms / 1000 * 2)
        # Create a VAD instance with moderate aggressiveness (mode 2)
        self.vad = webrtcvad.Vad(2)
        self.audio_interface = pyaudio.PyAudio()

    def run(self):
        stream = self.audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=int(self.sample_rate * self.frame_duration_ms / 1000)
        )
        ring_buffer = collections.deque(maxlen=10)
        triggered = False
        voiced_frames = []

        while self.running_flag.is_set():
            try:
                frame = stream.read(
                    int(self.sample_rate * self.frame_duration_ms / 1000),
                    exception_on_overflow=False
                )
            except Exception:
                continue

            is_speech = self.vad.is_speech(frame, self.sample_rate)

            if not triggered:
                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in ring_buffer if speech])
                if num_voiced > 0.9 * ring_buffer.maxlen:
                    triggered = True
                    voiced_frames.extend([f for f, s in ring_buffer])
                    ring_buffer.clear()
            else:
                voiced_frames.append(frame)
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in ring_buffer if not speech])
                if num_unvoiced > 0.9 * ring_buffer.maxlen:
                    # In a real application, process 'voiced_frames' to run STT.
                    # Here we simulate a recognized speech result.
                    recognized_text = "[Simulated STT] Speech recognized."
                    self.result_queue.put(recognized_text)
                    triggered = False
                    ring_buffer.clear()
                    voiced_frames = []

        stream.stop_stream()
        stream.close()
        self.audio_interface.terminate()


# -------------------------------------------------------
# The Flet app integrating STT and TTS (using Kokoro TTS)
# -------------------------------------------------------

def main(page: ft.Page):
    page.title = "STT and TTS with Kokoro in Flet"

    # A thread-safe queue to receive recognized text from STT.
    result_queue = queue.Queue()
    recognized_texts = []
    text_display = ft.Text(value="", size=16)
    toggle_btn = ft.ElevatedButton(text="Start Listening")

    # Variables to manage the background STT thread.
    vad_thread = None
    running_flag = None
    listening = False

    def toggle_listening(e):
        nonlocal vad_thread, running_flag, listening, toggle_btn
        if listening:
            running_flag.clear()
            if vad_thread:
                vad_thread.join(timeout=1)
            listening = False
            toggle_btn.text = "Start Listening"
        else:
            running_flag = threading.Event()
            running_flag.set()
            vad_thread = STTVADLoop(result_queue, running_flag)
            vad_thread.daemon = True
            vad_thread.start()
            listening = True
            toggle_btn.text = "Stop Listening"
        page.update()

    def clear_text(e):
        nonlocal recognized_texts, text_display
        recognized_texts = []
        text_display.value = ""
        page.update()

    def speak_text(e):
        text = text_display.value
        if text.strip():
            # Run Kokoro TTS in a separate thread to avoid blocking the UI.
            def tts_run():
                try:
                    # Initialize the Kokoro pipeline (using default parameters).
                    from kokoro import KPipeline
                    pipeline = KPipeline(lang_code='a')  # 'a' for American English
                    audio_chunks = []
                    # Synthesize audio from text.
                    generator = pipeline(
                        text,
                        voice='af_sarah',  # Change voice as desired.
                        speed=1.0,
                        split_pattern=r'\n+'
                    )
                    for segment in generator:
                        # Each segment is assumed to have an 'audio' attribute (a NumPy array).
                        audio_chunks.append(segment.audio)
                    if audio_chunks:
                        full_audio = np.concatenate(audio_chunks)
                        # Play the audio using sounddevice.
                        import sounddevice as sd
                        sd.play(full_audio, 24000)  # 24000 Hz is the typical sample rate for Kokoro.
                        sd.wait()
                except Exception as ex:
                    print(f"TTS error: {ex}")

            threading.Thread(target=tts_run, daemon=True).start()

    # Build the UI layout.
    page.add(
        ft.Column([
            ft.Text("Recognized Speech:", size=20, weight="bold"),
            text_display,
            ft.Row([
                toggle_btn,
                ft.ElevatedButton("Clear", on_click=clear_text),
                ft.ElevatedButton("Speak", on_click=speak_text)
            ])
        ])
    )

    # Asynchronous function to poll the result queue.
    async def poll_queue():
        nonlocal recognized_texts, text_display
        while True:
            try:
                recognized_text = result_queue.get_nowait()
            except queue.Empty:
                recognized_text = None
            if recognized_text:
                recognized_texts.append(recognized_text)
                text_display.value = "\n".join(recognized_texts)
                page.update()
            await asyncio.sleep(0.5)

    # Instead of using page.add_async_task (which no longer exists),
    # start a background thread that runs the async poll_queue function.
    def start_polling():
        asyncio.run(poll_queue())
    threading.Thread(target=start_polling, daemon=True).start()

ft.app(target=main)
