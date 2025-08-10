import os
import sys
from datetime import datetime
from loguru import logger

import config

from pagelist import PageWidget, PRoleID
from pdfdata import PDFData
from pdfdata import PDFPage
from scaner import ScanerWindow
from window import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
import shortcut


# pyuic5 window.ui -o ./src/pdfshuffle/window.py


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        icon = QtGui.QIcon(config.ICON_PATH_SHUFFLE.as_posix())

        self.wScan = None  # объект окна сканера
        self.status_viewer = 0
        self.pathfile = config.CURRENT_PATH
        self.current_pages_view: PageWidget = None
        self.scale_size = config.SCALE_SIZE

        # Set up the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('PDF Shuffle (сортировщик страниц)')
        self.setWindowIcon(icon)

        self.ui.comboBoxSizePaper.setCurrentIndex(
            0 if self.ui.comboBoxSizePaper.findText(config.PAGE_PAPER_SIZE) < 0 else
            self.ui.comboBoxSizePaper.findText(config.PAGE_PAPER_SIZE))
        self.ui.comboBoxOrientation.setCurrentIndex(
            0 if self.ui.comboBoxOrientation.findText(config.PAGE_PAPER_ORIENTATION) < 0 else
            self.ui.comboBoxOrientation.findText(config.PAGE_PAPER_ORIENTATION))

        self.ui.lineviewpath.setText(self.pathfile)
        self.ui.toolButtonPathFile.clicked.connect(lambda: os.system(f'xdg-open "{self.ui.lineviewpathfile.text()}"'))

        self.ui.lineviewpathfile.setText(self.pathfile)
        self.ui.toolButtonPath.clicked.connect(lambda: os.system(f'xdg-open "{self.ui.lineviewpath.text()}"'))

        self.ui.comboBoxPaperDPI.addItem('75 dpi', 75)
        self.ui.comboBoxPaperDPI.addItem('100 dpi', 100)
        self.ui.comboBoxPaperDPI.addItem('150 dpi', 150)
        self.ui.comboBoxPaperDPI.addItem('200 dpi', 200)
        self.ui.comboBoxPaperDPI.addItem('300 dpi', 300)
        self.ui.comboBoxPaperDPI.addItem('600 dpi', 600)
        self.ui.comboBoxPaperDPI.addItem('1200 dpi', 1200)
        self.ui.comboBoxPaperDPI.setCurrentIndex(
            0 if self.ui.comboBoxPaperDPI.findData(config.PAGE_PAPER_DPI) < 0 else
            self.ui.comboBoxPaperDPI.findData(config.PAGE_PAPER_DPI))

        self.ui.spinquality.setValue(config.PAGE_QUALITY)
        self.ui.spinImageSize.setValue(config.PAGE_IMAGE_SIZE)

        self.ui.checkBoxImageFormatting.setChecked(config.PAGE_PAPER_FORMATTING)
        self.ui.checkBoxImageExtend.setChecked(config.PAGE_IMAGE_EXTEND)

        self.pagesBasic = PageWidget(self.ui.centralwidget, pdf_storage)
        self.ui.BasicLayout.addWidget(self.pagesBasic)
        self.pagesSecond = PageWidget(self.ui.centralwidget, pdf_storage)
        self.ui.SecondLayout.addWidget(self.pagesSecond)

        self.ui.spinquality.valueChanged.connect(self.changedSpinQuality)
        self.ui.spinImageSize.valueChanged.connect(self.changedImageSize)

        self.ui.comboBoxOrientation.currentIndexChanged.connect(self.changePaperOrientation)
        self.ui.comboBoxSizePaper.currentIndexChanged.connect(self.changePaperSize)
        self.ui.comboBoxPaperDPI.currentIndexChanged.connect(self.changePaperDPI)

        self.ui.checkBoxImageFormatting.stateChanged.connect(self.changePaperFormatting)
        self.ui.checkBoxImageExtend.stateChanged.connect(self.changeImageExtend)

        self.ui.pushButtonScan.clicked.connect(self.winScaner)

        self.ui.toolButtonSecondView.clicked.connect(
            lambda: self.pagesSecond.setVisible(False if self.pagesSecond.isVisible() else True))
        self.ui.toolButtonExchange.clicked.connect(self.pressedButtonExchange)

        self.ui.toolButtonAdd.clicked.connect(lambda: self.pressedButtonAdd(self.pagesBasic))
        self.ui.toolButtonSecondAdd.clicked.connect(lambda: self.pressedButtonAdd(self.pagesSecond))
        self.ui.toolButtonSave.clicked.connect(lambda: self.pressedButtonSave(self.pagesBasic))
        self.ui.toolButtonSaveSecond.clicked.connect(lambda: self.pressedButtonSave(self.pagesSecond))
        self.ui.toolButtonRotate.clicked.connect(lambda: self.pressedButtonRotate(self.pagesBasic))
        self.ui.toolButtonSecondRotate.clicked.connect(lambda: self.pressedButtonRotate(self.pagesSecond))
        self.ui.toolButtonClear.clicked.connect(lambda: self.pagesBasic.clear())
        self.ui.toolButtonSecondClear.clicked.connect(lambda: self.pagesSecond.clear())

        self.ui.toolButtonRestore.clicked.connect(self.pressedButtonRestored)

        # Tool Image
        self.ui.toolImage_1.clicked.connect(self.pressed_tool_save_image)
        self.ui.toolButtonScalePlus.clicked.connect(lambda: self.pressed_scale(config.SCALE_SIZE))
        self.ui.toolButtonScaleMinus.clicked.connect(lambda: self.pressed_scale(config.SCALE_SIZE * -1))
        self.ui.toolButtonExtendWidth.clicked.connect(lambda: self.pressed_scale())
        self.ui.toolButtonExtendHeigth.clicked.connect(lambda: self.pressed_scale())

        # Menu
        self.ui.actionAddBasic.triggered.connect(lambda: self.pressedButtonAdd(self.pagesBasic))
        self.ui.actionClearBasic.triggered.connect(lambda: self.pagesBasic.clear())
        self.ui.actionAddSecond.triggered.connect(lambda: self.pressedButtonAdd(self.pagesSecond))
        self.ui.actionClearSecond.triggered.connect(lambda: self.pagesSecond.clear())
        self.ui.actionSaveTo.triggered.connect(lambda: self.pressedButtonSave(self.pagesBasic))
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.winAbout)
        self.ui.actionShortcutDesktop.triggered.connect(self.pressed_action_shortcut_desktop)
        self.ui.actionShortcutMenu.triggered.connect(self.pressed_action_shortcut_menu)
        self.ui.actionScan.triggered.connect(self.winScaner)

        self.ui.actionSavetoImage.triggered.connect(lambda: self.tool_save_to_image(self.pagesBasic))
        self.ui.actionTransformtoImage.triggered.connect(
            lambda: self.tool_transform_to_image(self.pagesBasic, self.pagesSecond))

        if not self.restoreGeometry(config.OPTION_WINDOW):
            logger.error(f'Error restore state windows: {config.OPTION_WINDOW}')
        if not self.ui.splitterView.restoreState(config.OPTION_SPLITTER):
            logger.error(f'Error restore state splitter: {config.OPTION_SPLITTER}')

        self.pagesBasic.connect_add_file(self.pressedButtonAdd)
        self.pagesSecond.connect_add_file(self.pressedButtonAdd)
        self.pagesBasic.clicked.connect(lambda: self.clickViewPage(self.pagesBasic))
        self.pagesSecond.clicked.connect(lambda: self.clickViewPage(self.pagesSecond))

        self.pagesBasic.message.connect(self.set_message)
        self.pagesSecond.message.connect(self.set_message)

    @QtCore.pyqtSlot(str)
    def set_message(self, text):
        self.ui.statusbar.showMessage(text)

    def tool_save_to_image(self, pages: PageWidget):
        filedir = QFileDialog.getExistingDirectory(None, "Save Images to directory", self.pathfile,
                                                   QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        today = datetime.today().strftime('%Y%m%d%H%M%S')
        # todo Добавить либо все страницы, либо только выделенные
        if filedir:
            for i, item in enumerate(pages, 1):
                filename = os.path.join(filedir, f'save_img-{today}_{i + 1:03}.jpg')
                page: PDFPage = pages.get_page(item)
                page.save_image_as(filename, config.PAGE_IMAGE_SIZE, quality=config.PAGE_QUALITY,
                                   dpi=config.PAGE_PAPER_DPI)
        else:
            self.ui.statusbar.showMessage('Отмена сохранения. Каталог не выбран.', 3000)

    @staticmethod
    def tool_transform_to_image(pages_in: PageWidget, pages_out: PageWidget):
        for item in pages_in:
            image = pages_in.get_page(item).get_image(config.MAX_INT, config.PAGE_IMAGE_SIZE,
                                                      keep_aspect=False)
            pages_out.add_page(pdf_storage.add_image_file('', img=image))

    def pressed_scale(self, scale=0):
        self.scale_size += scale
        if self.scale_size > config.SCALE_SIZE * 16:
            self.scale_size = config.SCALE_SIZE * 16
        if self.scale_size < config.SCALE_SIZE:
            self.scale_size = config.SCALE_SIZE
        self.clickViewPage()
        self.ui.lineEditScale.setText(f'{self.scale_size / config.SCALE_SIZE}x')

    def clickViewPage(self, pages: PageWidget = None):
        logger.info(pages)
        if pages is not None and pages is not self.current_pages_view:
            self.current_pages_view = pages
        elif self.current_pages_view is None:
            return

        id_page = self.current_pages_view.get_current_id()
        page: PDFPage = pdf_storage.get_page(id_page)
        width_cm = (page.pdf.mediabox.width / 72) * 2.54
        height_cm = (page.pdf.mediabox.height / 72) * 2.54

        width_extend = 0
        height_extend = 0
        if self.ui.toolButtonExtendWidth.isChecked():
            width_extend = self.ui.scrollArea.width() - 20
        if self.ui.toolButtonExtendHeigth.isChecked():
            height_extend = self.ui.scrollArea.height() - 20

        if width_extend or height_extend:
            pix_scaled: QPixmap = page.get_pixmap(width_extend, height_extend)
        else:
            pix_scaled: QPixmap = page.get_pixmap(height=self.scale_size)

        self.ui.labelView.setPixmap(pix_scaled)
        # self.ui.labelView.setFixedSize(pix_scaled.width(), pix_scaled.height())
        self.ui.scrollAreaWidgetContents.setMinimumSize(pix_scaled.width(), pix_scaled.height())
        self.ui.status_image_size.setText(f'pdf ({width_cm:.1f} см, {height_cm:.1f} см), '
                                          f'loud ({page.pix.width()}, {page.pix.height()}), '
                                          f'scr ({pix_scaled.width()}, {pix_scaled.height()}), '
                                          f'size {page.size // 1024} Кб'
                                          )

        self.ui.lineviewpathfile.setText(page.path)
        self.updatePages()
        self.ui.statusbar.showMessage(self.current_pages_view.get_size_selected() +
                                      '(' + self.current_pages_view.get_text_selected() + ')')

    def updatePages(self):
        self.pagesBasic.setGridSize(QSize())
        self.pagesSecond.setGridSize(QSize())

    def pressedButtonRestored(self):
        self.pagesBasic.clear()
        for i in range(len(pdf_storage.data)):
            self.pagesBasic.add_page(pdf_storage.data[i])

    def pressedButtonSave(self, pages: PageWidget):
        filename, _ = QFileDialog.getSaveFileName(None, "Save File", self.pathfile,
                                                  "PDF Files (*.pdf)")
        if filename:
            self.pathfile = os.path.dirname(filename)
            if not filename.lower().endswith('.pdf'):
                filename += '.pdf'
            pgs = []
            for i in range(pages.count()):
                item = pages.item(i)
                pgs.append(item.data(PRoleID))

            pdf_storage.save_as(filename, pgs)
        else:
            self.ui.statusbar.showMessage('Отмена сохранения. Файл не выбран.', 3000)
        self.ui.lineviewpath.setText(self.pathfile)

    def pressedButtonRotate(self, pages: PageWidget):
        if len(pages.selectedItems()) > 0:
            for _ in pages.rotate_page(90):
                pass
            self.clickViewPage(pages)
        else:
            logger.info('Not selected page on rotate')

    def pressedButtonExchange(self):
        self.pagesBasic.clicked.disconnect()
        self.pagesSecond.clicked.disconnect()
        self.ui.BasicLayout.removeWidget(self.pagesBasic)
        self.ui.SecondLayout.removeWidget(self.pagesSecond)
        self.pagesBasic, self.pagesSecond = self.pagesSecond, self.pagesBasic
        self.ui.BasicLayout.addWidget(self.pagesBasic)
        self.ui.SecondLayout.addWidget(self.pagesSecond)
        if not self.pagesBasic.isVisible():
            self.pagesBasic.setVisible(True)
            self.pagesSecond.setVisible(False)

        self.pagesBasic.clicked.connect(lambda: self.clickViewPage(self.pagesBasic))
        self.pagesSecond.clicked.connect(lambda: self.clickViewPage(self.pagesSecond))

    def pressedButtonAdd(self, pages: PageWidget, filename: str = None):
        if filename is None:
            filename, _ = QFileDialog.getOpenFileName(None, "Open File", self.pathfile,
                                                      "PDF Files (*.pdf *.PDF);;"
                                                      "Image Files (*.jpg *.jpeg *.png *.JPG *.JPEG *.PNG)")
        if filename:
            if filename.lower().endswith('.pdf'):
                self.pathfile = os.path.dirname(filename)
                start_page, end_page = pdf_storage.add_pdf_file(filename)
                for i in range(start_page, end_page):
                    pages.add_page(pdf_storage.data[i])
            elif (filename.lower().endswith('.jpg') or filename.lower().endswith('.png')
                  or filename.lower().endswith('.jpeg')):
                self.pathfile = os.path.dirname(filename)
                pages.add_page(pdf_storage.add_image_file(filename))
        self.ui.lineviewpath.setText(self.pathfile)

    def pressed_tool_save_image(self):
        if self.current_pages_view is None:
            self.ui.statusbar.showMessage('Не выбрано изображения для сохранения', 1500)
            return

        filename, _ = QFileDialog.getSaveFileName(None, "Save Image File", self.pathfile,
                                                  "JPG Files (*.jpg)")
        if filename:
            self.pathfile = os.path.dirname(filename)
            if not filename.lower().endswith('.jpg'):
                filename += '.jpg'

            pdf_storage.get_page(self.current_pages_view.get_current_id()
                ).save_image_as(
                filename, self.scale_size,
                config.PAGE_QUALITY, config.PAGE_PAPER_DPI)
        else:
            self.ui.statusbar.showMessage('Отмена сохранения. Файл не выбран.', 3000)
        self.ui.lineviewpath.setText(self.pathfile)

    def changePaperSize(self, index):
        config.PAGE_PAPER_SIZE = self.ui.comboBoxSizePaper.currentText()

    def changePaperOrientation(self, index):
        config.PAGE_PAPER_ORIENTATION = self.ui.comboBoxOrientation.currentText()

    def changePaperDPI(self, index):
        config.PAGE_PAPER_DPI = self.ui.comboBoxPaperDPI.currentData()

    def changedSpinQuality(self, value):
        config.PAGE_QUALITY = self.ui.spinquality.value()

    def changedImageSize(self, value):
        config.PAGE_IMAGE_SIZE = self.ui.spinImageSize.value()

    def changePaperFormatting(self, state):
        if state == QtCore.Qt.Checked:
            config.PAGE_PAPER_FORMATTING = True
        else:
            config.PAGE_PAPER_FORMATTING = False

    def changeImageExtend(self, state):
        if state == QtCore.Qt.Checked:
            config.PAGE_IMAGE_EXTEND = True
        else:
            config.PAGE_IMAGE_EXTEND = False

    @QtCore.pyqtSlot(object, int)
    def addScanImage(self, image, dpi):
        if self.ui.comboBoxPaperDPI.findData(dpi) >= 0:
            self.ui.comboBoxPaperDPI.setCurrentIndex(self.ui.comboBoxPaperDPI.findData(dpi))

        self.pagesSecond.add_page(pdf_storage.add_image_file('', img=image))

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.updatePages()

    def winAbout(self):
        QMessageBox.about(self, "О программе PDF shuffler",
                          "PDF shuffler - программа для пересортировки страниц PDF файлов.\n\n"
                          f"Version {config.VERSION_PROGRAM}\n"
                          f"Date production: {config.VERSION_DATE}\n\n"
                          "Design: Dmitriy Aldunin \n"
                          "Created Date: 04/10/2023\n"
                          "Powered by open source software: pdf2image, PyPDF, PyQt5, python-sane\n")

    def winScaner(self):
        if self.wScan is None:
            self.wScan = ScanerWindow()
            self.wScan.push_image_scan.connect(self.addScanImage)
            self.wScan.close_window.connect(self.close_win_scaner)
            self.wScan.show()
        else:
            self.wScan.activateWindow()  # Активируем (фокус)
            self.wScan.raise_()

    @QtCore.pyqtSlot()
    def close_win_scaner(self):
        logger.debug('Shuffle slot close scaner')
        self.wScan = None

    @staticmethod
    def pressed_action_shortcut_desktop():
        """Вызывает создателя ярлыков на рабочий стол"""
        shortcut.create_desktop_entry('PDF Shuffle', 'pdfshuffle.py', 'icons/pdfshuffle.png',
                                      'Пересортировка страниц pdf файлов, добавление изображений',
                                      categories=shortcut.CATEGORIES_OFFICE)
        shortcut.create_desktop_entry('PDF Scaner', 'pdfscaner.py', 'icons/pdfscaner.png',
                                      'Сканер изображений',
                                      categories=shortcut.CATEGORIES_OFFICE)

    @staticmethod
    def pressed_action_shortcut_menu():
        """Вызывает создателя ярлыков в меню"""
        shortcut.create_desktop_entry('PDF Shuffle', 'pdfshuffle.py', 'icons/pdfshuffle.png',
                                      'Пересортировка страниц pdf файлов, добавление изображений',
                                      desktop=False, menu=True, categories=shortcut.CATEGORIES_OFFICE)
        shortcut.create_desktop_entry('PDF Scaner', 'pdfscaner.py', 'icons/pdfscaner.png',
                                      'Сканер изображений',
                                      desktop=False, menu=True, categories=shortcut.CATEGORIES_OFFICE)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        config.OPTION_SPLITTER = self.ui.splitterView.saveState()
        config.OPTION_WINDOW = self.saveGeometry()
        config.save_config()
        if self.wScan is not None:
            self.wScan.close()


def main():
    logger.info('Start shuffle!')
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    print('The script is not start on terminal!')

else:
    pdf_storage = PDFData()
