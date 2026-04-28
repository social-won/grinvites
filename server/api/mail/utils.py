from enum import Enum
from typing import TypeVar
from iso639.exceptions import InvalidLanguageValue
from iso639 import Lang

T = TypeVar('T', bound=Enum)

def get_enum_value(enum_class : type[T], value : str | T) -> str:
    if isinstance(value, enum_class):
        return value.value
    elif isinstance(value, str):
        try:
            return enum_class(value).value
        except:
            raise ValueError(f'{value} is not a valid {enum_class.__name__}')
    else:
        raise TypeError(f'Received {value.__name__} but expected {enum_class.__name__} or string.')

def get_iso639_language_name(language: str | Lang ) -> str:
    if isinstance(language, Lang):
        return language.name
    else:
        try:
            return Lang(language.lower().capitalize()).name
        except InvalidLanguageValue:
            raise InvalidLanguageValue()