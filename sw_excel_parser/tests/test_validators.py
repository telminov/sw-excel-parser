import random
from unittest import TestCase
from unittest import mock

from sw_excel_parser import validators


class RequiredValidatorTestCase(TestCase):
    def setUp(self):
        self.validator = validators.RequiredValidator()

        self.item = mock.Mock()
        self.item.required = True


    def test_validator(self):
        value = 'testValue'
        self.assertEqual(self.validator(self.item, value), value)

        with self.assertRaises(validators.ValidationError) as e:
            self.validator(self.item, None)

        self.assertEqual(str(e.exception), self.validator.message)


class MinValueValidatorTestCase(TestCase):
    def setUp(self):
        self.validator = validators.MinValueValidator()

        self.min_value = random.randint(1, 100)
        self.item = mock.Mock()
        self.item.min_value = self.min_value

    def test_validator(self):
        value = random.randint(self.min_value, 200)
        self.assertEqual(self.validator(self.item, value), value)

        with self.assertRaises(validators.ValidationError) as e:
            self.validator(self.item, self.min_value - random.randint(1, 100))

        self.assertEqual(str(e.exception), self.validator.message)


class MaxValueValidator(TestCase):
    def setUp(self):
        self.validator = validators.MaxValueValidator()

        self.max_value = random.randint(1, 100)
        self.item = mock.Mock()
        self.item.max_value = self.max_value

    def test_validator(self):
        value = random.randint(-100 , self.max_value)
        self.assertEqual(self.validator(self.item, value), value)

        with self.assertRaises(validators.ValidationError) as e:
            self.validator(self.item, self.max_value + random.randint(1, 100))

        self.assertEqual(str(e.exception), self.validator.message)


class EmailValidatorTestCase(TestCase):
    def setUp(self):
        self.validator = validators.EmailValidator()
        self.item = mock.Mock()

    def test_validator(self):
        value = 'foo_bar@baz.qoox'
        self.assertEqual(self.validator(self.item, value), value)

        with self.assertRaises(validators.ValidationError) as e:
            self.validator(self.item, 'wrong_email')

        self.assertEqual(str(e.exception), self.validator.message)
