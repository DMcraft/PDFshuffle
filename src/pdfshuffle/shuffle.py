import os
import sys
from datetime import datetime
from pathlib import Path
from loguru import logger

import config

from pagelist import PageWidget, PRoleID
from pdfdata import PDFData
from pdfdata import PDFPage
from toolextract import detect_file_format
from scaner import ScanerWindow
from window import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QProgressDialog
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
import shortcut


# pyuic5 window.ui -o ./src/pdfshuffle/window.py


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        icon = QtGui.QIcon(config.ICON_PATH_SHUFFLE.as_posix())

        self.wScan = None  # объект окна сканера
        self.pathfile = config.CURRENT_PATH
        self.page_view = None
        self.scale_size = config.SCALE_SIZE * 3

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

        self.ui.lineEditScale.setText(f'{self.scale_size / config.SCALE_SIZE}x')

        self.ui.lineviewpath.setText(self.pathfile)
        self.ui.toolButtonPathFile.clicked.connect(lambda: os.system(f'xdg-open "{self.ui.lineviewpathfile.text()}"'))

        self.ui.lineviewpathfile.setText(self.pathfile)
        self.ui.toolButtonPath.clicked.connect(lambda: os.system(f'xdg-open "{self.ui.lineviewpath.text()}"'))

        self.ui.toolButtonCopyPath.clicked.connect(
            lambda: self.ui.lineviewpath.setText(self.ui.lineviewpathfile.text()))

        for dpi in config.DEFAULT_DPI_VALUES:
            self.ui.comboBoxPaperDPI.addItem(f'{dpi} dpi', dpi)
        self.ui.comboBoxPaperDPI.setCurrentIndex(
            0 if self.ui.comboBoxPaperDPI.findData(config.PAGE_PAPER_DPI) < 0 else
            self.ui.comboBoxPaperDPI.findData(config.PAGE_PAPER_DPI))

        self.ui.spinquality.setValue(config.PAGE_QUALITY)
        self.ui.spinImageSize.setValue(config.PAGE_IMAGE_SIZE)

        self.ui.checkBoxImageFormatting.setChecked(config.PAGE_PAPER_FORMATTING)
        self.ui.checkBoxImageExtend.setChecked(config.PAGE_IMAGE_EXTEND)
        self.ui.checkBoxAutoSize.setChecked(config.PAGE_AUTO_SIZE)
        self.ui.checkBoxAutoRotate.setChecked(config.PAGE_AUTO_ROTATE)

        self.ui.toolButtonExtendWidth.setChecked(config.PAGE_SCALE_WIDTH_EXTEND)
        self.ui.toolButtonExtendHeigth.setChecked(config.PAGE_SCALE_HEIGHT_EXTEND)

        self.pagesBasic = PageWidget(self.ui.centralwidget)
        self.ui.BasicLayout.addWidget(self.pagesBasic)
        self.pagesSecond = PageWidget(self.ui.centralwidget)
        self.ui.SecondLayout.addWidget(self.pagesSecond)

        self.ui.spinquality.valueChanged.connect(self.changed_spin_quality)
        self.ui.spinImageSize.valueChanged.connect(self.changed_image_size)

        self.ui.comboBoxOrientation.currentIndexChanged.connect(self.change_paper_orientation)
        self.ui.comboBoxSizePaper.currentIndexChanged.connect(self.change_paper_size)
        self.ui.comboBoxPaperDPI.currentIndexChanged.connect(self.change_paper_dpi)

        self.ui.checkBoxImageFormatting.stateChanged.connect(self.change_paper_formatting)
        self.ui.checkBoxImageExtend.stateChanged.connect(self.change_image_extend)
        self.ui.checkBoxAutoSize.stateChanged.connect(self.change_auto_size)
        self.ui.checkBoxAutoRotate.stateChanged.connect(self.change_auto_rotate)

        self.ui.pushButtonScan.clicked.connect(self.call_window_scaner)

        self.ui.toolButtonSecondView.clicked.connect(
            lambda: self.pagesSecond.setVisible(False if self.pagesSecond.isVisible() else True))
        self.ui.toolButtonExchange.clicked.connect(self.pressed_button_exchange)

        self.ui.toolButtonAdd.clicked.connect(lambda: self.pressed_button_add(self.pagesBasic))
        self.ui.toolButtonSecondAdd.clicked.connect(lambda: self.pressed_button_add(self.pagesSecond))
        self.ui.toolButtonSave.clicked.connect(lambda: self.pressed_button_save(self.pagesBasic))
        self.ui.toolButtonSaveSecond.clicked.connect(lambda: self.pressed_button_save(self.pagesSecond))
        self.ui.toolButtonRotate.clicked.connect(lambda: self.pressed_button_rotate(self.pagesBasic))
        self.ui.toolButtonRotateDefault.clicked.connect(
            lambda: self.pressed_button_rotate(self.pagesBasic, 0, reset=True))
        self.ui.toolButtonRotateContr.clicked.connect(lambda: self.pressed_button_rotate(self.pagesBasic, -90))
        self.ui.toolButtonSecondRotate.clicked.connect(lambda: self.pressed_button_rotate(self.pagesSecond))
        self.ui.toolButtonSecondRotateDefault.clicked.connect(
            lambda: self.pressed_button_rotate(self.pagesSecond, 0, reset=True))
        self.ui.toolButtonSecondRotateContr.clicked.connect(lambda: self.pressed_button_rotate(self.pagesSecond, -90))
        self.ui.toolButtonClear.clicked.connect(lambda: self.pagesBasic.clear())
        self.ui.toolButtonSecondClear.clicked.connect(lambda: self.pagesSecond.clear())

        self.ui.toolButtonRestore.clicked.connect(self.pressed_button_restored)

        # Tool Image
        self.ui.toolImage_1.clicked.connect(self.tool_save_image_view)
        self.ui.toolButtonScalePlus.clicked.connect(lambda: self.pressed_scale(config.SCALE_SIZE))
        self.ui.toolButtonScaleMinus.clicked.connect(lambda: self.pressed_scale(config.SCALE_SIZE * -1))
        self.ui.toolButtonExtendWidth.toggled.connect(
            lambda checked: (setattr(config, 'PAGE_SCALE_WIDTH_EXTEND', checked), self.click_view_pages()))
        self.ui.toolButtonExtendHeigth.toggled.connect(
            lambda checked: (setattr(config, 'PAGE_SCALE_HEIGHT_EXTEND', checked), self.click_view_pages()))

        # Menu
        self.ui.actionNew.triggered.connect(lambda: self.pressed_action_new())
        self.ui.actionAddBasic.triggered.connect(lambda: self.pressed_button_add(self.pagesBasic))
        self.ui.actionClearBasic.triggered.connect(lambda: self.pagesBasic.clear())
        self.ui.actionAddSecond.triggered.connect(lambda: self.pressed_button_add(self.pagesSecond))
        self.ui.actionClearSecond.triggered.connect(lambda: self.pagesSecond.clear())
        self.ui.actionClearAll.triggered.connect(lambda: (self.pagesBasic.clear(), self.pagesSecond.clear()))
        self.ui.actionSaveTo.triggered.connect(lambda: self.pressed_button_save(self.pagesBasic))
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.call_window_about)
        self.ui.actionShortcutDesktop.triggered.connect(self.pressed_action_shortcut_desktop)
        self.ui.actionShortcutMenu.triggered.connect(self.pressed_action_shortcut_menu)
        self.ui.actionScan.triggered.connect(self.call_window_scaner)
        self.ui.actionViewCompact.triggered.connect(lambda: self.adjustSize())
        self.ui.actionViewFullScreen.triggered.connect(lambda: self.showFullScreen())
        self.ui.actionViewNormalScreen.triggered.connect(lambda: self.showNormal())

        self.ui.actionSavetoImage.triggered.connect(lambda: self.tool_save_to_images(self.pagesBasic))
        self.ui.actionSaveSelectedtoImage.triggered.connect(
            lambda: self.tool_save_to_images(self.pagesBasic, selected=True))
        self.ui.actionTransformtoImage.triggered.connect(
            lambda: self.tool_transform_to_image(self.pagesBasic, self.pagesSecond))
        self.ui.actionTransformSelectedtoImage.triggered.connect(
            lambda: self.tool_transform_to_image(self.pagesBasic, self.pagesSecond, selected=True))
        self.ui.actionCurePages.triggered.connect(lambda: self.tool_cure_pages(self.pagesBasic, selected=True))
        self.ui.actionExtract.triggered.connect(lambda: self.tool_extract_images(self.pagesBasic, selected=True))

        if not self.restoreGeometry(config.OPTION_WINDOW):
            logger.error(f'Error restore state windows: {config.OPTION_WINDOW}')
        if not self.ui.splitterView.restoreState(config.OPTION_SPLITTER):
            logger.error(f'Error restore state splitter: {config.OPTION_SPLITTER}')

        self.pagesBasic.connect_add_file(self.pressed_button_add)
        self.pagesSecond.connect_add_file(self.pressed_button_add)
        self.pagesBasic.clicked.connect(lambda: self.click_view_pages(self.pagesBasic))
        self.pagesSecond.clicked.connect(lambda: self.click_view_pages(self.pagesSecond))

        self.pagesBasic.message.connect(self.set_message)
        self.pagesSecond.message.connect(self.set_message)

    def tool_save_to_images(self, pages: PageWidget, selected=False):
        output_folder = QFileDialog.getExistingDirectory(None, "Save Images to directory", self.pathfile,
                                                         QFileDialog.Option(QFileDialog.ShowDirsOnly |
                                                                            QFileDialog.DontResolveSymlinks))
        today = datetime.today().strftime('%Y%m%d%H%M')
        if output_folder:
            # Определяем источник элементов (все или выделенные)
            items_source = pages.selected_items() if selected else pages

            for i, item in enumerate(items_source, 1):
                filename = os.path.join(output_folder, f'save_{today}_page_{i:03}.jpg')
                page: PDFPage = pages.get_page(item)
                page.save_image_as(
                    filename,
                    config.PAGE_IMAGE_SIZE,
                    quality=config.PAGE_QUALITY,
                    dpi=config.PAGE_PAPER_DPI
                )
        else:
            self._set_message('Отмена сохранения. Каталог не выбран.', 3)

    def tool_save_image_view(self):
        if self.page_view is None:
            self._set_message('Не выбрано изображения для сохранения', 2)
            return

        filename, _ = QFileDialog.getSaveFileName(None, "Save Image File", self.pathfile,
                                                  "JPG Files (*.jpg *.JPEG)")
        if filename:
            self.pathfile = os.path.dirname(filename)
            if not filename.lower().endswith('.jpg'):
                filename += '.jpg'

            self.page_view.save_image_as(
                filename,
                self.scale_size,
                quality=config.PAGE_QUALITY,
                dpi=config.PAGE_PAPER_DPI
            )
        else:
            self._set_message('Отмена сохранения. Файл не выбран.')
        self.ui.lineviewpath.setText(self.pathfile)

    @staticmethod
    def tool_transform_to_image(pages_in: PageWidget, pages_out: PageWidget, selected=False):
        # Определяем источник элементов (все или выделенные)
        items_source = pages_in.selected_items() if selected else pages_in
        if hasattr(items_source, '__len__'):
            total_items = len(items_source)
        else:
            total_items = sum(1 for _ in items_source)
            items_source = pages_in.selected_items() if selected else pages_in

        logger.info(f'Items for : {total_items}')

        # Создаем диалог прогресса
        progress = QProgressDialog("Преобразование...", "Отмена", 0, total_items)
        # progress.setWindowModality(Qt.WindowModal)
        progress.setWindowModality(Qt.ApplicationModal)
        progress.setMinimumDuration(0)  # Показываем сразу
        progress.setWindowTitle("Преобразование")
        progress.setFixedSize(500, 150)
        QApplication.processEvents()

        for index, item in enumerate(items_source):
            # Проверяем, не нажал ли пользователь Cancel
            if progress.wasCanceled():
                break
            image = pages_in.get_page(item).get_image(config.PAGE_IMAGE_SIZE, config.PAGE_IMAGE_SIZE,
                                                      keep_size_page=config.PAGE_AUTO_SIZE, keep_aspect_ratio=True)
            pages_out.add_page(pdf_storage.add_image_file('', img=image))

            progress.setValue(index)
            progress.setLabelText(f"Обработка элемента {index + 1} из {total_items}")
            QApplication.processEvents()

        progress.setValue(total_items)

    def tool_extract_images(self, pages: PageWidget, selected=False):
        output_folder = QFileDialog.getExistingDirectory(None, "Save Images to directory",
                                                         self.pathfile,
                                                         QFileDialog.Option(QFileDialog.ShowDirsOnly |
                                                                            QFileDialog.DontResolveSymlinks))
        today = datetime.today().strftime('%Y%m%d%H%M')
        if not output_folder:
            self._set_message('Отмена извлечения. Каталог не выбран.', 5)
            return

        items_source = pages.selected_items() if selected else pages
        for num, item in enumerate(items_source):
            page = pages.get_page(item).pdf
            image_count = 1
            try:
                if "/Resources" in page:
                    resources = page["/Resources"]

                    if "/XObject" in resources:
                        x_object = resources["/XObject"]

                        for obj_name, obj in x_object.items():
                            if obj.get("/Subtype") == "/Image":
                                filter_type = obj.get("/Filter", "")

                                # определение типа вложения
                                extensions = {
                                    "/FlateDecode": "FLT",
                                    "/DCTDecode": "DCT",
                                    "/JPXDecode": "JPX",
                                    "/CCITTFaxDecode": "CCT"
                                }
                                if isinstance(filter_type, list):
                                    type_f = ""
                                    for t in filter_type:
                                        type_f += extensions.get(t, "OBJ")
                                else:
                                    type_f = extensions.get(filter_type, "OBJ")

                                # Сохраняем изображение
                                image_data = obj.get_data()
                                extension = detect_file_format(image_data)
                                filename = f'extract_{today}_page_{num:03}_{image_count:02}-{type_f}{extension}'
                                filepath = os.path.join(output_folder, filename)

                                with open(filepath, "wb") as f:
                                    f.write(image_data)

                                logger.debug(f"Извлечен объект: {filename}")
                                image_count += 1
            except Exception as e:
                self._set_message(f'Ошибка при извлечении объекта, на странице {num}')
                self._set_message(f'Ошибка при извлечении объекта, на странице {num}')
                logger.debug(f'Ошибка при извлечении объекта на странице {num}: {e}')
                continue

    def click_view_pages(self, pages: PageWidget = None):
        if pages is None:
            return

        self.page_view = pdf_storage.get_page(pages.get_current_id())
        self.update_view_image_size()

        self.ui.lineviewpathfile.setText(self.page_view.path)
        self.update_pages_size()
        self._set_message(f'{pages.get_size_selected()} ({pages.get_text_selected()})', 0)

    def update_pages_size(self):
        self.pagesBasic.setGridSize(QSize())
        self.pagesSecond.setGridSize(QSize())

    def update_view_image_size(self):
        if self.page_view is None:
            self.ui.labelView.clear()
            return

        page = self.page_view
        width_cm = (page.pdf.mediabox.width / 72) * 2.54
        height_cm = (page.pdf.mediabox.height / 72) * 2.54
        effective_size_max = max(page.pdf.mediabox.width, page.pdf.mediabox.height) * config.PAGE_PAPER_DPI / 72

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
        self.ui.scrollAreaWidgetContents.setMinimumSize(pix_scaled.width(), pix_scaled.height())

        self.ui.status_image_size.setText(f'pdf ({width_cm:.1f} см, {height_cm:.1f} см), '
                                          f'loud ({page.pix.width()}, {page.pix.height()}), '
                                          f'scr ({pix_scaled.width()}, {pix_scaled.height()}), '
                                          f'effect ({effective_size_max:.0f}px), '
                                          f'size {page.size // 1024} Кб'
                                          )

    def pressed_scale(self, scale=0):
        self.scale_size += scale
        if self.scale_size > config.SCALE_SIZE * 16:
            self.scale_size = config.SCALE_SIZE * 16
        if self.scale_size < config.SCALE_SIZE:
            self.scale_size = config.SCALE_SIZE
        self.click_view_pages()
        self.ui.lineEditScale.setText(f'{self.scale_size / config.SCALE_SIZE}x')

    def pressed_button_restored(self):
        self.pagesBasic.clear()
        for i in range(len(pdf_storage.data)):
            self.pagesBasic.add_page(pdf_storage.data[i])

    def pressed_action_new(self):
        self.pagesBasic.clear()
        self.pagesSecond.clear()
        self.ui.labelView.clear()
        pdf_storage.clear()

    def pressed_button_save(self, pages: PageWidget):
        filename, _ = QFileDialog.getSaveFileName(None, "Save File", self.pathfile,
                                                  "PDF Files (*.pdf *.PDF)")
        if filename:
            self.pathfile = os.path.dirname(filename)
            if not filename.lower().endswith('.pdf'):
                filename += '.pdf'
            pgs = []
            for i in range(pages.count()):
                item = pages.item(i)
                pgs.append(item.data(PRoleID))
            path = Path(filename)
            pdf_storage.save_as(path, pgs)
        else:
            self._set_message('Отмена сохранения. Файл не выбран.')
        self.ui.lineviewpath.setText(self.pathfile)

    def pressed_button_rotate(self, pages: PageWidget, angle=90, reset=False):
        if len(pages.selectedItems()) > 0:
            for _ in pages.rotate_page(angle, reset):
                pass
            self.click_view_pages(pages)
        else:
            logger.info('Not selected page on rotate')

    def pressed_button_exchange(self):
        # Функция обмена страниц
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

        self.pagesBasic.clicked.connect(lambda: self.click_view_pages(self.pagesBasic))
        self.pagesSecond.clicked.connect(lambda: self.click_view_pages(self.pagesSecond))

    def pressed_button_add(self, pages: PageWidget, filename: str = None):
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

    def change_paper_size(self, index):
        config.PAGE_PAPER_SIZE = self.ui.comboBoxSizePaper.currentText()
        self.auto_size_paper_image()

    def change_paper_orientation(self, index):
        config.PAGE_PAPER_ORIENTATION = self.ui.comboBoxOrientation.currentText()
        self.auto_size_paper_image()

    def change_paper_dpi(self, index):
        config.PAGE_PAPER_DPI = self.ui.comboBoxPaperDPI.currentData()
        self.auto_size_paper_image()

    def changed_spin_quality(self, value):
        config.PAGE_QUALITY = self.ui.spinquality.value()

    def changed_image_size(self, value):
        config.PAGE_IMAGE_SIZE = self.ui.spinImageSize.value()

    def change_paper_formatting(self, state):
        if state == QtCore.Qt.Checked:
            config.PAGE_PAPER_FORMATTING = True
        else:
            config.PAGE_PAPER_FORMATTING = False

    def change_image_extend(self, state):
        if state == QtCore.Qt.Checked:
            config.PAGE_IMAGE_EXTEND = True
        else:
            config.PAGE_IMAGE_EXTEND = False

    def change_auto_size(self, state):
        if state == QtCore.Qt.Checked:
            config.PAGE_AUTO_SIZE = True
        else:
            config.PAGE_AUTO_SIZE = False
        self.auto_size_paper_image()

    def change_auto_rotate(self, state):
        if state == QtCore.Qt.Checked:
            config.PAGE_AUTO_ROTATE = True
        else:
            config.PAGE_AUTO_ROTATE = False

    def auto_size_paper_image(self):
        if config.PAGE_AUTO_SIZE:
            size = max(config.get_size_page())
            if size > 0:
                self.ui.spinImageSize.setValue(size)

    def call_window_about(self):
        QMessageBox.about(self, "О программе PDF shuffler",
                          "PDF shuffler - программа для пересортировки страниц PDF файлов.\n\n"
                          f"Version {config.VERSION_PROGRAM}\n"
                          f"Date production: {config.VERSION_DATE}\n\n"
                          "Design: Dmitriy Aldunin \n"
                          "Created Date: 04/10/2023\n"
                          "Powered by open source software: pdf2image, PyPDF, PyQt5, python-sane\n")

    def call_window_scaner(self):
        # вызов окна сканера
        if self.wScan is None:
            self.wScan = ScanerWindow()
            self.wScan.push_image_scan.connect(self.add_scan_image)
            self.wScan.close_window.connect(self.close_win_scaner)
            self.wScan.show()
        else:
            self.wScan.activateWindow()  # Активируем (фокус)
            self.wScan.raise_()

    @QtCore.pyqtSlot(str, int)
    def set_message(self, text, timeout):
        # Выводим сообщения в статус бар
        self._set_message(text, timeout)

    def _set_message(self, text, timeout=3):
        """Внутренняя реализация отображения сообщения."""
        if hasattr(self, 'ui') and self.ui is not None:
            self.ui.statusbar.showMessage(text, int(timeout * 1000))
        else:
            print(f"Status: {text}")
            logger.info(f"Status message (UI is not initialized): {text}")

    @QtCore.pyqtSlot(object, int)
    def add_scan_image(self, image, dpi):
        if self.ui.comboBoxPaperDPI.findData(dpi) >= 0:
            self.ui.comboBoxPaperDPI.setCurrentIndex(self.ui.comboBoxPaperDPI.findData(dpi))

        self.pagesSecond.add_page(pdf_storage.add_image_file('', img=image))

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

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        # logger.debug(f'Resize event {event.size().width()}x{event.size().height()}')
        self.update_view_image_size()
        self.update_pages_size()

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
