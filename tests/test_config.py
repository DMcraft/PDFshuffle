import pytest
from src.pdfshuffle import config

def test_get_size_page():
    config.PAGE_FORMAT = 'A4'
    assert config.get_size_page() == (1654, 2338)
    # config.PAGE_FORMAT = 'A8'
    # assert config.get_size_page() == (0, 0)

def test_int_to_bytes():
    assert config.int_to_bytes((70000,))[0] == 0
    assert config.int_to_bytes((-1,))[0] == 0
    assert config.int_to_bytes((-100, 0, 10, 500, 70000)) == bytes((0, 0, 0, 0, 0, 10, 1, 244, 0, 0))
    assert config.int_to_bytes((0, 4386, 19991)) == bytes((0, 0, 17, 34, 78, 23))


def test_bytes_to_int():
    assert len(config.bytes_to_int(bytes((0,)))) == 0
    assert config.bytes_to_int(bytes((0, 0))) == [0, ]
    assert config.bytes_to_int(bytes((0, 0, 0, 0, 0, 10, 1, 244, 0))) == [0, 0, 10, 500]
    assert config.bytes_to_int(bytes((0, 0)), 3) == [0, 0, 0]
    assert config.bytes_to_int(bytes((0, 0, 17, 34, 78, 23, 45)), 5) == [0, 4386, 19991, 0, 0]
