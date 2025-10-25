from pathlib import Path

from PIL import Image, ImageDraw
from PyQt5.QtGui import QPixmap, QImage
import os
from loguru import logger


def load_pil_from_file(file_path: Path, size: int) ->  Image.Image:
    """
    Загружает изображение и вписывает в квадрат с сохранением пропорций.
    Если изображение не найдено, создает розовый квадрат указанного размера.

    :param file_path: Путь к файлу изображения.
    :param size: Размер квадрата (ширина и высота одинаковые).
    :return: Объект QPixmap размером size x size.
    """
    if not os.path.exists(file_path):
        logger.warning(f"Файл изображения не найден: {file_path}. Создается розовый квадрат.")
        return create_pink_square(size)

    try:
        # Загрузка изображения с помощью PIL
        pil_image = Image.open(file_path)

        # Преобразование в RGB
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')

        # Вписываем изображение в квадрат с сохранением пропорций
        pil_image = fit_image_in_square(pil_image, size)

        logger.debug(f"Изображение успешно загружено и обработано: {file_path}")
        return pil_image

    except Exception as e:
        logger.error(f"Ошибка при загрузке изображения {file_path}: {str(e)}")
        return create_pink_square(size)


def pil_image_to_qpixmap(pil_image: Image.Image) -> QPixmap:
    """
    Конвертирует PIL Image в QPixmap.

    :param pil_image: Изображение PIL.
    :return: QPixmap.
    """
    # Конвертируем PIL Image в байты
    if pil_image.mode == 'RGB':
        format = QImage.Format_RGB888
    elif pil_image.mode == 'RGBA':
        format = QImage.Format_RGBA8888
    else:
        pil_image = pil_image.convert('RGB')
        format = QImage.Format_RGB888

    data = pil_image.tobytes('raw', pil_image.mode)
    qimage = QImage(data, pil_image.width, pil_image.height,
                    pil_image.width * len(pil_image.mode), format)

    return QPixmap.fromImage(qimage)


def create_pink_square(size: int) -> QPixmap:
    """
    Создает розовый квадрат указанного размера.

    :param size: Размер квадрата.
    :return: QPixmap с розовым квадратом.
    """
    # Создаем изображение с розовым фоном
    pink_color = (255, 192, 203)  # Розовый цвет RGB
    pil_image = Image.new('RGB', (size, size), pink_color)

    # Добавляем крестик для индикации отсутствия изображения
    draw = ImageDraw.Draw(pil_image)
    # Рисуем диагональный крестик
    draw.line((0, 0, size, size), fill=(200, 100, 120), width=2)
    draw.line((0, size, size, 0), fill=(200, 100, 120), width=2)

    return pil_image_to_qpixmap(pil_image)


def fit_image_in_square(pil_image: Image.Image, square_size: int) -> Image.Image:
    """
    Вписывает изображение в квадрат с сохранением пропорций.

    :param pil_image: Исходное изображение PIL.
    :param square_size: Размер квадрата.
    :return: Изображение, вписанное в квадрат.
    """
    original_width, original_height = pil_image.size

    # Вычисляем масштаб для вписывания в квадрат с сохранением пропорций
    scale = min(square_size / original_width, square_size / original_height)
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    # Изменяем размер с сохранением пропорций
    resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Создаем квадратное изображение с серым фоном
    square_image = Image.new('RGB', (square_size, square_size), (240, 240, 240))

    # Вычисляем позицию для центрирования
    x_offset = (square_size - new_width) // 2
    y_offset = (square_size - new_height) // 2

    # Вставляем изображение в центр квадрата
    square_image.paste(resized_image, (x_offset, y_offset))

    return square_image


# Альтернативный способ конвертации (более простой)
def pil_image_to_qpixmap_simple(pil_image: Image.Image) -> QPixmap:
    """
    Простой способ конвертации PIL Image в QPixmap через временный файл.
    Менее эффективный, но надежный.
    """
    import tempfile
    import io

    # Сохраняем изображение в буфер памяти
    buffer = io.BytesIO()
    pil_image.save(buffer, format='PNG')
    buffer.seek(0)

    # Загружаем из буфера в QPixmap
    pixmap = QPixmap()
    pixmap.loadFromData(buffer.getvalue())

    return pixmap