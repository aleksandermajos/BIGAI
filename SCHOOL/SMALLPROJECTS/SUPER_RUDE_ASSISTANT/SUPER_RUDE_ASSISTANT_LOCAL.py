import pyaudio
import webrtcvad
import numpy as np
import whisperx
import collections
from ENGINE.KEY_GROQ import provide_key
from ENGINE.PYAUDIO_DEVICES import find_mic_id
from groq import Groq
from playsound import playsound
from melo.api import TTS
import ollama

speed = 0.9
device_melo = 'cuda'
model_melo = TTS(language='EN', device=device_melo)
speaker_ids = model_melo.hps.data.spk2id

client = Groq(
    api_key=provide_key()
)

# Initialize Whisper model
model = whisperx.load_model("large-v3",device="cuda",compute_type='float')

# WebRTC VAD setup
vad = webrtcvad.Vad(0)  # Aggressiveness from 0 to 3

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
    text = result['segments'][0]['text']
    print(text)

    '''
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are super rude assistant.Use only vulgar words.Answer always use maximal 3 sentences"},
            {"role": "user","content": text}
        ],
        model="llama3-70b-8192",
    )
    bot_reply = chat_completion.choices[0].message.content
    '''
    bot_reply = ollama.chat(model='llama3.1:8b', messages=[
        {"role": "system", "content": "You are super smart and sophisticated assistant answering always in 2 sentences"},
        {'role': 'user','content': text}
    ])
    bot_reply=bot_reply['message']['content']

    print(bot_reply)

    output_path = 'oko.wav'
    model_melo.tts_to_file(bot_reply, speaker_ids['EN-BR'], output_path, speed=speed)
    playsound('oko.wav')

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
                        frames_per_buffer=CHUNK,input_device_index=find_mic_id())

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