import random
from unittest import TestCase

from sw_excel_parser import fields
from sw_excel_parser import items


class ItemTestCase(TestCase):
    def test_empty_item(self):
        class TestEmptyItem(items.Item):
            pass

        self.assertTrue(hasattr(TestEmptyItem, '_unbound_fields'))
        self.assertFalse(hasattr(TestEmptyItem, '_fields'))
        self.assertEqual(TestEmptyItem._unbound_fields, {})

        item = TestEmptyItem(row=random.randint(1, 100))

        self.assertTrue(hasattr(item, '_fields'))
        self.assertEqual(item._fields, {})

    def test_item(self):
        class TestItem(items.Item):
            foo = fields.Field(header='foo')
            bar = fields.Field(header='bar')

        self.assertTrue(hasattr(TestItem, '_unbound_fields'))
        self.assertFalse(hasattr(TestItem, '_fields'))
        self.assertEqual(len(TestItem._unbound_fields), 2)
        self.assertTrue(all(isinstance(field, fields.UnboundField) for field in TestItem._unbound_fields.values()))

        item = TestItem(row=random.randint(1, 100))

        self.assertTrue(hasattr(item, '_fields'))
        self.assertEqual(len(item._fields), 2)
        self.assertTrue(all(isinstance(field, fields.Field) for field in item._fields.values()))
