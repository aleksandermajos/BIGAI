from fastapi import FastAPI, File, UploadFile
import whisper
import uvicorn
from io import BytesIO
import numpy as np
import librosa

# Load the Whisper model
model = whisper.load_model("medium")

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
    result = model.transcribe(audio)

    # Extract the transcription text
    transcription = result["text"]

    return {"transcription": transcription}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)