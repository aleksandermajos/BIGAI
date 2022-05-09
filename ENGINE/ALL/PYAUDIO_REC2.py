import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
RATE = 16000
RECORD_SECONDS = 8
WAVE_OUTPUT_FILENAME = "../../DATA/FRENCH_16K.wav"

p = pyaudio.PyAudio()
device_id = 0
device_info = p.get_device_info_by_index(device_id)
CHANNELS = 1
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=device_info["index"],
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()