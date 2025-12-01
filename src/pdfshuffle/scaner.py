import random
import subprocess
import sys
import datetime

import config

from loguru import logger

from pathlib import Path

from getscan import WorkerDrive
from scanerwindow import Ui_ScanerForm
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QTimer

# pyuic5 scanerwindow.ui -o ./src/pdfshuffle/scanerwindow.py

SCANER_START_MAIN = False
SCANER_TEST_PICTURE = 0


class ScanerWindow(QWidget):
    get_devices = pyqtSignal()
    get_options = pyqtSignal(str)
    start_scan = pyqtSignal(dict)
    push_image_scan = pyqtSignal(object, int)
    close_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.image_buf = None
        self.test_image = []

        icon = QtGui.QIcon(config.ICON_PATH_SCANER.as_posix())
        # Set up the UI
        self.ui = Ui_ScanerForm()
        self.ui.setupUi(self)
        self.setWindowTitle('Scaner Shuffle')
        self.setWindowIcon(icon)

        # Таймер для очистки строки
        self.timer_message = QTimer()
        self.timer_message.setSingleShot(True)  # Таймер сработает только один раз
        self.timer_message.timeout.connect(lambda: self.ui.lineEdit_message.setText(''))

        self.ui.groupBoxSave.setEnabled(config.SCAN_AUTOSAVE if SCANER_START_MAIN else False)
        self.ui.checkBox_autosave.setChecked(config.SCAN_AUTOSAVE)

        self.ui.comboBox_dpi.addItem(f'{config.SCAN_DPI} dpi', config.SCAN_DPI)

        for key, value in config.SCAN_SPLIT.items():
            self.ui.comboBox_area.addItem(key, value)
        self.ui.comboBox_area.setCurrentIndex(self.ui.comboBox_area.findText(config.SCAN_AREA))

        shift = 0 if 'flatbed' in config.SCAN_SOURCE.lower() else 4
        split = config.SCAN_SPLIT.get(config.SCAN_AREA)
        if split is not None:
            self.ui.spinBox_left.setValue(split[0 + shift])
            self.ui.spinBox_upper.setValue(split[1 + shift])
            self.ui.spinBox_width.setValue(split[2 + shift])
            self.ui.spinBox_height.setValue(split[3 + shift])

        # Подключаем сигналы изменения значений спин боксов
        self.ui.spinBox_left.valueChanged.connect(self.changed_on_crop_area)
        self.ui.spinBox_upper.valueChanged.connect(self.changed_on_crop_area)
        self.ui.spinBox_width.valueChanged.connect(self.changed_on_crop_area)
        self.ui.spinBox_height.valueChanged.connect(self.changed_on_crop_area)

        self.ui.comboBox_typefile.addItem('JPEG', 'jpg')
        self.ui.comboBox_typefile.addItem('PDF', 'pdf')
        self.ui.comboBox_typefile.setCurrentIndex(0)

        self.ui.spinBox_quality.setValue(config.SCAN_QUALITY)

        self.ui.lineEdit_path.setText(config.SCAN_PATH)
        self.ui.lineEdit_filename.setText(config.SCAN_FILE_NAME)

        self.ui.lineEdit_filename.textEdited.connect(self.set_scan_file_name)

        self.ui.toolButton_path.clicked.connect(self.pressed_tool_button_path)
        self.ui.pushButton_scan.clicked.connect(self.pressed_button_scan)
        self.ui.pushButton_exit.clicked.connect(self.pressed_button_exit)
        self.ui.toolButton_devreload.clicked.connect(self.pressed_tool_reload_devices)
        self.ui.toolButtonOpenDir.clicked.connect(lambda: subprocess.run([
            'xdg-open', str(self.ui.lineEdit_path.text())], check=False))
        self.ui.checkBox_autosave.clicked.connect(self.pressed_check_autosave)
        self.ui.pushButton_save.clicked.connect(self.save_image)

        # Создание потока
        # create thread
        self.thread = QtCore.QThread()
        # create object which will be moved to another thread
        self.sane_thread = WorkerDrive()
        # move object to another thread
        self.sane_thread.moveToThread(self.thread)
        # after that, we can connect signals from this object to slot in GUI thread
        self.get_devices.connect(self.sane_thread.get_devices)
        self.start_scan.connect(self.sane_thread.scaner)
        self.get_options.connect(self.sane_thread.get_options)
        self.sane_thread.devices_signal.connect(self.set_devices)
        self.sane_thread.message_signal.connect(self.set_message)
        self.sane_thread.options_signal.connect(self.set_options)
        self.sane_thread.file_scan_signal.connect(self.processing_scan)
        self.thread.started.connect(self.sane_thread.run)
        self.sane_thread.finished.connect(self.thread.quit)
        self.thread.start()

        self.ui.comboBox_mode.addItem(config.SCAN_MODE, config.SCAN_MODE)
        self.ui.comboBox_dpi.addItem(f'{config.SCAN_DPI} dpi', config.SCAN_DPI)
        self.ui.comboBox_source.addItem(config.SCAN_SOURCE, config.SCAN_SOURCE)

        self.ui.comboBox_source.currentIndexChanged.connect(self.changed_source)
        self.ui.comboBox_area.currentIndexChanged.connect(self.changed_source)

        # reload device
        self.ui.comboBox_device.addItem('Не определен', 'NONE')
        self.ui.comboBox_device.currentIndexChanged.connect(self.changed_device)
        if config.SCAN_DEVICE_SIGNATURE == 'NONE':
            self.pressed_tool_reload_devices()
        else:
            self.ui.comboBox_device.addItem(config.SCAN_DEVICE_NAME, config.SCAN_DEVICE_SIGNATURE)
            self.ui.comboBox_device.setCurrentText(config.SCAN_DEVICE_NAME)

        if not self.restoreGeometry(config.OPTION_WINDOW_SCAN):
            logger.error(f'Error restore state window scan: {config.OPTION_WINDOW_SCAN}')

    @QtCore.pyqtSlot(str, object)
    def set_message(self, msg, extended_msg=''):
        logger.info(f'text {msg}, {extended_msg}')
        self._set_message(msg, 5)

    def _set_message(self, msg, timeout=0):
        self.ui.lineEdit_message.setText(msg)
        self.timer_message.stop()
        if timeout > 0:
            self.timer_message.start(timeout * 1000)

    @QtCore.pyqtSlot(str, object)
    def set_devices(self, string, devices):
        """ function description """
        logger.debug(f'text {string}, {devices}')
        self.ui.comboBox_device.clear()
        for device in devices:
            self.ui.comboBox_device.addItem(device[2], device[0])
        if self.ui.comboBox_device.count() > 0:
            self.ui.comboBox_device.setCurrentIndex(0)
            config.SCAN_DEVICE_NAME = self.ui.comboBox_device.itemText(0)
            config.SCAN_DEVICE_SIGNATURE = self.ui.comboBox_device.itemData(0)

    @QtCore.pyqtSlot(dict)
    def set_options(self, options):
        logger.info(f'option {options}')

        if isinstance(options['mode'], (list, tuple)):
            self.ui.comboBox_mode.clear()
            for opt in options['mode']:
                self.ui.comboBox_mode.addItem(opt, opt)
        else:
            self.ui.comboBox_mode.addItem(options['mode'], options['mode'])
        self.ui.comboBox_mode.setCurrentIndex(self.ui.comboBox_mode.findData(config.SCAN_MODE))

        if isinstance(options['resolution'], (list, tuple)):
            self.ui.comboBox_dpi.clear()
            for opt in options['resolution']:
                self.ui.comboBox_dpi.addItem(f'{opt} dpi', opt)
        else:
            self.ui.comboBox_dpi.addItem(options['resolution'], options['resolution'])
        self.ui.comboBox_dpi.setCurrentIndex(self.ui.comboBox_dpi.findData(config.SCAN_DPI))

        if isinstance(options['source'], (list, tuple)):
            self.ui.comboBox_source.clear()
            for opt in options['source']:
                self.ui.comboBox_source.addItem(opt, opt)
        else:
            self.ui.comboBox_source.addItem(options['source'], options['source'])
        self.ui.comboBox_source.setCurrentIndex(self.ui.comboBox_source.findData(config.SCAN_SOURCE))

        # test image (эмулятор сканера)
        if options.get('test-picture') is not None:
            if isinstance(options['test-picture'], (list, tuple)):
                logger.debug('Find: test-picture')
                for i, opt in enumerate(options['test-picture']):
                    self.test_image.append(opt)
                    logger.debug(f'{i + 1}. {opt}')

    @QtCore.pyqtSlot(str)
    def set_scan_file_name(self, text):
        """Function set file name in config."""
        config.SCAN_FILE_NAME = text

    @QtCore.pyqtSlot(object)
    def processing_scan(self, image):
        logger.debug(f'processing image {type(image)}')

        dpm = self.ui.comboBox_dpi.currentData() / 25.4
        left = int(self.ui.spinBox_left.value() * dpm)
        upper = int(self.ui.spinBox_upper.value() * dpm)
        right = int(left + self.ui.spinBox_width.value() * dpm)
        lower = int(upper + self.ui.spinBox_height.value() * dpm)
        # Validate and adjust the coordinates to be within image bounds
        left = max(0, min(left, image.width - 1))
        upper = max(0, min(upper, image.height - 1))
        right = max(left + 1, min(right, image.width))
        lower = max(upper + 1, min(lower, image.height))

        crop_image = image.crop((left, upper, right, lower))

        self.image_buf = crop_image
        if SCANER_START_MAIN:
            self.ui.groupBoxSave.setEnabled(True)
            if self.ui.checkBox_autosave.isChecked():
                self.save_image()
        else:
            self.push_image_scan.emit(crop_image, self.ui.comboBox_dpi.currentData())

    def changed_device(self, index):
        logger.debug('Device changed')
        if index >= 0:
            if self.sane_thread.is_ready():
                config.SCAN_MODE = self.ui.comboBox_mode.currentData()
                config.SCAN_DPI = self.ui.comboBox_dpi.currentData()
                config.SCAN_SOURCE = self.ui.comboBox_source.currentData()

                self.get_options.emit(self.ui.comboBox_device.itemData(index))
            else:
                self._set_message('Процесс занят выполнением задачи...', 2)

    def changed_source(self, index):
        config.SCAN_AREA = self.ui.comboBox_area.currentText()
        config.SCAN_SOURCE = self.ui.comboBox_source.currentText()

        shift = 0 if 'flatbed' in config.SCAN_SOURCE.lower() else 4
        split = config.SCAN_SPLIT.get(config.SCAN_AREA)
        if split is not None:
            self.ui.spinBox_left.blockSignals(True)
            self.ui.spinBox_upper.blockSignals(True)
            self.ui.spinBox_width.blockSignals(True)
            self.ui.spinBox_height.blockSignals(True)
            self.ui.spinBox_left.setValue(split[0 + shift])
            self.ui.spinBox_upper.setValue(split[1 + shift])
            self.ui.spinBox_width.setValue(split[2 + shift])
            self.ui.spinBox_height.setValue(split[3 + shift])
            self.ui.spinBox_left.blockSignals(False)
            self.ui.spinBox_upper.blockSignals(False)
            self.ui.spinBox_width.blockSignals(False)
            self.ui.spinBox_height.blockSignals(False)

    def changed_on_crop_area(self):
        """Вызывается при изменении любого параметра области обрезки."""
        left = self.ui.spinBox_left.value()
        upper = self.ui.spinBox_upper.value()
        width = self.ui.spinBox_width.value()
        height = self.ui.spinBox_height.value()

        logger.debug(f"Crop area updated: ({left}, {upper}, {width}, {height})")

        shift = 0 if 'flatbed' in config.SCAN_SOURCE.lower() else 4
        area = config.SCAN_SPLIT[config.SCAN_AREA]
        if area is not None:
            area[shift] = left
            area[shift + 1] = upper
            area[shift + 2] = width
            area[shift + 3] = height
            config.SCAN_SPLIT[config.SCAN_AREA] = area

    def pressed_check_autosave(self, check):
        if SCANER_START_MAIN:
            if check:
                self.ui.groupBoxSave.setEnabled(True)
            else:
                self.ui.groupBoxSave.setEnabled(False)

    def pressed_tool_button_path(self):
        dir_name = QFileDialog.getExistingDirectory(None, 'Выбор пути для сканированных файлов', config.SCAN_PATH)
        if len(dir_name) > 0:
            self.ui.lineEdit_path.setText(dir_name)
            config.SCAN_PATH = dir_name

    def pressed_tool_reload_devices(self):
        if self.sane_thread.is_ready():
            self.get_devices.emit()
        else:
            self._set_message('Процесс занят выполнением задачи...', 2)

    def pressed_button_scan(self):
        logger.debug(f'Ready thread: {self.sane_thread.is_ready()}')
        logger.debug(f'{self.ui.comboBox_device.currentData()}')

        if self.sane_thread.is_ready():
            self.start_scan.emit({
                'device': self.ui.comboBox_device.currentData(),
                'mode': self.ui.comboBox_mode.currentData(),
                'dpi': self.ui.comboBox_dpi.currentData(),
                'source': self.ui.comboBox_source.currentData(),
                'test-picture': self.test_image[SCANER_TEST_PICTURE if SCANER_TEST_PICTURE > 0 else
                random.randint(0, len(self.test_image) - 1)
                ] if len(self.test_image) > 0 else None,
            })
        else:
            self._set_message('Процесс занят выполнением задачи...', 2)

    def pressed_button_exit(self):
        logger.info('Button Exit')
        self.close()

    def save_image(self):
        if self.image_buf is None:
            self._set_message('Нет изображения', 3)
        else:
            if SCANER_START_MAIN:
                path = Path(self.ui.lineEdit_path.text())
                if path.is_dir():
                    file_name = ''.join((self.ui.lineEdit_filename.text(), '_',
                                         datetime.datetime.today().strftime("%Y%m%d-%H%M%S"),
                                         '.', self.ui.comboBox_typefile.currentData()))
                    path = Path.joinpath(path, file_name)
                    self.image_buf.save(path, quality=self.ui.spinBox_quality.value(),
                                        dpi=(self.ui.comboBox_dpi.currentData(), self.ui.comboBox_dpi.currentData()))
                else:
                    self._set_message('Неверное имя каталога', 3)
            else:
                self.push_image_scan.emit(self.image_buf, self.ui.comboBox_dpi.currentData())

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        logger.info('Close scaner!')
        config.SCAN_DEVICE_NAME = self.ui.comboBox_device.currentText()
        config.SCAN_DEVICE_SIGNATURE = self.ui.comboBox_device.currentData()
        config.SCAN_SOURCE = self.ui.comboBox_source.currentText()
        config.SCAN_MODE = self.ui.comboBox_mode.currentText()
        config.SCAN_DPI = self.ui.comboBox_dpi.currentData()
        config.SCAN_AREA = self.ui.comboBox_area.currentText()
        config.SCAN_AUTOSAVE = self.ui.checkBox_autosave.isChecked()
        config.SCAN_QUALITY = self.ui.spinBox_quality.value()
        config.OPTION_WINDOW_SCAN = self.saveGeometry()

        config.save_config()
        self.thread.quit()
        self.thread.wait()
        # готов к уничтожению экземпляра
        self.close_window.emit()


def main():
    logger.info('Start scaner!')
    app = QApplication(sys.argv)
    window = ScanerWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    print('The script is not start on terminal!')
