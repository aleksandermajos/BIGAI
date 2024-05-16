from fastapi import FastAPI, File, UploadFile
from faster_whisper import WhisperModel
# import whisper
import uvicorn
from io import BytesIO
import numpy as np
import librosa

# Load the Whisper model
# model = whisper.load_model("medium")
model_size = "large-v3"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# Initialize FastAPI app
app = FastAPI()


@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    # Read the file as bytes
    audio_bytes = await file.read()

    # Convert bytes to BytesIO
    audio_file = BytesIO(audio_bytes)

    # Load the audio file with librosa
    audio, sr = librosa.load(audio_file, sr=None)  # sr=None to preserve the original sampling rate

    # Ensure audio is a 1D numpy array
    if audio.ndim == 2:
        audio = np.mean(audio, axis=1)

    # Transcribe the audio using Whisper
    segments, info = model.transcribe(audio, beam_size=5, task='transcribe',language='en')

    transcription = ''
    for segment in segments:
        transcription += ("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    return {"transcription": transcription}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)