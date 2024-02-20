from KEY_HF import provide_key
import moviepy.editor as mp
import whisperx


hf_key = provide_key()
device = "cuda"
audio_file = "audio.mp3"
batch_size = 16
compute_type = "float16"
model = whisperx.load_model("large-v3", device, compute_type=compute_type)


my_clip = mp.VideoFileClip(r"movie_1.mp4")
my_clip.audio.write_audiofile(r"audio.mp3")
audio = whisperx.load_audio(audio_file)


languages = ["pl", "ko", "ru", 'uk']
for language in languages:
    result = model.transcribe(audio, batch_size=batch_size, task="transcribe", language= language)
    print(result["segments"]) # before alignment
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    print(result["segments"]) # after alignment
    '''
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=hf_key, device=device)
    diarize_segments = diarize_model(audio)
    result = whisperx.assign_word_speakers(diarize_segments, result)
    print(diarize_segments)
    print(result["segments"])
    '''