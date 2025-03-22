from pathlib import Path
from ENGINE.KEY_OPENAI import provide_key
from openai import OpenAI

key=provide_key()
client = OpenAI(api_key=key)


speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="gpt-4o-mini-tts",
  voice="coral",
  input = 'Wędrowały dwie krawcowe,Szyły piękne suknie nowe.Szyły suknie w groszki, w kwiatki,W paski, w kratki i w zakładki,W krążki, w prążki oraz w cętki,Aż cieszyły się klientki.Kiedy przyszły do Skierniewic,Zobaczyły osiem dziewic,Osiem panien burmistrzanekRóżowiutkich jak poranek.',
  instructions="Delivery: Exaggerated and theatrical, with dramatic pauses, sudden outbursts, and gleeful cackling.Voice: High-energy, eccentric, and slightly unhinged, with a manic enthusiasm that rises and falls unpredictably. Tone: Excited, chaotic, and grandiose, as if reveling in the brilliance of a mad experiment.Pronunciation: Sharp and expressive, with elongated vowels, sudden inflections, and an emphasis on big words to sound more diabolical.Language : polish",
)
response.stream_to_file(speech_file_path)


