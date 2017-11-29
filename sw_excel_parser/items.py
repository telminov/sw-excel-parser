from typing import Any, Dict

from sw_excel_parser import fields
from sw_excel_parser import validators


class ItemMeta(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)

        unbound_fields = {}
        for key, value in cls.__dict__.items():
            if isinstance(value, fields.UnboundField):
                unbound_fields[key] = value

        cls._unbound_fields = unbound_fields


class BaseItem:
    def __init__(self, fields, *args, **kwargs):
        self._fields = {}
        for name, unbound_field in fields.items():
            bound_field = unbound_field.bind(item=self, name=name)
            self._fields[name] = bound_field
            setattr(self, name, bound_field)


class Item(BaseItem, metaclass=ItemMeta):
    def __init__(self, row: int, data: Dict[str, Any] = None):
        super().__init__(fields=self._unbound_fields)
        self.row = row
        self.data = data or {}
        self.errors = {}
        self.cleaned_data = {}

        self.validate()

    def is_valid(self) -> bool:
        return not self.errors

    def validate(self) -> None:
        self.errors.clear()
        self.cleaned_data.clear()

        for name, field in self._fields.items():
            try:
                value = field.clean(self.data)
                field_cleaner = getattr(self, 'clean_{}'.format(name), None)
                if field_cleaner:
                    value = field_cleaner(value)

                self.cleaned_data[name] = value
            except validators.ValidationError as e:
                self.errors[name] = e
