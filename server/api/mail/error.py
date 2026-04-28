from typing import TypeVar

T = TypeVar('T')
class InvalidCalendarAddress(ValueError):
    def __init__(self, message):
        super().__init__(message)

class InvalidMailAddressParameter(ValueError):
    def __init__(self, message):
        super().__init__(message)

class UndeliverableMailAddress(ValueError):
    def __init__(self, message):
        super().__init__(message)

def invalid_parameter_error_message(_class: type[T], param_name: str) -> str:
    return f'Invalid Parameter Error. The provided {param_name} is not a valid {_class.__name__}'
