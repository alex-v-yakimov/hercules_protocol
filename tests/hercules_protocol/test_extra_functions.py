import pytest
from hercules_protocol import make_scheme
from . import sample_data


def test_make_scheme():
    assert make_scheme(sample_data.from_github['tuple'][3])[1] == sample_data.from_github['scheme']

    assert make_scheme(sample_data.container['tuple'][3])[1] == sample_data.container['scheme']

    assert make_scheme(sample_data.vectors['tuple'][3])[1] == sample_data.vectors['scheme']

    assert make_scheme(sample_data.from_balconlib['tuple'][3])[1] == sample_data.from_balconlib['scheme']

    with pytest.raises(ValueError, match='The payload has to be a dict'):
        make_scheme([])  # type: ignore  # type hints error for testing
