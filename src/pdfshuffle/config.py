import configparser
import os
from pathlib import Path
from loadimage import load_pixmap_from_file

from loguru import logger

# Константы программы
VERSION_PROGRAM = '2.10.1'
VERSION_DATE = '02/10/2025'

# Путь к конфигурационному файлу
FILE_CFG = 'config.ini'

# Словарь для преобразования строковых значений в булевы
BOOLEAN_STATES = {
    '1': True, 'yes': True, 'true': True, 'on': True,
    '0': False, 'no': False, 'false': False, 'off': False
}

# Другие константы
MAX_UINT16 = 2 ** 16  # Используется для проверки диапазона значений

# Пути иконок (используем относительные пути)
ICON_PATH_SHUFFLE = Path(__file__).parent / 'icons' / 'pdfshuffle.png'
ICON_PATH_SCANER = Path(__file__).parent / 'icons' / 'pdfscaner.png'
ICON_PATH_PAGE = Path(__file__).parent / 'icons' / 'page.png'
logger.debug(f"Icon paths: {ICON_PATH_SHUFFLE}, {ICON_PATH_SCANER}")

DEFAULT_ICON_PAGE = load_pixmap_from_file(ICON_PATH_PAGE, 80)


def _int_value(s: str) -> int:
    """Преобразует строку в целое число, возвращает 0 при ошибке."""
    try:
        return int(s)
    except ValueError as v:
        logger.error(f'Value error: {v}')
        return 0


def _get_value(section: str, option: str, fallback):
    """
    Получает значение из конфигурации с учётом типа fallback.
    Поддерживает типы: str, int, bool, bytes.
    """
    if not config.has_section(section):
        return fallback

    value = config[section].get(option.lower())

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


def int_to_bytes(mas: (tuple, list)) -> bytes:
    """
    Преобразует список или кортеж целых чисел в байты.
    Каждое число должно быть в диапазоне [0, 2^16).
    """
    result = []
    for m in mas:
        if 0 <= m < MAX_UINT16:
            result.append(m // 256)
            result.append(m % 256)
        else:
            result.extend((0, 0))
    return bytes(result)


def bytes_to_int(bas: bytes, min_length: int = 0):
    """
    Преобразует байты в список целых чисел.
    Каждая пара байт интерпретируется как 16-битное число.
    """
    result = []
    for i in range(0, len(bas), 2):
        if i + 1 < len(bas):
            result.append(bas[i] * 256 + bas[i + 1])
    if len(result) < min_length:
        result.extend([0] * (min_length - len(result)))
    return result


# Инициализация конфига
config = configparser.ConfigParser()

# Создаём файл конфигурации, если его нет
if not Path(FILE_CFG).exists():
    try:
        logger.info(f"Файл конфигурации {FILE_CFG} не найден. Создаём новый.")
        with open(FILE_CFG, 'w', encoding='utf-8') as f:
            pass
    except PermissionError as e:
        logger.error(f"Не удалось создать файл {FILE_CFG}: {e}")

config.read(FILE_CFG)

# Установка дефолтных секций и значений
config['DEFAULT'] = {'program': 'PDFshuffle'}
config['VERSION'] = {'version': VERSION_PROGRAM, 'date': VERSION_DATE}

for section in ['OPTION', 'PAGE', 'FILE', 'SCAN']:
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
PAGE_PAPER_FORMATTING = _get_value('PAGE', 'paperformatting', True)
PAGE_IMAGE_EXTEND = _get_value('PAGE', 'imageextend', True)
PAGE_AUTO_SIZE = _get_value('PAGE', 'autosize', True)
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

    try:
        with open(FILE_CFG, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
    except PermissionError as e:
        logger.error(f'Недостаточно прав для записи конфига: {e}')


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
