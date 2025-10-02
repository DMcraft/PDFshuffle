from src.pdfshuffle.configstring import ConfigString
import pytest



def test_init_str():
    cs = ConfigString("test", typ=str)
    assert cs.get() == "test"
    assert isinstance(cs._data, str)


def test_init_int():
    cs = ConfigString(123, typ=int)
    assert cs.get() == 123
    assert isinstance(cs._data, int)


def test_init_list():
    cs = ConfigString([1, 2, 3], typ=list)
    assert cs.get() == [1, 2, 3]
    assert isinstance(cs._data, list)


def test_init_float_as_str():
    cs = ConfigString("3.14", typ=str)
    assert cs.get() == "3.14"


def test_set_str_from_int():
    cs = ConfigString(123, typ=str)
    assert cs.get() == "123"


def test_set_int_from_str_valid():
    cs = ConfigString("456", typ=int)
    assert cs.get() == 456


def test_set_int_from_str_invalid():
    with pytest.raises(ValueError):
        ConfigString("abc", typ=int)


def test_set_list_from_string():
    cs = ConfigString("abc", typ=list)
    assert cs.get() == ["a", "b", "c"]


def test_set_list_from_iterable():
    cs = ConfigString((1, 2, 3), typ=list)
    assert cs.get() == [1, 2, 3]


def test_set_list_from_uniterable():
    with pytest.raises(TypeError):
        ConfigString(None, typ=list)


def test_set_invalid_type():
    with pytest.raises(TypeError):
        ConfigString("test", typ=dict)


def test_set_typ_must_be_class():
    with pytest.raises(TypeError):
        ConfigString("test", typ=ConfigString())


def test_get_returns_original_data():
    cs = ConfigString([1, 2, 3], typ=list)
    assert cs.get() == [1, 2, 3]


def test_str_representation_str():
    cs = ConfigString("hello", typ=str)
    assert str(cs) == "hello"


def test_str_representation_int():
    cs = ConfigString(123, typ=int)
    assert str(cs) == "123"


def test_str_representation_list():
    cs = ConfigString([1, 2, 3], typ=list)
    assert str(cs) == "1,2,3"


def test_str_representation_unsupported_type():
    cs = ConfigString(None, typ=int)  # Will raise error in __str__
    with pytest.raises(TypeError):
        str(cs)


def test_eq_same_instance():
    cs1 = ConfigString("test")
    cs2 = cs1
    assert cs1 == cs2


def test_eq_same_data():
    cs1 = ConfigString("test")
    cs2 = ConfigString("test")
    assert cs1 == cs2


def test_eq_different_data():
    cs1 = ConfigString("test")
    cs2 = ConfigString("other")
    assert cs1 != cs2


def test_eq_with_primitive():
    cs = ConfigString(123, typ=int)
    assert cs == 123


def test_hash_str():
    cs = ConfigString("test")
    assert hash(cs) == hash("test")


def test_hash_int():
    cs = ConfigString(123, typ=int)
    assert hash(cs) == hash(123)


def test_hash_list():
    cs = ConfigString([1, 2, 3], typ=list)
    assert hash(cs) == hash((1, 2, 3))


def test_hash_unhashable_data():
    cs = ConfigString([1, 2, 3], typ=list)
    cs._data[0] = None  # Make unhashable
    with pytest.raises(TypeError):
        hash(cs)


def test_len_str():
    cs = ConfigString("test")
    assert len(cs) == 4


def test_len_int():
    cs = ConfigString(123, typ=int)
    with pytest.raises(TypeError):
        len(cs)


def test_len_list():
    cs = ConfigString([1, 2, 3], typ=list)
    assert len(cs) == 3


def test_getitem_list_valid():
    cs = ConfigString([1, 2, 3], typ=list)
    assert cs[1] == 2


def test_getitem_list_invalid():
    cs = ConfigString("test", typ=str)
    with pytest.raises(TypeError):
        cs[0]


def test_setitem_list_valid():
    cs = ConfigString([1, 2, 3], typ=list)
    cs[1] = 99
    assert cs.get() == [1, 99, 3]


def test_setitem_list_invalid_index():
    cs = ConfigString([1, 2, 3], typ=list)
    with pytest.raises(IndexError):
        cs[3] = 99


def test_setitem_non_list():
    cs = ConfigString("test", typ=str)
    with pytest.raises(TypeError):
        cs[0] = "x"


def test_repr_str():
    cs = ConfigString("test")
    assert repr(cs) == "ConfigString(str, 'test')"


def test_repr_int():
    cs = ConfigString(123, typ=int)
    assert repr(cs) == "ConfigString(int, 123)"


def test_repr_list():
    cs = ConfigString([1, 2, 3], typ=list)
    assert repr(cs) == "ConfigString(list, [1, 2, 3])"
