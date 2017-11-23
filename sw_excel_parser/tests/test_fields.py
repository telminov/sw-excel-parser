import uuid
import random
from unittest import TestCase

import dateutil.parser

from sw_excel_parser import fields
from sw_excel_parser import items
from sw_excel_parser import validators


class UnboundFieldTestCase(TestCase):
    def setUp(self):
        class TestItem(items.Item):
            foo = fields.Field(header='foo', required=True)
            bar = fields.Field(header='bar', required=False)

        self.test_item_class = TestItem
        self.test_item = self.test_item_class(row=random.randint(1, 100))

    def test_unbound_field(self):
        header = 'foo'
        field_args = (header,)
        field_kwargs = dict(required=False)

        unbound_field = fields.Field(header, **field_kwargs)

        self.assertIsInstance(unbound_field, fields.UnboundField)
        self.assertIs(unbound_field.field_class, fields.Field)

        self.assertEqual(field_kwargs, unbound_field.kwargs)
        self.assertEqual(field_args, unbound_field.args)

        field = unbound_field.bind(item=None, name='foo')

        self.assertIsInstance(field, fields.Field)
        self.assertTrue(field_kwargs.items() < field.__dict__.items())
        self.assertTrue(field.header == header)
        self.assertTrue(field_kwargs['required'] == field.required)

    def test_field(self):
        self.assertTrue(all(field._item is self.test_item) for field in self.test_item._fields.values())
        self.assertTrue(all(key == value._name for key, value in self.test_item._fields.items()))


class FieldTestCase(TestCase):
    def setUp(self):
        class TestItem(items.Item):
            foo = fields.Field(header='foo', required=True)
            bar = fields.Field(header='bar', required=False)

        self.test_item_class = TestItem
        self.test_item = self.test_item_class(row=random.randint(1, 100))
        self.fields_data = dict(foo='   foo ', bar=' bar  ')

    def test_field_extract(self):
        self.assertEqual(self.test_item.foo.extract_data(self.fields_data), self.fields_data['foo'])
        self.assertEqual(self.test_item.foo.extract_data(dict(bar='  bar ')), None)

    def test_field_to_python(self):
        self.assertEqual(self.test_item.foo.to_python(self.fields_data['foo']), self.fields_data['foo'])


class BooleanFieldTestCase(FieldTestCase):
    def setUp(self):
        class TestItem(items.Item):
            foo = fields.BooleanField(header='foo', false_values=['baz', 'quux'], required=True)
            bar = fields.BooleanField(header='bar', required=False)

        self.test_item_class = TestItem
        self.test_item = self.test_item_class(row=random.randint(1, 100))
        self.fields_data = dict(foo='baz', bar='-')

    def test_field_to_python(self):
        self.assertTrue(self.test_item.bar.to_python(self.fields_data['bar']))
        self.assertFalse(self.test_item.bar.to_python(''))

        self.assertTrue(self.test_item.foo.to_python('true'))
        self.assertFalse(self.test_item.foo.to_python(self.fields_data['foo']))
        self.assertFalse(self.test_item.foo.to_python('quux'))


class CharFieldTestCase(FieldTestCase):
    def setUp(self):
        class TestItem(items.Item):
            foo = fields.CharField(header='foo', required=True)
            bar = fields.BooleanField(header='bar', required=False)

        self.test_item_class = TestItem
        self.test_item = self.test_item_class(row=random.randint(1, 100))
        self.fields_data = dict(foo=' baz  ', bar=100)

    def test_field_to_python(self):
        self.assertEqual(self.test_item.foo.to_python(self.fields_data['foo']), self.fields_data['foo'].strip())


class DateFieldTestCase(FieldTestCase):
    def setUp(self):
        class TestItem(items.Item):
            foo = fields.DateField(header='foo', dayfirst=True)
            bar = fields.DateField(header='bar')

        self.test_item_class = TestItem
        self.test_item = self.test_item_class(row=random.randint(1, 100))
        self.fields_data = dict(foo='2011.05.05', bar='2011.05.05')

    def test_field_to_python(self):
        foo_expected_value = dateutil.parser.parse(self.fields_data['foo'], dayfirst=self.test_item.foo.dayfirst)
        bar_expected_value = dateutil.parser.parse(self.fields_data['bar'], dayfirst=self.test_item.bar.dayfirst)

        self.assertEqual(self.test_item.foo.to_python(self.fields_data['foo']), foo_expected_value)
        self.assertEqual(self.test_item.bar.to_python(self.fields_data['bar']), bar_expected_value)

        with self.assertRaises(validators.ValidationError) as e:
            self.test_item.foo.to_python('testDate')

        self.assertEqual(str(e.exception), 'Некорректное значение.')


class FloatFieldTestCase(FieldTestCase):
    def setUp(self):
        class TestItem(items.Item):
            foo = fields.FloatField(header='foo', min_value=10)
            bar = fields.FloatField(header='bar', max_value=100)

        self.test_item_class = TestItem
        self.test_item = self.test_item_class(row=random.randint(1, 100))
        self.fields_data = dict(foo='9.025', bar='100.001')

    def test_field_to_python(self):
        self.assertEqual(self.test_item.foo.to_python(self.fields_data['foo']), float(self.fields_data['foo']))
        self.assertEqual(self.test_item.foo.to_python(self.fields_data['bar']), float(self.fields_data['bar']))

        with self.assertRaises(validators.ValidationError) as e:
            self.test_item.foo.to_python('testFloat')

        self.assertEqual(str(e.exception), 'Некорректное значение.')


class IntegerFieldTestCase(FieldTestCase):
    def setUp(self):
        class TestItem(items.Item):
            foo = fields.IntegerField(header='foo')
            bar = fields.IntegerField(header='bar')

        self.test_item_class = TestItem
        self.test_item = self.test_item_class(row=random.randint(1, 100))
        self.fields_data = dict(foo=random.randint(0, 100), bar=random.randint(-100, 0))

    def test_field_to_python(self):
        self.assertEqual(self.test_item.foo.to_python(self.fields_data['foo']), int(self.fields_data['foo']))
        self.assertEqual(self.test_item.foo.to_python(self.fields_data['bar']), int(self.fields_data['bar']))

        with self.assertRaises(validators.ValidationError) as e:
            self.test_item.foo.to_python('testInt')

        self.assertEqual(str(e.exception), 'Некорректное значение.')


class EmailFieldTestCase(CharFieldTestCase):
    def setUp(self):
        class TestItem(items.Item):
            foo = fields.EmailField(header='foo')
            bar = fields.EmailField(header='bar')

        self.test_item_class = TestItem
        self.test_item = self.test_item_class(row=random.randint(1, 100))
        self.fields_data = dict(foo='  foo\\bar@baz.qoox ', bar=' qoox\\baz@bar.foo')


class UUIDFieldTestCase(FieldTestCase):
    def setUp(self):
        class TestItem(items.Item):
            foo = fields.UUIDField(header='foo', version=5)
            bar = fields.UUIDField(header='bar', version=4)

        self.test_item_class = TestItem
        self.test_item = self.test_item_class(row=random.randint(1, 100))
        self.fields_data = dict(foo=str(uuid.uuid5(uuid.NAMESPACE_URL, 'testUUID')), bar=str(uuid.uuid4()))

    def test_field_to_python(self):
        foo_expected_value = uuid.UUID(self.fields_data['foo'], version=self.test_item.foo.version)
        bar_expected_value = uuid.UUID(self.fields_data['bar'], version=self.test_item.bar.version)

        self.assertEqual(self.test_item.foo.to_python(self.fields_data['foo']), foo_expected_value)
        self.assertEqual(self.test_item.bar.to_python(self.fields_data['bar']), bar_expected_value)
