import os
from unittest import TestCase

import xlrd

from sw_excel_parser import parsers
from sw_excel_parser import fields


class ParserTestCase(TestCase):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_book.xls')

    def setUp(self):
        self.workbook = xlrd.open_workbook(self.file_path)

        class TestParser(parsers.Parser):
            foo = fields.CharField(header='foo')
            bar = fields.CharField(header='bar')
            baz = fields.CharField(header='baz')

        self.parser_class = TestParser
        self.parser = self.parser_class(workbook=self.workbook)

    def test_constructor(self):
        with open(self.file_path, 'rb') as workbook_file:
            file_contents = workbook_file.read()

        self.assertEqual(self.workbook, self.parser.workbook)

        parser = self.parser_class(file_contents=file_contents)
        self.assertEqual(self.workbook.sheet_names(), parser.workbook.sheet_names())

        with self.assertRaises(ValueError) as e:
            self.parser_class().parse()

        self.assertEqual(str(e.exception), 'You must provide workbook or file_contents')

    def test_find_headers(self):
        self.assertEqual(list(self.parser.find_headers().values()), [4, 1])

    def test_get_header(self):
        self.assertEqual(self.parser.get_header(self.workbook.sheets()[0]), ['', '', 'Foo ', '  Bar ', 'Baz'])

    def test_parse(self):
        self.parser.parse()
        self.assertEqual(len(self.parser.sheet_items.values()), 2)

    def test_is_recognized(self):
        self.assertTrue(self.parser.is_recognized())
