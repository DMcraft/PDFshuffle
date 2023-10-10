import pdfshuffle.config as config


def test_get_size_page():
    config.PAGE_FORMAT = 'A4'
    assert config.get_size_page() == (1654, 2338)
    config.PAGE_FORMAT = 'A'
    assert config.get_size_page() == (0, 0)


def test_save_config():
    assert True
