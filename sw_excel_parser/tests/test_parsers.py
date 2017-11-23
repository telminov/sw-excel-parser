import os
import hashlib
from unittest import TestCase

import xlrd

from sw_excel_parser import parsers
from sw_excel_parser import items
from sw_excel_parser import fields


class ParserTestCase(TestCase):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_book.xls')
    test_book_md5 = '5e1b0b29b7380adaef7fd1fb340b5273'

    @classmethod
    def setUpClass(cls):
        with open(cls.file_path, 'rb') as workbook_file:
            message = 'File test_book.xls has been changed since the last revision tests.'
            assert hashlib.md5(workbook_file.read()).hexdigest() == cls.test_book_md5, message

    def setUp(self):
        self.workbook = xlrd.open_workbook(self.file_path)

        class TestItem(items.Item):
            foo = fields.CharField(header='foo')
            bar = fields.CharField(header='bar')
            baz = fields.CharField(header='baz')

        class TestParser(parsers.Parser):
            item = TestItem

        self.item_class = TestItem
        self.parser_class = TestParser
        self.parser = self.parser_class(workbook=self.workbook)

    def test_constructor(self):
        with open(self.file_path, 'rb') as workbook_file:
            file_contents = workbook_file.read()

        self.assertEqual(self.workbook, self.parser.workbook)

        parser = self.parser_class(file_contents=file_contents)
        self.assertEqual(self.workbook.sheet_names(), parser.workbook.sheet_names())

        with self.assertRaises(ValueError) as e:
            self.parser_class()

        self.assertEqual(str(e.exception), 'You must provide workbook or file_contents')

    def test_find_headers(self):
        self.assertEqual(list(self.parser.find_headers().values()), [0, 1])

    def test_get_header(self):
        self.assertEqual(self.parser.get_header(self.workbook.sheets()[0]), ['Foo ', '  Bar ', 'Baz'])

    def test_parse(self):
        self.parser.parse()
        self.assertEqual(len(self.parser.sheet_items.values()), 2)

    def test_is_recognized(self):
        self.assertTrue(self.parser.is_recognized())
