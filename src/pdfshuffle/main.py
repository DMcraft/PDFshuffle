import os
import sys
import config
from loguru import logger

from PyQt5.QtCore import QSize

from pagelist import PageWidget, PRoleID
from pdfdata import PDFData
from window import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5 import QtGui


# pyuic5 window.ui -o window.py

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.pathfile = config.CURRENT_PATH

        # Set up the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('PDF Shuffle')

        self.pagesBasic = PageWidget(self.ui.centralwidget)
        self.ui.BasicLayout.addWidget(self.pagesBasic)
        self.pagesSecond = PageWidget(self.ui.centralwidget)
        self.ui.SecondLayout.addWidget(self.pagesSecond)

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
            self.pagesBasic.addPage(i, pid.name_page, pid.pix)

    def pressedButtonSave(self, pages: PageWidget):
        filename, _ = QFileDialog.getSaveFileName(None, "Save File", self.pathfile, "PDF Files (*.pdf)")
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
            filename, _ = QFileDialog.getOpenFileName(None, "Open File", self.pathfile, "PDF Files (*.pdf);;"
                                                                                        "Image Files (*.jpg *.jpeg *.png)")
        if filename:

            if filename.lower().endswith('.pdf'):
                self.pathfile = os.path.dirname(filename)
                start_page, end_page = pdf.add_pdf_file(filename)
                for i in range(start_page, end_page):
                    pid = pdf.data[i]
                    pages.addPage(i, pid.name_page, pid.pix)
            elif (filename.lower().endswith('.jpg') or filename.lower().endswith('.png')
                  or filename.lower().endswith('.jpeg')):
                self.pathfile = os.path.dirname(filename)
                num_page = pdf.add_image_file(filename) - 1
                pid = pdf.data[num_page]
                pages.addPage(num_page, pid.name_page, pid.pix)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.updatePages()

    def winAbout(self):
        QMessageBox.about(self, "О программе PDF shuffler",
                          "PDF shuffler - программа для пересортировки  страниц PDF файлов.\n\n"
                          "version 1.1\n"
                          "Автор: Алдунин Д.А.\n"
                          "Date production: 2023\n"
                          "Powered by open source software: pdf2image, PyPDF2, PyQt5\n")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        config.save_config()


if __name__ == '__main__':
    logger.info('Start program')
    pdf = PDFData()
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
