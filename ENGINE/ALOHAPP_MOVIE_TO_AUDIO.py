import subprocess

video_path = "LP.mp4"
audio_path = "LPJP.mp3"

# Run ffmpeg command
command = f"ffmpeg -i {video_path} -q:a 0 -map a {audio_path} -y"
subprocess.run(command, shell=True)
print("Audio extracted successfully!")