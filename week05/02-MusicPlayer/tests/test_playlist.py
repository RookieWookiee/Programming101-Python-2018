import unittest
from src.playlist import Playlist
from src.song import Song


class PlaylistTests(unittest.TestCase):
    def test_total_length(self):
        with self.subTest('3:30 + 3:30 -> 7:00'):
            pl = Playlist('foo')
            s = Song(title='foo', artist='bar', album='baz', length='0:03:30')
            pl.add_songs([s, s])

            self.assertEqual(pl.total_length(), '7:00')

        with self.subTest('33:00 + 33:00 -> 1:06:00'):
            pl = Playlist('foo')
            s = Song(title='foo', artist='bar', album='baz', length='0:33:00')
            pl.add_songs([s, s])

            self.assertEqual(pl.total_length(), '1:06:00')

        with self.subTest('12 h + 13 h -/> 25 h'):
            pl = Playlist('foo')
            s1 = Song(title='foo', artist='bar', album='baz', length='12:00:00')
            s2 = Song(title='foo', artist='bar', album='baz', length='13:00:00')
            pl.add_songs([s1, s2])

            self.assertNotEqual(pl.total_length(), '25:00:00')

        with self.subTest('30 s + 30 s + 30 s -> 1:30'):
            pl = Playlist('foo')
            s = Song(title='foo', artist='bar', album='baz', length='30')
            pl.add_songs([s, s, s])

            self.assertEqual(pl.total_length(), '1:30')

        with self.subTest('1:00 * 60 -> 1:00:00'):
            pl = Playlist('foo')
            s = Song(title='foo', artist='bar', album='baz', length='1:00')
            pl.add_songs([s] * 60)

            self.assertEqual(pl.total_length(), '1:00:00')

    def test_artists(self):
        with self.subTest('empty playlist -> {}'):
            p = Playlist('foo')
            self.assertEqual(p.artists(), {})

        with self.subTest('3 songs 2 artists -> correct'):
            p = Playlist('foo')
            p.add_song(Song(title='bar1_song1', artist='bar1', length=60))
            p.add_song(Song(title='bar1_song2', artist='bar1', length=60))
            p.add_song(Song(title='bar2_song1', artist='bar2', length=60))

            expected = {'bar1': 2, 'bar2': 1 }
            self.assertEqual(p.artists(), expected)

if __name__ == '__main__':
    unittest.main()
