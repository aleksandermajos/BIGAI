import pyaudio
import webrtcvad
import numpy as np
import whisperx
import collections

# Initialize Whisper model
model = whisperx.load_model("base",device="cuda")

# WebRTC VAD setup
vad = webrtcvad.Vad(3)  # Aggressiveness from 0 to 3

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Sample rate
FRAME_DURATION_MS = 30  # Duration of each frame in milliseconds
CHUNK = int(RATE * FRAME_DURATION_MS / 1000)  # Number of samples per frame

# Initialize PyAudio
audio = pyaudio.PyAudio()


def process_audio(buffer):
    print("Processing audio for transcription...")
    # Convert the buffer to a single byte string
    audio_data = b''.join(buffer)

    # Convert byte string to numpy array
    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

    # Transcribe using Whisperx
    print("Transcribing audio...")
    result = model.transcribe(audio_np, language="en")

    if 'text' in result:
        print("Transcription:", result['text'])
    else:
        print("Error: 'text' not in transcription result")
        print(result)


def record_and_transcribe():
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,input_device_index=11)

    num_padding_frames = int(300 / FRAME_DURATION_MS)  # 300ms padding
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    triggered = False
    frames = []

    print("Listening...")
    while True:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            if len(data) != CHUNK * 2:
                continue

            active = vad.is_speech(data, RATE)
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
                    process_audio(frames)
                    frames = []
                    triggered = False

        except Exception as e:
            print(f"Error: {e}")
            break


if __name__ == "__main__":
    try:
        record_and_transcribe()
    finally:
        audio.terminate()