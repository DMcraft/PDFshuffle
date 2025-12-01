

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