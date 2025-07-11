import os
import sys
import datetime
import config

from loguru import logger

from pathlib import Path

from getscan import WorkerDrive
from scanerwindow import Ui_ScanerForm
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QWidget
from PyQt5 import QtGui, QtCore

# pyuic5 scanerwindow.ui -o ./src/pdfshuffle/scanerwindow.py

SCANER_START_MAIN = False


class ScanerWindow(QWidget):
    get_devices = QtCore.pyqtSignal()
    get_options = QtCore.pyqtSignal(str)
    start_scan = QtCore.pyqtSignal(dict)
    push_image_scan = QtCore.pyqtSignal(object, int)
    close_window = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.image_buf = None
        icon = QtGui.QIcon(config.ICON_PATH_SCANER.as_posix())
        # Set up the UI
        self.ui = Ui_ScanerForm()
        self.ui.setupUi(self)
        self.setWindowTitle('Scaner Shuffle')
        self.setWindowIcon(icon)

        self.ui.groupBoxSave.setEnabled(config.SCAN_AUTOSAVE if SCANER_START_MAIN else False)
        self.ui.checkBox_autosave.setChecked(config.SCAN_AUTOSAVE)

        self.ui.spinBox_left.setValue(config.SCAN_SPLIT[0])
        self.ui.spinBox_upper.setValue(config.SCAN_SPLIT[1])
        self.ui.spinBox_right.setValue(config.SCAN_SPLIT[2])
        self.ui.spinBox_lower.setValue(config.SCAN_SPLIT[3])

        self.ui.comboBox_dpi.addItem(f'{config.SCAN_DPI} dpi', config.SCAN_DPI)

        self.ui.comboBox_area.addItem('Full', (0, 0, 220, 300))
        self.ui.comboBox_area.addItem('A4', (0, 0, 210, 297))
        self.ui.comboBox_area.addItem('A4-split', (2, 2, 212, 295))
        self.ui.comboBox_area.setCurrentIndex(self.ui.comboBox_area.findText(config.SCAN_AREA))

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
        self.ui.toolButtonOpenDir.clicked.connect(lambda: os.system(f'xdg-open "{self.ui.lineEdit_path.text()}"'))
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
        # self.thread.finished.connect(app.exit)
        # start thread
        self.thread.start()

        self.ui.comboBox_mode.addItem(config.SCAN_MODE, config.SCAN_MODE)
        self.ui.comboBox_dpi.addItem(f'{config.SCAN_DPI} dpi', config.SCAN_DPI)
        self.ui.comboBox_source.addItem(config.SCAN_SOURCE, config.SCAN_SOURCE)

        # reload device
        self.ui.comboBox_device.addItem('Не определен', 'NONE')
        self.ui.comboBox_device.currentIndexChanged.connect(self.device_changed)
        if config.SCAN_DEVICE_SIGNATURE == 'NONE':
            self.pressed_tool_reload_devices()
        else:
            self.ui.comboBox_device.addItem(config.SCAN_DEVICE_NAME, config.SCAN_DEVICE_SIGNATURE)
            self.ui.comboBox_device.setCurrentText(config.SCAN_DEVICE_NAME)

        if not self.restoreGeometry(config.OPTION_WINDOW_SCAN):
            logger.error(f'Error restore state window scan: {config.OPTION_WINDOW_SCAN}')

    @QtCore.pyqtSlot(str, object)
    def set_devices(self, string, devices):
        """ function description """
        logger.info(f'text {string}, {devices}')
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

        if isinstance(options['mode'], list):
            self.ui.comboBox_mode.clear()
            for opt in options['mode']:
                self.ui.comboBox_mode.addItem(opt, opt)
        else:
            self.ui.comboBox_mode.addItem(options['mode'], options['mode'])
        self.ui.comboBox_mode.setCurrentIndex(self.ui.comboBox_mode.findData(config.SCAN_MODE))

        if isinstance(options['resolution'], list):
            self.ui.comboBox_dpi.clear()
            for opt in options['resolution']:
                self.ui.comboBox_dpi.addItem(f'{opt} dpi', opt)
        else:
            self.ui.comboBox_dpi.addItem(options['resolution'], options['resolution'])
        self.ui.comboBox_dpi.setCurrentIndex(self.ui.comboBox_dpi.findData(config.SCAN_DPI))

        if isinstance(options['source'], list):
            self.ui.comboBox_source.clear()
            for opt in options['source']:
                self.ui.comboBox_source.addItem(opt, opt)
        else:
            self.ui.comboBox_source.addItem(options['source'], options['source'])
        self.ui.comboBox_source.setCurrentIndex(self.ui.comboBox_source.findData(config.SCAN_SOURCE))

    @QtCore.pyqtSlot(str)
    def set_scan_file_name(self, text):
        """Function set file name in config."""
        config.SCAN_FILE_NAME = text

    def pressed_check_autosave(self, check):
        if SCANER_START_MAIN:
            if check:
                self.ui.groupBoxSave.setEnabled(True)
            else:
                self.ui.groupBoxSave.setEnabled(False)

    def save_image(self):
        if self.image_buf is None:
            self.set_message('Нет изображения')
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
                    self.set_message('Неверное имя каталога')
            else:
                self.push_image_scan.emit(self.image_buf, self.ui.comboBox_dpi.currentData())

    @QtCore.pyqtSlot(object)
    def processing_scan(self, image):
        logger.info(f'processing image {type(image)}')

        area = self.ui.comboBox_area.currentData()

        dpm = self.ui.comboBox_dpi.currentData() / 25.4
        left = int(area[0] * dpm + self.ui.spinBox_left.value() * dpm)
        upper = int(area[1] * dpm + self.ui.spinBox_upper.value() * dpm)
        right = int(min(image.width, area[2] * dpm) - self.ui.spinBox_right.value() * dpm)
        lower = int(min(image.height, area[3] * dpm) - self.ui.spinBox_lower.value() * dpm)
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

    def device_changed(self, index):
        logger.info('Device changed')
        if index >= 0:
            if self.sane_thread.is_ready():
                config.SCAN_MODE = self.ui.comboBox_mode.currentData()
                config.SCAN_DPI = self.ui.comboBox_dpi.currentData()
                config.SCAN_SOURCE = self.ui.comboBox_source.currentData()

                self.get_options.emit(self.ui.comboBox_device.itemData(index))
            else:
                self.set_message('Процесс занят выполнением задачи...')

    @QtCore.pyqtSlot(str, object)
    def set_message(self, string, msg=''):
        logger.info(f'text {string}, {msg}')
        self.ui.lineEdit_message.setText(string)

    def pressed_tool_button_path(self):
        dirname = QFileDialog.getExistingDirectory(None, 'Выбор пути для сканированных файлов', config.SCAN_PATH)
        if len(dirname) > 0:
            self.ui.lineEdit_path.setText(dirname)
            config.SCAN_PATH = dirname

    def pressed_tool_reload_devices(self):
        if self.sane_thread.is_ready():
            self.get_devices.emit()
        else:
            self.set_message('Процесс занят выполнением задачи...')

    def pressed_button_scan(self):
        logger.info('Button Scan')
        logger.debug(f'Ready thread: {self.sane_thread.is_ready()}')
        logger.info(f'{self.ui.comboBox_device.currentData()}')

        if self.sane_thread.is_ready():
            self.start_scan.emit({
                'device': self.ui.comboBox_device.currentData(),
                'mode': self.ui.comboBox_mode.currentData(),
                'dpi': self.ui.comboBox_dpi.currentData(),
                'source': self.ui.comboBox_source.currentData(),
            })
        else:
            self.set_message('Процесс занят выполнением задачи...')

    def pressed_button_exit(self):
        logger.info('Button Exit')
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        logger.info('Close scaner!')
        config.SCAN_DEVICE_NAME = self.ui.comboBox_device.currentText()
        config.SCAN_DEVICE_SIGNATURE = self.ui.comboBox_device.currentData()
        config.SCAN_SOURCE = self.ui.comboBox_source.currentText()
        config.SCAN_MODE = self.ui.comboBox_mode.currentText()
        config.SCAN_DPI = self.ui.comboBox_dpi.currentData()
        config.SCAN_AREA = self.ui.comboBox_area.currentText()
        config.SCAN_SPLIT = (self.ui.spinBox_left.value(), self.ui.spinBox_upper.value(),
                             self.ui.spinBox_right.value(), self.ui.spinBox_lower.value())
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
