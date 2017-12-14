import random
from unittest import TestCase
from unittest import mock

from sw_excel_parser import fields
from sw_excel_parser import items


class ItemTestCase(TestCase):
    def test_empty_item(self):
        class TestEmptyItem(items.Item):
            pass

        self.assertTrue(hasattr(TestEmptyItem, '_unbound_fields'))
        self.assertFalse(hasattr(TestEmptyItem, '_fields'))
        self.assertEqual(TestEmptyItem._unbound_fields, {})

        item = TestEmptyItem(nrow=random.randint(1, 100))

        self.assertTrue(hasattr(item, 'fields'))
        self.assertEqual(item.fields, {})

    def test_item(self):
        class TestItem(items.Item):
            foo = fields.Field(header='foo')
            bar = fields.Field(header='bar')

            def clean_foo(self, value):
                return value

        self.assertTrue(hasattr(TestItem, '_unbound_fields'))
        self.assertFalse(hasattr(TestItem, 'fields'))
        self.assertEqual(len(TestItem._unbound_fields), 2)
        self.assertTrue(all(isinstance(field, fields.UnboundField) for field in TestItem._unbound_fields.values()))

        item = TestItem(nrow=random.randint(1, 100), data=dict(foo='foo', bar='bar'))

        self.assertTrue(hasattr(item, 'fields'))
        self.assertEqual(len(item.fields), 2)
        self.assertTrue(all(isinstance(field, fields.Field) for field in item.fields.values()))
        self.assertTrue(item.is_valid())

        with mock.patch.object(TestItem, 'clean_foo') as mocked_cleaner:
            mocked_item = TestItem(nrow=random.randint(1, 100), data=dict(foo='foo'))
            self.assertFalse(mocked_item.is_valid())

        mocked_cleaner.assert_called_with('foo')
