from collections import OrderedDict
from itertools import chain
from typing import List, Dict, Optional

import xlrd
from xlrd.sheet import Sheet


class BaseEngine:
    item = None

    def __init__(self, workbook: xlrd.Book = None, file_contents: bytes = None, *args, **kwargs):
        if file_contents:
            self.workbook = xlrd.open_workbook(file_contents=file_contents)
        elif workbook:
            self.workbook = workbook
        else:
            raise ValueError('You must provide workbook or file_contents')

        self.sheet_items = OrderedDict()

    def __iter__(self):
        return iter(self.sheet_items.items())

    def keys(self):
        return self.sheet_items.keys()

    def items(self):
        return self.sheet_items.items()

    def values(self):
        return self.sheet_items.values()

    def get_sheets(self) -> List[Sheet]:
        return self.workbook.sheets()

    def find_headers(self) -> Dict[Sheet, Optional[int]]:
        sheets = self.get_sheets()
        fields = self.item._unbound_fields.values()
        header = {field.kwargs['header'].lower() for field in fields}

        result = OrderedDict()
        for sheet in sheets:
            sheet_data = (sheet.row_values(nrow) for nrow in range(sheet.nrows))
            for nrow, row_values in enumerate(sheet_data):
                row_values = {str(field).lower().strip() for field in row_values}
                if row_values >= header:
                    result[sheet] = nrow
                    break

        return result

    def get_header(self, sheet) -> List[str] or None:
        header = None
        header_map = self.find_headers()
        if sheet in header_map:
            header_nrow = header_map[sheet]
            header = sheet.row_values(header_nrow)

        return header

    def prepare_items(self) -> None:
        header_map = self.find_headers()
        for sheet, header_nrow in header_map.items():
            data_offset = header_nrow + 1
            sheet_header = list(title.lower().strip() for title in self.get_header(sheet))
            sheet_data = list(sheet.row_values(nrow) for nrow in range(data_offset, sheet.nrows))

            if sheet_data:
                self.sheet_items[sheet] = []

            for nrow, row_data in enumerate(sheet_data, start=data_offset):
                item = self.item(nrow, dict(zip(sheet_header, row_data)))
                self.sheet_items[sheet].append(item)

    def parse(self) -> None:
        self.sheet_items.clear()
        self.prepare_items()

    def is_recognized(self) -> bool:
        headers_nrows = self.find_headers().values()

        return any(nrow is not None for nrow in headers_nrows)

    def get_cleaned_data(self):
        cleaned_data = OrderedDict()

        for sheet, items in self.sheet_items.items():
            sheet_name = sheet.name
            sheet_data = []
            for item in items:
                if item.cleaned_data:
                    sheet_data.append(item.cleaned_data)

            cleaned_data[sheet_name] = sheet_data

        return cleaned_data


class StatsMixin:
    def __init__(self, *args, **kwargs):
        super(StatsMixin, self).__init__(*args, **kwargs)
        self.stats = {}

    def parse(self):
        super().parse()
        self.compute_stats()

    def compute_stats(self):
        items = list(chain.from_iterable(self.sheet_items.values()))

        success_count = len([item for item in items if item.is_valid()])
        errors_count = len(items) - success_count
        erroneous_sheets = {sheet for sheet, items in self if any(not item.is_valid() for item in items)}

        self.stats = dict(
            total_count=len(items),
            success_count=success_count,
            errors_count=errors_count,
            erroneous_sheets=erroneous_sheets
        )


class Engine(StatsMixin, BaseEngine):
    pass
