import os
import sys
import config
from loguru import logger

from PyQt5.QtCore import QSize

from pagelist import PageWidget, PRoleID
from pdfdata import PDFData
from scaner import ScanerWindow
from window import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5 import QtGui, QtCore
import shortcut


# pyuic5 window.ui -o window.py


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.wScan = None  # объект окна сканера
        self.pathfile = config.CURRENT_PATH

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

        self.ui.toolButtonViewerVisible.clicked.connect(
            lambda: self.ui.labelView.setVisible(False if self.ui.labelView.isVisible() else True))
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

        self.pagesBasic.connectAddFile(self.pressedButtonAdd)
        self.pagesSecond.connectAddFile(self.pressedButtonAdd)
        self.pagesBasic.clicked.connect(lambda: self.clickViewPage(self.pagesBasic))
        self.pagesSecond.clicked.connect(lambda: self.clickViewPage(self.pagesSecond))

    def clickViewPage(self, pages: PageWidget):
        logger.info(pages)
        pix = pages.getPixmapSelected()
        self.ui.labelView.setPixmap(pix)
        self.updatePages()
        self.ui.statusbar.showMessage(pages.getTextSelected())

    def updatePages(self):
        self.pagesBasic.setGridSize(QSize())
        self.pagesSecond.setGridSize(QSize())

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

    def pressedButtonRotate(self, pages: PageWidget):
        for i in pages.rotatePage(90):
            pdf.rotatepage(i, 90)

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
                    pages.addPage(i, pid.name_page, pid.pix, pid.comment)
            elif (filename.lower().endswith('.jpg') or filename.lower().endswith('.png')
                  or filename.lower().endswith('.jpeg')):
                self.pathfile = os.path.dirname(filename)
                num_page = pdf.add_image_file(filename) - 1
                pid = pdf.data[num_page]
                pages.addPage(num_page, pid.name_page, pid.pix, pid.comment)

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
                          "PDF shuffler - программа для пересортировки  страниц PDF файлов.\n\n"
                          "version 2.2\n"
                          "Автор: Алдунин Д.А.\n"
                          "Date production: 2023\n"
                          "Powered by open source software: pdf2image, PyPDF2, PyQt5\n")

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
