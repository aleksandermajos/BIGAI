from KEY_HF import provide_key
import moviepy.editor as mp
import whisperx
import math

def format_time(seconds):

    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

    return formatted_time


def generate_subtitle_file(language, segments, file_name,speaker = False):
    translator = pipeline('translation', model=model_trans, tokenizer=tokenizer, src_lang='en', tgt_lang=language,
                          max_length=400)
    subtitle_file = f"{file_name}.{language}.srt"
    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment['start'])
        segment_end = format_time(segment['end'])
        text += f"{str(index + 1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        if speaker: text += f"{segment['speaker']+':'}"

        output = translator(segment['text'])
        translated_text = output[0]['translation_text']

        text += f"{translated_text} \n"
        text += "\n"

    f = open(subtitle_file, "w",encoding="utf-8")
    f.write(text)
    f.close()

    return subtitle_file


hf_key = provide_key()
device = "cuda" #tu sobie wpisz cpu zamiast cuda i poleci na procku
audio_file = "../SCHOOL/audio.mp3"
batch_size = 16
if device =='cpu':
    compute_type = "float"
else:
    compute_type = "float16"
model = whisperx.load_model("large-v3", device, compute_type=compute_type)
speaker = False # ta flaga ustawia czy dodaje do napisow dzielenie na poszczegolnych ludzi w filmie



checkpoint = 'facebook/nllb-200-distilled-600M'
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
model_trans = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)



languages = ['rus_Cyrl','pol_Latn','kor_Hang','ukr_Cyrl']  # lista jezykow
movies = ["movie_1.mp4"] #lista filmow
for movie in movies:
    my_clip = mp.VideoFileClip(movie)
    my_clip.audio.write_audiofile(r"audio.mp3")
    audio = whisperx.load_audio(audio_file)
    for language in languages:
        result = model.transcribe(audio, batch_size=batch_size, task="transcribe", language= 'en')
        print(result["segments"]) # before alignment
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
        print(result["segments"]) # after alignment

        if speaker:
            diarize_model = whisperx.DiarizationPipeline(use_auth_token=hf_key, device=device)
            diarize_segments = diarize_model(audio)
            result = whisperx.assign_word_speakers(diarize_segments, result)
            print(diarize_segments)
            print(result["segments"])

        segments = result['segments']

        generate_subtitle_file(language=language, segments=segments, file_name=movie, speaker=speaker)
