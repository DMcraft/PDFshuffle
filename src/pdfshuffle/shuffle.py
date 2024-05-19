import os
import sys
from datetime import datetime

from PyQt5.QtGui import QPixmap

import config
from loguru import logger

from PyQt5.QtCore import QSize, Qt

from pagelist import PageWidget, PRoleID, PRoleSize
from pdfdata import PDFData
from scaner import ScanerWindow
from window import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5 import QtGui, QtCore
import shortcut


# pyuic5 window.ui -o ./src/pdfshuffle/window.py


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.wScan = None  # объект окна сканера
        self.status_viewer = 0
        self.pathfile = config.CURRENT_PATH
        self.current_pages_view: PageWidget = None
        self.scale_size = config.SCALE_SIZE

        # Set up the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('PDF Shuffle (сортировщик страниц)')

        self.ui.comboBoxSizePaper.setCurrentIndex(
            0 if self.ui.comboBoxSizePaper.findText(config.PAGE_PAPER_SIZE) < 0 else
            self.ui.comboBoxSizePaper.findText(config.PAGE_PAPER_SIZE))
        self.ui.comboBoxOrientation.setCurrentIndex(
            0 if self.ui.comboBoxOrientation.findText(config.PAGE_PAPER_ORIENTATION) < 0 else
            self.ui.comboBoxOrientation.findText(config.PAGE_PAPER_ORIENTATION))

        self.ui.lineviewpath.setText(self.pathfile)
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

        self.ui.checkBoxImageFormatting.setChecked(config.PAGE_PAPER_FORMATTING)
        self.ui.checkBoxImageExtend.setChecked(config.PAGE_IMAGE_EXTEND)

        self.pagesBasic = PageWidget(self.ui.centralwidget)
        self.ui.BasicLayout.addWidget(self.pagesBasic)
        self.pagesSecond = PageWidget(self.ui.centralwidget)
        self.ui.SecondLayout.addWidget(self.pagesSecond)

        self.ui.spinquality.valueChanged.connect(self.changedSpinQuality)

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

        self.ui.toolButtonViewerVisible.clicked.connect(lambda: self.pressedButtonViewer(0))
        self.ui.toolButtonViewerVisible_1.clicked.connect(lambda: self.pressedButtonViewer(1))
        self.ui.toolButtonViewerVisible_2.clicked.connect(lambda: self.pressedButtonViewer(2))

        self.ui.toolButtonScalePlus.clicked.connect(self.pressed_scale_plus)
        self.ui.toolButtonScaleMinus.clicked.connect(self.pressed_scale_minus)
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

        self.ui.actionViewNormal.triggered.connect(lambda: self.pressedButtonViewer(0))
        self.ui.actionViewMax.triggered.connect(lambda: self.pressedButtonViewer(2))
        self.ui.actionViewMin.triggered.connect(lambda: self.pressedButtonViewer(1))

        self.ui.actionSavetoImage.triggered.connect(lambda: self.tool_save_to_image(self.pagesBasic))
        self.ui.actionTransformtoImage.triggered.connect(
            lambda: self.tool_tranform_to_image(self.pagesBasic, self.pagesSecond))

        self.pagesBasic.connectAddFile(self.pressedButtonAdd)
        self.pagesSecond.connectAddFile(self.pressedButtonAdd)
        self.pagesBasic.clicked.connect(lambda: self.clickViewPage(self.pagesBasic))
        self.pagesSecond.clicked.connect(lambda: self.clickViewPage(self.pagesSecond))

        self.pagesBasic.message.connect(self.setMessage)
        self.pagesSecond.message.connect(self.setMessage)

    @QtCore.pyqtSlot(str)
    def setMessage(self, text):
        self.ui.statusbar.showMessage(text)

    def tool_save_to_image(self, pages: PageWidget):
        filedir = QFileDialog.getExistingDirectory(None, "Save Images to directory", self.pathfile,
                                                   QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
                                                   )
        today = datetime.today().strftime('%Y%m%d%H%M%S')
        if filedir:
            for i in range(pages.count()):
                filename = os.path.join(filedir, f'save_img-{today}_{i + 1:03}.pdf')
                pdf.save_as(filename, (pages.item(i).data(PRoleID), ))

        else:
            self.ui.statusbar.showMessage('Отмена сохранения. Каталог не выбран.', 3000)

    def tool_tranform_to_image(self, pages_in: PageWidget, pages_out: PageWidget):
        for i in range(pages_in.count()):
            item = pages_in.item(i)
            image = pdf.get_image_page(item.data(PRoleID), config.PAGE_PAPER_DPI)

            num_page = pdf.add_image_file('', img=image) - 1
            pid = pdf.data[num_page]
            pages_out.addPage(num_page, pid.name_page, pid.pix, pid.size, pid.comment)

    def pressed_scale_plus(self):
        self.scale_size *= 2
        if self.scale_size > config.SCALE_SIZE * 16:
            self.scale_size = config.SCALE_SIZE * 16
        self.ui.lineEditScale.setText(f'{self.scale_size / config.SCALE_SIZE}x')
        if self.current_pages_view is not None:
            self.clickViewPage(self.current_pages_view)

    def pressed_scale_minus(self):
        self.scale_size //= 2
        if self.scale_size < config.SCALE_SIZE // 4:
            self.scale_size = config.SCALE_SIZE // 4
        self.ui.lineEditScale.setText(f'{self.scale_size / config.SCALE_SIZE}x')
        if self.current_pages_view is not None:
            self.clickViewPage(self.current_pages_view)

    def clickViewPage(self, pages: PageWidget):
        logger.info(pages)
        self.current_pages_view = pages

        pix: QPixmap = pages.getPixmapSelected()
        if pix.height() < self.scale_size:
            pix = pdf.reload_image(pages.getIDSelected(), self.scale_size)
            pages.setPixmapSelected(pix)

        pix_scaled: QPixmap = pix.scaledToHeight(self.scale_size, Qt.SmoothTransformation)
        self.ui.labelView.setPixmap(pix_scaled)
        self.ui.labelView.setFixedSize(pix_scaled.width(), pix_scaled.height())
        self.ui.scrollAreaWidgetContents.setMinimumSize(pix_scaled.width(), pix_scaled.height())
        self.updatePages()
        self.ui.statusbar.showMessage(pages.getSizeSelected() + '(' + pages.getTextSelected() + ')')

    def updatePages(self):
        self.pagesBasic.setGridSize(QSize())
        self.pagesSecond.setGridSize(QSize())

    def pressedButtonViewer(self, status):
        if status == 2:
            self.ui.scrollArea.setMaximumWidth(1800)
            self.ui.scrollArea.setMinimumWidth(1350)
        elif status == 1:
            self.ui.scrollArea.setMaximumWidth(250)
            self.ui.scrollArea.setMinimumWidth(0)
        else:
            self.ui.scrollArea.setMaximumWidth(500)
            self.ui.scrollArea.setMinimumWidth(500)

    def pressedButtonRestored(self):
        self.pagesBasic.clear()
        for i in range(len(pdf.data)):
            pid = pdf.data[i]
            self.pagesBasic.addPage(i, pid.name_page, pid.pix, pid.comment)

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

            pdf.save_as(filename, pgs)
        else:
            self.ui.statusbar.showMessage('Отмена сохранения. Файл не выбран.', 3000)
        self.ui.lineviewpath.setText(self.pathfile)

    def pressedButtonRotate(self, pages: PageWidget):
        for i in pages.rotatePage(90):
            pdf.rotatepage(i, 90)
        self.clickViewPage(pages)

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
                                                      "PDF Files (*.pdf);;"
                                                      "Image Files (*.jpg *.jpeg *.png)")
        if filename:

            if filename.lower().endswith('.pdf'):
                self.pathfile = os.path.dirname(filename)
                start_page, end_page = pdf.add_pdf_file(filename)
                for i in range(start_page, end_page):
                    pid = pdf.data[i]
                    pages.addPage(i, pid.name_page, pid.pix, pid.size, pid.comment)
            elif (filename.lower().endswith('.jpg') or filename.lower().endswith('.png')
                  or filename.lower().endswith('.jpeg')):
                self.pathfile = os.path.dirname(filename)
                num_page = pdf.add_image_file(filename) - 1
                pid = pdf.data[num_page]
                pages.addPage(num_page, pid.name_page, pid.pix, pid.size, pid.comment)
        self.ui.lineviewpath.setText(self.pathfile)

    def changePaperSize(self, index):
        config.PAGE_PAPER_SIZE = self.ui.comboBoxSizePaper.currentText()

    def changePaperOrientation(self, index):
        config.PAGE_PAPER_ORIENTATION = self.ui.comboBoxOrientation.currentText()

    def changePaperDPI(self, index):
        config.PAGE_PAPER_DPI = self.ui.comboBoxPaperDPI.currentData()

    def changedSpinQuality(self, value):
        config.PAGE_QUALITY = self.ui.spinquality.value()

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

        num_page = pdf.add_image_file('', img=image) - 1
        pid = pdf.data[num_page]
        self.pagesSecond.addPage(num_page, pid.name_page, pid.pix, pid.comment)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.updatePages()

    def winAbout(self):
        QMessageBox.about(self, "О программе PDF shuffler",
                          "PDF shuffler - программа для пересортировки страниц PDF файлов.\n\n"
                          f"version {config.VERSION_PROGRAM}\n"
                          f"Date production: {config.VERSION_DATE}\n\n"
                          "Автор: Алдунин Д.А.\n"
                          "Created Date: 04/10/2023\n"
                          "Powered by open source software: pdf2image, PyPDF2, PyQt5, python-sane\n")

    def winScaner(self):
        if self.wScan is None:
            self.wScan = ScanerWindow()
            self.wScan.push_image_scan.connect(self.addScanImage)
            self.wScan.close_window.connect(self.close_win_scaner)
            self.wScan.show()

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
    pdf = PDFData()
