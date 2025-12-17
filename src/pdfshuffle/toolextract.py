import io

from PIL import Image


def detect_file_format(image_data):
    """Определяет формат изображения и других файлов по сигнатурам"""
    signatures = {
        # Изображения
        b'\xFF\xD8\xFF': '.jpg',  # JPEG
        b'\x89PNG\r\n\x1a\n': '.png',  # PNG
        b'GIF8': '.gif',  # GIF
        b'II*\x00': '.tiff',  # TIFF little-endian
        b'MM\x00*': '.tiff',  # TIFF big-endian
        b'\x00\x00\x00\x0c': '.jp2',  # JPEG 2000
        b'\x0A': '.pcx',  # PCX
        b'BM': '.bmp',  # BMP
        b'\x00\x00\x01\x00': '.ico',  # ICO
        b'\x00\x00\x02\x00': '.cur',  # CUR
        b'\x49\x49\x2A\x00': '.tif',  # TIFF (little-endian)
        b'\x4D\x4D\x00\x2A': '.tif',  # TIFF (big-endian)

        # Архивы и сжатые данные
        b'PK\x03\x04': '.zip',  # ZIP
        b'PK\x05\x06': '.zip',  # ZIP (empty archive)
        b'PK\x07\x08': '.zip',  # ZIP (spanned archive)
        b'\x1F\x8B\x08': '.gz',  # GZIP
        b'BZh': '.bz2',  # BZIP2
        b'\x50\x4B\x03\x04': '.zip',  # ZIP (alternative)
        b'\x52\x61\x72\x21\x1A\x07\x00': '.rar',  # RAR
        b'\x52\x61\x72\x21\x1A\x07\x01\x00': '.rar',  # RAR5
        b'\x37\x7A\xBC\xAF\x27\x1C': '.7z',  # 7-Zip

        # Документы
        b'%PDF': '.pdf',  # PDF
        b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1': '.doc',  # MS Office (DOC, XLS, PPT)
        b'PK\x03\x04\x14\x00\x06\x00': '.docx',  # MS Office 2007+ (DOCX, XLSX)

        # Векторная графика
        b'%!PS': '.eps',  # EPS
        b'\xC5\xD0\xD3\xC6': '.eps',  # EPS (alternative)
        b'<?xml': '.svg',  # SVG (XML-based)
        b'<svg': '.svg',  # SVG

        # Метаданные и другие
        b'\x42\x4D': '.bmp',  # BMP (alternative)
        b'\x47\x49\x46\x38\x37\x61': '.gif',  # GIF87a
        b'\x47\x49\x46\x38\x39\x61': '.gif',  # GIF89a
        b'\x00\x00\x01\xF0': '.avi',  # AVI
        b'\x52\x49\x46\x46': '.avi',  # AVI/RIFF
        b'\x1A\x45\xDF\xA3': '.mkv',  # Matroska (MKV)
        b'ftyp': '.mp4',  # MP4
        b'\x30\x26\xB2\x75\x8E\x66\xCF\x11': '.wmv',  # WMV
    }

    # Проверяем длину данных
    if len(image_data) < 4:
        return '.bin'

    for signature, extension in signatures.items():
        if image_data.startswith(signature):
            return extension

    return '.bin'  # неизвестный формат


def decode_indexed_image(raw_data, width, height, colorspace_info)-> Image.Image:
    """
    Декодирует изображение с Indexed цветовым пространством

    Args:
        raw_data: Сырые данные изображения (индексы палитры)
        width, height: Размеры изображения
        colorspace_info: Массив вида ['/Indexed', base_space, hival, palette]
    """

    # Проверяем, что это Indexed
    if not isinstance(colorspace_info, list) or colorspace_info[0] != "/Indexed":
        raise ValueError("Не Indexed colorspace")

    # Извлекаем информацию о палитре
    base_space = colorspace_info[1]  # Обычно /DeviceRGB или /DeviceGray
    hival = colorspace_info[2]  # Максимальный индекс (обычно 255)
    palette_bytes = colorspace_info[3]  # Байты палитры

    # Декодируем палитру
    palette = []

    if base_space == "/DeviceRGB":
        # Палитра в формате RGB (3 байта на цвет)
        color_count = len(palette_bytes) // 3
        print(f"Colors in palette: {color_count}")

        for i in range(color_count):
            r = palette_bytes[i * 3]
            g = palette_bytes[i * 3 + 1]
            b = palette_bytes[i * 3 + 2]
            palette.append((r, g, b))

    elif base_space == "/DeviceCMYK":
        # Палитра в формате CMYK (4 байта на цвет)
        color_count = len(palette_bytes) // 4
        print(f"Colors in palette: {color_count} (CMYK)")

        for i in range(color_count):
            c = palette_bytes[i * 4]
            m = palette_bytes[i * 4 + 1]
            y = palette_bytes[i * 4 + 2]
            k = palette_bytes[i * 4 + 3]
            # Конвертируем CMYK в RGB, так как PIL работает в RGB для палитры
            r = int(255 * (1 - c / 255) * (1 - k / 255))
            g = int(255 * (1 - m / 255) * (1 - k / 255))
            b = int(255 * (1 - y / 255) * (1 - k / 255))
            palette.append((r, g, b))

    elif base_space == "/DeviceGray":
        # Палитра в формате Grayscale (1 байт на цвет)
        for i in range(len(palette_bytes)):
            gray = palette_bytes[i]
            palette.append((gray, gray, gray))

    # Проверяем размер данных
    expected_size = width * height
    actual_size = len(raw_data)

    print(f"\nImage data analysis:")
    print(f"  Expected pixels: {width} x {height} = {expected_size}")
    print(f"  Actual data size: {actual_size} bytes")
    print(f"  First 20 indices: {list(raw_data[:20])}")

    if actual_size != expected_size:
        print(f"  WARNING: Data size mismatch! Maybe padding or compression")

    # Создаем изображение
    img = Image.new("P", (width, height))

    # Устанавливаем палитру
    # PIL ожидает палитру как плоский список [r,g,b, r,g,b, ...]
    flat_palette = []
    for color in palette:
        flat_palette.extend(color)

    # Дополняем до 768 байт (256 цветов * 3)
    while len(flat_palette) < 768:
        flat_palette.append(0)

    img.putpalette(flat_palette)

    # Загружаем данные (индексы палитры)
    img.frombytes(raw_data)

    return img


def decode_1bit_image(data, width, height)-> Image.Image:
    """
    Обработка 1-битных (черно-белых) изображений
    """

    # Создаем изображение
    img = Image.new("1", (width, height))
    pixels = img.load()

    # Конвертируем байты в биты
    bit_index = 0
    for byte in data:
        for bit in range(8):
            if bit_index >= width * height:
                break
            x = bit_index % width
            y = bit_index // width
            # Проверяем бит (старший бит первым)
            pixel_value = 0 if (byte >> (7 - bit)) & 1 else 1
            pixels[x, y] = pixel_value
            bit_index += 1

    return img