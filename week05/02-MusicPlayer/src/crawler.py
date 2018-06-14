import os
import mutagen
from .song import Song
from .playlist import Playlist


class MusicCrawler:
    def __init__(self, path):
        self.path = path
        if not self.path.endswith('/'):
            self.path += '/'
        self.thing = []

    def generate_playlist(self, name=None): 
        if name is None:
            name = self.path
        pl = Playlist(name)

        for root, dirs, files in os.walk(self.path):
            for f in files:
                mutagen_f = mutagen.File(root + f)
                # import pdb; pdb.set_trace()
                song = Song.from_mutagen_file(mutagen_f, path=root + f)
                pl.add_song(song)

        return pl 


m = MusicCrawler('/home/yrl/Test/')
p = m.generate_playlist()
