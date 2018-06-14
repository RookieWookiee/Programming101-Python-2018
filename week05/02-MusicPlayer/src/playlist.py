from enum import IntEnum
from functools import reduce
from tabulate import tabulate
from random import shuffle
from utils.jsonable import JsonableMixin
from mpd import MPDClient
from src.song import Song, SongLength
from utils.decorators import with_mpd_client, popen

import json, re, operator, os, click, sys


class PlaylistOptions(IntEnum):
    REPEAT = 2 ** 0
    SHUFFLE = 2 ** 1


class Playlist(JsonableMixin):
    def __init__(self, name, *, repeat=False, shuffle=False, songs=None):
        self.name = name
        self._play_order = []
        self.songs = set()
        self._options = (repeat + (shuffle << 1))
        self._current_song = 0

        if songs is not None:
            self.add_songs(songs)

    def __iter__(self):
        return iter(self._play_order)

    def __contains__(self, song):
        return song in self.songs

    def __len__(self):
        return len(self._play_order)

    def add_song(self, song):
        self.songs.add(song)
        self._play_order.append(song)

    def add_songs(self, songs):
        self.songs = self.songs.union(set(songs))
        self._play_order.extend(songs)

    def remove_song(self, song):
        self.songs.remove(song)
        self._play_order.remove(song)

    def total_length(self):
        zero = SongLength()
        return str(reduce(operator.add, self._play_order, zero))

    def artists(self):
        artists = {}
        for s in self:
            if s.artist not in artists:
                artists[s.artist] = 0
            artists[s.artist] += 1

        return artists

    def next_song(self):
        if len(self.songs) == 0:
            raise StopIteration

        if self._current_song == len(self._play_order):
            if self._options & PlaylistOptions.REPEAT:
                self._current_song = 0
            else:
                raise StopIteration

        if self._current_song == 0 and (self._options & PlaylistOptions.SHUFFLE):
            shuffle(self._play_order)

        song = self._play_order[self._current_song]
        self._current_song += 1

        return song

    def pprint_playlist(self, tablefmt='orgtbl'):
        pl = [(s.artist, s.title, s.length()) for s in self._play_order]
        print(tabulate(pl, ['Artist', 'Song', 'Length'], tablefmt=tablefmt))

    def to_json(self, **kwargs):
        def marshall_options(self, v):
            return [('repeat', self._options & PlaylistOptions.REPEAT != 0),
                    ('shuffle', self._options & PlaylistOptions.SHUFFLE != 0)]

        return super().to_json(_options=marshall_options)

    def save(self):
        filename = re.sub('\s+', '-', self.name) + '.json'
        os.makedirs('playlist-data', mode=0o511, exist_ok=True)
        with open('playlist-data/' + filename, 'w') as f:
            json.dump(self.to_json(), f, indent=4)

    @staticmethod
    def load(path):
        try:
            with open(path, 'r') as f:
                dict_ = json.load(f)
        except FileNotFoundError:
            with open('playlist-data/' + path, 'r') as f:
                dict_ = json.load(f)

        return Playlist.from_json(dict_, globals())


@click.group(short_help='group of commands for manipulating playlists')
def playlist():
    pass


@playlist.command()
@click.argument('start', type=click.INT, default=0)
@click.argument('end', type=click.INT, default=0)
@click.option('-id', '--with-id', is_flag=True, default=False)
@click.option('--no-pager', 'pager', flag_value=False,
        default=True)
@with_mpd_client
def show(client, start, end, with_id, pager):
    ''' Print the current playlist in a table. 
        By default start and end are set to '''
    pl = client.playlistinfo()

    if end == 0 or end > len(pl):
        end = len(pl)
       
    fields =  ['artist', 'title', 'time']
    if with_id:
        fields.insert(0, 'id')

    info = [[x.get(field, 'Unknown') for field in fields] for x in pl[start:end]]

    table_fields = map(str.capitalize, fields)

    for seq in info:
        seq[-1] = SongLength.from_seconds(int(seq[-1]))

    if len(info) > 25 and pager:
        with popen('less', 'w') as output:
            click.echo(tabulate(info, table_fields, tablefmt='orgtbl'), file=output)
    else:
        click.echo(tabulate(info, table_fields, tablefmt='orgtbl'))


if __name__ == '__main__':
    p = Playlist('FooPl', shuffle=True)

    p.add_song(Song(title='Odin', artist='Manowar', length='3:44'))
    p.add_song(Song(title='The Sons of Odin', artist='Manowar', length='6:26'))
    p.add_song(Song(title='Pass the Buck (ft. DRS)', artist='Artificial Intelligence', length='4:47'))
    p.add_song(Song(title='Centrifuge', artist='Enei', length='5:17'))

    p2 = Playlist.load('FooPl.json')
    p2.pprint_playlist()
    s = Song(title='Odin', artist='Manowar', length='3:44')
