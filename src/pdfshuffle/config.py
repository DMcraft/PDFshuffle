import configparser
import os

from loguru import logger

FILE_CFG = 'config.ini'


def _int_value(s: str) -> int:
    try:
        return int(s)
    except ValueError as v:
        logger.error(f'Value error {v}')
        return 0


config = configparser.ConfigParser()
config.read(FILE_CFG)

config['DEFAULT'] = {'program': 'PDFshuffle'}
config['VERSION'] = {'version': '2.5',
                     'date': '02.02.2024'}

if not config.has_section('PAGE'):
    config.add_section('PAGE')
if not config.has_section('FILE'):
    config.add_section('FILE')
if not config.has_section('SCAN'):
    config.add_section('SCAN')


PAGE_BACKGROUND_COLOR = config['PAGE'].get('BACKGROUND_COLOR', fallback='white')
PAGE_PAPER_DPI = _int_value(config['PAGE'].get('paperDPI', fallback='200'))
PAGE_QUALITY = _int_value(config['PAGE'].get('QUALITY', fallback='90'))
PAGE_PAPER_SIZE = config['PAGE'].get('papersize', fallback='A4')
PAGE_PAPER_ORIENTATION = config['PAGE'].get('paperorientation', fallback='portret')
try:
    PAGE_PAPER_FORMATTING = config['PAGE'].getboolean('paperformatting', fallback=True)
except ValueError:
    PAGE_PAPER_FORMATTING = True
try:
    PAGE_IMAGE_EXTEND = config['PAGE'].getboolean('imageextend', fallback=True)
except ValueError:
    PAGE_IMAGE_EXTEND = True

CURRENT_PATH = config['FILE'].get('current_path', fallback=os.path.expanduser('~'))
SCAN_PATH = config['FILE'].get('scan_path', fallback=os.path.expanduser('~'))
SCAN_FILE_NAME = config['FILE'].get('file_name', fallback='ScanShuffle')

SCAN_DEVICE_NAME = config['SCAN'].get('dev', fallback='NONE')
SCAN_DEVICE_SIGNATURE = config['SCAN'].get('dev_signature', fallback='NONE')
SCAN_SOURCE = config['SCAN'].get('source', fallback='Flatbed')
SCAN_MODE = config['SCAN'].get('mode', fallback='Color')
SCAN_DPI = _int_value(config['SCAN'].get('dpi', fallback='200'))
SCAN_AREA = config['SCAN'].get('area', fallback='Full')

SCAN_SPLIT = tuple(map(_int_value, config['SCAN'].get('split', fallback='5,6, 7,8').split(',', 4)))


def _landing_size(size, land=False):
    w, h = size
    if land:
        return max(w, h), min(w, h)
    else:
        return min(w, h), max(w, h)


def get_size_page():
    format_paper = {'A10': (1.46, 1.02),
                    'A9': (1.46, 2.05),
                    'A8': (2.05, 2.91),
                    'A7': (2.91, 4.13),
                    'A6': (4.13, 5.83),
                    'A5': (5.83, 8.27),
                    'A4': (8.27, 11.69),
                    'A3': (11.69, 16.54),
                    'A2': (16.54, 23.39),
                    'A1': (23.39, 33.11),
                    'A0': (33.11, 46.81)
                    }

    if PAGE_PAPER_SIZE in format_paper:
        page_size = format_paper[PAGE_PAPER_SIZE]
    else:
        page_size = (0, 0)

    return _landing_size((int(page_size[0] * PAGE_PAPER_DPI), int(page_size[1] * PAGE_PAPER_DPI)),
                         PAGE_PAPER_ORIENTATION.lower() == 'landscape')


def save_config():
    # config.set('PAGE', 'FORMAT', PAGE_FORMAT)
    config.set('PAGE', 'BACKGROUND_COLOR', PAGE_BACKGROUND_COLOR)
    # config.set('PAGE', 'LANDING', PAGE_LANDING)
    config.set('PAGE', 'paperDPI', str(PAGE_PAPER_DPI))
    config.set('PAGE', 'QUALITY', str(PAGE_QUALITY))
    config.set('PAGE', 'papersize', PAGE_PAPER_SIZE)
    config.set('PAGE', 'paperorientation', PAGE_PAPER_ORIENTATION)
    config.set('PAGE', 'paperformatting', str(PAGE_PAPER_FORMATTING))
    config.set('PAGE', 'imageextend', str(PAGE_IMAGE_EXTEND))

    config.set('FILE', 'current_path', CURRENT_PATH)
    config.set('FILE', 'scan_path', SCAN_PATH)
    config.set('FILE', 'file_name', SCAN_FILE_NAME)

    config.set('SCAN', 'dev', SCAN_DEVICE_NAME)
    config.set('SCAN', 'dev_signature', SCAN_DEVICE_SIGNATURE)
    config.set('SCAN', 'source', SCAN_SOURCE)
    config.set('SCAN', 'mode', SCAN_MODE)
    config.set('SCAN', 'dpi', str(SCAN_DPI))
    config.set('SCAN', 'area', SCAN_AREA)
    config.set('SCAN', 'split', ','.join(map(str, SCAN_SPLIT)))

    with open(FILE_CFG, 'w') as configfile:
        config.write(configfile)
