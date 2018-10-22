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

Clone the repo, then: 
    $ pip3 install --editable .
    $ pip3 install -r requirements.txt

Or alternatively make a virtual environment and use the install script:
    $ curl https://raw.githubusercontent.com/kernel-panic96/Programming101-Python-2018/my-solutions/week05/02-MusicPlayer/install.sh | bash

    

Running it
----------
Every command and subcommand has a --help flag.

    $ pymusic
