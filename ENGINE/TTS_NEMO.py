import soundfile as sf
from nemo.collections.tts.models.base import SpectrogramGenerator, Vocoder

spec_generator = SpectrogramGenerator.from_pretrained(model_name="tts_de_fastpitch")
vocoder = Vocoder.from_pretrained(model_name="tts_hifigan")
parsed = spec_generator.parse("You can type your sentence here to get nemo to produce speech.")
spectrogram = spec_generator.generate_spectrogram(tokens=parsed)

audio = vocoder.convert_spectrogram_to_audio(spec=spectrogram)
sf.write("speech.wav", audio.to('cpu').detach().numpy()[0], 22050)