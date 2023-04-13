import pytest
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
    VectorNull
)


def test_Key():
    key = Key('time')
    with pytest.raises(ValueError, match='The key has to be equal *'):
        key.pack('host')
    with pytest.raises(ValueError, match='The slice of data has to be equal *'):
        key.unpack(b'host', start=0)


def test_Byte():
    with pytest.raises(TypeError, match=r'The .+ is not c_uint8'):
        Byte.verify(1)  # type: ignore  # type hints error for testing


def test_Short():
    with pytest.raises(TypeError, match=r'The .+ is not c_int16'):
        Short.verify(1)  # type: ignore  # type hints error for testing


def test_Integer():
    with pytest.raises(TypeError, match=r'The .+ is not c_int32'):
        Integer.verify(1)  # type: ignore  # type hints error for testing


def test_Long():
    with pytest.raises(TypeError, match=r'The .+ is not c_int64'):
        Long.verify(1)  # type: ignore  # type hints error for testing


def test_Flag():
    with pytest.raises(TypeError, match=r'The .+ is not c_bool'):
        Flag.verify(1)  # type: ignore  # type hints error for testing


def test_Float():
    with pytest.raises(TypeError, match=r'The .+ is not c_float'):
        Float.verify(1)  # type: ignore  # type hints error for testing


def test_Double():
    with pytest.raises(TypeError, match=r'The .+ is not c_double'):
        Double.verify(1)  # type: ignore  # type hints error for testing


def test_String():
    with pytest.raises(TypeError, match=r'The .+ is not c_char_p'):
        String.verify(1)  # type: ignore  # type hints error for testing


def test_Guid():
    with pytest.raises(TypeError, match=r'The .+ is not UUID'):
        Guid.verify(1)  # type: ignore  # type hints error for testing


def test_Null():
    with pytest.raises(TypeError, match=r'The .+ is not TypeNone'):
        Null.verify(1)  # type: ignore  # type hints error for testing


def test_ContainerDummy():
    with pytest.raises(TypeError, match=r'The .+ is not dict'):
        ContainerDummy.verify(1)  # type: ignore  # type hints error for testing


def test_VectorDummy():
    with pytest.raises(TypeError, match=r'The .+ is not Vector'):
        VectorDummy.verify(1)  # type: ignore  # type hints error for testing


def test_VectorByte():
    with pytest.raises(TypeError, match=r'The .+ is not Vector of c_uint8'):
        VectorByte.verify(1)  # type: ignore  # type hints error for testing


def test_VectorShort():
    with pytest.raises(TypeError, match=r'The .+ is not Vector of c_int16'):
        VectorShort.verify(1)  # type: ignore  # type hints error for testing


def test_VectorInteger():
    with pytest.raises(TypeError, match=r'The .+ is not Vector of c_int32'):
        VectorInteger.verify(1)  # type: ignore  # type hints error for testing


def test_VectorLong():
    with pytest.raises(TypeError, match=r'The .+ is not Vector of c_int64'):
        VectorLong.verify(1)  # type: ignore  # type hints error for testing


def test_VectorFlag():
    with pytest.raises(TypeError, match=r'The .+ is not Vector of c_bool'):
        VectorFlag.verify(1)  # type: ignore  # type hints error for testing


def test_VectorFloat():
    with pytest.raises(TypeError, match=r'The .+ is not Vector of c_float'):
        VectorFloat.verify(1)  # type: ignore  # type hints error for testing


def test_VectorDouble():
    with pytest.raises(TypeError, match=r'The .+ is not Vector of c_double'):
        VectorDouble.verify(1)  # type: ignore  # type hints error for testing


def test_VectorString():
    with pytest.raises(TypeError, match=r'The .+ is not Vector of c_char_p'):
        VectorString.verify(1)  # type: ignore  # type hints error for testing


def test_VectorGuid():
    with pytest.raises(TypeError, match=r'The .+ is not Vector of UUID'):
        VectorGuid.verify(1)  # type: ignore  # type hints error for testing


def test_VectorNull():
    with pytest.raises(TypeError, match=r'The .+ is not Vector of TypeNone'):
        VectorNull.verify(1)  # type: ignore  # type hints error for testing
