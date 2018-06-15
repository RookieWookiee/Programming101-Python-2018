import sys
import unittest
from assert_raises import assertRaises

class TestAssertRaises(unittest.TestCase):
    def test_catches_type_error_no_message_supplied(self):
        with assertRaises(TypeError):
            raise TypeError

    def test_catches_type_error_with_message_should_ignore_message(self):
        with assertRaises(TypeError):
            raise TypeError('test')

    def test_messages_differ_should_reraise_exception(self):
        with self.assertRaises(TypeError):
            with assertRaises(TypeError, msg='test'):
                raise TypeError('Test')

    def test_same_messages_same_exception_should_catch_it(self):
        with assertRaises(TypeError, msg='test'):
            raise TypeError('test')

    def test_multiple_exception_types_should_catch_them(self):
        with assertRaises(TypeError, ValueError):
            raise ValueError

        with assertRaises(TypeError, ValueError):
            raise TypeError

    def test_multiple_exceptions_should_ignore_message(self):
        with assertRaises(TypeError, ValueError):
            raise ValueError('test')

        with assertRaises(TypeError, ValueError):
            raise TypeError('test')

    def test_multiple_exceptions_wrong_message_should_reraise(self):
        with self.assertRaises(ValueError):
            with assertRaises(TypeError, ValueError, msg='test'):
                raise ValueError('Test')

        with self.assertRaises(TypeError):
            with assertRaises(TypeError, ValueError, msg='test'):
                raise TypeError('Test')

    def test_multiple_excpetions_same_message_should_catch_them(self):
        with assertRaises(TypeError, ValueError, msg='test'):
            raise ValueError('test')
        
        with assertRaises(TypeError, ValueError, msg='test'):
            raise ValueError('test')

