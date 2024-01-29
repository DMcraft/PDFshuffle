from configstring import ConfigString



def test_set():
    cfg = ConfigString(34, typ=int)
    assert cfg == 34

    cfg2 = ConfigString('48', typ=str)
    assert cfg2 == '48'
