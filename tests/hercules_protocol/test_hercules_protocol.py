import pytest
from ctypes import c_uint8, c_int16, c_int64, c_char_p
from uuid import uuid4
from hercules_protocol import serialize, deserialize, Vector, simplify
from hercules_protocol.serialization import _verify
from hercules_protocol.datatypes import LENGTH_OF_TAG_KEY, MAX_VERSION
from hercules_protocol.scheme import Key, Short, Long, String
from . import sample_data


def test_serialize():
    assert serialize(*sample_data.from_github['tuple']) == sample_data.from_github['bytes']

    assert serialize(*sample_data.container['tuple']) == sample_data.container['bytes']

    assert serialize(*sample_data.vectors['tuple']) == sample_data.vectors['bytes']

    assert serialize(*sample_data.from_balconlib['tuple']) == sample_data.from_balconlib['bytes']


def test_serialize_with_scheme():
    assert (
        serialize(*sample_data.from_github['tuple'], scheme=sample_data.from_github['scheme']) ==
        sample_data.from_github['bytes']
    )

    assert (
        serialize(*sample_data.container['tuple'], scheme=sample_data.container['scheme']) ==
        sample_data.container['bytes']
    )

    assert (
        serialize(*sample_data.vectors['tuple'], scheme=sample_data.vectors['scheme']) ==
        sample_data.vectors['bytes']
    )

    assert (
        serialize(*sample_data.from_balconlib['tuple'], scheme=sample_data.from_balconlib['scheme']) ==
        sample_data.from_balconlib['bytes']
    )


def test_serialize_raises():
    with pytest.raises(ValueError, match='The payload has to be a dict'):
        serialize(1, 12345, uuid4(), '')  # type: ignore  # type hints error for testing

    with pytest.raises(ValueError, match=f'The length of the key has to be less or equal {LENGTH_OF_TAG_KEY}'):
        serialize(1, 12345, uuid4(), {'h'*256: c_uint8(0)})

    with pytest.raises(ValueError, match="The key mustn't be a empty string"):
        serialize(1, 12345, uuid4(), {'': c_uint8(0)})

    with pytest.raises(ValueError, match='Permitted characters of the key: "a-z", "A-Z", "0-9", "_", ".", "-"'):
        serialize(1, 12345, uuid4(), {'+': c_uint8(0)})

    with pytest.raises(ValueError, match='The version has to be "int"'):
        serialize('1', 12345, uuid4(), {'h': c_uint8(0)})  # type: ignore  # type hints error for testing

    with pytest.raises(ValueError, match=f'The version has to be less or equal than {MAX_VERSION} and greater than 0'):
        serialize(2, 12345, uuid4(), {'h': c_uint8(0)})

    with pytest.raises(ValueError, match=f'The version has to be less or equal than {MAX_VERSION} and greater than 0'):
        serialize(-2, 12345, uuid4(), {'h': c_uint8(0)})

    with pytest.raises(ValueError, match='The timestamp has to be "int"'):
        serialize(1, '12345', uuid4(), {'h': c_uint8(0)})  # type: ignore  # type hints error for testing

    with pytest.raises(ValueError, match='The timestamp has to be a positive number'):
        serialize(1, -12345, uuid4(), {'h': c_uint8(0)})

    with pytest.raises(ValueError, match='Vector has to have same type elements'):
        serialize(1, 12345, uuid4(), {'h': Vector([c_uint8(0), c_int16(1)], c_uint8)})

    with pytest.raises(ValueError, match='Incorrect data type *'):
        serialize(1, 12345, uuid4(), {'h': Vector([0, 1], int)})  # type: ignore  # type hints error for testing

    with pytest.raises(ValueError, match='Incorrect data type *'):
        serialize(1, 12345, uuid4(), {'h': [c_uint8(0), c_uint8(1)]})  # type: ignore  # type hints error for testing

    with pytest.raises(ValueError, match='Incorrect data type *'):
        serialize(1, 12345, uuid4(), {'h': 0})  # type: ignore  # type hints error for testing

    with pytest.raises(ValueError, match='Incorrect data type *'):
        serialize(1, 12345, uuid4(), {'h': 'v'})  # type: ignore  # type hints error for testing

    with pytest.raises(ValueError, match='The key has to be a string'):
        serialize(1, 12345, uuid4(), {0: c_uint8(0)})  # type: ignore  # type hints error for testing


def test_deserialize():
    assert (
        simplify(deserialize(sample_data.from_github['bytes'])) ==
        simplify(sample_data.from_github['tuple'])
    )

    assert (
        simplify(deserialize(sample_data.container['bytes'])) ==
        simplify(sample_data.container['tuple'])
    )

    assert (
        simplify(deserialize(sample_data.vectors['bytes'])) ==
        simplify(sample_data.vectors['tuple'])
    )

    assert (
        simplify(deserialize(sample_data.from_balconlib['bytes'])) ==
        simplify(sample_data.from_balconlib['tuple'])
    )


def test_deserialize_with_scheme():
    assert (
        simplify(deserialize(sample_data.from_github['bytes'], scheme=sample_data.from_github['scheme'])) ==
        simplify(sample_data.from_github['tuple'])
    )

    assert (
        simplify(deserialize(sample_data.container['bytes'], scheme=sample_data.container['scheme'])) ==
        simplify(sample_data.container['tuple'])
    )

    assert (
        simplify(deserialize(sample_data.vectors['bytes'], scheme=sample_data.vectors['scheme'])) ==
        simplify(sample_data.vectors['tuple'])
    )

    assert (
        simplify(deserialize(sample_data.from_balconlib['bytes'], scheme=sample_data.from_balconlib['scheme'])) ==
        simplify(sample_data.from_balconlib['tuple'])
    )


def test___verify():
    with pytest.raises(
        ValueError, match='The payload container and the scheme container have to have the same length'
    ):
        _verify(
            payload={'time': c_int64(16648761657993749), 'status': c_int16(200)},
            scheme={Key('time'): Long}
        )

    with pytest.raises(ValueError, match='The payload list and the scheme list have to have the same length'):
        _verify(
            payload={
                'res_headers':
                Vector([
                    {'k': c_char_p(b'content-type'), 'v': c_char_p(b'application/json; charset=utf-8')},
                    {'k': c_char_p(b'x-kontur-trace-id'), 'v': c_char_p(b'35d0b2aca59358cf34404c1688e55244')}
                ], type_=dict)
            },
            scheme={
                Key('res_headers'): [
                    {Key('k'): String, Key('v'): String}
                ]
            }
        )

    with pytest.raises(ValueError, match=r'The .+ and .+ are not the same'):
        _verify(
            payload={
                'res_headers':
                Vector([
                    {'k': c_char_p(b'content-type'), 'v': c_char_p(b'application/json; charset=utf-8')},
                    {'k': c_char_p(b'x-kontur-trace-id'), 'v': c_char_p(b'35d0b2aca59358cf34404c1688e55244')}
                ], type_=dict)
            },
            scheme={
                Key('res_headers'): {Key('k'): String, Key('v'): String}
            }
        )

    with pytest.raises(TypeError, match=r'The .+ is not .+'):
        _verify(
            payload={'time': c_int64(16648761657993749)},
            scheme={Key('time'): Short}
        )
