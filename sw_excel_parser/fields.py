import itertools
from typing import Any, Type, List, Dict

from . import validators


class UnboundField:
    def __init__(self, field_class: Type['Field'], *args, **kwargs):
        self.field_class = field_class
        self.args = args
        self.kwargs = kwargs

    def bind(self, item, name: str) -> 'Field':
        return self.field_class(*self.args, **dict(self.kwargs, _item=item, _name=name))

    def __repr__(self):
        return '<{cls} ({field_cls} (args={args}, kwargs={kwargs}))>'.format(
            cls=self.__class__.__name__,
            field_cls=self.field_class.__name__,
            args=self.args,
            kwargs=self.kwargs
        )


class Field:
    default_validators = [validators.RequiredValidator()]

    def __new__(cls, *args, **kwargs):
        if '_item' and '_name' in kwargs:
            instance = super().__new__(cls)
        else:
            instance = UnboundField(cls, *args, **kwargs)

        return instance

    def __init__(self, header: str, required: bool = True, validators: List = list(), *args, **kwargs):
        self.header = header
        self.required = required
        self.validators = itertools.chain(self.default_validators, validators)
        self.value = None

        self._item = kwargs.get('_item')
        self._name = kwargs.get('_name')

    def run_validators(self, value: Any) -> Any:
        for validator in self.validators:
            value = validator(self, value)

        return value

    def to_python(self, value: Any) -> Any:
        return value

    def extract_data(self, data: Dict) -> Any:
        return data.get(self.header.lower())

    def clean(self, data: Dict) -> Any:
        self.value = self.extract_data(data)

        return self.run_validators(self.to_python(self.value))
