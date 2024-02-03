import time
import sane

from loguru import logger

from PyQt5 import QtCore


def _locker(func):
    def wrapper(*args, **kwargs):
        logger.debug('worker LOCK')
        args[0].lock = True
        start_time = time.perf_counter()
        original_result = func(*args, **kwargs)
        args[0].lock = False
        logger.debug(f'worker UNLOCK, time is {time.perf_counter() - start_time}')
        return original_result

    return wrapper


class WorkerDrive(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    devices_signal = QtCore.pyqtSignal(str, object)
    options_signal = QtCore.pyqtSignal(dict)
    file_scan_signal = QtCore.pyqtSignal(object)
    message_signal = QtCore.pyqtSignal(str, object)

    def __init__(self, parent=None):
        super(WorkerDrive, self).__init__(parent)
        self.version = None
        self.lock = False

    def isReady(self):
        if self.lock:
            return False
        else:
            return True

    @QtCore.pyqtSlot()
    def run(self):
        # Initialize sane
        try:
            self.version = sane.init()
            self.message_signal.emit('Sane initial completed...', self.version)
        except (RuntimeError, sane._sane.error) as err:
            self.message_signal.emit('Error sane initial!!!', err)
            return None
        logger.info('Initial SANE completed.')

    # [(0, 'option-cnt', 'Number of options', 'Read-only option that specifies how many options a specific devices supports.', 1, 0, 4, 4, None),
    #  (1, 'mode-group', 'Scan mode', None, 5, 0, 0, 0, None),
    #  (2, 'mode', 'Scan mode', 'Selects the scan mode (e.g., lineart, monochrome, or color).', 3, 0, 32, 5,  ['Lineart', 'Gray', 'Color']),
    #  (3, 'resolution', 'Scan resolution', 'Sets the resolution of the scanned image.', 1, 4, 4, 5, [75, 100, 200, 300, 600, 1200]),
    #  (4, 'source', 'Scan source', 'Selects the scan source (such as a document-feeder).', 3, 0, 32, 5, ['Flatbed']),
    #  (5, 'advanced-group', 'Advanced', None, 5, 0, 0, 64, None),
    #  (6, 'brightness', 'Brightness', 'Controls the brightness of the acquired image.', 1, 0, 4, 69, (0, 2000, 0)),
    #  (7, 'contrast', 'Contrast', 'Controls the contrast of the acquired image.', 1, 0, 4, 69, (0, 2000, 0)),
    #  (8, 'compression', 'Compression', 'Selects the scanner compression method ....', 3, 0, 32, 69, ['None', 'JPEG']),
    #  (9, 'jpeg-quality', 'JPEG compression factor', 'Sets the scanner JPEG compression factor...',
    #                      1, 0, 4, 101, (0, 100, 0)), (10, 'geometry-group', 'Geometry', None, 5, 0, 0, 64, None),
    #  (11, 'tl-x', 'Top-left x', 'Top-left x position of scan area.', 2, 3, 4, 5, (0.0, 215.90000915527344, 0.0)),
    #  (12, 'tl-y', 'Top-left y', 'Top-left y position of scan area.', 2, 3, 4, 5, (0.0, 297.01068115234375, 0.0)), (
    #  13, 'br-x', 'Bottom-right x', 'Bottom-right x position of scan area.', 2, 3, 4, 5, (0.0, 215.90000915527344, 0.0)),
    #  (14, 'br-y', 'Bottom-right y', 'Bottom-right y position of scan area.', 2, 3, 4, 5, (0.0, 297.01068115234375, 0.0))]

    @QtCore.pyqtSlot(str)
    @_locker
    def get_options(self, device):
        if self.version is not None:
            options = {}
            try:
                scaner = sane.open(device)
                params = scaner.get_options()
                for param in params:
                    options[param[1]] = param[8]
            except (RuntimeError, sane._sane.error) as err:
                self.message_signal.emit(f'Error get parameters!!! (device:{device})', err)
            else:
                scaner.close()
                self.options_signal.emit(options)

    @QtCore.pyqtSlot()
    @_locker
    def get_devices(self):
        if self.version is None:
            # Initialize sane
            try:
                self.version = sane.init()
                self.message.emit('Sane initial completed...', self.version)
            except (RuntimeError, sane._sane.error) as err:
                self.message_signal.emit('Error sane initial!!!', err)
                return None

        if self.version is not None:
            # Get devices
            try:
                devices = sane.get_devices()
                self.devices_signal.emit(f'Sane version {self.version[0]}', devices)
            except (RuntimeError, sane._sane.error) as err:
                self.message_signal.emit('Error getting list devices...', err)

    @QtCore.pyqtSlot(dict)
    @_locker
    def scaner(self, param):
        logger.info(f'Start scaner proces {param}')
        # QtCore.QThread.msleep(3000)
        try:
            dev = sane.open(param['device'])
        except (RuntimeError, sane._sane.error) as err:
            self.message_signal.emit('Error open device...', err)
            return

        _, max_area = dev.area  # min_area, max_area
        dev.source = param['source']
        dev.mode = param['mode']
        dev.resolution = param['dpi']

        try:
            for image in dev.multi_scan():
                # processing image and save
                dpm = image.height / max_area[1]
                crop_image = image.crop((int(param['cr_left'] * dpm + param['ar_left'] * dpm),
                                         int(param['cr_upper'] * dpm + param['ar_upper'] * dpm),
                                         int(min(image.width, param['ar_right'] * dpm) - param['cr_right'] * dpm),
                                         int(min(image.height, param['ar_lower'] * dpm) - param['cr_lower'] * dpm)))
                self.file_scan_signal.emit(crop_image)
                if dev.source.lower() == 'flatbed':
                    dev.cancel()
                    break

        except (RuntimeError, sane._sane.error) as err:
            self.message_signal.emit('Error scan image...', err)
        dev.close()
