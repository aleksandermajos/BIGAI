import os

os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

import vlc

url = 'https://direct.franceinter.fr/live/franceinter-midfi.mp3'

# define VLC instance
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

# Define VLC player
player = instance.media_player_new()

# Define VLC media
media = instance.media_new(url)

# Set player media
player.set_media(media)

# Play the media
player.play()

oko = 7
