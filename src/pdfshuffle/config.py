import configparser
import os
from pathlib import Path
from typing import Sequence
from loguru import logger

from loadimage import load_pil_from_file


def _int_value(s: str) -> int:
    """Преобразует строку в целое число, возвращает 0 при ошибке."""
    try:
        return int(s)
    except ValueError as v:
        logger.error(f'Value error: {v}')
        return 0


def _get_value(config_section: str, option: str, fallback):
    """
    Получает значение из конфигурации с учётом типа fallback.
    Поддерживает типы: str, int, bool, bytes.
    """
    if not config.has_section(config_section):
        return fallback

    value = config[config_section].get(option.lower())

    if value is None:
        return fallback

    if isinstance(fallback, str):
        return value
    elif isinstance(fallback, bool):
        normalized_value = value.lower()
        if normalized_value in BOOLEAN_STATES:
            return BOOLEAN_STATES[normalized_value]
        else:
            logger.error(f'Config value bool error for "{option}": "{value}"')
            return fallback
    elif isinstance(fallback, int):
        try:
            return int(value)
        except ValueError as v:
            logger.error(f'Config value int error for "{option}": "{v}"')
            return fallback
    elif isinstance(fallback, bytes):
        try:
            return bytes.fromhex(value)
        except ValueError as v:
            logger.error(f'Config value bytes error for "{option}": "{v}"')
            return fallback
    return fallback


def _landing_size(size, landscape=False):
    """
    Возвращает размер страницы в зависимости от ориентации.
    """
    w, h = size
    if landscape:
        return max(w, h), min(w, h)
    else:
        return min(w, h), max(w, h)


def get_size_page():
    """
    Возвращает размер страницы в пикселях на основе DPI и формата.
    """
    format_paper = {
        'A10': (1.46, 1.02),
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

    page_size = format_paper.get(PAGE_PAPER_SIZE, (0, 0))
    width_px = int(page_size[0] * PAGE_PAPER_DPI)
    height_px = int(page_size[1] * PAGE_PAPER_DPI)

    return _landing_size((width_px, height_px), PAGE_PAPER_ORIENTATION.lower() == 'landscape')


def int_to_bytes(int_sequence: Sequence[int]) -> bytes:
    """
    Преобразует последовательность целых чисел в байтовую строку.

    Каждое число из входной последовательности интерпретируется как 16-битное
    беззнаковое целое число (uint16) и преобразуется в два байта в формате
    big-endian (старший байт первым). Числа вне диапазона [0, 65535] заменяются
    на два нулевых байта (0x00).

    Аргументы:
        int_sequence: Последовательность целых чисел (список или кортеж).

    Возвращает:
        bytes: Байтовая строка длиной 2 * len(int_sequence).

    Возвращает:
        bytes: Байтовая строка, содержащая по два байта на каждое число из исходной
               последовательности. Длина результирующей строки — 2 * len(int_sequence).
    """
    result = []
    for m in int_sequence:
        if 0 <= m < MAX_UINT16:
            result.append(m // 256)
            result.append(m % 256)
        else:
            result.extend((0, 0))
    return bytes(result)


def bytes_to_int(data_bytes: bytes, min_length: int = 0):
    """Преобразует байтовую последовательность в список целых чисел по 16 бит.

    Каждая пара байтов из входной последовательности интерпретируется как
    16-битное беззнаковое целое число в порядке big-endian (старший байт первым).
    Если длина результирующего списка меньше заданного минимального значения,
    он дополняется нулями до нужной длины.

    Аргументы:
        data_bytes (bytes): Входная байтовая последовательность для преобразования.
        min_length (int): Минимальная длина результирующего списка. Если
            количество прочитанных 16-битных значений меньше, чем min_length,
            список будет дополнен нулями. По умолчанию 0.

    Возвращает:
        list[int]: Список целых чисел, полученных из пар байтов. Длина списка
        не меньше min_length.
    """
    result = []
    for i in range(0, len(data_bytes), 2):
        if i + 1 < len(data_bytes):
            result.append(data_bytes[i] * 256 + data_bytes[i + 1])
    if len(result) < min_length:
        result.extend([0] * (min_length - len(result)))
    return result


# Константы программы
VERSION_PROGRAM = '2.10.7'
VERSION_DATE = '05/12/2025'
DEFAULT_DPI_VALUES = (75, 100, 150, 200, 300, 600, 1200)
MAX_UINT16 = 2 ** 16  # Используется для проверки диапазона значений
FILE_CFG = 'config.ini'  # Путь к конфигурационному файлу
# Словарь для преобразования строковых значений в булевы
BOOLEAN_STATES = {
    '1': True, 'yes': True, 'true': True, 'on': True,
    '0': False, 'no': False, 'false': False, 'off': False
}

# Пути иконок (используем относительные пути)
ICON_PATH_SHUFFLE = Path(__file__).parent / 'icons' / 'pdfshuffle.png'
ICON_PATH_SCANER = Path(__file__).parent / 'icons' / 'pdfscaner.png'
ICON_PATH_PAGE = Path(__file__).parent / 'icons' / 'page.png'
logger.debug(f"Icon paths: {ICON_PATH_SHUFFLE}, {ICON_PATH_SCANER}")

DEFAULT_ICON_PAGE = load_pil_from_file(ICON_PATH_PAGE, 80)

# Инициализация конфига
config = configparser.ConfigParser()

files_read_ok = config.read(FILE_CFG)
if len(files_read_ok) > 0:
    print(f"Файл конфигурации {files_read_ok[0]} успешно прочитан.")
else:
    logger.error(f"Файл конфигурации {FILE_CFG} не найден.")
    print(f"Файл конфигурации {FILE_CFG} не найден.")

# Установка дефолтных секций и значений
config['DEFAULT'] = {'program': 'PDFshuffle'}
config['VERSION'] = {'version': VERSION_PROGRAM, 'date': VERSION_DATE}

for section in ['OPTION', 'PAGE', 'FILE', 'SCAN', 'SCAN_SPLIT']:
    if not config.has_section(section):
        config.add_section(section)

SCALE_SIZE = _get_value('DEFAULT', 'scale_size_default', 240)

# Чтение параметров из конфига
OPTION_SPLITTER = _get_value('OPTION', 'splitter', b'\x00')
OPTION_WINDOW = _get_value('OPTION', 'window', b'\x00')
OPTION_WINDOW_SCAN = _get_value('OPTION', 'windowscan', b'\x00')

PAGE_BACKGROUND_COLOR = _get_value('PAGE', 'background_color', 'white')
PAGE_PAPER_DPI = _get_value('PAGE', 'paper_dpi', 200)
PAGE_QUALITY = _get_value('PAGE', 'quality', 90)
PAGE_PAPER_SIZE = _get_value('PAGE', 'papersize', 'A4')
PAGE_PAPER_ORIENTATION = _get_value('PAGE', 'paperorientation', 'portrait')
PAGE_PAPER_FORMATTING = _get_value('PAGE', 'paperformatting', False)
PAGE_IMAGE_EXTEND = _get_value('PAGE', 'imageextend', False)
PAGE_AUTO_SIZE = _get_value('PAGE', 'autosize', False)
PAGE_AUTO_ROTATE = _get_value('PAGE', 'autorotate', False)
PAGE_SCALE_WIDTH_EXTEND = _get_value('PAGE', 'scalewidthextend', True)
PAGE_SCALE_HEIGHT_EXTEND = _get_value('PAGE', 'scaleheightextend', True)
PAGE_IMAGE_SIZE = _get_value('PAGE', 'imageresolution', 1169)

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

SCAN_SPLIT = {
    'Full': bytes_to_int(_get_value('SCAN_SPLIT',
                                    'Full', int_to_bytes((0, 0, 210, 297, 0, 0, 210, 297))), 8),
    'A4': bytes_to_int(_get_value('SCAN_SPLIT',
                                  'A4', int_to_bytes((1, 1, 210, 297, 5, 5, 210, 297))), 8),
    'A5': bytes_to_int(_get_value('SCAN_SPLIT',
                                  'A5', int_to_bytes((1, 1, 149, 210, 5, 5, 149, 210))), 8),
}


def save_config():
    """Сохраняет текущие настройки в конфигурационный файл."""
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
    config.set('PAGE', 'autosize', str(PAGE_AUTO_SIZE))
    config.set('PAGE', 'autorotate', str(PAGE_AUTO_ROTATE))
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

    for key, value in SCAN_SPLIT.items():
        config.set('SCAN_SPLIT', key, int_to_bytes(value).hex())

    try:
        with open(FILE_CFG, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
    except PermissionError as e:
        logger.error(f'Недостаточно прав для записи конфига: {e}')
