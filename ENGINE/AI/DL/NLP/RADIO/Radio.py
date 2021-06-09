import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

import vlc
import time

url = 'http://209.95.35.49:7300'

#define VLC instance
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

#Define VLC player
player=instance.media_player_new()

#Define VLC media
media=instance.media_new(url)

#Set player media
player.set_media(media)

#Play the media
player.play()

oko=7