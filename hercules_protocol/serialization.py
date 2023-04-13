from typing import Iterator, Optional, Tuple, Dict, Union, Type, List
from ctypes import c_char_p, c_uint8, c_int16, c_int32, c_int64, c_bool, c_float, c_double
from uuid import UUID
from struct import pack, unpack
from itertools import chain
from enum import Enum, IntEnum
from hercules_protocol.scheme import (
    Key,
)
from .datatypes import (
    PTypes,
    Vector,
    check_tag_key,
    check_version,
    check_timestamp,
)


class HTypes(IntEnum):
    #              Data Types
    #
    #  Hercules         Python       Format Strings
    CONTAINER = 0x01  # dict
    BYTE = 0x02       # c_uint8       # B
    SHORT = 0x03      # c_int16       # h
    INTEGER = 0x04    # c_int32       # i
    LONG = 0x05       # c_int64       # q
    FLAG = 0x06       # c_bool        # ?
    FLOAT = 0x07      # c_float       # f
    DOUBLE = 0x08     # c_double      # d
    STRING = 0x09     # c_char_p      # *s
    GUID = 0x0A       # UUID          # 16s
    NULL = 0x0B       # NoneType      #
    VECTOR = 0x80     # Vector


class HTypesBytes(bytes, Enum):
    CONTAINER = HTypes.CONTAINER.to_bytes(1, byteorder='big')
    BYTE = HTypes.BYTE.to_bytes(1, byteorder='big')
    SHORT = HTypes.SHORT.to_bytes(1, byteorder='big')
    INTEGER = HTypes.INTEGER.to_bytes(1, byteorder='big')
    LONG = HTypes.LONG.to_bytes(1, byteorder='big')
    FLAG = HTypes.FLAG.to_bytes(1, byteorder='big')
    FLOAT = HTypes.FLOAT.to_bytes(1, byteorder='big')
    DOUBLE = HTypes.DOUBLE.to_bytes(1, byteorder='big')
    STRING = HTypes.STRING.to_bytes(1, byteorder='big')
    GUID = HTypes.GUID.to_bytes(1, byteorder='big')
    NULL = HTypes.NULL.to_bytes(1, byteorder='big')
    VECTOR = HTypes.VECTOR.to_bytes(1, byteorder='big')


class HTypeSize(IntEnum):
    BYTE = 1
    SHORT = 2
    INTEGER = 4
    LONG = 8
    FLAG = 1
    FLOAT = 4
    DOUBLE = 8
    GUID = 16
    NULL = 0


HEAD_FORMAT = '>Bq16sh'
HEAD_STOP = 27


def _get_p_type(h_type: int) -> Type[PTypes]:
    if h_type == HTypes.CONTAINER:
        return dict
    elif h_type == HTypes.BYTE:
        return c_uint8
    elif h_type == HTypes.SHORT:
        return c_int16
    elif h_type == HTypes.INTEGER:
        return c_int32
    elif h_type == HTypes.LONG:
        return c_int64
    elif h_type == HTypes.FLAG:
        return c_bool
    elif h_type == HTypes.FLOAT:
        return c_float
    elif h_type == HTypes.DOUBLE:
        return c_double
    elif h_type == HTypes.STRING:
        return c_char_p
    elif h_type == HTypes.GUID:
        return UUID
    elif h_type == HTypes.NULL:
        return type(None)
    elif h_type == HTypes.VECTOR:
        return Vector
    else:
        raise ValueError(f'Incorrect data type {h_type}')


def _pack_key(key: str) -> bytes:
    check_tag_key(key)
    return pack(f'>B{len(key)}s', len(key), bytes(key, 'ascii'))


def _pack_value(value: PTypes, ikeys: Optional[Iterator[Key]] = None) -> List[bytes]:

    def pack_vector_length(value: Vector) -> bytes:
        return pack('>I', len(value))

    def pack_string_vector(value: Vector) -> List[bytes]:
        result = [HTypesBytes.STRING.value]
        format_ = ['>I']
        args = [len(value)]
        for e in value:
            format_.append(f'I{len(e.value)}s')
            args.extend([len(e.value), e.value])
        result.append(pack(''.join(format_), *args))
        return result

    def pack_vector(format_: str, value: Vector) -> bytes:
        return pack(f'>I{len(value)}{format_}', len(value), *[e.value for e in value])

    def get_vector(value: Vector) -> List[bytes]:
        if value.type_ is c_uint8:
            return [HTypesBytes.BYTE.value, pack_vector('B', value)]
        elif value.type_ is c_int16:
            return [HTypesBytes.SHORT.value, pack_vector('h', value)]
        elif value.type_ is c_int32:
            return [HTypesBytes.INTEGER.value, pack_vector('i', value)]
        elif value.type_ is c_int64:
            return [HTypesBytes.LONG.value, pack_vector('q', value)]
        elif value.type_ is c_bool:
            return [HTypesBytes.FLAG.value, pack_vector('?', value)]
        elif value.type_ is c_float:
            return [HTypesBytes.FLOAT.value, pack_vector('f', value)]
        elif value.type_ is c_double:
            return [HTypesBytes.DOUBLE.value, pack_vector('d', value)]
        elif value.type_ is c_char_p:
            return pack_string_vector(value)
        elif value.type_ is UUID:
            return [HTypesBytes.GUID.value, pack('>I', len(value))] + [e.bytes for e in value]
        elif value.type_ is type(None):  # noqa: E721
            return [HTypesBytes.NULL.value, pack_vector_length(value)]
        elif value.type_ is Vector:
            return [HTypesBytes.VECTOR.value, pack_vector_length(value)] + list(chain(*[get_vector(e) for e in value]))
        elif value.type_ is dict:
            return [HTypesBytes.CONTAINER, pack_vector_length(value)] + list(chain(*[get_container(e) for e in value]))
        else:
            raise ValueError(f'Incorrect data type {value.type_}')

    def get_container(value: Dict[str, PTypes]) -> List[bytes]:
        if ikeys:
            return (
                [pack('>h', len(value))] +
                list(chain(*[[next(ikeys).pack(k)] + get_value(v) for k, v in value.items()]))
            )
        else:
            return (
                [pack('>h', len(value))] +
                list(chain(*[[_pack_key(k)] + get_value(v) for k, v in value.items()]))
            )

    def get_value(value: PTypes) -> List[bytes]:
        if isinstance(value, c_uint8):
            return [HTypesBytes.BYTE.value, pack('>B', value.value)]
        elif isinstance(value, c_int16):
            return [HTypesBytes.SHORT.value, pack('>h', value.value)]
        elif isinstance(value, c_int32):
            return [HTypesBytes.INTEGER.value, pack('>i', value.value)]
        elif isinstance(value, c_int64):
            return [HTypesBytes.LONG.value, pack('>q', value.value)]
        elif isinstance(value, c_bool):
            return [HTypesBytes.FLAG.value, pack('>?', value.value)]
        elif isinstance(value, c_float):
            return [HTypesBytes.FLOAT.value, pack('>f', value.value)]
        elif isinstance(value, c_double):
            return [HTypesBytes.DOUBLE.value, pack('>d', value.value)]
        elif isinstance(value, c_char_p):
            if value.value:
                return [HTypesBytes.STRING.value, pack(f'>I{len(value.value)}s', len(value.value), value.value)]
            else:
                return [HTypesBytes.STRING.value, b'\x00\x00\x00\x00']
        elif isinstance(value, UUID):
            return [HTypesBytes.GUID.value, value.bytes]
        elif value is None:
            return [HTypesBytes.NULL.value]
        elif isinstance(value, Vector):
            return [HTypesBytes.VECTOR.value] + get_vector(value)
        elif isinstance(value, dict):
            return [HTypesBytes.CONTAINER.value] + get_container(value)
        else:
            raise ValueError(f'Incorrect data type {type(value)}')

    return get_value(value)


def serialize(
    version: int,
    timestamp: int,
    uuid_: UUID,
    payload: Dict[str, PTypes],
    scheme: Optional[dict] = None
) -> bytes:
    """ Translate a data structure into bytes
    """
    check_version(version)
    check_timestamp(timestamp)
    if not isinstance(payload, dict):
        raise ValueError('The payload has to be a dict')

    result: List[bytes] = [pack(HEAD_FORMAT, version, timestamp, uuid_.bytes, len(payload))]
    if scheme:
        _verify(payload, scheme)
        ikeys = make_iterator_of_keys(scheme)
        for key, value in payload.items():
            result.append(next(ikeys).pack(key))
            result.extend(_pack_value(value, ikeys))
    else:
        for key, value in payload.items():
            result.append(_pack_key(key))
            result.extend(_pack_value(value))
    return b''.join(result)


# ----------------------------------------------------------------------------------------------


def _unpack_key(data: bytes, start: int) -> Tuple[int, str]:
    lenght_of_key = data[start]
    start += 1
    stop = start + lenght_of_key
    key, = unpack(f'>{lenght_of_key}s', data[start:stop])
    return stop, check_tag_key(key.decode())


def _unpack_value(data: bytes, start: int, ikeys: Optional[Iterator[Key]] = None) -> Tuple[int, PTypes]:

    def get_h_type(start: int) -> Tuple[int, int]:
        return start + 1, data[start]

    def get_length(start: int) -> Tuple[int, int]:
        stop = start + 4
        return stop, unpack('>I', data[start:stop])[0]

    def get_tag_count(start: int) -> Tuple[int, int]:
        stop = start + 2
        return stop, unpack('>h', data[start:stop])[0]

    def get_vector(start: int) -> Tuple[int, Vector]:
        start, h_type = get_h_type(start)
        result = Vector([], _get_p_type(h_type))
        value: PTypes
        start, len_of_vector = get_length(start)
        for _ in range(len_of_vector):
            start, value = get_value(start, h_type)
            result.append(value)
        return start, result

    def get_container(start: int) -> Tuple[int, dict]:
        result = {}
        value: PTypes
        start, tag_count = get_tag_count(start)
        for _ in range(tag_count):
            if ikeys:
                start, key = next(ikeys).unpack(data, start)
            else:
                start, key = _unpack_key(data, start)
            start, value = get_value(*get_h_type(start))
            result[key] = value
        return start, result

    def get_value(start: int, h_type) -> Tuple[int, PTypes]:

        def unpack_(
                start: int,
                htype_size: HTypeSize,
                format_: str,
                object_: Type[Union[c_uint8, c_int16, c_int32, c_int64, c_bool, c_float, c_double]]
        ) -> Tuple[int, PTypes]:
            stop = start + htype_size
            result, = unpack(format_, data[start:stop])
            return stop, object_(result)

        def unpack_string(start: int) -> Tuple[int, c_char_p]:
            start, length = get_length(start)
            stop = start + length
            result, = unpack(f'>{length}s', data[start:stop])
            return stop, c_char_p(result)

        def unpack_uuid(start: int) -> Tuple[int, UUID]:
            stop = start + HTypeSize.GUID
            return stop, UUID(bytes=data[start:stop])

        if h_type == HTypes.BYTE:
            return unpack_(start, HTypeSize.BYTE, '>B', c_uint8)
        elif h_type == HTypes.SHORT:
            return unpack_(start, HTypeSize.SHORT, '>h', c_int16)
        elif h_type == HTypes.INTEGER:
            return unpack_(start, HTypeSize.INTEGER, '>i', c_int32)
        elif h_type == HTypes.LONG:
            return unpack_(start, HTypeSize.LONG, '>q', c_int64)
        elif h_type == HTypes.FLAG:
            return unpack_(start, HTypeSize.FLAG, '>?', c_bool)
        elif h_type == HTypes.FLOAT:
            return unpack_(start, HTypeSize.FLOAT, '>f', c_float)
        elif h_type == HTypes.DOUBLE:
            return unpack_(start, HTypeSize.DOUBLE, '>d', c_double)
        elif h_type == HTypes.STRING:
            return unpack_string(start)
        elif h_type == HTypes.GUID:
            return unpack_uuid(start)
        elif h_type == HTypes.NULL:
            return (start + HTypeSize.NULL, None)
        elif h_type == HTypes.VECTOR:
            return get_vector(start)
        elif h_type == HTypes.CONTAINER:
            return get_container(start)
        else:
            raise ValueError

    return get_value(*get_h_type(start))


def deserialize(data: bytes, scheme: Optional[dict] = None) -> Tuple[int, int, UUID, Dict[str, PTypes]]:
    """ Translate bytes into a data structure
    """
    version, timestamp, uuid_bytes, tag_count = unpack(HEAD_FORMAT, data[:HEAD_STOP])
    check_version(version)
    check_timestamp(timestamp)

    payload: Dict[str, PTypes] = {}
    start = HEAD_STOP
    if scheme:
        ikeys = make_iterator_of_keys(scheme)
        for _ in range(tag_count):
            start, key = next(ikeys).unpack(data, start)
            start, value = _unpack_value(data, start, ikeys)
            payload[key] = value

        _verify(payload, scheme)
    else:
        for _ in range(tag_count):
            start, key = _unpack_key(data, start)
            start, value = _unpack_value(data, start)
            payload[key] = value

    return version, timestamp, UUID(bytes=uuid_bytes), payload


def _verify(payload: Dict[str, PTypes], scheme: dict) -> None:

    def _verify_list(payload_list: list, scheme_list: list) -> None:
        if len(payload_list) != len(scheme_list):
            raise ValueError('The payload list and the scheme list have to have the same length')

        ipayload_list = iter(payload_list)
        for scheme_element in scheme_list:
            payload_element = next(ipayload_list)
            if isinstance(scheme_element, dict):
                if isinstance(payload_element, dict):
                    _verify_dict(payload_element, scheme_element)
                else:
                    raise ValueError(f'The {payload_element} and {scheme_element} are not the same')

            elif isinstance(scheme_element, list):
                if isinstance(payload_element, list):
                    _verify_list(payload_element, scheme_element)
                else:
                    raise ValueError(f'The {payload_element} and {scheme_element} are not the same')

            else:
                scheme_element.verify(payload_element)

    def _verify_dict(payload_dict: dict, scheme_dict: dict) -> None:
        if len(payload_dict) != len(scheme_dict):
            raise ValueError('The payload container and the scheme container have to have the same length')

        ipayload_dict = iter(payload_dict.values())
        for scheme_value in scheme_dict.values():
            payload_value = next(ipayload_dict)
            if isinstance(scheme_value, dict):
                if isinstance(payload_value, dict):
                    _verify_dict(payload_value, scheme_value)
                else:
                    raise ValueError(f'The {payload_value} and {scheme_value} are not the same')

            elif isinstance(scheme_value, list):
                if isinstance(payload_value, list):
                    _verify_list(payload_value, scheme_value)
                else:
                    raise ValueError(f'The {payload_value} and {scheme_value} are not the same')
            else:
                scheme_value.verify(payload_value)

    _verify_dict(payload, scheme)


def make_iterator_of_keys(scheme: dict) -> Iterator[Key]:
    if not isinstance(scheme, dict):
        raise TypeError

    result: List[Key] = []

    def expand_list(list_: list):
        for element in list_:
            if isinstance(element, dict):
                expand_dict(element)
            elif isinstance(element, list):
                expand_list(element)

    def expand_dict(dict_: dict):
        for key, value in dict_.items():
            if isinstance(key, Key):
                result.append(key)
            else:
                raise TypeError
            if isinstance(value, dict):
                expand_dict(value)
            elif isinstance(value, list):
                expand_list(value)

    expand_dict(scheme)

    return (e for e in result)
