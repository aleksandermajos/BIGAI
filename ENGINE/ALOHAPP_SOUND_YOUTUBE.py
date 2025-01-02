
import yt_dlp

url = "https://www.youtube.com/watch?v=Pmv6kNdHOT0&t=1320s&ab_channel=%E8%A5%BF%E6%9D%91%E4%BF%8A%E5%BD%A6%E3%81%AE%E6%9C%97%E8%AA%AD%E3%83%8E%E3%82%AA%E3%83%88"
ydl_opts = {
    'format': 'best',  # Best video + audio
    'outtmpl': '%(title)s.%(ext)s',  # Save file as video title
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])


