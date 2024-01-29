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


# pyuic5 scaner.ui -o scanerwindow.py


class ScanerWindow(QWidget):
    get_devices = QtCore.pyqtSignal()
    get_options = QtCore.pyqtSignal(str)
    start_scan = QtCore.pyqtSignal(dict)
    push_image_scan = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        # Set up the UI
        self.ui = Ui_ScanerForm()
        self.ui.setupUi(self)
        self.setWindowTitle('Scaner Shuffle')

        self.ui.spinBox_left.setValue(config.SCAN_SPLIT[0])
        self.ui.spinBox_upper.setValue(config.SCAN_SPLIT[1])
        self.ui.spinBox_right.setValue(config.SCAN_SPLIT[2])
        self.ui.spinBox_lower.setValue(config.SCAN_SPLIT[3])

        self.ui.comboBox_dpi.addItem(f'{config.SCAN_DPI} dpi', config.SCAN_DPI)

        self.ui.comboBox_area.addItem('Full', (0, 0, 220, 300))
        self.ui.comboBox_area.addItem('A4', (0, 0, 210, 297))
        self.ui.comboBox_area.addItem('A4-split', (2, 2, 212, 295))
        self.ui.comboBox_area.setCurrentIndex(self.ui.comboBox_area.findText(config.SCAN_AREA))

        self.ui.comboBox_typefile.addItem('PDF', 'pdf')
        self.ui.comboBox_typefile.addItem('JPEG', 'jpg')
        self.ui.comboBox_typefile.addItem('TIFF', 'tiff')
        self.ui.comboBox_typefile.setCurrentIndex(0)

        self.ui.lineEdit_path.setText(config.SCAN_PATH)
        self.ui.lineEdit_filename.setText(config.SCAN_FILE_NAME)

        # self.ui.lineEdit_path.textEdited.connect(self.set_scan_path)
        self.ui.lineEdit_filename.textEdited.connect(self.set_scan_file_name)

        self.ui.toolButton_path.clicked.connect(self.pressedtoolButtonPath)
        self.ui.pushButton_scan.clicked.connect(self.pressedButtonScan)
        self.ui.pushButton_exit.clicked.connect(self.pressedButtonExit)
        self.ui.toolButton_devreload.clicked.connect(self.pressedtoolReloadDevices)


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
        self.sane_thread.devices_signal.connect(self.setDevices)
        self.sane_thread.message_signal.connect(self.setMessage)
        self.sane_thread.options_signal.connect(self.setOptions)
        self.sane_thread.file_scan_signal.connect(self.processingScan)
        self.thread.started.connect(self.sane_thread.run)
        self.sane_thread.finished.connect(self.thread.quit)
        # self.thread.finished.connect(app.exit)
        # start thread
        self.thread.start()

        self.ui.comboBox_mode.addItem(config.SCAN_MODE, config.SCAN_MODE)
        self.ui.comboBox_dpi.addItem(f'{config.SCAN_DPI} dpi', config.SCAN_DPI)
        self.ui.comboBox_source.addItem(config.SCAN_SOURCE, config.SCAN_SOURCE)

        # reload device
        self.ui.comboBox_device.addItem('нетути', 'NONE')
        self.ui.comboBox_device.currentIndexChanged.connect(self.deviceChanged)
        if config.SCAN_DEVICE_SIGNATURE == 'NONE':
            self.pressedtoolReloadDevices()
        else:
            self.ui.comboBox_device.addItem(config.SCAN_DEVICE_NAME, config.SCAN_DEVICE_SIGNATURE)
            self.ui.comboBox_device.setCurrentText(config.SCAN_DEVICE_NAME)


    @QtCore.pyqtSlot(str, object)
    def setDevices(self, string, devices):
        logger.info(f'text {string}, {devices}')
        self.ui.comboBox_device.clear()
        for device in devices:
            self.ui.comboBox_device.addItem(device[2], device[0])
        if self.ui.comboBox_device.count() > 0:
            self.ui.comboBox_device.setCurrentIndex(0)
            config.SCAN_DEVICE_NAME = self.ui.comboBox_device.itemText(0)
            config.SCAN_DEVICE_SIGNATURE = self.ui.comboBox_device.itemData(0)

    @QtCore.pyqtSlot(dict)
    def setOptions(self, options):
        logger.info(f'option {options}')

        if type(options['mode']) is list:
            self.ui.comboBox_mode.clear()
            for opt in options['mode']:
                self.ui.comboBox_mode.addItem(opt, opt)
        else:
            self.ui.comboBox_mode.addItem(options['mode'], options['mode'])
        self.ui.comboBox_mode.setCurrentIndex(self.ui.comboBox_mode.findData(config.SCAN_MODE))

        if type(options['resolution']) is list:
            self.ui.comboBox_dpi.clear()
            for opt in options['resolution']:
                self.ui.comboBox_dpi.addItem(f'{opt} dpi', opt)
        else:
            self.ui.comboBox_dpi.addItem(options['resolution'], options['resolution'])
        self.ui.comboBox_dpi.setCurrentIndex(self.ui.comboBox_dpi.findData(config.SCAN_DPI))

        if type(options['source']) is list:
            self.ui.comboBox_source.clear()
            for opt in options['source']:
                self.ui.comboBox_source.addItem(opt, opt)
        else:
            self.ui.comboBox_source.addItem(options['source'], options['source'])
        self.ui.comboBox_source.setCurrentIndex(self.ui.comboBox_source.findData(config.SCAN_SOURCE))

    # @QtCore.pyqtSlot(str)
    # def set_scan_path(self, text):
    #     config.SCAN_PATH = text

    @QtCore.pyqtSlot(str)
    def set_scan_file_name(self, text):
        config.SCAN_FILE_NAME = text

    @QtCore.pyqtSlot(object)
    def processingScan(self, image):
        logger.info(f'processing image {type(image)}')

        if __name__ == '__main__':
            path = Path(self.ui.lineEdit_path.text())
            if path.is_dir():
                file_name = self.ui.lineEdit_filename.text() + datetime.datetime.today().strftime("%Y%m%d-%H%M%S") + '.jpg'
                path = Path.joinpath(path,  file_name)
                image.save(path, quality=90, dpi=(self.ui.comboBox_dpi.currentData(), self.ui.comboBox_dpi.currentData()))
            else:
                self.setMessage('Неверное имя каталога')
        else:
            self.push_image_scan.emit(image)

    def deviceChanged(self, index):
        logger.info('Device changed')
        if index >= 0:
            if self.sane_thread.isReady():
                config.SCAN_MODE = self.ui.comboBox_mode.currentData()
                config.SCAN_DPI = self.ui.comboBox_dpi.currentData()
                config.SCAN_SOURCE = self.ui.comboBox_source.currentData()

                self.get_options.emit(self.ui.comboBox_device.itemData(index))
            else:
                self.setMessage('Процесс занят выполнением задачи...')

    @QtCore.pyqtSlot(str, object)
    def setMessage(self, string, msg=''):
        logger.info(f'text {string}, {msg}')
        self.ui.lineEdit_message.setText(string)

    def pressedtoolButtonPath(self):
        dirname = QFileDialog.getExistingDirectory(None, 'Выбор пути для сканированных фалов', config.SCAN_PATH)
        self.ui.lineEdit_path.setText(dirname)
        config.SCAN_PATH = dirname


    def pressedtoolReloadDevices(self):
        if self.sane_thread.isReady():
            self.get_devices.emit()
        else:
            self.setMessage('Процесс занят выполнением задачи...')

    def pressedButtonScan(self):
        logger.info('Button Scan')
        logger.debug(f'Ready thread: {self.sane_thread.isReady()}')
        logger.info(f'{self.ui.comboBox_device.currentData()}')

        if self.sane_thread.isReady():
            area = self.ui.comboBox_area.currentData()
            self.start_scan.emit({
                'device': self.ui.comboBox_device.currentData(),
                'mode': self.ui.comboBox_mode.currentData(),
                'dpi': self.ui.comboBox_dpi.currentData(),
                'source': self.ui.comboBox_source.currentData(),
                'cr_left': self.ui.spinBox_left.value(),
                'cr_upper': self.ui.spinBox_upper.value(),
                'cr_right': self.ui.spinBox_right.value(),
                'cr_lower': self.ui.spinBox_lower.value(),
                'ar_left': area[0], 'ar_upper': area[1], 'ar_right': area[2], 'ar_lower': area[3],

            })
        else:
            self.setMessage('Процесс занят выполнением задачи...')


    def pressedButtonExit(self):
        logger.info('Button Exit')
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        config.SCAN_DEVICE_NAME = self.ui.comboBox_device.currentText()
        config.SCAN_DEVICE_SIGNATURE = self.ui.comboBox_device.currentData()
        config.SCAN_SOURCE = self.ui.comboBox_source.currentText()
        config.SCAN_MODE = self.ui.comboBox_mode.currentText()
        config.SCAN_DPI = self.ui.comboBox_dpi.currentData()
        config.SCAN_AREA = self.ui.comboBox_area.currentText()
        config.SCAN_SPLIT = (self.ui.spinBox_left.value(), self.ui.spinBox_upper.value(),
                             self.ui.spinBox_right.value(), self.ui.spinBox_lower.value())

        config.save_config()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScanerWindow()
    window.show()
    sys.exit(app.exec_())
