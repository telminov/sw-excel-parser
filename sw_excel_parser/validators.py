class ValidationError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)


class RequiredValidator:
    message = 'Это поле обязательно.'

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message

    def __call__(self, field, value):
        if field.required and not value:
            raise ValidationError(self.message)

        return value
