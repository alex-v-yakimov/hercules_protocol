from typing import Any, Union, Tuple
from abc import abstractmethod
from ctypes import c_char_p, c_uint8, c_int16, c_int32, c_int64, c_bool, c_float, c_double
from uuid import UUID
from ..datatypes import Vector


class SimpleRepr(type):
    def __repr__(cls):
        return cls.__name__


class Repr(metaclass=SimpleRepr):
    pass


class Value(Repr):
    @staticmethod
    @abstractmethod
    def verify(value: Any) -> None:
        pass


class Key(Repr, str):  # type: ignore # error: Metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases # noqa E501
    def __new__(cls, str_):
        instance = super().__new__(cls, str_)
        return instance

    def __init__(self, str_: str) -> None:
        self.bytes_ = len(str_).to_bytes(1, byteorder='big') + bytes(str_, 'ascii')
        self.str_ = str_

    def pack(self, key: str) -> bytes:
        if key != self.str_:
            raise ValueError('The key has to be equal {!r}'.format(self.str_))
        return self.bytes_

    def unpack(self, data: bytes, start: int) -> Tuple[int, str]:
        stop = start + 1 + len(self.str_)
        if data[start:stop] != self.bytes_:
            raise ValueError('The slice of data has to be equal {!r}'.format(self.bytes_))
        return stop, self.str_

    def __repr__(self):
        return f"{type(self).__name__}('{self.str_}')"


class Byte(Value):
    @staticmethod
    def verify(value: c_uint8) -> None:
        if not isinstance(value, c_uint8):
            raise TypeError(f'The {value} is not c_uint8')


class Short(Value):
    @staticmethod
    def verify(value: c_int16) -> None:
        if not isinstance(value, c_int16):
            raise TypeError(f'The {value} is not c_int16')


class Integer(Value):
    @staticmethod
    def verify(value: c_int32) -> None:
        if not isinstance(value, c_int32):
            raise TypeError(f'The {value} is not c_int32')


class Long(Value):
    @staticmethod
    def verify(value: c_int64) -> None:
        if not isinstance(value, c_int64):
            raise TypeError(f'The {value} is not c_int64')


class Flag(Value):
    @staticmethod
    def verify(value: c_bool) -> None:
        if not isinstance(value, c_bool):
            raise TypeError(f'The {value} is not c_bool')


class Float(Value):
    @staticmethod
    def verify(value: c_float) -> None:
        if not isinstance(value, c_float):
            raise TypeError(f'The {value} is not c_float')


class Double(Value):
    @staticmethod
    def verify(value: c_double) -> None:
        if not isinstance(value, c_double):
            raise TypeError(f'The {value} is not c_double')


class String(Value):
    @staticmethod
    def verify(value: c_char_p) -> None:
        if not isinstance(value, c_char_p):
            raise TypeError(f'The {value} is not c_char_p')


class Guid(Value):
    @staticmethod
    def verify(value: UUID) -> None:
        if not isinstance(value, UUID):
            raise TypeError(f'The {value} is not UUID')


class Null(Value):
    @staticmethod
    def verify(value: None) -> None:
        if not isinstance(value, type(None)):
            raise TypeError(f'The {value} is not TypeNone')


class ContainerDummy(Value):
    @staticmethod
    def verify(value: dict) -> None:
        if not isinstance(value, dict):
            raise TypeError(f'The {value} is not dict')


class VectorDummy(Value):
    @staticmethod
    def verify(value: Vector) -> None:
        if not isinstance(value, Vector):
            raise TypeError(f'The {value} is not Vector')


class VectorByte(Value):
    @staticmethod
    def verify(value: Vector) -> None:
        if not isinstance(value, Vector) or value.type_ is not c_uint8:
            raise TypeError(f'The {value} is not Vector of c_uint8')


class VectorShort(Value):
    @staticmethod
    def verify(value: Vector) -> None:
        if not isinstance(value, Vector) or value.type_ is not c_int16:
            raise TypeError(f'The {value} is not Vector of c_int16')


class VectorInteger(Value):
    @staticmethod
    def verify(value: Vector) -> None:
        if not isinstance(value, Vector) or value.type_ is not c_int32:
            raise TypeError(f'The {value} is not Vector of c_int32')


class VectorLong(Value):
    @staticmethod
    def verify(value: Vector) -> None:
        if not isinstance(value, Vector) or value.type_ is not c_int64:
            raise TypeError(f'The {value} is not Vector of c_int64')


class VectorFlag(Value):
    @staticmethod
    def verify(value: Vector) -> None:
        if not isinstance(value, Vector) or value.type_ is not c_bool:
            raise TypeError(f'The {value} is not Vector of c_bool')


class VectorFloat(Value):
    @staticmethod
    def verify(value: Vector) -> None:
        if not isinstance(value, Vector) or value.type_ is not c_float:
            raise TypeError(f'The {value} is not Vector of c_float')


class VectorDouble(Value):
    @staticmethod
    def verify(value: Vector) -> None:
        if not isinstance(value, Vector) or value.type_ is not c_double:
            raise TypeError(f'The {value} is not Vector of c_double')


class VectorString(Value):
    @staticmethod
    def verify(value: Vector) -> None:
        if not isinstance(value, Vector) or value.type_ is not c_char_p:
            raise TypeError(f'The {value} is not Vector of c_char_p')


class VectorGuid(Value):
    @staticmethod
    def verify(value: Vector) -> None:
        if not isinstance(value, Vector) or value.type_ is not UUID:
            raise TypeError(f'The {value} is not Vector of UUID')


class VectorNull(Value):
    @staticmethod
    def verify(value: Vector) -> None:
        if not isinstance(value, Vector) or value.type_ is not type(None):  # noqa: E721
            raise TypeError(f'The {value} is not Vector of TypeNone')


SchemeValues = Union[
    Byte,
    Short,
    Integer,
    Long,
    Flag,
    Float,
    Double,
    String,
    Guid,
    Null,
    ContainerDummy,
    VectorDummy,
    VectorByte,
    VectorShort,
    VectorInteger,
    VectorLong,
    VectorFlag,
    VectorFloat,
    VectorDouble,
    VectorString,
    VectorGuid,
    VectorNull
]
