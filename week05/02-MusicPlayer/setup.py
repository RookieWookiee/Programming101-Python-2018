from setuptools import setup

setup(
    name='Python Music Player',
    version='1.0',
    py_modules=['src.crawler', 'src.playlist', 'src.song', 'pmp'],
    install_requires=[
        'Click',
        'mutagen',
        'python-mpd2',
        'tabulate',
    ],
    entry_points='''
        [console_scripts]
        pymusic=pmp:cli
    '''
)

# to install it: pip install --editable .
# then run: $ pymusic
