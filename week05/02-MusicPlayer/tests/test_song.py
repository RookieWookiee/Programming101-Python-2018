import unittest
from src.song import Song
import json


class SongTests(unittest.TestCase):
    def test_init(self):
        with self.subTest('length: 3:44 -> should not raise error'):
            Song(title='foo', artist='bar', album='baz', length='3:44')

        with self.subTest('length: 03:44 -> should not raise error'):
            Song(title='foo', artist='bar', album='baz', length='03:44')

        with self.subTest('length: 1:30:44 -> should not raise ValueError'):
            Song(title='foo', artist='bar', album='baz', length='1:30:44')

        with self.subTest('length: 3:64 -> should raise ValueError'):
            with self.assertRaises(ValueError):
                Song(title='foo', artist='bar', album='baz', length='3:64')

        with self.subTest('length 60:03 -> should raise ValueError'):
            with self.assertRaises(ValueError):
                Song(title='foo', artist='bar', album='baz', length='60:03')

        with self.subTest('length 24:30:30 -> should raise ValueError'):
            with self.assertRaises(ValueError):
                Song(title='foo', artist='bar', album='baz', length='24:30:30')

    def test_length(self):
        with self.subTest('length 1:00:10 as seconds -> 3610'):
            s = Song(title='foo', artist='bar', album='baz', length='1:00:10')
            self.assertEqual(s.length(seconds=True), 3610)

        with self.subTest('length 1:00:10 as minutes -> 60'):
            s = Song(title='foo', artist='bar', album='baz', length='1:00:10')
            self.assertEqual(s.length(minutes=True), 60)

        with self.subTest('length 1:00:10 as hours -> 1'):
            s = Song(title='foo', artist='bar', album='baz', length='1:00:10')
            self.assertEqual(s.length(hours=True), 1)

        with self.subTest('length 1:00:10 no args -> "1:00:10"'):
            s = Song(title='foo', artist='bar', album='baz', length='1:00:10')
            self.assertEqual(s.length(), '1:00:10')

        with self.subTest('Two valid kwargs -> raise ValueError'):
            s = Song(title='foo', artist='bar', album='baz', length='1:00:10')
            with self.assertRaises(ValueError):
                s.length(hours=True, minutes=True)

        with self.subTest('Invalid kwarg -> raise ValueError'):
            s = Song(title='foo', artist='bar', album='baz', length='1:00:10')
            with self.assertRaises(ValueError):
                s.length(I_dont_exist=True)

        with self.subTest('length as float(61.3) -> 1:01'):
            s = Song(artist='foo', title='bar', length=61.3)
            self.assertEqual(s.length(), '1:01')

        with self.subTest('length as int(62) -> 1:02'):
            s = Song(artist='foo', title='bar', length=62)
            self.assertEqual(s.length(), '1:02')

    def test_json(self):
        with self.subTest('to_json: no album no path -> should be correct'):
            s = Song(title='foo', artist='bar', length='30')

            expected = json.dumps({
                'class_name': s.__class__.__name__,
                'dict': {
                    'title': 'foo',
                    'artist': 'bar',
                    'album': None,
                    'path': None,
                    'length': '0:30'
                }
            })
            actual = s.to_json()

            self.assertEqual(actual, expected)

        with self.subTest('to_json: no path -> should be correct'):
            s = Song(title='foo', artist='bar', album='baz', length=60)

            expected = json.dumps({
                'class_name': s.__class__.__name__,
                'dict': {
                    'title': 'foo',
                    'artist': 'bar',
                    'album': 'baz',
                    'path': None,
                    'length': '1:00'
                }
            })
            actual = s.to_json()

            self.assertEqual(actual, expected)

        with self.subTest('to_json: full info -> should be correct'):
            s = Song(title='foo', artist='bar', album='baz', path='foo/bar/baz', length=60)

            expected = json.dumps({
                'class_name': s.__class__.__name__,
                'dict': {
                    'title': 'foo',
                    'artist': 'bar',
                    'album': 'baz',
                    'path': 'foo/bar/baz',
                    'length': '1:00'
                }
            })
            actual = s.to_json()

            self.assertEqual(actual, expected)

        with self.subTest('from_json: full info -> should be correct'):
            expected = Song(artist='bar', title='foo', album='baz', path='foo/bar/baz', length=60)
            json_dict = {
                'class_name': s.__class__.__name__,
                'dict': {
                    'title': 'foo',
                    'artist': 'bar',
                    'album': 'baz',
                    'path': 'foo/bar/baz',
                    'length': '1:00'
                }
            }
            actual = Song.from_json(json.dumps(json_dict), namespace={'Song': Song})

            self.assertEqual(actual.artist, expected.artist)
            self.assertEqual(actual.title, expected.title)
            self.assertEqual(actual.album, expected.album)
            self.assertEqual(actual.length(), expected.length())
            self.assertEqual(actual.path, expected.path)


if __name__ == '__main__':
    unittest.main()
