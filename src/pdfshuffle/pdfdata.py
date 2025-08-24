import io
import os

from loguru import logger
import config
from function import calculate_fitted_image_size

from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap, QTransform
from pdf2image import convert_from_path, convert_from_bytes
from pypdf import PdfReader, PdfWriter, PageObject
from PIL import Image


class PDFPage:
    def __init__(self, page, pix: QPixmap = None,
                 name_page: str = '', pathfile: str = '', comment: str = ''):
        self._index = None
        self.pdf: PageObject = page
        self.size = 0

        self.pix: QPixmap = pix

        self.path = pathfile
        self.name_page = name_page
        self.comment = comment

    def copy(self):
        page_copy = PageObject.create_blank_page(
            width=self.pdf.mediabox.width,
            height=self.pdf.mediabox.height
        )
        page_copy.merge_page(self.pdf)
        new_page = PDFPage(page_copy, None, self.name_page, self.path, self.comment)

        return new_page

    def get_id(self):
        if self._index is None:
            return 0
        else:
            return self._index

    def get_image(self, width, height, keep_aspect: bool = True):
        if not keep_aspect:
            width, height = calculate_fitted_image_size(self.pix.width(), self.pix.height(), width, height)
        byte_arr = io.BytesIO()
        output = PdfWriter()
        output.add_page(self.pdf)
        output.write(byte_arr)
        self.size = len(byte_arr.getvalue())
        images = convert_from_bytes(byte_arr.getvalue(), size=(width, height),
                                    dpi=600, fmt="png")
        return images[0]

    def get_pixmap(self, width: int = 0, height: int = 0) -> Image:
        if self.pix is None:
            self._reload_pixmap()
            return self.pix.scaled(width, height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        width_scale, height_scale = calculate_fitted_image_size(self.pix.width(), self.pix.height(),
                                                                width, height)
        if width_scale > self.pix.width() or height_scale > self.pix.height():
            self._reload_pixmap(max(width_scale, self.pix.width()), max(height_scale, self.pix.height()))

        return self.pix.scaled(width_scale, height_scale, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

    def _reload_pixmap(self, width: int = 0, height: int = 0):
        if width == 0 and height == 0:
            height = config.SCALE_SIZE
        else:
            if width > self.pix.width():
                width = ((width + config.SCALE_SIZE - 1) // config.SCALE_SIZE) * config.SCALE_SIZE
            if height > self.pix.height():
                height = ((height + config.SCALE_SIZE - 1) // config.SCALE_SIZE) * config.SCALE_SIZE
        width_scale, height_scale = calculate_fitted_image_size(self.pdf.mediabox.width, self.pdf.mediabox.height,
                                                                0, height, extend=True)
        logger.debug(f'Reload scale: w{width_scale} х h{height_scale}')
        image = self.get_image(width_scale or None, height_scale or None)
        # format to pixmap
        image_pix = image.convert("RGB")
        data = image_pix.tobytes("raw", "RGB")
        qi = QImage(data, image.size[0], image_pix.size[1], image_pix.size[0] * 3, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qi)
        self.pix = pixmap
        return self

    def rotate(self, angle):
        self.pdf.rotate(angle)
        trans_rotate = QTransform().rotate(angle)
        self.pix = QPixmap(self.pix).transformed(trans_rotate)
        return self

    def save_image_as(self, filename, height_size: int, quality: int = 90, dpi: int = 200):
        byte_arr = io.BytesIO()
        output = PdfWriter()
        output.add_page(self.pdf)
        output.write(byte_arr)

        images = convert_from_bytes(byte_arr.getvalue(), size=(None, height_size), fmt="png")
        if images is not None and images:
            images[0].save(filename,
                           format='JPEG',
                           quality=quality,
                           optimize=True,
                           progressive=False,
                           dpi=(dpi, dpi)
                           )


class PDFData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.data = []  # Список страниц PDF
            cls._instance.index_file = 0  # Номер загружаемого файла
        return cls._instance

    def _addpage(self, page):
        if page is not None:
            page._index = len(self.data)
            self.data.append(page)
            logger.debug(f'Add page # {page._index}')

    def last_page(self):
        if len(self.data) > 0:
            return self.data[-1]
        return None

    def clone_id(self, id_page):
        if id_page is None:
            copy_page = self.last_page().copy()
        else:
            copy_page = self.get_page(id_page).copy()
        if copy_page is None:
            logger.error(f"clone_id error, id_page {id_page} not found")
            return None
        else:
            self._addpage(copy_page)
            return copy_page.get_id()

    def add_pdf_file(self, filename):
        start_page = len(self.data)
        logger.debug("Start convert images size (80)...")
        images = convert_from_path(filename, size=(None, 80))
        logger.debug(f"End convert images len - {len(images)}")

        pdf = PdfReader(filename)
        path = os.path.dirname(filename)
        self.index_file += 1
        for i in range(len(pdf.pages)):
            if i < len(images):
                im = images[i].convert("RGB")
                data = im.tobytes("raw", "RGB")
                qi = QImage(data, im.size[0], im.size[1], im.size[0] * 3, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(qi)
            else:
                pixmap = None
            self._addpage(PDFPage(pdf.pages[i], pixmap,
                                  name_page=f'{self.index_file} p{i + 1}',
                                  pathfile=path))

        return start_page, len(self.data)

    def add_image_file(self, filename='', img=None):
        if img is None:
            img = Image.open(filename)

        img_byte_arr = io.BytesIO()

        # Конвертируем RGBA в RGB с белым фоном
        if img.mode == 'RGBA':
            white_bg = Image.new('RGB', img.size, (255, 255, 255))  # Создаем белый фон
            white_bg.paste(img, mask=img.split()[3])  # Вставляем изображение с учетом альфа-канала
            img = white_bg

        if config.PAGE_PAPER_FORMATTING:
            page_size = config.get_size_page()
            canvas_image = Image.new(mode='RGB', size=page_size, color=config.PAGE_BACKGROUND_COLOR)
            if config.PAGE_IMAGE_EXTEND:
                image_pdf = self.resize_image(img, page_size[0], page_size[1]).convert("RGB")
            else:
                image_pdf = img.convert("RGB")
            canvas_image.paste(image_pdf,
                               box=((page_size[0] - image_pdf.size[0]) // 2, (page_size[1] - image_pdf.size[1]) // 2))
        else:
            canvas_image = img.convert("RGB")

        logger.info(f'PAGE_QUALITY {config.PAGE_QUALITY}, PAGE_PAPER_DPI {config.PAGE_PAPER_DPI}')

        canvas_image.save(img_byte_arr, format='PDF', quality=config.PAGE_QUALITY,
                          dpi=(config.PAGE_PAPER_DPI, config.PAGE_PAPER_DPI))
        pdf = PdfReader(img_byte_arr)
        path = os.path.dirname(filename)
        self.index_file += 1
        self._addpage(PDFPage(pdf.pages[0], name_page=f'{self.index_file} Image', pathfile=path))
        return self.last_page()

    def get_page(self, id_page=None):
        if not self.data:  # если список пуст
            raise ValueError("self.data is empty!")
        if id_page is None:
            return self.data[len(self.data) - 1]
        if 0 <= id_page < len(self.data):
            return self.data[id_page]
        else:
            raise ValueError("id_page error value")

    def save_as(self, filename, pgs):
        output = PdfWriter()
        for i in pgs:
            output.add_page(self.get_page(i).pdf)

        with open(filename, 'wb') as f:
            output.write(f)

    @staticmethod
    def resize_image(image, width, height):
        aspect_ratio = min(width / float(image.size[0]), height / float(image.size[1]))
        new_width = int(aspect_ratio * image.size[0])
        new_height = int(aspect_ratio * image.size[1])
        return image.resize((new_width, new_height), resample=Image.Resampling.BILINEAR)
