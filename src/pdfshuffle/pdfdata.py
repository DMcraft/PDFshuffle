import io

from PyQt5.QtGui import QImage, QPixmap
from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter, PageObject
from PIL import Image

import config


class PDFPage:
    def __init__(self, name_page: str = '', pix=None, pdf=None):
        self.name_page = name_page
        self.pix = pix
        self.pdf: PageObject = pdf


class PDFData:
    def __init__(self):
        self.data: list[PDFPage] = []
        self.pdf_read = []

    def _addpage(self, page):
        self.data.append(page)

    def rotatepage(self, page, rotate):
        self.data[page].pdf.rotate(rotate)

    def add_pdf_file(self, filename):
        start_page = len(self.data)
        images = convert_from_path(filename, size=(None, 600))

        pdf = PdfReader(filename)
        self.pdf_read.append(pdf)
        information = pdf.metadata
        number_of_pages = len(pdf.pages)
        for i in range(len(pdf.pages)):
            im = images[i].convert("RGB")
            data = im.tobytes("raw", "RGB")
            qi = QImage(data, im.size[0], im.size[1], im.size[0] * 3, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qi)
            self._addpage(PDFPage(f'{len(self.pdf_read)}| Page {i + 1}', pixmap, pdf.pages[i]))

        return start_page, len(self.data)

    def add_image_file(self, filename):
        img = Image.open(filename)
        img_byte_arr = io.BytesIO()

        page_size = config.get_size_page()
        canvas_image = Image.new(mode='RGB', size=page_size, color='white')
        imgpdf = self.resize_image(img, page_size[0], page_size[1]).convert("RGB")
        canvas_image.paste(imgpdf, box=((page_size[0] - imgpdf.size[0]) // 2, (page_size[1] - imgpdf.size[1]) // 2))
        canvas_image.save(img_byte_arr, format='PDF', quality=config.PAGE_DPI)
        pdf = PdfReader(img_byte_arr)
        self.pdf_read.append(pdf)

        img = self.resize_image(canvas_image, 600, 600).convert("RGB")
        data = img.tobytes("raw", "RGB")
        qi = QImage(data, img.size[0], img.size[1], img.size[0] * 3, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qi)
        self._addpage(PDFPage(f'{len(self.pdf_read)}| Image', pixmap, pdf.pages[0]))
        return len(self.data)


    def resize_image(self, image, width, height):
        aspect_ratio = min(width / float(image.size[0]), height / float(image.size[1]))
        new_width = int(aspect_ratio * image.size[0])
        new_height = int(aspect_ratio * image.size[1])
        return image.resize((new_width, new_height), resample=Image.Resampling.BILINEAR)

    def save_as(self, filename, pgs):
        output = PdfWriter()
        for i in pgs:
            output.add_page(self.data[i].pdf)

        with open(filename, 'wb') as f:
            output.write(f)
