import soundcard as sc
import time
import soundfile as sf

RATE = 16000


# get a list of all speakers:
speakers = sc.all_speakers()
# get the current default speaker on your system:
default_speaker = sc.default_speaker()

# get a list of all microphones:v
mics = sc.all_microphones(include_loopback=True)
# get the current default microphone on your system:
default_rec = mics[1]

for i in range(len(mics)):
    try:
        print(f"{i}: {mics[i].name}")
    except Exception as e:
        print(e)

with default_rec.recorder(samplerate=RATE) as rec, \
            default_speaker.player(samplerate=RATE) as sp:
    print("Recording...")
    data = rec.record(numframes=1000000)
    print("Done...Stop your sound so you can hear playback")
    time.sleep(5)
    sp.play(data)
    sf.write("../../DATA/FRENCH_16K.wav", data, RATE)
    oko=5