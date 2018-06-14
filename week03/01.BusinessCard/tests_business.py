import unittest
import os
import json

from business import *


TEST_JSON = """
{
    "people": [{
        "first_name": "Ivo",
        "last_name": "Ivo",
        "age": 25,
        "birth_date": "05/05/2005",
        "birth_place": "Sofia",
        "gender": "male",
        "interests": ["eating", "sleeping", "programming", "skiing"],
        "avatar": "ivo.png",
        "skills": [{
            "name": "C++",
            "level": 30
        }, {
            "name": "PHP",
            "level": 25
        }, {
            "name": "Python",
            "level": 80
        }, {
            "name": "C#",
            "level": 25
        }]
    }, {
        "first_name": "Rado",
        "last_name": "Rado",
        "age": 26,
        "birth_date": "06/06/2006",
        "birth_place": "Pleven",
        "gender": "male",
        "interests": ["eating", "sleeping", "programming", "snowboarding"],
        "avatar": "rado.png",
        "skills": [{
            "name": "C++",
            "level": 20
        }, {
            "name": "PHP",
            "level": 37
        }, {
            "name": "Haskell",
            "level": 70
        }, {
            "name": "Java",
            "level": 50
        }, {
            "name": "C#",
            "level": 10
        }, {
            "name": "JavaScript",
            "level": 60
        }]
    }, {
        "first_name": "Radina",
        "last_name": "Radina",
        "age": 26,
        "birth_date": "06/06/2006",
        "birth_place": "Pleven",
        "gender": "female",
        "interests": ["eating", "sleeping", "programming", "snowboarding"],
        "avatar": "rado.png",
        "skills": [{
            "name": "C++",
            "level": 20
        }, {
            "name": "PHP",
            "level": 37
        }, {
            "name": "Haskell",
            "level": 70
        }, {
            "name": "Java",
            "level": 50
        }, {
            "name": "C#",
            "level": 10
        }, {
            "name": "JavaScript",
            "level": 60
        }]
    }]
}
"""


class GenHeadTests(unittest.TestCase):
    def setUp(self):
        with open('test_json', 'r') as f:
            self.data = json.load(f)['people']

    def test_title_should_be_full_name(self):
        expected_names = ['Ivo Ivo', 'Rado Rado']
        inputs = [self.data[0], self.data[1]]

        for fx, x in zip(expected_names, inputs):
            actual = gen_head(x)
            self.assertIsInstance(actual, list)
            actual = [x.strip() for x in actual]
            self.assertTrue(f'<title>{fx}</title>' in actual,
                             msg=f'<title>{fx}</title> not found in head')

    def test_title_should_be_only_one(self):
        inputs = [self.data[0], self.data[1]]

        for x in inputs:
            actual = gen_head(x)
            self.assertIsInstance(actual, list)

            count = sum(True for x in actual if '<title>' in x)
            self.assertEqual(count, 1)

    def test_should_be_valid_head(self):
        actual = gen_head(self.data[0])
        expected = ['<head>',
                    '<title>Ivo Ivo</title>',
                    '<link rel="stylesheet" type="text/css" href="styles.css">',
                    '</head>']

        self.assertEqual(actual, expected)


class GenBaseInfoTests(unittest.TestCase):
    def setUp(self):
        with open('test_json', 'r') as f:
            self.data = json.load(f)['people']

    def test_should_work_correctly(self):
        inputs = [self.data[0], self.data[1]]
        for x in inputs:
            age = x.get('age')
            birth_date = x.get('birth_date')
            birth_place = x.get('birth_place')
            gender = x.get('gender')

            expected = ['<div class="base-info">',
                        f'<p>Age: {age}</p>',
                        f'<p>Birth date: {birth_date}</p>',
                        f'<p>Birth place: {birth_place}</p>',
                        f'<p>Gender: {gender}</p>',
                        '</div>']

            actual = gen_base_info(x)
            self.assertEqual([x.strip() for x in actual], expected)


class GenInterestsTests(unittest.TestCase):
    def setUp(self):
        with open('test_json', 'r') as f:
            self.data = json.load(f)['people']

    def test_list_items_should_be_correct(self):
        inputs = [self.data[0], self.data[2]]  # Ivo, Radina
        for x in inputs:
            actual = gen_interests(x)
            self.assertIsInstance(actual, list)
            actual = [x.strip() for x in actual]
            interests = [f'<li>{_in}</li>' for _in in x.get('interests')]
            for li in interests:
                self.assertIn(li, actual)

    def test_should_be_correct(self):
        expected = ['<div class="interests">',
                    '<h2>Interests:</h2>',
                    '<ul>',
                    '<li>eating</li>',
                    '<li>sleeping</li>',
                    '<li>programming</li>',
                    '<li>skiing</li>',
                    '</ul>',
                    '</div>']
        self.assertEqual([x.strip() for x in gen_interests(self.data[0])], expected)


class GenSkillsTests(unittest.TestCase):
    def setUp(self):
        with open('test_json', 'r') as f:
            self.data = json.load(f)['people']

    def test_should_contain_correct_list_items_at_least_once(self):
        inputs = [self.data[0], self.data[1]]

        for x in inputs:
            expected = [f"<li>{entry['name']} - {entry['level']}</li>" for entry in x['skills']]
            actual = gen_skills(x)
            actual = [x.strip() for x in actual]
            for line in expected:
                self.assertIn(line, actual)

    def test_whole_div_should_be_correct(self):
        expected = ['<div class="skills">',
                    '<h2>Skills:</h2>',
                    '<ul>',
                    '<li>C++ - 30</li>',
                    '<li>PHP - 25</li>',
                    '<li>Python - 80</li>',
                    '<li>C# - 25</li>',
                    '</ul>',
                    '</div>']

        actual = gen_skills(self.data[0])

        self.assertEqual([x.strip() for x in actual], expected)









        pass


class GenBodyTests(unittest.TestCase):
    def setUp(self):
        with open('test_json', 'r') as f:
            self.data = json.load(f)['people']

    def test_business_card_div_should_have_male_classname(self):
        actual = gen_body(self.data[0])  # Ivo

        gender = self.data[0]['gender']
        self.assertIsInstance(actual, list)
        self.assertIn(f'<div class="business-card {gender}">', actual)

    def test_business_card_div_should_have_female_classname(self):
        actual = gen_body(self.data[2])  # Radina

        gender = self.data[2]['gender']
        self.assertIsInstance(actual, list)
        self.assertIn(f'<div class="business-card {gender}">', actual)


class GenHTMLTests(unittest.TestCase):
    def setUp(self):
        with open('test_json', 'r') as f:
            self.data = json.load(f)['people']

    def test_should_be_correct(self):
        x = self.data[0]  # Ivo

        with open('test_whole_html_ivo.html', 'r') as f:
            expected = f.readlines()

        # import pdb; pdb.set_trace()
        expected = [x.strip() for x in expected]
        actual = gen_html(x)
        for i, x in enumerate(zip(actual, expected)):
            if x[0] != x[1]:
                print(i)
            self.assertEqual(x[0], x[1])

        # self.assertEqual(actual, expected)

if __name__ == '__main__':
    with open('test_json', 'w') as f:
        f.write(TEST_JSON)

    unittest.main(exit=False)

    os.remove('test_json')
