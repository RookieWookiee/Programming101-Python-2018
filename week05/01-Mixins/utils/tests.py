import unittest
import json

from jsonable import JsonableMixin as Jsonable

class Car:
    pass


class Pet(Jsonable):
    def __init__(self):
        self.name = 'Bari'


class Person(Jsonable):
    def __init__(self):
        self.name = 'Ivan'
        self.age = 24
        self.weight = 79.5
        self.interests = ['x', 'y']
        self.family = {'mother': 'Ivanka', 'father': 'Ivan I'}
        self.employed = True
        self.girlfriend = None

    def __eq__(self):
        # TODO
        pass


class JsonableTests(unittest.TestCase):
    def setUp(self):
        self.test_person = Person()

    def test_to_json_works_with_simple_values(self):
        result = self.test_person.to_json()

        expected_value = {
            'class_name': self.test_person.__class__.__name__,
            'dict': self.test_person.__dict__
        }

        self.assertEqual(result, json.dumps(expected_value, indent=4))

    def test_to_json_works_with_instances_of_other_classes(self):
        self.test_person.pet = Pet()

        result = self.test_person.to_json()

        dict_ = self.test_person.__dict__
        dict_['pet'] = {
            'class_name': 'Pet',
            'dict': {'name': 'Bari'}
        }

        expected_value = {
            'class_name': self.test_person.__class__.__name__,
            'dict': dict_
        }

        self.assertEqual(result, json.dumps(expected_value, indent=4))

    def test_to_json_raises_value_error_if_there_is_a_notserializable_attribute(self):
        self.test_person.car = Car()

        with self.assertRaises(TypeError) as exc:
            self.test_person.to_json()
            self.assertEqual(exc.message, f'{self.test_person.car} is not JSON serializable')


if __name__ == '__main__':
    unittest.main()
