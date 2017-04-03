#  -*- coding: utf-8 -*-

import unittest

from faker.providers.python import Provider


class TestPython(unittest.TestCase):

    def test_random_pystr_characters(self):
        provider = Provider(None)
        characters = provider.pystr()
        self.assertEqual(len(characters), 20)
        characters = provider.pystr(max_chars=255)
        self.assertEqual(len(characters), 255)
        characters = provider.pystr(max_chars=0)
        self.assertEqual(characters, '')
        characters = provider.pystr(max_chars=-10)
        self.assertEqual(characters, '')
        characters = provider.pystr(min_chars=10, max_chars=255)
        self.assertTrue((len(characters) >= 10))

    def test_random_pyfloat(self):
        provider = Provider(None)
        self.assertTrue(0 <= abs(provider.pyfloat(left_digits=1)) < 10)
        self.assertTrue(0 <= abs(provider.pyfloat(left_digits=0)) < 1)
        x = abs(provider.pyfloat(right_digits=0))
        self.assertTrue(x-int(x) == 0)
        with self.assertRaises(ValueError,
                               msg='A float number cannot have 0 digits '
                                   'in total'):
            provider.pyfloat(left_digits=0, right_digits=0)

