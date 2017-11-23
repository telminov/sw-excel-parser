import random
from unittest import TestCase

from sw_excel_parser import fields
from sw_excel_parser import items
from sw_excel_parser import validators


class BaseFieldsTestCase(TestCase):
    def setUp(self):
        class TestItem(items.Item):
            foo = fields.Field(header='foo', required=True)
            bar = fields.Field(header='bar', required=False)

        self.test_item_class = TestItem
        self.test_item = self.test_item_class(row=random.randint(1, 100))
        self.fields_data = dict(foo='   foo ', bar=' bar  ')

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


    def test_field_extract(self):
        self.assertEqual(self.test_item.foo.extract_data(self.fields_data), self.fields_data['foo'])
        self.assertEqual(self.test_item.foo.extract_data(dict(bar='  bar ')), None)


    def test_field_to_python(self):
        self.assertEqual(self.test_item.foo.to_python(self.fields_data['foo']), self.fields_data['foo'])


    def test_field_run_validators(self):
        self.assertEqual(self.test_item.foo.run_validators(self.fields_data['foo']), self.fields_data['foo'])
        with self.assertRaises(validators.ValidationError) as e:
            self.test_item.foo.run_validators(value=None)

        self.assertEqual(str(e.exception), validators.RequiredValidator.message)

    def test_field_clean(self):
        self.assertEqual(self.test_item.foo.clean(self.fields_data), self.fields_data['foo'])

