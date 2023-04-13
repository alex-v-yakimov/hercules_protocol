from typing import Union, Iterable, Type
from ctypes import c_char_p, c_uint8, c_int16, c_int32, c_int64, c_bool, c_float, c_double
import re
from uuid import UUID


LENGTH_OF_TAG_KEY = 255
MAX_VERSION = 1

PTypes = Union[
    dict,
    c_uint8,      # byte in C#/Java
    c_int16,      # short in C#/Java
    c_int32,      # int in C#/Java
    c_int64,      # long in C#/Java
    c_bool,
    c_float,
    c_double,
    c_char_p,
    UUID,
    None,
    'Vector'
]


class Vector(list):
    def __init__(self, value: Iterable[PTypes], type_: Type[PTypes]) -> None:
        if all(isinstance(e, type_) for e in value):
            self.type_ = type_
        else:
            raise ValueError('Vector has to have same type elements')

        super().__init__(value)

    def __repr__(self):
        return f'{type(self).__name__}({super().__repr__()}, type_={self.type_.__name__})'


def check_tag_key(key: str) -> str:
    if not isinstance(key, str):
        raise ValueError('The key has to be a string')

    if not key:
        raise ValueError("The key mustn't be a empty string")

    if len(key) > LENGTH_OF_TAG_KEY:
        raise ValueError(f'The length of the key has to be less or equal {LENGTH_OF_TAG_KEY}')

    regex = re.compile(r'\A[a-zA-Z0-9_.-]+\Z')
    if not bool(regex.match(key)):
        raise ValueError('Permitted characters of the key: "a-z", "A-Z", "0-9", "_", ".", "-"')

    return key


def check_version(version: int) -> None:
    if not isinstance(version, int):
        raise ValueError('The version has to be "int"')

    if not MAX_VERSION >= version > 0:
        raise ValueError(f'The version has to be less or equal than {MAX_VERSION} and greater than 0')


def check_timestamp(timestamp: int) -> None:
    if not isinstance(timestamp, int):
        raise ValueError('The timestamp has to be "int"')

    if timestamp < 0:
        raise ValueError('The timestamp has to be a positive number')
