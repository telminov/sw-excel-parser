import uuid
import itertools
from typing import Any, Type, List, Dict

import dateutil.parser

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
    default_validators = [
        validators.RequiredValidator()
    ]

    def __new__(cls, *args, **kwargs):
        if '_item' and '_name' in kwargs:
            instance = super().__new__(cls)
        else:
            instance = UnboundField(cls, *args, **kwargs)

        return instance

    def __init__(self, header: str, required: bool = True, validators: List = list(), *args, **kwargs):
        self.header = header
        self.required = required
        self.validators = list(itertools.chain(self.default_validators, validators))
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
        val = self.to_python(self.value)
        return self.run_validators(val)


class BooleanField(Field):
    default_validators = []

    def __init__(self, *args , **kwargs):
        super().__init__(*args, **kwargs)
        self.false_values = kwargs.get('false_values')

    def to_python(self, value: Any):
        if value in self.false_values:
            value = False
        else:
            value = bool(value)

        return value


class CharField(Field):
    def to_python(self, value: Any):
        if value:
            if not isinstance(value, str):
                value = str(value).strip()

        return value


class DateField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dayfirst = kwargs.get('dayfirst', False)

    def to_python(self, value: Any):
        try:
            value = dateutil.parser.parse(value, dayfirst=self.dayfirst)
        except (ValueError, OverflowError):
            raise validators.ValidationError('Некорректное значение.')

        return value


class BaseNumericField(Field):
    default_validators = [
        validators.RequiredValidator(),
        validators.MinValueValidator(),
        validators.MaxValueValidator()
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_value = kwargs.get('min_value', None)
        self.max_value = kwargs.get('max_value', None)


class FloatField(BaseNumericField):
    def to_python(self, value: Any) -> float:
        if not isinstance(value, float):
            try:
                value = float(value)
            except ValueError:
                raise validators.ValidationError('Некорректное значение.')

        return value


class IntegerField(BaseNumericField):
    def to_python(self, value: Any) -> int:
        if not isinstance(value, int):
            try:
                value = float(value)
                if value.is_integer():
                    value = int(value)
                else:
                    raise validators.ValidationError('Значение не является целым.')
            except ValueError:
                raise validators.ValidationError('Некорректное значение.')

        return value


class EmailField(CharField):
    default_validators = [
        validators.RequiredValidator(),
        validators.EmailValidator()
    ]


class UUIDField(CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = kwargs.get('version', 4)

    def to_python(self, value: Any):
        try:
            value = uuid.UUID(value, version=self.version)
        except ValueError:
            raise validators.ValidationError('Некорректное значение.')

        return value
