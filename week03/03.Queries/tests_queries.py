import unittest
import os
from queries import *


class GetFieldsTests(unittest.TestCase):
    def test_should_work_correctly_with_one_actual_field(self):
        test_input = 'name'

        with open(TEST_FNAME, 'w') as f:
            f.write(test_input)

        with open(TEST_FNAME, 'r') as f:
            actual = get_fields(f)

        self.assertEqual(actual, ['name'])

    def test_should_work_correctly_with_two_actual_field(self):
        test_input = 'name,age'

        with open(TEST_FNAME, 'w') as f:
            f.write(test_input)

        with open(TEST_FNAME, 'r') as f:
            actual = get_fields(f)

        self.assertEqual(actual, ['name', 'age'])

    def test_should_work_correctly_with_no_fields(self):
        test_input = ''

        with open(TEST_FNAME, 'w') as f:
            f.write(test_input)

        with open(TEST_FNAME, 'r') as f:
            actual = get_fields(f)

        self.assertEqual(actual, [])


class BindFieldsTests(unittest.TestCase):
    def test_should_work_correctly_with_one_field(self):
        fields = ['name']
        expected = {'name': 0}
        actual = bind_fields_to_indeces(fields)

        self.assertEqual(actual, expected)

    def test_should_work_correctly_with_two_fields(self):
        fields = ['name', 'age']
        expected = {'name': 0, 'age': 1}
        actual = bind_fields_to_indeces(fields)

        self.assertEqual(actual, expected)


class FilterEqualsTests(unittest.TestCase):
    def test_first_field_should_match_2_lines_out_of_3(self):
        test_input = [['Test', 'pesho'], ['Test'], ['Should, not match']]
        f = gen_filters(fields_lookup={'first': 0}, first='Test')[0]

        self.assertTrue(f(test_input[0]))
        self.assertTrue(f(test_input[1]))
        self.assertFalse(f(test_input[2]))

    def test_first_field_should_match_0_lines(self):
        test_input = [['Test', 'pesho'], ['Test'], ['Should', 'not match']]
        f = gen_filters(fields_lookup={'first': 0}, first='NOMATCH')[0]

        self.assertFalse(f(test_input[0]))
        self.assertFalse(f(test_input[1]))
        self.assertFalse(f(test_input[2]))

    def test_last_field_should_match_2_lines(self):
        test_input = [['No', 'no', 'yes'], ['yes', 'nom', 'nom', 'no'], ['should', 'match', 'yes']]
        f = gen_filters(fields_lookup={'third': 2}, third='yes')[0]

        self.assertTrue(f(test_input[0]))
        self.assertFalse(f(test_input[1]))
        self.assertTrue(f(test_input[2]))


class FilterStartsWithTests(unittest.TestCase):
    def test_first_field_should_match_2_lines_out_of_3(self):
        test_input = [['match me', 'baby one more time'], ['I should not be doing this'], ['match', 'in the code']]
        f = gen_filters(fields_lookup={'first': 0}, first__startswith='match')[0]

        self.assertTrue(f(test_input[0]))
        self.assertFalse(f(test_input[1]))
        self.assertTrue(f(test_input[2]))

    def test_last_field_should_match_2_out_of_3(self):
        test_input = [['all', 'I', 'do is'], ['m', 'm', 'match'], ['m', 'm', 'match no matter what']]
        f = gen_filters(fields_lookup={'last': 2}, last__startswith='match')[0]

        self.assertFalse(f(test_input[0]))
        self.assertTrue(f(test_input[1]))
        self.assertTrue(f(test_input[2]))

    def test_should_match_none(self):
        test_input = [['no'], ['match'], ['hopefully']]
        f = gen_filters(fields_lookup={'no': 0}, no__startswith='MATCH')[0]

        self.assertFalse(f(test_input[0]))
        self.assertFalse(f(test_input[1]))
        self.assertFalse(f(test_input[2]))


class FilterContainsTests(unittest.TestCase):
    def test_first_field_should_match_4_out_of_4(self):
        test_input = [['match'], ['mmatch'], ['matchmatch'], ['!match']]
        f = gen_filters(fields_lookup={'first': 0}, first__contains='match')[0]

        self.assertTrue(f(test_input[0]))
        self.assertTrue(f(test_input[1]))
        self.assertTrue(f(test_input[2]))
        self.assertTrue(f(test_input[3]))

    def test_last_field_should_match_2_out_of_3(self):
        test_input = [['MATCH'], ['MMATCHH'], ['MATCha gotcha']]
        f = gen_filters(fields_lookup={'first': 0}, first__contains='MATCH')[0]

        self.assertTrue(f(test_input[0]))
        self.assertTrue(f(test_input[1]))
        self.assertFalse(f(test_input[2]))

    def test_should_match_none(self):
        test_input = [['nope', 'nope', 'nope'], ['nope', 'nope', 'nein'], ['nope', 'nooope', 'no']]
        f = gen_filters(fields_lookup={'second': 1}, second__contains='yes')[0]

        self.assertFalse(f(test_input[0]))
        self.assertFalse(f(test_input[1]))
        self.assertFalse(f(test_input[2]))


class FilterLessThanTests(unittest.TestCase):
    def test_second_field_should_match_2_lines_out_of_3(self):
        test_input = [['a', '15', 'c'], ['b', '23'], ['c', '33']]
        f = gen_filters(fields_lookup={'second': 1}, second__lt=33)[0]

        self.assertTrue(f(test_input[0]))
        self.assertTrue(f(test_input[1]))
        self.assertFalse(f(test_input[2]))

    def test_should_match_none(self):
        test_input = [['a', '15', 'c'], ['b', '23'], ['c', '33']]
        f = gen_filters(fields_lookup={'second': 1}, second__lt=10)[0]

        self.assertFalse(f(test_input[0]))
        self.assertFalse(f(test_input[1]))
        self.assertFalse(f(test_input[2]))


class FilterGreaterThanTests(unittest.TestCase):
    def test_second_field_should_match_2_lines_out_of_3(self):
        test_input = [['a', '15', 'c'], ['b', '23'], ['c', '33']]
        f = gen_filters(fields_lookup={'second': 1}, second__gt=15)[0]

        self.assertFalse(f(test_input[0]))
        self.assertTrue(f(test_input[1]))
        self.assertTrue(f(test_input[2]))

    def test_should_match_none(self):
        test_input = [['a', '15', 'c'], ['b', '23'], ['c', '33']]
        f = gen_filters(fields_lookup={'second': 1}, second__gt=33)[0]

        self.assertFalse(f(test_input[0]))
        self.assertFalse(f(test_input[1]))
        self.assertFalse(f(test_input[2]))


class CombinedFiltersTests(unittest.TestCase):
    def test_first_field_startswith_and_contains_should_match_1_out_of_3(self):
        test_input = [['test T'], ['T test'], ['test test']]
        filters = gen_filters(fields_lookup={'first': 0}, first__startswith='test', first__contains='T')

        self.assertTrue(apply_filters(filters, test_input[0]))
        self.assertFalse(apply_filters(filters, test_input[1]))
        self.assertFalse(apply_filters(filters, test_input[2]))

    def test_first_field_startswith_second_field_gt_match_1_ouf_of_3(self):
        test_input = [['test T', '101'], ['test t', '50'], ['TEST test', '101']]
        filters = gen_filters(fields_lookup={'first': 0, 'second': 1}, first__startswith='test', second__gt=100)

        self.assertTrue(apply_filters(filters, test_input[0]))
        self.assertFalse(apply_filters(filters, test_input[1]))
        self.assertFalse(apply_filters(filters, test_input[2]))

    def test_field_one_lt_and_gt_should_match_2_out_of_3(self):
        test_input = [['test T', '101'], ['test t', '50'], ['TEST test', '101']]
        filters = gen_filters(fields_lookup={'f': 0, 's': 1}, s__lt=150, s__gt=100)

        self.assertTrue(apply_filters(filters, test_input[0]))
        self.assertFalse(apply_filters(filters, test_input[1]))
        self.assertTrue(apply_filters(filters, test_input[2]))


TEST_FNAME = 'test_get_fields.csv'
if __name__ == '__main__':
    unittest.main(exit=False)
    os.remove(TEST_FNAME)
