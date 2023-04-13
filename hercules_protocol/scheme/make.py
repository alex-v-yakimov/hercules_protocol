import sys
import os
import argparse
from ..serialization import deserialize
from ..extra_functions import make_scheme


PAYLOAD_ELEMENT_NUMBER = 3


def _pformat_import(modules: tuple) -> str:
    result = ['from hercules_protocol.scheme import (\n']

    for module in modules:
        result.extend(('    ', repr(module), ',\n'))

    result[-1] = '\n)'

    return ''.join(result)


def _pformat_variable(varible_name: str, variable_value: dict) -> str:
    result = [varible_name, ' = {\n']

    def expand_list(indent: str):
        result.extend((indent, repr(key), ': [\n'))
        for element in value:
            result.extend((indent * 2, repr(element), ',\n'))
        result.extend((indent, '],\n'))

    def expand_dict(indent: str):
        result.extend((indent, repr(key), ': {\n'))
        for k, v in value.items():
            result.extend((indent * 2, repr(k), ': ', repr(v), ',\n'))
        result.extend((indent, '},\n'))

    for key, value in variable_value.items():
        if isinstance(value, list):
            expand_list('    ')
        elif isinstance(value, dict):
            expand_dict('    ')
        else:
            result.extend(('    ', repr(key), ': ', repr(value), ',\n'))

    result[-1] = '\n}'

    return ''.join(result)


def main():
    parser = argparse.ArgumentParser(
        description='Make a scheme for the hercules protocol',
        prog='python3 -m hercules_protocol.scheme.make'
    )
    parser.add_argument('-b', dest='binary_file', type=str, help='binary file', required=True)
    parser.add_argument('-o', dest='module_file', type=str, help='output python module file', required=False)
    options = parser.parse_args()

    binary_file = options.binary_file
    module_file = options.module_file

    try:
        with open(binary_file, mode='rb') as bfh:
            bytes_data = bfh.read()
    except IOError as err:
        print(str(err))
        sys.exit(err.errno)

    try:
        event = deserialize(data=bytes_data)
    except ValueError as err:
        print(str(err))
        sys.exit(os.EX_DATAERR)

    payload = event[PAYLOAD_ELEMENT_NUMBER]

    try:
        scheme_classes, scheme = make_scheme(payload=payload)
    except ValueError as err:
        print(str(err))
        sys.exit(os.EX_SOFTWARE)

    if module_file:
        try:
            with open(module_file, mode='x', encoding='utf-8') as mfh:
                mfh.write(_pformat_import(tuple(scheme_classes)))
                mfh.write('\n')
                mfh.write(_pformat_variable('scheme', scheme))
                mfh.write('\n')
        except IOError as err:
            print(str(err))
            sys.exit(err.errno)
    else:
        print(_pformat_import(tuple(scheme_classes)))
        print()
        print(_pformat_variable('scheme', scheme))


if __name__ == '__main__':
    main()
