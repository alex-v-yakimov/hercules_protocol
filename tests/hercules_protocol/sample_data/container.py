from ctypes import c_char_p, c_uint8, c_int16, c_int32, c_int64, c_bool, c_float, c_double
from uuid import UUID
from hercules_protocol import Vector
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
    VectorString,
)


container = {
    'bytes': (
        b'\x01'  # Version is 1
        b'\x00\x3b\x21\x46\x91\x97\xca\x00'  # Timestamp 16 643 610 600 000 000 in 100ns-ticks
        # UUID d9d0e8ea-7c01-4e72-8704-7f340da4e26a
        b'\xd9\xd0\xe8\xea\x7c\x01\x4e\x72\x87\x04\x7f\x34\x0d\xa4\xe2\x6a'

        b'\x00\x0f'  # Tag count is 15

        b'\x07\x63\x5f\x75\x69\x6e\x74\x38'  # Tag key is tiny string 'c_uint8' with length 7
        b'\x02\x01'  # Tag value is Hercules Byte 1, python data type is c_uint8

        b'\x07\x63\x5f\x69\x6e\x74\x31\x36'   # Tag key is tiny string 'c_int16' with length 7
        b'\x03\x56\x06'  # Tag value is Hercules Short 2022, python data type is c_int16

        b'\x07\x63\x5f\x69\x6e\x74\x33\x32'  # Tag key is tiny string 'c_int32' with length 5
        b'\x04\x7f\xff\xff\xff'  # Tag value is Hercules Integer 2147483647, python data type is c_int32

        b'\x07\x63\x5f\x69\x6e\x74\x36\x34'  # Tag key is tiny string 'c_int64' with length 6
        b'\x05\x00\x05\x6D\x6A\xB2\xF6\x4C\x00'  # Tag value is Hercules Long 1,527,679,920,000,000,
                                                 # python data type is c_int64

        b'\x06\x63\x5f\x62\x6f\x6f\x6c'  # Tag key is tiny string 'c_bool' with length 6
        b'\x06\x01'  # Tag value is Hercules Flag True, python data type is c_bool

        b'\x07\x63\x5f\x66\x6c\x6f\x61\x74'  # Tag key is tiny string 'c_float' with length 7
        b'\x07\x3f\x80\x00\x00'  # Tag value is Hercules Float 1.0, python data type is c_float

        b'\x08\x63\x5f\x64\x6f\x75\x62\x6c\x65'  # Tag key is tiny string 'c_double' with length 8
        b'\x08\x40\x08\x3d\x70\xa3\xd7\x0a\x3d'  # Tag value is Hercules Double 3.03, python data type is c_double

        b'\x06\x73\x74\x72\x69\x6e\x67'  # Tag key is tiny string 'string' with length 6
        b'\x09\x00\x00\x00\x05\x66\x64\x65\x76\x31'  # Tag value is Hercules String 'fdev1',
                                                     # python data type is c_char_p

        b'\x04\x55\x55\x49\x44'  # Tag key is tiny string 'UUID' with length 4
        # Tag value is Hercules GUID 11203800-63FD-11E8-83E2-3A587D902000, python data type is uuid.UUID
        b'\x0a\x11\x20\x38\x00\x63\xfd\x11\xe8\x83\xe2\x3a\x58\x7d\x90\x20\x00'

        b'\x04\x4e\x6f\x6e\x65'  # Tag key is tiny string 'None' with length 4
        b'\x0b'  # Tag value is Hercules Null, python data type is NoneType

        # Tag key is tiny string 'vector-of-strings' with length 17
        b'\x11\x76\x65\x63\x74\x6f\x72\x2d\x6f\x66\x2d\x73\x74\x72\x69\x6e\x67\x73'
        b'\x80'                                          # type Hercules Vector
        b'\x09'                                          # type Hercules String
        b'\x00\x00\x00\x03'                              # length vector of strings is 3
        b'\x00\x00\x00\x05\x66\x69\x72\x73\x74'          # string 'first', len('first') = 5
        b'\x00\x00\x00\x06\x73\x65\x63\x6f\x6e\x64'      # string 'second', len('second') = 6
        b'\x00\x00\x00\x05\x74\x68\x69\x72\x64'          # string 'third', len('second') = 6


        b'\x09\x63\x6f\x6e\x74\x61\x69\x6e\x65\x72'  # Tag key is tiny string 'container' with length 9
        b'\x01'                                      # type Hercules Container
        b'\x00\x01'                                  # length of container
        b'\x09\x68\x6f\x73\x74\x5f\x6e\x61\x6d\x65'  # Tag key is tiny string 'host_name' with length 9
        b'\x09\x00\x00\x00\x05\x66\x64\x65\x76\x32'  # Tag value is String 'fdev2' with length 5

        # Tag key is tiny string 'container-in-container' with length 16
        b'\x16\x63\x6f\x6e\x74\x61\x69\x6e\x65\x72\x2d\x69\x6e\x2d\x63\x6f\x6e\x74\x61\x69\x6e\x65\x72'
        b'\x01'                              # type Hercules Container
        b'\x00\x01'                          # length of container
        b'\x04\x68\x6f\x73\x74'
        b'\x01\x00\x02'
        b'\x08\x68\x6f\x73\x74\x6e\x61\x6d\x65'
        b'\x09\x00\x00\x00\x05\x66\x64\x65\x76\x32'
        b'\x02\x6f\x73'
        b'\x09\x00\x00\x00\x06\x63\x65\x6e\x74\x6f\x73'

        # Tag key is tiny string 'empty-container' with length 15
        b'\x0f\x65\x6d\x70\x74\x79\x2d\x63\x6f\x6e\x74\x61\x69\x6e\x65\x72'
        b'\x01'                              # type Hercules Container
        b'\x00\x00'                          # length of container

        # Tag key is tiny string 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-' with length 65
        b'\x41'
        # a-z
        b'\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a'
        # A-Z
        b'\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a'
        b'\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x5f\x2e\x2d'  # '0123456789_.-'
        b'\x09\x00\x00\x00\x00'  # Tag value is string '' with length 0
    ),
    'tuple': (
        1,  # Version is 1
        16643610600000000,  # Timestamp 16 643 610 600 000 000 in 100ns-ticks
        # UUID d9d0e8ea-7c01-4e72-8704-7f340da4e26a
        UUID(bytes=b'\xd9\xd0\xe8\xea\x7c\x01\x4e\x72\x87\x04\x7f\x34\x0d\xa4\xe2\x6a'),
        {   # Tag count is 15

            'c_uint8':  # Tag key is tiny string 'c_uint8' with length 7
            c_uint8(1),  # Tag value is byte 1, python data type is c_uint8

            'c_int16':  # Tag key is tiny string 'c_int16' with length 7
            c_int16(22022),  # Tag value is Hercules Short 2022, python data type is c_int16

            'c_int32':  # Tag key is tiny string 'c_int32' with length 5
            c_int32(2147483647),  # Tag value is Hercules Integer 2147483647, python data type is c_int32

            'c_int64':  # Tag key is tiny string 'c_int64' with length 6
            c_int64(1527679920000000),  # Tag value is Hercules Long 1,527,679,920,000,000, python data type is c_int64

            'c_bool':  # Tag key is tiny string 'c_bool' with length 6
            c_bool(True),  # Tag value is Hercules Flag True, python data type is c_bool

            'c_float':  # Tag key is tiny string 'c_float' with length 7
            c_float(1.0),  # Tag value is Hercules Float 1.0, python data type is c_float

            'c_double':  # Tag key is tiny string 'c_double' with length 8
            c_double(3.03),  # Tag value is Hercules Double 3.03, python data type is c_double

            'string':  # Tag key is tiny string 'string' with length 6
            c_char_p(b'fdev1'),  # Tag value is Hercules String 'fdev1', python data type is c_char_p

            'UUID':  # Tag key is tiny string 'UUID' with length 4
            # Tag value is GUID 11203800-63FD-11E8-83E2-3A587D902000, python data type is uuid.UUID
            UUID(bytes=b'\x11\x20\x38\x00\x63\xfd\x11\xE8\x83\xE2\x3A\x58\x7D\x90\x20\x00'),

            'None':  # Tag key is tiny string 'None' with length 4
            None,  # Tag value is Hercules Null, python data type is NoneType

            'vector-of-strings':  # Tag key is tiny string 'vector-of-strings' with length 17
            # Tag value list of strings
            Vector([c_char_p(b'first'), c_char_p(b'second'), c_char_p(b'third')], type_=c_char_p),

            'container':  # Tag key is tiny string 'container' with length 9
            {      # Tag value is container
                'host_name':  # Tag key is tiny string 'host_name' with length 9
                c_char_p(b'fdev2')  # Tag value is string 'fdev2' with length 5
            },

            'container-in-container':  # Tag key is tiny string 'container-in-container' with length 16
            {
                'host': {'hostname': c_char_p(b'fdev2'), 'os': c_char_p(b'centos')}
            },

            'empty-container': {},  # Tag key is tiny string 'empty-container' with length 15

            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-': c_char_p(b'')
        }
    ),
    'scheme': {
        Key('c_uint8'): Byte,
        Key('c_int16'): Short,
        Key('c_int32'): Integer,
        Key('c_int64'): Long,
        Key('c_bool'): Flag,
        Key('c_float'): Float,
        Key('c_double'): Double,
        Key('string'): String,
        Key('UUID'): Guid,
        Key('None'): Null,
        Key('vector-of-strings'): VectorString,
        Key('container'): {
            Key('host_name'): String
        },
        Key('container-in-container'): {
            Key('host'): {
                Key('hostname'): String,
                Key('os'): String
            }
        },
        Key('empty-container'): ContainerDummy,
        Key('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-'): String,
    }
}
