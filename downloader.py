from pytube import *
from slugify import slugify
import os
playlist_link = 'https://www.youtube.com/playlist?list=PLl6lrX1yD3BSjiLogL5cYODGdK7T2Km__'

playlist = Playlist(playlist_link)
print('Number of videos in playlist: %s' % len(playlist.video_urls))
path = 'C:/Users/Francesco/Videos/Casey Neistat'
os.chdir(path)
offset = 225

for index in range(len(playlist) - offset):
    video = YouTube(playlist[index + offset])
    filename = "{} - {}.mp4".format(index + offset, slugify(video.title))
    if os.path.isfile(filename):
        print("File already exists!")
        continue
    print("Downloading {} - {}".format(index + offset,video.title))
    video.streams. \
        filter(type='video', progressive=True, file_extension='mp4'). \
        order_by('resolution'). \
        desc(). \
        first(). \
        download(output_path= path,
                 filename=filename)
