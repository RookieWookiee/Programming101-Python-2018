'''
A python mpd client

At the moment, the program assumes mpd is running on localhost at port 6600.
If that is not the case, you can edit the global variables HOST and/or PORT
Whenever play is invoked with a new song, the song will be copied/moved to MUSIC_DIR
by default that directory is $HOME/Music
'''

from os.path import expanduser

from mpd import CommandError
from src.song import SongLength
from utils.decorators import with_mpd_client, open_client
from utils.file_utils import copy_file, move_file
from time import sleep
from os import linesep

import click


PORT = 6600
HOST = 'localhost'
MUSIC_DIR = expanduser('~/Music')


# This is the entry point
@click.group()
@click.option('-p', '--port', default=6600,
              help='The port to connect to.')
@click.option('-H', '--host', default='localhost',
              help='The host to connect to.')
def cli(host, port):
    pass


@cli.command(short_help='resume or stop the current song')
@with_mpd_client
def pause(client):
    state = client.status().get('state')
    if state == 'play':
        client.pause()


@cli.command(short_help='advance to next song')
@with_mpd_client
def next(client):
    client.next()


@cli.command(short_help='go back one song')
@with_mpd_client
def prev(client):
    client.previous()


@cli.command(short_help='stop playing')
@with_mpd_client
def stop(client):
    client.stop()


@cli.command(short_help='start playing if stopped, else toggle between playing and paused')
@with_mpd_client
def toggle(client):
    state = client.status().get('state')
    if state == 'stop':
        client.play()
    else:
        client.pause()


# This function is doing too many things
def get_song_id(client, id_or_fname, copy):
    try:
        _id = int(id_or_fname)
        with open_client(HOST, PORT) as client:
            client.playlistid(_id)
        return ('id', _id)
    except CommandError:
        raise click.BadParameter(f'No song with ID {_id} exists')
    except ValueError:
        fname = id_or_fname
        if client.search('filename', fname):  # Already in the music db
            # But not nesecessarily added to the playlist
            for s in client.playlistinfo():
                if s.get('file') == id_or_fname:
                    return ('pos', int(s.get('pos')))
            else:
                client.addid(fname, 0)
                return ('pos', 0)
        else:  # Not in the music db
            try:
                if copy:
                    copy_file(fname, MUSIC_DIR)
                else:
                    move_file(fname, MUSIC_DIR)
            except OSError as e:
                raise click.UsageError(f'Invalid filename: no such file {fname}')

            client.update(fname)
            while(client.playlistinfo()[0].get('file') != fname):
                try:
                    client.addid(fname, 0)
                except CommandError:
                    sleep(0.1)
                    continue

            return ('pos', 0)


@cli.command(short_help='plays song by given id or filename')
@click.argument('play_object', type=click.STRING,
                metavar='[<songid> | <filename>]',
                nargs=-1)
@click.option('--copy/--move', default=True)
@with_mpd_client
def play(client, copy, play_object):
    if len(play_object) > 1:
        raise click.BadParameter(
            'Expected songid or filename for play_object,'
            f'got {len(play_object)} things'
        )

    elif len(play_object) == 1:
        play_object = play_object[0]
        type, ret = get_song_id(client, play_object, copy)
        if type == 'pos':
            client.play(ret)
        else:
            client.playid(ret)
    else:
        state = client.status().get('state')
        if state == 'stop' or state == 'pause':
            client.play()


@cli.command(short_help='show information about the current song')
@with_mpd_client
def curr(client):
    info = client.status()
    state = info.get('state')

    if state == 'stop':
        click.echo('[stopped]')
    elif state == 'play' or state == 'pause':
        curr_song = client.currentsong()

        elapsed_time = SongLength.from_seconds(int(float(info.get('elapsed'))))
        total_time = SongLength.from_seconds(int(curr_song.get('time')))
        artist = curr_song.get('artist', 'Unknown')
        title = curr_song.get('title', 'Unknown')
        filename = curr_song.get('file', 'Unknown')

        click.echo(f'{artist} - {title}{linesep}'
                f'filename: {filename}')
        if state == 'play':
            click.echo(f'[playing] {elapsed_time}/{total_time}')
        else:
            click.echo(f'[paused] {elapsed_time}/{total_time}')


def validate_time(ctx, param, time):
    try:
        t = time[1:] if time[0] in '+-' else time
        SongLength.to_seconds(SongLength.parse(t))
        return time
    except ValueError:
        raise click.BadParameter(f'{time} is not in valid format')


@cli.command(short_help='advance, rewind or set the time of the current song')
@click.argument('time', type=click.STRING, metavar='[-- -<time> | [+]<time>]',
                callback=validate_time)
@with_mpd_client
def seek(client, time):
    '''Advances, rewinds, or sets the time of the song
       if the time is prefixed with "-", "--" should be used
       before the <time> argument.'''
    if time[0] not in '+-':
        time = SongLength.to_seconds(SongLength.parse(time))

    client.seekcur(time)


from src.playlist import playlist
cli.add_command(playlist)
