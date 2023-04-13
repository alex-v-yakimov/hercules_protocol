#!/usr/bin/python3

from ctypes import c_char_p, c_int64
from uuid import UUID
from hercules_protocol import serialize, deserialize, simplify


data_in_bytes = (
    b'\x01'  # Version is 1
    b'\x00\x36\x46\x2A\xFD\x9E\xF8\x00'  # Timestamp 15 276 799 200 000 000 in 100ns-ticks
    b'\x11\x20\x38\x00\x63\xfd\x11\xE8\x83\xE2\x3A\x58\x7D\x90\x20\x00'  # UUID 11203800-63FD-11E8-83E2-3A587D902000
    b'\x00\x02'  # Tag count is 2
    b'\x04\x68\x6F\x73\x74'  # Tag key is tiny string 'host' with length 4
    b'\x09\x00\x00\x00\x09\x6C\x6F\x63\x61\x6C\x68\x6F\x73\x74'  # Tag value is string 'localhost' with length 9
    b'\x09\x74\x69\x6D\x65\x73\x74\x61\x6D\x70'  # Tag key is tiny string 'timestamp' with length 9
    b'\x05\x00\x05\x6D\x6A\xB2\xF6\x4C\x00'  # Tag value is long 1 527 679 920 000 000
)

data_in_tuple = (
    1,  # Version is 1
    15276799200000000,  # # Timestamp 15 276 799 200 000 000 in 100ns-ticks
    # UUID 11203800-63FD-11E8-83E2-3A587D902000
    UUID(bytes=b'\x11\x20\x38\x00\x63\xfd\x11\xE8\x83\xE2\x3A\x58\x7D\x90\x20\x00'),
    {  # Tag count is 2
        'host':  # Tag key is tiny string 'host' with length 4
        c_char_p(b'localhost'),  # Tag value is string 'localhost' with length 9
        'timestamp':  # Tag key is tiny string 'timestamp' with length 9
        c_int64(1527679920000000)  # Tag value is long (int64) 1 527 679 920 000 000
    }
)


if __name__ == '__main__':
    assert serialize(*data_in_tuple) == data_in_bytes
    assert simplify(deserialize(data_in_bytes)) == simplify(data_in_tuple)
