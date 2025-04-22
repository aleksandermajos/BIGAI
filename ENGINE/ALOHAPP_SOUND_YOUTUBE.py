import yt_dlp

def download_best_audio_as_mp3(video_url, save_path="downloads/"):
    ydl_opts = {
        'outtmpl': save_path + '%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',  # best available
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

download_best_audio_as_mp3("https://www.youtube.com/watch?v=-WEgTq8_ei4&ab_channel=ADCNClubforCreativity")

