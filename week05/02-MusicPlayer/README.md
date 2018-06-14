Pymusic
-------
Pymusic is a MPD command line client.
Currently it assumes that you have a running mpd backend
at localhost:6600 and ~/Music directory [configured](https://wiki.archlinux.org/index.php/Music_Player_Daemon#Configuration) as
the music_directory for mpd. You could edit the global variables inside pmp.py if you have configured it otherwise.

Dependencies
------------

mpd, python3.6

Installing
----------

    $ pip3 install --editable .
    $ pip3 install -r requirements.txt

Running it
----------
Every command and subcommand has a --help flag.

    $ pymusic
