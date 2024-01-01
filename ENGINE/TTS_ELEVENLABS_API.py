from elevenlabs import generate, play
from elevenlabs import set_api_key

from ENGINE.KEY_ELEVENLABS import provide_key

key = provide_key().strip()
set_api_key(key)



def generate_and_play(text, voice):
    audio = generate(
      text=text,
      voice=voice,
      model="eleven_multilingual_v2")
    play(audio)

