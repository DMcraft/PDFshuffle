import configparser
import os
from pathlib import Path

from loguru import logger

VERSION_PROGRAM = '2.9'
VERSION_DATE = '01/08/2025'

FILE_CFG = 'config.ini'
BOOLEAN_STATES = {'1': True, 'yes': True, 'true': True, 'on': True,
                  '0': False, 'no': False, 'false': False, 'off': False}

SCALE_SIZE = 240
MAX_INT = 2 ** 16

ICON_PATH_SHUFFLE = Path.cwd() / 'icons/pdfshuffle.png'
ICON_PATH_SCANER = Path.cwd() / 'icons/pdfscaner.png'
logger.debug(ICON_PATH_SHUFFLE)


def _int_value(s: str) -> int:
    try:
        return int(s)
    except ValueError as v:
        logger.error(f'Value error {v}')
        return 0


def _get_value(section: str, option: str, fallback):
    value = None
    if isinstance(fallback, (str, int, bool, bytes)):
        try:
            value = config[section].get(option.lower())
            if value is None:
                return fallback
        except Exception as e:
            logger.error(f'Error config "{e}"!')
            return fallback

    if isinstance(fallback, str):
        return value
    elif isinstance(fallback, bool):
        if value.lower() not in BOOLEAN_STATES:
            logger.error(f'Config value bool error {option}  "{value}"')
            return fallback
        else:
            return BOOLEAN_STATES[value.lower()]
    elif isinstance(fallback, int):
        try:
            return int(value)
        except ValueError as v:
            logger.error(f'Config value int error {option} "{v}"')
            return fallback
    elif isinstance(fallback, bytes):
        try:
            return bytes.fromhex(value)
        except ValueError as v:
            logger.error(f'Config value bytes error {option} "{v}"')
            return fallback
    return None


def int_to_bytes(mas: (tuple, list)) -> bytes:
    t = []
    for m in mas:
        if 0 < m < 2 ** 16:
            t.append(m // 256)
            t.append(m % 256)
        else:
            t.extend((0, 0))
    return bytes(t)


def bytes_to_int(bas: bytes, min_length: int = 0):
    t = []
    for i in range(0, len(bas), 2):
        if i + 1 < len(bas):
            t.append(bas[i] * 256 + bas[i + 1])
    if len(t) < min_length:
        t.extend([0] * (min_length - len(t)))
    return t


config = configparser.ConfigParser()
config.read(FILE_CFG)

config['DEFAULT'] = {'program': 'PDFshuffle'}
config['VERSION'] = {'version': f'{VERSION_PROGRAM}',
                     'date': f'{VERSION_DATE}'}

if not config.has_section('OPTION'):
    config.add_section('OPTION')
if not config.has_section('PAGE'):
    config.add_section('PAGE')
if not config.has_section('FILE'):
    config.add_section('FILE')
if not config.has_section('SCAN'):
    config.add_section('SCAN')

OPTION_SPLITTER = _get_value('OPTION', 'splitter', b'\x00')
OPTION_WINDOW = _get_value('OPTION', 'window', b'\x00')
OPTION_WINDOW_SCAN = _get_value('OPTION', 'windowscan', b'\x00')

PAGE_BACKGROUND_COLOR = _get_value('PAGE', 'background_color', 'white')
PAGE_PAPER_DPI = _get_value('PAGE', 'paper_dpi', 200)
PAGE_QUALITY = _get_value('PAGE', 'quality', 90)
PAGE_PAPER_SIZE = _get_value('PAGE', 'papersize', 'A4')
PAGE_PAPER_ORIENTATION = _get_value('PAGE', 'paperorientation', 'portret')
PAGE_PAPER_FORMATTING = _get_value('PAGE', 'paperformatting', True)
PAGE_IMAGE_EXTEND = _get_value('PAGE', 'imageextend', True)
PAGE_SCALE_WIDTH_EXTEND = _get_value('PAGE', 'scalewidthextend', False)
PAGE_SCALE_HEIGHT_EXTEND = _get_value('PAGE', 'scaleheightextend', False)

PAGE_IMAGE_SIZE = _get_value('PAGE', 'imageresolution', 720)

CURRENT_PATH = _get_value('FILE', 'current_path', os.path.expanduser('~'))
SCAN_PATH = _get_value('FILE', 'scan_path', os.path.expanduser('~'))
SCAN_FILE_NAME = _get_value('FILE', 'file_name', 'ScanShuffle')

SCAN_DEVICE_NAME = _get_value('SCAN', 'dev', 'NONE')
SCAN_DEVICE_SIGNATURE = _get_value('SCAN', 'dev_signature', 'NONE')
SCAN_SOURCE = _get_value('SCAN', 'source', 'Flatbed')
SCAN_MODE = _get_value('SCAN', 'mode', 'Color')
SCAN_DPI = _get_value('SCAN', 'dpi', 200)
SCAN_AREA = _get_value('SCAN', 'area', 'Full')
SCAN_QUALITY = _get_value('SCAN', 'quality', 90)
SCAN_AUTOSAVE = _get_value('SCAN', 'autosave', False)

SCAN_SPLIT = bytes_to_int(_get_value('SCAN', 'split', int_to_bytes((0, 0, 0, 0))), 4)


def save_config():
    config.set('OPTION', 'splitter', bytes(OPTION_SPLITTER).hex())
    config.set('OPTION', 'window', bytes(OPTION_WINDOW).hex())
    config.set('OPTION', 'windowscan', bytes(OPTION_WINDOW_SCAN).hex())

    config.set('PAGE', 'background_color', PAGE_BACKGROUND_COLOR)
    config.set('PAGE', 'paper_dpi', str(PAGE_PAPER_DPI))
    config.set('PAGE', 'quality', str(PAGE_QUALITY))
    config.set('PAGE', 'papersize', PAGE_PAPER_SIZE)
    config.set('PAGE', 'paperorientation', PAGE_PAPER_ORIENTATION)
    config.set('PAGE', 'paperformatting', str(PAGE_PAPER_FORMATTING))
    config.set('PAGE', 'imageextend', str(PAGE_IMAGE_EXTEND))
    config.set('PAGE', 'scalewidthextend', str(PAGE_SCALE_WIDTH_EXTEND))
    config.set('PAGE', 'scaleheightextend', str(PAGE_SCALE_HEIGHT_EXTEND))
    config.set('PAGE', 'imageresolution', str(PAGE_IMAGE_SIZE))

    config.set('FILE', 'current_path', CURRENT_PATH)
    config.set('FILE', 'scan_path', SCAN_PATH)
    config.set('FILE', 'file_name', SCAN_FILE_NAME)

    config.set('SCAN', 'dev', SCAN_DEVICE_NAME)
    config.set('SCAN', 'dev_signature', SCAN_DEVICE_SIGNATURE)
    config.set('SCAN', 'source', SCAN_SOURCE)
    config.set('SCAN', 'mode', SCAN_MODE)
    config.set('SCAN', 'dpi', str(SCAN_DPI))
    config.set('SCAN', 'area', SCAN_AREA)
    config.set('SCAN', 'autosave', str(SCAN_AUTOSAVE))
    config.set('SCAN', 'quality', str(SCAN_QUALITY))

    config.set('SCAN', 'split', int_to_bytes(SCAN_SPLIT).hex())

    with open(FILE_CFG, 'w') as configfile:
        config.write(configfile)


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
