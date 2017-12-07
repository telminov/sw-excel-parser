from unittest import TestCase
from unittest import mock

from sw_excel_parser import fields
from sw_excel_parser import validators


class RequiredValidatorTestCase(TestCase):
    def setUp(self):
        self.validator = validators.RequiredValidator()
        self.field = mock.Mock(spec=fields.Field, required=True)

    def test_validator(self):
        value = 'testValue'
        self.assertEqual(self.validator(self.field, value), value)

        with self.assertRaises(validators.ValidationError) as e:
            self.validator(self.field, None)

        self.assertEqual(str(e.exception), self.validator.message)


class MinValueValidatorTestCase(TestCase):
    def setUp(self):
        self.validator = validators.MinValueValidator()
        self.min_value = 10
        self.field = mock.Mock(spec=fields.IntegerField, min_value=self.min_value)

    def test_validator(self):
        self.assertEqual(self.validator(self.field, self.min_value), self.min_value)

        with self.assertRaises(validators.ValidationError) as e:
            self.validator(self.field, -self.min_value)

        self.assertEqual(str(e.exception), self.validator.message)


class MaxValueValidator(TestCase):
    def setUp(self):
        self.validator = validators.MaxValueValidator()
        self.max_value = 10
        self.field = mock.Mock(spec=fields.IntegerField, max_value=self.max_value)

    def test_validator(self):
        self.assertEqual(self.validator(self.field, self.max_value), self.max_value)

        with self.assertRaises(validators.ValidationError) as e:
            self.validator(self.field, self.max_value * 2)

        self.assertEqual(str(e.exception), self.validator.message)


class EmailValidatorTestCase(TestCase):
    def setUp(self):
        self.validator = validators.EmailValidator()
        self.field = mock.Mock(spec=fields.EmailField)

    def test_validator(self):
        value = 'foo_bar@baz.qoox'
        self.assertEqual(self.validator(self.field, value), value)

        with self.assertRaises(validators.ValidationError) as e:
            self.validator(self.field, 'wrong_email')

        self.assertEqual(str(e.exception), self.validator.message)
