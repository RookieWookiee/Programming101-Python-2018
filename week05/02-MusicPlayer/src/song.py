from utils.jsonable import JsonableMixin


class SongLength:
    units = ['seconds', 'minutes', 'hours', 'days']

    def __init__(self, *, days=0, hours=0, minutes=0, seconds=0):
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def __eq__(self, other):
        return (self.days == other.days and
                self.hours == other.hours and
                self.minutes == other.minutes and
                self.seconds == other.seconds)

    def __add__(self, other):
        seconds = self.to_seconds(self) + self.to_seconds(other)
        return self.from_seconds(seconds)

    @classmethod
    def parse(cls, length):
        seq = list(reversed(length.split(':')))

        if any(x == '' for x in seq):
            raise ValueError('Invalid length input')

        time_dict = {k: int(v) for v, k in zip(seq, cls.units)}

        if any(y >= 60 or y < 0 for x, y in time_dict.items()
                if x not in ['days', 'hours']):
            if time_dict['seconds'] >= 60:
                if any(y != 0 for x, y in time_dict.items() if x != 'seconds'):
                    raise ValueError('Invalid seconds value')
                else:
                    return cls.from_seconds(time_dict['seconds'])
            else:
                raise ValueError('Invalid length input')

        if time_dict.get('hours', 0) > 23 or time_dict.get('hours', 0) < 0:
            raise ValueError('Invalid hours value')

        return cls(
                days=time_dict.get('days', 0),
                hours=time_dict.get('hours', 0),
                minutes=time_dict.get('minutes', 0),
                seconds=time_dict.get('seconds', 0)
                )

    @classmethod
    def from_seconds(cls, seconds):
        s = seconds % 60
        m = (seconds // 60) % 60
        h = (seconds // 3600) % 24
        d = (seconds // 86400)

        return cls(days=d, hours=h, minutes=m, seconds=s)

    def __str__(self):
        if self.hours != 0:
            return f'{self.hours}:{self.minutes:02}:{self.seconds:02}'
        elif self.minutes != 0:
            return f'{self.minutes}:{self.seconds:02}'
        else:
            return f'0:{self.seconds:02}'

    def __repr__(self):
        return str(self)

    @classmethod
    def to_minutes(cls, self):
        if type(self) is Song:
            self = self.length_
        return self.hours * 60 + self.minutes

    @classmethod
    def to_seconds(cls, self):
        if type(self) is Song:
            self = self.length_
        return self.hours * 3600 + self.minutes * 60 + self.seconds

    @classmethod
    def to_hours(cls, self):
        if type(self) is Song:
            self = self.length_
        return self.hours


class Song(JsonableMixin):
    __valid_args = {'seconds', 'minutes', 'hours'}

    def __init__(self, *, title, artist, album=None, length, path=None):
        self.title = title
        self.artist = artist
        self.album = album
        self.path = path

        if type(length) is float or type(length) is int:
            self.length_ = SongLength.from_seconds(int(length))
        else:
            self.length_ = SongLength.parse(length)

    def __str__(self):
        s = f'{self.artist} - {self.title} from {self.album} - {self.length_}'
        return s

    def __eq__(self, other):
        self_list = [self.artist, self.title]
        other_list = [other.artist, other.title]

        return all(x == y for x, y in zip(self_list, other_list))

    def __hash__(self):
        s = f'{self.artist.lower()}{self.title.lower()}'
        return hash(s)

    def __add__(self, other):
        return self.length_ + other.length_

    __length_lookup = {
            'seconds': SongLength.to_seconds,
            'minutes': SongLength.to_minutes,
            'hours': SongLength.to_hours
            }

    def length(self, **kwargs):
        if len(kwargs) != 0 and len(kwargs) != 1:
            raise ValueError('Too many arguments supplied')

        if any(x not in self.__valid_args for x in kwargs):
            raise ValueError('Invalid method argument')

        try:
            key = next(iter(kwargs))
            return self.__length_lookup[key](self.length_)
        except StopIteration:
            return str(self.length_)


    def to_json(self, **kwargs):
        marshall = { 'length_': lambda self, v: [('length', self.length())] }
        kwargs.update(marshall)

        return super().to_json(**kwargs)

    __tags_key_lookup = {
            'artist': {
                    '©ART',
                    'ARTIST',
                    'TPE1'
                },
            'title': {
                    'TIT2',
                    'TITLE',
                    '©nam'
                },
            'album': {
                    '©alb',
                    'ALBUM',
                    'TALB'
                }
        }
    
    @classmethod
    def from_mutagen_file(cls, f, path=None):
        kwargs = {}
        for attr in cls.__tags_key_lookup:
            for k in cls.__tags_key_lookup[attr]:
                try:
                    kwargs[attr] = f.tags.get(k)
                except ValueError:
                    kwargs[attr] = None

                if kwargs[attr] != None:
                    if type(kwargs[attr]) is list:
                        kwargs[attr] = str(kwargs[attr][0])
                    else:
                        kwargs[attr] = str(kwargs[attr])
                    break

        return cls(length=f.info.length, path=path, **kwargs)
