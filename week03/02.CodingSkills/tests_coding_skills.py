from coding_skills import extract_people, parse_json, extract_languages, get_best_people
import unittest
import json
import os

FNAME = 'test.json'
TEST_JSON = """
{
    "people": [{
        "first_name": "Ivo",
        "last_name": "Ivo",
        "skills": [{
            "name": "C++",
            "level": 25
        }, {
            "name": "Python",
            "level": 50
        }]
    }, {
        "first_name": "Gosho",
        "last_name": "Gosho",
        "skills": [{
            "name": "C++",
            "level": 50
        }, {
            "name": "Python",
            "level": 50
        }]
    }, {
        "first_name": "Pesho",
        "last_name": "Pesho",
        "skills": [{
            "name": "PHP",
            "level": 25
        }, {
            "name": "Python",
            "level": 50
        }]
    }]
}
"""


class LoadJSONTests(unittest.TestCase):
    def setUp(self):
        with open(FNAME, 'w') as f:
            f.write(TEST_JSON)

    def test_should_return_dict(self):
        self.assertIsInstance(parse_json(FNAME), dict)

    def test_dict_should_have_key_people(self):
        self.assertNotEqual(parse_json(FNAME).get('people'), None)

    def test_person_count_should_be_3(self):
        self.assertEqual(len(parse_json(FNAME).get('people')), 3)

    def tearDown(self):
        os.remove(FNAME)


class ExtractPeopleTests(unittest.TestCase):
    def setUp(self):
        with open(FNAME, 'w') as f:
            f.write(TEST_JSON)

        self.test_dict = parse_json(FNAME)
        self.actual = extract_people(self.test_dict)

    def test_should_return_list(self):
        self.assertIsInstance(self.actual, list)

    def test_return_list_count_should_be_three(self):
        self.assertEqual(len(extract_people(self.test_dict)), 3)

    def test_all_elements_should_be_dicts_non_empty_list(self):
        self.assertNotEqual(len(self.actual), 0)
        self.assertTrue(all(type(x) is dict for x in self.actual))

    def test_all_elements_should_have_first_and_last_name_non_empty_list(self):
        self.assertNotEqual(len(self.actual), 0)
        self.assertTrue(all(x.get('first_name') is not None for x in self.actual))
        self.assertTrue(all(x.get('last_name') is not None for x in self.actual))

    def tearDown(self):
        os.remove(FNAME)


class ExtractLanguagesTests(unittest.TestCase):
    def setUp(self):
        with open(FNAME, 'w') as f:
            f.write(TEST_JSON)

        with open(FNAME, 'r') as f:
            self.test_list = json.load(f)['people']

    def tearDown(self):
        os.remove(FNAME)

    def test_valid_input_dict_keys_should_be_equal(self):
        actual = extract_languages(self.test_list)
        expected = {
                'C++': [],
                'Python': [],
                'PHP': []
                }
        self.assertEqual(actual.keys(), expected.keys())

    def test_valid_input_dicts_should_be_equal(self):
        actual = extract_languages(self.test_list)
        expected = {
                'C++': [('Ivo Ivo', 25), ('Gosho Gosho', 50)],
                'Python': [('Ivo Ivo', 50), ('Gosho Gosho', 50),
                           ('Pesho Pesho', 50)],
                'PHP': [('Pesho Pesho', 25)]
                }

        self.assertEqual(actual, expected)


class GetBestPeopleTests(unittest.TestCase):
    def setUp(self):
        self.test_list = {
                'C++': [('Ivo Ivo', 25), ('Gosho Gosho', 50)],
                'Python': [('Ivo Ivo', 50), ('Gosho Gosho', 50),
                           ('Pesho Pesho', 50)],
                'PHP': [('Pesho Pesho', 25)]
                }

    def test_should_return_correct_result(self):
        expected = {
                'C++': 'Gosho Gosho',
                'Python': 'Ivo Ivo',
                'PHP': 'Pesho Pesho'
                }
        actual = get_best_people(self.test_list)

        self.assertEqual(actual, expected)
        
