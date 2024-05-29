import pyaudio
import numpy as np
import whisperx
import webrtcvad
import time

RATE = 16000  # Sampling rate
CHUNK = 1024  # Size of each audio chunk
CHANNELS = 1  # Mono audio
FORMAT = pyaudio.paInt16  # Audio format

p = pyaudio.PyAudio()
vad = webrtcvad.Vad()
vad.set_mode(1)  # Set aggressiveness: 0, 1, 2, or 3

audio_buffer = []

def callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    if vad.is_speech(audio_data.tobytes(), RATE):
        audio_buffer.extend(audio_data)
    return (in_data, pyaudio.paContinue)

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=callback)
stream.start_stream()


def record_audio(duration):
    global audio_buffer
    audio_buffer = []

    start_time = time.time()
    while time.time() - start_time < duration:
        time.sleep(0.1)  # Adjust as necessary for performance

    stream.stop_stream()

    if audio_buffer:
        audio_data = np.concatenate(audio_buffer, axis=0)
        return audio_data
    else:
        return np.array([])

def transcribe_audio(audio_data):
    model = whisperx.load_model("base")
    transcription = model.transcribe(audio_data.tobytes(), rate=RATE)
    return transcription['text']

if __name__ == "__main__":
    duration = 10  # Duration of recording in seconds
    print("Recording...")
    recorded_audio = record_audio(duration)
    if recorded_audio.size > 0:
        print("Transcribing...")
        transcription = transcribe_audio(recorded_audio)
        print("Transcription: ", transcription)
    else:
        print("No speech detected.")
    stream.close()
    p.terminate()