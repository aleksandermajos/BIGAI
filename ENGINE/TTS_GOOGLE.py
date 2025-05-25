from ENGINE.KEY_GOOGLE import provide_key
from google import genai
from google.genai import types
import wave

key = provide_key()
client = genai.Client(api_key=key)


# Set up the wave file to save the output:
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
   with wave.open(filename, "wb") as wf:
      wf.setnchannels(channels)
      wf.setsampwidth(sample_width)
      wf.setframerate(rate)
      wf.writeframes(pcm)


response = client.models.generate_content(
   model="gemini-2.5-flash-preview-tts",
   contents="Stimmt. Aber wir könnten uns ja ein nettes kleines Airbnb suchen, vielleicht ein bisschen außerhalb vom direkten Zentrum, um Kosten zu sparen. Hauptsache, wir erleben die Stadt",
   config=types.GenerateContentConfig(
      response_modalities=["AUDIO"],
      speech_config=types.SpeechConfig(
         voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
               voice_name='Kore',
            )
         )
      ),
   )
)

data = response.candidates[0].content.parts[0].inline_data.data

file_name='out_de.wav'
wave_file(file_name, data) # Saves the file to current directory
