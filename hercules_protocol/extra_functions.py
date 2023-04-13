from typing import Set, Tuple, Dict, Union, Type
from ctypes import c_char_p, c_uint8, c_int16, c_int32, c_int64, c_bool, c_float, c_double, _SimpleCData
from uuid import UUID
from hercules_protocol.scheme import (
    Key,
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
    VectorNull,
    SchemeValues,
)
from .datatypes import (
    PTypes,
    Vector
)


def make_scheme(
    payload: Dict[str, PTypes]
) -> Tuple[Set[Union[Type[Key], Type[SchemeValues]]], Dict[Key, Union[Type[SchemeValues], dict, list]]]:
    if not isinstance(payload, dict):
        raise ValueError('The payload has to be a dict')

    def construct_list(list_: Vector) -> list:
        result = []
        for element in list_:
            result.append(construct(element))
        return result

    def construct_dict(dict_: dict) -> dict:
        result = {}
        for key, value in dict_.items():
            result[Key(key)] = construct(value)
        return result

    def construct(
        value: PTypes
    ) -> Union[Type[SchemeValues], dict, list]:
        if isinstance(value, c_uint8):
            scheme_classes.add(Byte)
            return Byte
        elif isinstance(value, c_int16):
            scheme_classes.add(Short)
            return Short
        elif isinstance(value, c_int32):
            scheme_classes.add(Integer)
            return Integer
        elif isinstance(value, c_int64):
            scheme_classes.add(Long)
            return Long
        elif isinstance(value, c_bool):
            scheme_classes.add(Flag)
            return Flag
        elif isinstance(value, c_float):
            scheme_classes.add(Float)
            return Float
        elif isinstance(value, c_double):
            scheme_classes.add(Double)
            return Double
        elif isinstance(value, c_char_p):
            scheme_classes.add(String)
            return String
        elif isinstance(value, UUID):
            scheme_classes.add(Guid)
            return Guid
        elif isinstance(value, type(None)):
            scheme_classes.add(Null)
            return Null
        elif isinstance(value, Vector):
            if value.type_ is c_uint8:
                scheme_classes.add(VectorByte)
                return VectorByte
            elif value.type_ is c_int16:
                scheme_classes.add(VectorShort)
                return VectorShort
            elif value.type_ is c_int32:
                scheme_classes.add(VectorInteger)
                return VectorInteger
            elif value.type_ is c_int64:
                scheme_classes.add(VectorLong)
                return VectorLong
            elif value.type_ is c_bool:
                scheme_classes.add(VectorFlag)
                return VectorFlag
            elif value.type_ is c_float:
                scheme_classes.add(VectorFloat)
                return VectorFloat
            elif value.type_ is c_double:
                scheme_classes.add(VectorDouble)
                return VectorDouble
            elif value.type_ is c_char_p:
                scheme_classes.add(VectorString)
                return VectorString
            elif value.type_ is UUID:
                scheme_classes.add(VectorGuid)
                return VectorGuid
            elif value.type_ is type(None):  # noqa: E721
                scheme_classes.add(VectorNull)
                return VectorNull
            elif value.type_ is Vector or value.type_ is dict:
                if len(value):
                    return construct_list(value)
                else:
                    scheme_classes.add(VectorDummy)
                    return VectorDummy
            else:
                raise TypeError(f'{value} Vector Type Error')
        elif isinstance(value, dict):
            if len(value):
                return construct_dict(value)
            else:
                scheme_classes.add(VectorDummy)
                return ContainerDummy
        else:
            raise TypeError(f'{value} Type Error')

    scheme: Dict[Key, Union[Type[SchemeValues], dict, list]] = {}
    scheme_classes: Set[Union[Type[Key], Type[SchemeValues]]] = {Key}

    for key, value in payload.items():
        scheme[Key(key)] = construct(value)

    return scheme_classes, scheme


def simplify(
    data: Tuple[int, int, UUID, Dict[str, PTypes]]
) -> Tuple[int, int, UUID, Dict[str, Union[dict, int, bool, float, str, UUID, None, list]]]:
    """ Replace c_uint8 with int,
        replace c_int16 with int,
        replace c_int32 with int,
        replace c_int64 with int,
        replace c_bool with bool,
        replace c_float with float,
        replace c_double with float,
        replace c_char_p with str,
        replace Vector with list
    """

    if not isinstance(data, tuple):
        raise TypeError('The data has to be a tuple')

    result = []

    def _simplify(item):
        if isinstance(item, dict):
            new_item = {}
            for key, value in item.items():
                new_item[key] = _simplify(value)
        elif isinstance(item, list):
            new_item = []
            for i in item:
                new_item.append(_simplify(i))
        elif isinstance(item, _SimpleCData):
            new_item = item.value
        else:
            new_item = item

        return new_item

    for item in data:
        result.append(_simplify(item))

    return tuple(result)  # type: ignore
