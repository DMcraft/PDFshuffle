from loguru import logger
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QKeySequence, QDragEnterEvent, QColor, QFont, QPixmap, QTransform, QDragLeaveEvent
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView, QStyledItemDelegate, QStyle

from pdfdata import PDFPage
from pdfdata import PDFData

PRoleID = Qt.UserRole + 33
PRoleSize = Qt.UserRole + 37
PRoleComment = Qt.UserRole + 36



class PageDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        img: QPixmap = index.model().data(index, Qt.DecorationRole)
        x0, y0, x1, y1 = option.rect.getRect()

        if option.state & QStyle.State_Selected:
            painter.setBrush(QColor(155, 193, 219))
            painter.drawRect(QtCore.QRect(x0 + 5, y0 + 5, x1 - 10, y1 - 10))
            if img.width() > img.height():
                img = img.scaledToWidth(70)
            else:
                img = img.scaledToHeight(70)
            w, h = img.width(), img.height()
            painter.drawPixmap(QtCore.QRect(x0 + (x1 - w) // 2, y0 + (y1 - h) // 2 - 15, w, h), img)
        else:
            if img.width() > img.height():
                img = img.scaledToWidth(80)
            else:
                img = img.scaledToHeight(80)
            w, h = img.width(), img.height()
            painter.drawPixmap(QtCore.QRect(x0 + (x1 - w) // 2, y0 + (y1 - h) // 2 - 15, w, h), img)

        # Подпись
        txt = index.data()
        txt2 = f'( {index.row() + 1} )'
        painter.setPen(QColor(100, 34, 50))
        painter.setFont(QFont('Decorative', 8))
        painter.drawText(QtCore.QRect(x0 + 10, y0 + y1 - 30, x1 - 20, 30), Qt.AlignCenter, txt)
        painter.setPen(QColor(160, 75, 50))
        painter.fillRect(QtCore.QRect(x0 + 10, y0 + y1 - 40, 30, 15), QColor('white'))
        painter.drawText(QtCore.QRect(x0 + 10, y0 + y1 - 40, x1 - 20, 20), Qt.AlignLeft, txt2)

    def sizeHint(self, option, index: QtCore.QModelIndex) -> QtCore.QSize:
        img: QPixmap = index.model().data(index, Qt.DecorationRole)
        if img.width() > img.height():
            return QSize(100, img.height() + 40)
        else:
            return QSize(img.width() + 20, 120)


class PageWidget(QListWidget):

    message = QtCore.pyqtSignal(str)

    def __init__(self, wg, pdf:PDFData):
        super().__init__(wg)

        self._func_add_file = None
        self._pdf:PDFData = pdf

        self.setWrapping(True)
        self.setAcceptDrops(True)
        self.setFlow(self.LeftToRight)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setItemDelegate(PageDelegate())

    def __iter__(self):
        for i in range(self.count()):
            yield self.item(i)

    def add_page(self, page:PDFPage):
        item = QListWidgetItem()
        item.setData(PRoleID, page.get_id())
        item.setData(Qt.DecorationRole, page.get_pixmap(80, 80))
        item.setText(page.name_page)
        self.addItem(item)

    def dragLeaveEvent(self, e: QDragLeaveEvent):
        pass

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls() or e.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            e.accept()

    def dragMoveEvent(self, e):
        t = self.itemAt(e.pos())
        if t is not None:
            pass
            # t.setSelected(False)

    def dropEvent(self, event: QDragEnterEvent):
        # e.accept()
        if event.mimeData().hasUrls():
            for f in event.mimeData().urls():
                if f.isLocalFile() and self._func_add_file is not None:
                    self._func_add_file(self, f.toLocalFile())
                logger.info(f'Resive mime: {f}')
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            items = event.source().selectedItems()
            source = event.source()
            for i, item in enumerate(items):
                # Обрабатываем элемент из источника
                if event.keyboardModifiers() != Qt.ShiftModifier:
                    source.takeItem(source.row(item))
                else:
                    item = item.clone()
                    page = self.get_page(item).copy()
                    self._pdf._addpage(page)
                    item.setData(PRoleID, page.get_id())
                    item.setData(Qt.DecorationRole, page.get_pixmap(80, 80))

                # Добавляем элемент в текущий список
                row = self.row(self.itemAt(event.pos()))
                if row < 0:
                    self.addItem(item)
                else:
                    self.insertItem(row + i, item)
                item.setSelected(True)

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Delete):
            for item in self.selectedItems():
                self.takeItem(self.row(item))
        elif event.key() == Qt.Key_Escape:
            self.currentList.currentList.setCurrentRow(-1)
        else:
            QListWidget.keyPressEvent(self, event)

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_A:
            self.message.emit(self.get_size_selected())

    def rotate_page(self, angle=90):
        angle = angle % 360
        if angle < 0:
            angle = 360 - angle
        if angle in (0, 90, 180, 270):
            trans_rotate = QTransform().rotate(angle)
            for item in self.selectedItems():
                item.setData(Qt.DecorationRole, QPixmap(item.data(Qt.DecorationRole).transformed(trans_rotate)))
                self._pdf.get_page(item.data(PRoleID)).rotate(angle)
                yield item.data(PRoleID)
        else:
            raise ValueError('Rotate page may be angle 0, 90, 180, 270')

    def get_current_id(self):
        return self.currentItem().data(PRoleID)

    def get_current_page(self) -> PDFPage:
        return self._pdf.get_page(self.currentItem().data(PRoleID))

    def get_page(self, item) -> PDFPage:
        return self._pdf.get_page(item.data(PRoleID))

    def get_text_selected(self):
        t_names = []
        for item in self.selectedItems():
            t_names.append(self._pdf.get_page(item.data(PRoleID)).name_page)

        return ', '.join(t_names)

    def get_size_selected(self):
        size_all = 0
        for item in self.selectedItems():
            size_all += self._pdf.get_page(item.data(PRoleID)).size

        return f'Размер выбранного: {size_all // 1024} кб'

    def connect_add_file(self, func):
        self._func_add_file = func
