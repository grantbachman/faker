# coding=utf-8

from __future__ import unicode_literals

import unittest

from email_validator import validate_email

import re
from faker import Factory
from faker.providers.person.ja_JP import Provider as JaProvider
from faker.providers.internet import Provider
from faker.utils import text
from .. import string_types


class TestBaseInternet(unittest.TestCase):

    def test_ipv4(self):
        provider = Provider(None)

        for _ in range(999):
            address = provider.ipv4()
            self.assertTrue(len(address) >= 7)
            self.assertTrue(len(address) <= 15)
            self.assertTrue(
                re.compile(r'^(\d{1,3}\.){3}\d{1,3}$').search(address))

        for _ in range(999):
            address = provider.ipv4(network=True)
            self.assertTrue(len(address) >= 9)
            self.assertTrue(len(address) <= 18)
            self.assertTrue(
                re.compile(r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$').search(address))

    def test_ipv6(self):
        provider = Provider(None)

        for _ in range(999):
            address = provider.ipv6()
            self.assertTrue(len(address) >= 3)  # ::1
            self.assertTrue(len(address) <= 39)
            self.assertTrue(re.compile(r'^([0-9a-f]{0,4}:){2,7}[0-9a-f]{1,4}$').search(address))

        for _ in range(999):
            address = provider.ipv6(network=True)
            self.assertTrue(len(address) >= 4)  # ::/8
            self.assertTrue(len(address) <= 39 + 4)
            self.assertTrue(re.compile(r'^([0-9a-f]{0,4}:){2,7}[0-9a-f]{0,4}/\d{1,3}$').search(address))


class TestJaJP(unittest.TestCase):
    """ Tests internet in the ja_JP locale """

    def setUp(self):
        self.factory = Factory.create('ja')

    def test_internet(self):
        names = JaProvider.last_romanized_names

        domain_word = self.factory.domain_word()
        assert isinstance(domain_word, string_types)
        assert any(domain_word == text.slugify(name) for name in names)

        user_name = self.factory.user_name()
        assert isinstance(user_name, string_types)

        tld = self.factory.tld()
        assert isinstance(tld, string_types)


class TestZhCN(unittest.TestCase):

    def setUp(self):
        self.factory = Factory.create(locale='zh_CN')

    def test_email(self):
        email = self.factory.email()
        validate_email(email, check_deliverability=False)
