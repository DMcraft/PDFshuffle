# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scanerwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ScanerForm(object):
    def setupUi(self, ScanerForm):
        ScanerForm.setObjectName("ScanerForm")
        ScanerForm.resize(370, 460)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ScanerForm.sizePolicy().hasHeightForWidth())
        ScanerForm.setSizePolicy(sizePolicy)
        ScanerForm.setMinimumSize(QtCore.QSize(370, 460))
        ScanerForm.setMaximumSize(QtCore.QSize(370, 460))
        font = QtGui.QFont()
        font.setPointSize(10)
        ScanerForm.setFont(font)
        self.label = QtWidgets.QLabel(ScanerForm)
        self.label.setGeometry(QtCore.QRect(10, 20, 161, 22))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(ScanerForm)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 161, 22))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(ScanerForm)
        self.label_3.setGeometry(QtCore.QRect(10, 100, 161, 22))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(ScanerForm)
        self.label_4.setGeometry(QtCore.QRect(10, 80, 161, 22))
        self.label_4.setObjectName("label_4")
        self.comboBox_dpi = QtWidgets.QComboBox(ScanerForm)
        self.comboBox_dpi.setGeometry(QtCore.QRect(170, 80, 191, 21))
        self.comboBox_dpi.setObjectName("comboBox_dpi")
        self.comboBox_area = QtWidgets.QComboBox(ScanerForm)
        self.comboBox_area.setGeometry(QtCore.QRect(170, 100, 191, 21))
        self.comboBox_area.setObjectName("comboBox_area")
        self.comboBox_source = QtWidgets.QComboBox(ScanerForm)
        self.comboBox_source.setGeometry(QtCore.QRect(170, 40, 191, 21))
        self.comboBox_source.setObjectName("comboBox_source")
        self.comboBox_device = QtWidgets.QComboBox(ScanerForm)
        self.comboBox_device.setGeometry(QtCore.QRect(170, 20, 171, 21))
        self.comboBox_device.setObjectName("comboBox_device")
        self.groupBoxSample = QtWidgets.QGroupBox(ScanerForm)
        self.groupBoxSample.setEnabled(False)
        self.groupBoxSample.setGeometry(QtCore.QRect(10, 290, 351, 131))
        self.groupBoxSample.setObjectName("groupBoxSample")
        self.pushButton_template_add = QtWidgets.QPushButton(self.groupBoxSample)
        self.pushButton_template_add.setGeometry(QtCore.QRect(280, 80, 61, 21))
        self.pushButton_template_add.setObjectName("pushButton_template_add")
        self.pushButton_template_del = QtWidgets.QPushButton(self.groupBoxSample)
        self.pushButton_template_del.setGeometry(QtCore.QRect(280, 60, 61, 21))
        self.pushButton_template_del.setObjectName("pushButton_template_del")
        self.pushButton_template_default = QtWidgets.QPushButton(self.groupBoxSample)
        self.pushButton_template_default.setGeometry(QtCore.QRect(280, 30, 61, 31))
        self.pushButton_template_default.setObjectName("pushButton_template_default")
        self.pushButton_template_replace = QtWidgets.QPushButton(self.groupBoxSample)
        self.pushButton_template_replace.setGeometry(QtCore.QRect(280, 100, 61, 21))
        self.pushButton_template_replace.setObjectName("pushButton_template_replace")
        self.list_template = QtWidgets.QListView(self.groupBoxSample)
        self.list_template.setGeometry(QtCore.QRect(10, 30, 261, 91))
        self.list_template.setObjectName("list_template")
        self.pushButton_exit = QtWidgets.QPushButton(ScanerForm)
        self.pushButton_exit.setGeometry(QtCore.QRect(280, 260, 81, 21))
        self.pushButton_exit.setText("Выйти")
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.toolButton_devreload = QtWidgets.QToolButton(ScanerForm)
        self.toolButton_devreload.setGeometry(QtCore.QRect(340, 20, 21, 21))
        self.toolButton_devreload.setObjectName("toolButton_devreload")
        self.lineEdit_message = QtWidgets.QLineEdit(ScanerForm)
        self.lineEdit_message.setEnabled(False)
        self.lineEdit_message.setGeometry(QtCore.QRect(10, 430, 351, 21))
        self.lineEdit_message.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit_message.setAcceptDrops(True)
        self.lineEdit_message.setFrame(False)
        self.lineEdit_message.setReadOnly(True)
        self.lineEdit_message.setClearButtonEnabled(False)
        self.lineEdit_message.setObjectName("lineEdit_message")
        self.label_8 = QtWidgets.QLabel(ScanerForm)
        self.label_8.setGeometry(QtCore.QRect(10, 60, 161, 22))
        self.label_8.setObjectName("label_8")
        self.comboBox_mode = QtWidgets.QComboBox(ScanerForm)
        self.comboBox_mode.setGeometry(QtCore.QRect(170, 60, 191, 21))
        self.comboBox_mode.setObjectName("comboBox_mode")
        self.spinBox_upper = QtWidgets.QSpinBox(ScanerForm)
        self.spinBox_upper.setGeometry(QtCore.QRect(220, 120, 45, 21))
        self.spinBox_upper.setMaximum(300)
        self.spinBox_upper.setObjectName("spinBox_upper")
        self.spinBox_right = QtWidgets.QSpinBox(ScanerForm)
        self.spinBox_right.setGeometry(QtCore.QRect(270, 120, 45, 21))
        self.spinBox_right.setMaximum(300)
        self.spinBox_right.setObjectName("spinBox_right")
        self.spinBox_left = QtWidgets.QSpinBox(ScanerForm)
        self.spinBox_left.setGeometry(QtCore.QRect(170, 120, 45, 21))
        self.spinBox_left.setMaximum(300)
        self.spinBox_left.setObjectName("spinBox_left")
        self.spinBox_lower = QtWidgets.QSpinBox(ScanerForm)
        self.spinBox_lower.setGeometry(QtCore.QRect(320, 120, 45, 21))
        self.spinBox_lower.setMaximum(300)
        self.spinBox_lower.setObjectName("spinBox_lower")
        self.label_9 = QtWidgets.QLabel(ScanerForm)
        self.label_9.setGeometry(QtCore.QRect(10, 120, 151, 22))
        self.label_9.setObjectName("label_9")
        self.groupBoxSave = QtWidgets.QGroupBox(ScanerForm)
        self.groupBoxSave.setEnabled(True)
        self.groupBoxSave.setGeometry(QtCore.QRect(10, 150, 351, 101))
        self.groupBoxSave.setObjectName("groupBoxSave")
        self.toolButton_path = QtWidgets.QToolButton(self.groupBoxSave)
        self.toolButton_path.setGeometry(QtCore.QRect(300, 50, 21, 21))
        self.toolButton_path.setObjectName("toolButton_path")
        self.lineEdit_filename = QtWidgets.QLineEdit(self.groupBoxSave)
        self.lineEdit_filename.setGeometry(QtCore.QRect(140, 70, 201, 21))
        self.lineEdit_filename.setObjectName("lineEdit_filename")
        self.label_7 = QtWidgets.QLabel(self.groupBoxSave)
        self.label_7.setGeometry(QtCore.QRect(10, 30, 131, 22))
        self.label_7.setObjectName("label_7")
        self.label_6 = QtWidgets.QLabel(self.groupBoxSave)
        self.label_6.setGeometry(QtCore.QRect(10, 70, 131, 22))
        self.label_6.setObjectName("label_6")
        self.lineEdit_path = QtWidgets.QLineEdit(self.groupBoxSave)
        self.lineEdit_path.setEnabled(True)
        self.lineEdit_path.setGeometry(QtCore.QRect(140, 50, 161, 21))
        self.lineEdit_path.setReadOnly(True)
        self.lineEdit_path.setObjectName("lineEdit_path")
        self.label_5 = QtWidgets.QLabel(self.groupBoxSave)
        self.label_5.setGeometry(QtCore.QRect(10, 50, 131, 22))
        self.label_5.setObjectName("label_5")
        self.comboBox_typefile = QtWidgets.QComboBox(self.groupBoxSave)
        self.comboBox_typefile.setGeometry(QtCore.QRect(140, 30, 141, 21))
        self.comboBox_typefile.setObjectName("comboBox_typefile")
        self.toolButtonOpenDir = QtWidgets.QToolButton(self.groupBoxSave)
        self.toolButtonOpenDir.setGeometry(QtCore.QRect(320, 50, 21, 21))
        self.toolButtonOpenDir.setShortcut("")
        self.toolButtonOpenDir.setObjectName("toolButtonOpenDir")
        self.spinBox_quality = QtWidgets.QSpinBox(self.groupBoxSave)
        self.spinBox_quality.setGeometry(QtCore.QRect(290, 30, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setKerning(True)
        self.spinBox_quality.setFont(font)
        self.spinBox_quality.setMouseTracking(False)
        self.spinBox_quality.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.spinBox_quality.setAutoFillBackground(False)
        self.spinBox_quality.setPrefix("")
        self.spinBox_quality.setMinimum(10)
        self.spinBox_quality.setMaximum(100)
        self.spinBox_quality.setProperty("value", 90)
        self.spinBox_quality.setObjectName("spinBox_quality")
        self.pushButton_save = QtWidgets.QPushButton(ScanerForm)
        self.pushButton_save.setGeometry(QtCore.QRect(140, 260, 121, 21))
        self.pushButton_save.setObjectName("pushButton_save")
        self.pushButton_scan = QtWidgets.QPushButton(ScanerForm)
        self.pushButton_scan.setGeometry(QtCore.QRect(10, 260, 121, 21))
        self.pushButton_scan.setObjectName("pushButton_scan")
        self.checkBox_autosave = QtWidgets.QCheckBox(ScanerForm)
        self.checkBox_autosave.setGeometry(QtCore.QRect(230, 150, 131, 20))
        self.checkBox_autosave.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_autosave.setObjectName("checkBox_autosave")

        self.retranslateUi(ScanerForm)
        QtCore.QMetaObject.connectSlotsByName(ScanerForm)

    def retranslateUi(self, ScanerForm):
        _translate = QtCore.QCoreApplication.translate
        ScanerForm.setWindowTitle(_translate("ScanerForm", "Form"))
        self.label.setText(_translate("ScanerForm", "Устройство"))
        self.label_2.setText(_translate("ScanerForm", "Источник сканирования"))
        self.label_3.setText(_translate("ScanerForm", "Область сканирования"))
        self.label_4.setText(_translate("ScanerForm", "Разрешение"))
        self.groupBoxSample.setTitle(_translate("ScanerForm", "Шаблоны"))
        self.pushButton_template_add.setText(_translate("ScanerForm", "Add"))
        self.pushButton_template_del.setText(_translate("ScanerForm", "Del"))
        self.pushButton_template_default.setText(_translate("ScanerForm", "Default"))
        self.pushButton_template_replace.setText(_translate("ScanerForm", "Repl"))
        self.toolButton_devreload.setText(_translate("ScanerForm", "..."))
        self.lineEdit_message.setText(_translate("ScanerForm", "Init..."))
        self.label_8.setText(_translate("ScanerForm", "Режим сканирования"))
        self.label_9.setText(_translate("ScanerForm", "Обрезка (l, up, r, lo)"))
        self.groupBoxSave.setTitle(_translate("ScanerForm", "Сохранение"))
        self.toolButton_path.setText(_translate("ScanerForm", "..."))
        self.label_7.setText(_translate("ScanerForm", "Формат файла"))
        self.label_6.setText(_translate("ScanerForm", "Имя файла"))
        self.label_5.setText(_translate("ScanerForm", "Путь сканирования"))
        self.toolButtonOpenDir.setText(_translate("ScanerForm", ">>"))
        self.spinBox_quality.setWhatsThis(_translate("ScanerForm", "качество сжатия изображения"))
        self.pushButton_save.setText(_translate("ScanerForm", "Сохранить"))
        self.pushButton_scan.setText(_translate("ScanerForm", "Сканировать"))
        self.checkBox_autosave.setText(_translate("ScanerForm", "автосохранение"))
