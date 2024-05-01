import io
from loguru import logger

from PyQt5.QtGui import QImage, QPixmap, QTransform
from pdf2image import convert_from_path, convert_from_bytes
from PyPDF2 import PdfReader, PdfWriter, PageObject
from PIL import Image

import config


class PDFPage:
    def __init__(self, name_page: str = '', pix=None, pdf=None, comment: str = ''):
        self.name_page = name_page
        self.pix = pix
        self.pdf: PageObject = pdf
        self.comment = comment


class PDFData:
    def __init__(self):
        self.data: list[PDFPage] = []
        self.pdf_read = []

    def _addpage(self, page):
        self.data.append(page)

    def rotatepage(self, page, rotate):
        self.data[page].pdf.rotate(rotate)
        trans_rotate = QTransform().rotate(rotate)
        self.data[page].pix = QPixmap(self.data[page].pix).transformed(trans_rotate)

    def add_pdf_file(self, filename):
        start_page = len(self.data)
        images = convert_from_path(filename, size=(None, config.SCALE_SIZE))

        pdf = PdfReader(filename)
        self.pdf_read.append(pdf)
        for i in range(len(pdf.pages)):
            im = images[i].convert("RGB")
            data = im.tobytes("raw", "RGB")
            qi = QImage(data, im.size[0], im.size[1], im.size[0] * 3, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qi)
            self._addpage(PDFPage(f'{len(self.pdf_read)}| Page {i + 1}', pixmap, pdf.pages[i]))

        return start_page, len(self.data)

    def add_image_file(self, filename, img=None):
        if img is None:
            img = Image.open(filename)

        img_byte_arr = io.BytesIO()

        if config.PAGE_PAPER_FORMATTING:
            page_size = config.get_size_page()
            canvas_image = Image.new(mode='RGB', size=page_size, color=config.PAGE_BACKGROUND_COLOR)
            if config.PAGE_IMAGE_EXTEND:
                image_pdf = self.resize_image(img, page_size[0], page_size[1]).convert("RGB")
            else:
                image_pdf = img
            canvas_image.paste(image_pdf,
                               box=((page_size[0] - image_pdf.size[0]) // 2, (page_size[1] - image_pdf.size[1]) // 2))
        else:
            canvas_image = img

        logger.info(f'PAGE_QUALITY {config.PAGE_QUALITY}, PAGE_PAPER_DPI {config.PAGE_PAPER_DPI}')

        canvas_image.save(img_byte_arr, format='PDF', quality=config.PAGE_QUALITY,
                          dpi=(config.PAGE_PAPER_DPI, config.PAGE_PAPER_DPI))
        pdf = PdfReader(img_byte_arr)
        self.pdf_read.append(pdf)

        img = self.resize_image(canvas_image, config.SCALE_SIZE, config.SCALE_SIZE).convert("RGB")
        data = img.tobytes("raw", "RGB")
        qi = QImage(data, img.size[0], img.size[1], img.size[0] * 3, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qi)
        self._addpage(PDFPage(f'{len(self.pdf_read)}| Image',
                              pixmap, pdf.pages[0],
                              f'Размер: {img_byte_arr.getbuffer().nbytes // 1024} кб'
                              ))
        return len(self.data)

    def resize_image(self, image, width, height):
        aspect_ratio = min(width / float(image.size[0]), height / float(image.size[1]))
        new_width = int(aspect_ratio * image.size[0])
        new_height = int(aspect_ratio * image.size[1])
        return image.resize((new_width, new_height), resample=Image.Resampling.BILINEAR)

    def reload_image(self, id_page: int, size: int = config.SCALE_SIZE * 4):
        byte_arr = io.BytesIO()
        output = PdfWriter()
        output.add_page(self.data[id_page].pdf)
        output.write(byte_arr)

        image = convert_from_bytes(byte_arr.getvalue(), size=(None, size))
        im = image[0].convert("RGB")
        data = im.tobytes("raw", "RGB")
        qi = QImage(data, im.size[0], im.size[1], im.size[0] * 3, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qi)

        self.data[id_page].pix = pixmap
        return pixmap

    def save_as(self, filename, pgs):
        output = PdfWriter()
        for i in pgs:
            output.add_page(self.data[i].pdf)

        with open(filename, 'wb') as f:
            output.write(f)
