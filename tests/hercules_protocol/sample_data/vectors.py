from ctypes import c_char_p, c_uint8, c_int16, c_int32, c_int64, c_bool, c_float, c_double
from uuid import UUID
from hercules_protocol import Vector
from hercules_protocol.scheme import (
    Key,
    ContainerDummy,
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
)

vectors = {
    'bytes': (
        b'\x01'  # Version is 1
        b'\x00\x3b\x21\x46\x91\x97\xca\x00'  # Timestamp 16 643 610 600 000 000 in 100ns-ticks
        # UUID d9d0e8ea-7c01-4e72-8704-7f340da4e26a
        b'\xd9\xd0\xe8\xea\x7c\x01\x4e\x72\x87\x04\x7f\x34\x0d\xa4\xe2\x6a'

        b'\x00\x0c'  # Tag count is

        b'\x11\x76\x65\x63\x74\x6f\x72\x2d\x6f\x66\x5f\x63\x5f\x75\x69\x6e\x74\x38'  # 'vector-of_c_uint8'
        b'\x80'
        b'\x02'
        b'\x00\x00\x00\x02'
        b'\x01'
        b'\x02'

        b'\x11\x76\x65\x63\x74\x6f\x72\x2d\x6f\x66\x5f\x63\x5f\x69\x6e\x74\x31\x36'  # 'vector-of_c_int16'
        b'\x80'
        b'\x03'
        b'\x00\x00\x00\x03'
        b'\x00\x01'
        b'\x00\x02'
        b'\x00\x03'

        b'\x11\x76\x65\x63\x74\x6f\x72\x2d\x6f\x66\x5f\x63\x5f\x69\x6e\x74\x33\x32'  # 'vector-of_c_int32'
        b'\x80'
        b'\x04'
        b'\x00\x00\x00\x02'
        b'\x00\x00\x00\x01'
        b'\x00\x00\x00\x02'

        b'\x11\x76\x65\x63\x74\x6f\x72\x2d\x6f\x66\x5f\x63\x5f\x69\x6e\x74\x36\x34'  # 'vector-of_c_int64'
        b'\x80'
        b'\x05'
        b'\x00\x00\x00\x03'
        b'\x00\x00\x00\x00\x00\x00\x00\x01'
        b'\x00\x00\x00\x00\x00\x00\x00\x02'
        b'\x00\x00\x00\x00\x00\x00\x00\x03'

        b'\x10\x76\x65\x63\x74\x6f\x72\x2d\x6f\x66\x5f\x63\x5f\x62\x6f\x6f\x6c'  # 'vector-of_c_bool'
        b'\x80'
        b'\x06'
        b'\x00\x00\x00\x04'
        b'\x01'
        b'\x00'
        b'\x00'
        b'\x01'

        b'\x11\x76\x65\x63\x74\x6f\x72\x2d\x6f\x66\x5f\x63\x5f\x66\x6c\x6f\x61\x74'  # 'vector-of_c_float'
        b'\x80'
        b'\x07'
        b'\x00\x00\x00\x02'
        b'\x3d\xcc\xcc\xcd'
        b'\x3e\x4c\xcc\xcd'

        b'\x12\x76\x65\x63\x74\x6f\x72\x2d\x6f\x66\x5f\x63\x5f\x64\x6f\x75\x62\x6c\x65'  # 'vector-of_c_double'
        b'\x80'
        b'\x08'
        b'\x00\x00\x00\x01'
        b'\x3f\xb9\x99\x99\x99\x99\x99\x9a'

        b'\x0e\x76\x65\x63\x74\x6f\x72\x2d\x6f\x66\x5f\x55\x55\x49\x44'  # 'vector-of_UUID'
        b'\x80'
        b'\x0a'
        b'\x00\x00\x00\x01'
        b'\xd9\xd0\xe8\xea\x7c\x01\x4e\x72\x87\x04\x7f\x34\x0d\xa4\xe2\x6a'

        b'\x12\x76\x65\x63\x74\x6f\x72\x2d\x6f\x66\x5f\x4e\x6f\x6e\x65\x54\x79\x70\x65'  # 'vector-of_NoneType'
        b'\x80'
        b'\x0b'
        b'\x00\x00\x00\x02'

        b'\x11\x76\x65\x63\x74\x6f\x72\x2d\x6f\x66\x2d\x76\x65\x63\x74\x6f\x72\x73'  # 'vector-of-vectors'
        b'\x80'
        b'\x80'
        b'\x00\x00\x00\x03'
        b'\x02'
        b'\x00\x00\x00\x01'
        b'\x01'
        b'\x02'
        b'\x00\x00\x00\x02'
        b'\x02'
        b'\x03'
        b'\x02'
        b'\x00\x00\x00\x03'
        b'\x04'
        b'\x05'
        b'\x06'

        b'\x13\x76\x65\x63\x74\x6f\x72\x2d\x6f\x66\x2d\x63\x6f\x6e\x74\x61\x69\x6e\x65\x72'  # 'vector-of-container'
        b'\x80'
        b'\x01'
        b'\x00\x00\x00\x01'
        b'\x00\x00'

        b'\x0c\x65\x6d\x70\x74\x79\x2d\x76\x65\x63\x74\x6f\x72'  # 'empty-vector'
        b'\x80'
        b'\x09'
        b'\x00\x00\x00\x00'
    ),
    'tuple': (
        1,  # Version is 1
        16643610600000000,  # Timestamp 16 643 610 600 000 000 in 100ns-ticks
        # UUID d9d0e8ea-7c01-4e72-8704-7f340da4e26a
        UUID(bytes=b'\xd9\xd0\xe8\xea\x7c\x01\x4e\x72\x87\x04\x7f\x34\x0d\xa4\xe2\x6a'),
        {
            'vector-of_c_uint8':
            Vector([c_uint8(1), c_uint8(2)], c_uint8),

            'vector-of_c_int16':
            Vector([c_int16(1), c_int16(2), c_int16(3)], c_int16),

            'vector-of_c_int32':
            Vector([c_int32(1), c_int32(2)], c_int32),

            'vector-of_c_int64':
            Vector([c_int64(1), c_int64(2), c_int64(3)], c_int64),

            'vector-of_c_bool':
            Vector([c_bool(True), c_bool(False), c_bool(False), c_bool(True)], c_bool),

            'vector-of_c_float':
            Vector([c_float(0.1), c_float(0.2)], c_float),

            'vector-of_c_double':
            Vector([c_double(0.1)], c_double),

            'vector-of_UUID':
            Vector([UUID(bytes=b'\xd9\xd0\xe8\xea\x7c\x01\x4e\x72\x87\x04\x7f\x34\x0d\xa4\xe2\x6a')], UUID),

            'vector-of_NoneType':
            Vector([None, None], type(None)),

            'vector-of-vectors':
            Vector([
                Vector([c_uint8(1)], type_=c_uint8),
                Vector([c_uint8(2), c_uint8(3)], type_=c_uint8),
                Vector([c_uint8(4), c_uint8(5), c_uint8(6)], type_=c_uint8)
            ], type_=Vector),

            'vector-of-container':
            Vector([{}], dict),

            'empty-vector':
            Vector([], type_=c_char_p),
        }
    ),
    'scheme': {
        Key('vector-of_c_uint8'): VectorByte,
        Key('vector-of_c_int16'): VectorShort,
        Key('vector-of_c_int32'): VectorInteger,
        Key('vector-of_c_int64'): VectorLong,
        Key('vector-of_c_bool'): VectorFlag,
        Key('vector-of_c_float'): VectorFloat,
        Key('vector-of_c_double'): VectorDouble,
        Key('vector-of_UUID'): VectorGuid,
        Key('vector-of_NoneType'): VectorNull,
        Key('vector-of-vectors'): [
            VectorByte, VectorByte, VectorByte
        ],
        Key('vector-of-container'): [ContainerDummy],
        Key('empty-vector'): VectorString,
    }
}
