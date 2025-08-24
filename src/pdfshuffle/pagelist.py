from typing import Any

from loguru import logger
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, QPoint, QRect
from PyQt5.QtGui import QKeySequence, QDragEnterEvent, QColor, QFont, QPixmap, QTransform, \
    QBrush, QPainter, QDragLeaveEvent
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView, QStyledItemDelegate, QStyle

from pdfdata import PDFPage, PDFData

# Пользовательские роли для хранения данных
PRoleID = Qt.UserRole + 33
PRoleComment = Qt.UserRole + 36


class PageDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pdf = PDFData()

    @staticmethod
    def draw_indicator(
        painter: QPainter,
        rect: QRect,
        indicator_type: str = "red",
        position: int = 0
    ):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        circle_radius = 8  # Радиус круга

        colors = {
            "red": QColor(255, 0, 0),
            "orange": QColor(255, 165, 0),
            "green": QColor(0, 255, 0),
        }
        color = colors.get(indicator_type, QColor(255, 0, 0))  # По умолчанию красный

        # Вычисляем координаты круга
        circle_x = rect.left() + circle_radius + 5 + circle_radius * 3 * position  # Отступ от правого края
        circle_y = rect.top() + circle_radius + 5  # По центру по вертикали

        # Рисуем круг
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(circle_x, circle_y, circle_radius, circle_radius)

        painter.restore()

    def paint(self, painter: QPainter, option, index: QtCore.QModelIndex):
        """
        Перерисовывает элемент списка с учетом его статуса и данных.
        """
        img: QPixmap = index.model().data(index, Qt.DecorationRole)
        page: PDFPage = self._pdf.get_page(index.model().data(index, PRoleID))
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

        if page.size == 0:
            self.draw_indicator(painter, option.rect, "orange")

        # Подпись
        txt = index.data(Qt.DisplayRole)
        txt2 = f'стр.{index.row() + 1}'
        painter.setPen(QColor(100, 34, 50))
        painter.setFont(QFont('Decorative', 8))
        painter.drawText(QtCore.QRect(x0 + 10, y0 + y1 - 30, x1 - 20, 30), Qt.AlignCenter, txt)

        painter.setPen(QColor(80, 75, 250))
        font_metrics = painter.fontMetrics()
        text_width = font_metrics.horizontalAdvance(txt2)
        font_height = font_metrics.height()
        painter.fillRect(QtCore.QRect(x0 + x1 - 12 - text_width, y0  + 8, text_width + 4, font_height + 4), QColor('white'))
        painter.drawText(QtCore.QRect(x0 + x1 - 10 - text_width, y0  + 10, text_width, font_height), Qt.AlignLeft, txt2)

    def sizeHint(self, option, index: QtCore.QModelIndex) -> QtCore.QSize:
        """
        Возвращает размеры элемента списка.
        """
        img: QPixmap = index.model().data(index, Qt.DecorationRole)
        if img.width() > img.height():
            return QSize(100, img.height() + 40)
        else:
            return QSize(img.width() + 20, 120)


class PageWidget(QListWidget):
    message = QtCore.pyqtSignal(str)

    def __init__(self, wg):
        super().__init__(wg)

        self._func_add_file = None
        self._pdf: PDFData = PDFData()

        self.setWrapping(True)
        self.setAcceptDrops(True)
        self.setFlow(self.LeftToRight)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.setItemDelegate(PageDelegate())

    def __iter__(self):
        for i in range(self.count()):
            yield self.item(i)

    def selected_items(self):
        """Итератор по выделенным элементам"""
        for item in self.selectedItems():
            yield item

    def add_page(self, page: PDFPage):
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
                    try:
                        self._func_add_file(self, f.toLocalFile())
                    except Exception as e:
                        logger.error(f"Ошибка при добавлении файла: {e}")
                logger.info(f'Получен файл: {f}')

        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            items = event.source().selectedItems()
            source = event.source()
            for i, item in enumerate(items):
                if event.keyboardModifiers() != Qt.ShiftModifier:
                    source.takeItem(source.row(item))
                else:
                    page_id = self._pdf.clone_id(item.data(PRoleID))
                    if page_id is None:
                        logger.error(f'Ошибка при копировании страницы: {item.data(PRoleID)}')
                        return
                    item = item.clone()
                    item.setData(PRoleID, page_id)
                    item.setData(Qt.DecorationRole, self._pdf.get_page(page_id).get_pixmap(80, 80))

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
            self.setCurrentRow(-1)
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
                pixmap = item.data(Qt.DecorationRole)
                if pixmap:
                    item.setData(Qt.DecorationRole, pixmap.transformed(trans_rotate))
                    page = self._pdf.get_page(item.data(PRoleID))
                    if page:
                        page.rotate(angle)
                        yield item.data(PRoleID)
        else:
            raise ValueError('Rotate page may be angle 0, 90, 180, 270')

    def get_current_id(self):
        current_item = self.currentItem()
        if current_item:
            return current_item.data(PRoleID)
        return None

    def get_current_page(self):
        page_id = self.get_current_id()
        if page_id is not None:
            return self._pdf.get_page(page_id)
        return None

    def get_page(self, item):
        page_id = item.data(PRoleID)
        if page_id is not None:
            return self._pdf.get_page(page_id)
        return None

    def get_text_selected(self):
        t_names = []
        for item in self.selectedItems():
            page = self.get_page(item)
            if page:
                t_names.append(page.name_page)
        return ', '.join(t_names)

    def get_size_selected(self):
        size_all = 0
        for item in self.selectedItems():
            page = self.get_page(item)
            if page:
                size_all += page.size

        return f'Размер выбранного: {size_all // 1024} кб'

    def connect_add_file(self, func):
        self._func_add_file = func
