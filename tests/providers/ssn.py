#  -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
import re

from faker import Factory
from faker.providers.ssn.hr_HR import Provider as HrProvider, checksum as hr_checksum
from faker.providers.ssn.pt_BR import Provider as PtProvider, checksum as pt_checksum
from faker.providers.ssn.en_US import Provider as EnProvider
from faker.providers.ssn.nl_BE import Provider as NlProvider


class TestEnUS(unittest.TestCase):

    def test_ssn_valid(self):
        provider = EnProvider(None)
        for i in range(1000):
            ssn = provider.ssn()
            self.assertEqual(len(ssn), 11)
            self.assertNotEqual(ssn[0], '9')
            self.assertNotEqual(ssn[0:3], '666')
            self.assertNotEqual(ssn[0:3], '000')
            self.assertNotEqual(ssn[4:6], '00')
            self.assertNotEqual(ssn[7:11], '0000')


class TestNlBE(unittest.TestCase):

    def test_nl_BE_ssn_valid(self):
        provider = NlProvider(None)

        for i in range (1000):
            ssn = provider.ssn()
            self.assertEqual(len(ssn), 11)
            gen_ssn_base = ssn[0:6]
            gen_seq = ssn[6:9]
            gen_chksum = ssn[9:11]
            gen_seq_as_int = int(gen_seq)
            gen_chksum_as_int = int(gen_chksum)
            # Check that the sequence nr is between 1 inclusive and 998 inclusive
            self.assertGreater(gen_seq_as_int,0)
            self.assertLessEqual(gen_seq_as_int, 998)

            # validate checksum calculation
            # Since the century is not part of ssn, try both below and above year 2000
            ssn_below = int(ssn[0:9])
            chksum_below = 97 - (ssn_below % 97)
            ssn_above = ssn_below + 2000000000
            chksum_above = 97 - (ssn_above % 97)
            results = [chksum_above, chksum_below]
            self.assertIn(gen_chksum_as_int,results)


class TestHrHR(unittest.TestCase):
    """ Tests SSN in the hr_HR locale """

    def setUp(self):
        self.factory = Factory.create('hr_HR')

    def test_ssn_checksum(self):
        self.assertEqual(hr_checksum([0, 0, 2, 2, 8, 2, 6, 9, 2, 8]), 9)
        self.assertEqual(hr_checksum([5, 8, 9, 3, 6, 9, 5, 1, 2, 5]), 1)
        self.assertEqual(hr_checksum([5, 7, 8, 0, 2, 0, 3, 4, 2, 3]), 7)
        self.assertEqual(hr_checksum([4, 3, 3, 3, 1, 4, 6, 7, 6, 2]), 2)
        self.assertEqual(hr_checksum([0, 5, 9, 3, 7, 7, 5, 9, 1, 8]), 7)
        self.assertEqual(hr_checksum([7, 1, 1, 4, 9, 9, 1, 2, 4, 1]), 6)

    def test_ssn(self):
        for i in range(100):
            self.assertTrue(re.search(r'^\d{11}$', HrProvider.ssn()))


class TestPtBR(unittest.TestCase):

    def setUp(self):
        self.factory = Factory.create('pt_BR')

    def test_pt_BR_ssn_checksum(self):
        self.assertEqual(pt_checksum([8, 8, 2, 8, 2, 1, 6, 5, 2]), 2)
        self.assertEqual(pt_checksum([8, 8, 2, 8, 2, 1, 6, 5, 2, 2]), 1)

    def test_pt_BR_ssn(self):
        for _ in range(100):
            self.assertTrue(re.search(r'^\d{11}$', PtProvider.ssn()))

    def test_pt_BR_cpf(self):
        for _ in range(100):
            self.assertTrue(re.search(r'\d{3}\.\d{3}\.\d{3}\-\d{2}', PtProvider.cpf()))

