from pydub import AudioSegment

# Load audio file
audio = AudioSegment.from_file("LPJP.mp3")

# Define start and end times (in milliseconds)
start_time = 90 * 1000  # 10 seconds
end_time = 329 * 1000    # 20 seconds

# Crop audio
cropped_audio = audio[start_time:end_time]

# Save the cropped audio
cropped_audio.export("LPJP_CHAPTER1.mp3", format="mp3")
print("Audio cropped successfully!")