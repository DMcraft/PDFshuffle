import configparser
import os

FILE_CFG = 'config.ini'

config = configparser.ConfigParser()
config.read(FILE_CFG)

config['DEFAULT'] = {'program': 'PDFshuffle'}
config['VERSION'] = {'version': '1.01',
                     'date': '15.09.2023'}
config.add_section('PAGE')
config.add_section('FILE')

PAGE_FORMAT = config['PAGE'].get('FORMAT', fallback='A4')
PAGE_BACKGROUND_COLOR = config['PAGE'].get('BACKGROUND_COLOR', fallback='white')
PAGE_LANDING = config['PAGE'].get('LANDING', fallback='portret')
PAGE_DPI = config['PAGE'].getint('DPI', fallback=200)

CURRENT_PATH = config['FILE'].get('current_path', fallback=os.path.expanduser('~'))


def _landing_size(size, land=False):
    w, h = size
    if land:
        return max(w, h), min(w, h)
    else:
        return min(w, h), max(w, h)


def get_size_page():
    formatA = {'A10': (1.46, 1.02),
               'A9': (1.46, 2.05),
               'A8': (2.05, 2.91),
               'A7': (2.91, 4.13),
               'A6': (4.13, 5.83),
               'A5': (5.83, 8.27),
               'A4': (8.27, 11.69),
               'A3': (11.69, 16.54),
               'A2': (16.54, 23.39),
               'A1': (23.39, 33.11),
               'A0': (33.11, 46.81)}

    if PAGE_FORMAT in formatA:
        page_size = formatA[PAGE_FORMAT]
    else:
        page_size = (0, 0)

    return _landing_size((int(page_size[0] * PAGE_DPI), int(page_size[1] * PAGE_DPI)),
                         PAGE_LANDING.lower() == 'landscape')


def save_config():
    config.set('PAGE', 'FORMAT', PAGE_FORMAT)
    config.set('PAGE', 'BACKGROUND_COLOR', PAGE_BACKGROUND_COLOR)
    config.set('PAGE', 'LANDING', PAGE_LANDING)
    config.set('PAGE', 'DPI', str(PAGE_DPI))

    config.set('FILE', 'current_path', CURRENT_PATH)

    with open(FILE_CFG, 'w') as configfile:
        config.write(configfile)
