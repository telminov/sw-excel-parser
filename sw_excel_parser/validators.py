import re

class ValidationError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)


class Validator():
    message = None

    def __init__(self, message: str = None, *args, **kwargs):
        if message is not None:
            self.message = message


class RequiredValidator(Validator):
    message = 'Это поле обязательно.'

    def __call__(self, field, value):
        if field.required and not value:
            raise ValidationError(self.message)

        return value


class MinValueValidator(Validator):
    message = 'Значение меньше допустимого.'

    def __call__(self, field, value):
        if field.min_value and value < field.min_value:
            raise ValidationError(self.message)

        return value


class MaxValueValidator(Validator):
    message = 'Значение больше допустимого.'

    def __call__(self, field, value):
        if field.max_value and value > field.max_value:
            raise ValidationError(self.message)

        return value


class EmailValidator(Validator):
    message = 'Невалидный email адрес.'
    regexp = re.compile('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$')

    def __call__(self, field, value):
        if not self.regexp.match(value):
            raise ValidationError(self.message)

        return value
