# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 700)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.comboBoxSizePaper = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxSizePaper.setCurrentText("A4")
        self.comboBoxSizePaper.setObjectName("comboBoxSizePaper")
        self.comboBoxSizePaper.addItem("")
        self.comboBoxSizePaper.setItemText(0, "A0")
        self.comboBoxSizePaper.addItem("")
        self.comboBoxSizePaper.setItemText(1, "A1")
        self.comboBoxSizePaper.addItem("")
        self.comboBoxSizePaper.setItemText(2, "A2")
        self.comboBoxSizePaper.addItem("")
        self.comboBoxSizePaper.setItemText(3, "A3")
        self.comboBoxSizePaper.addItem("")
        self.comboBoxSizePaper.setItemText(4, "A4")
        self.comboBoxSizePaper.addItem("")
        self.comboBoxSizePaper.setItemText(5, "A5")
        self.comboBoxSizePaper.addItem("")
        self.comboBoxSizePaper.setItemText(6, "A6")
        self.comboBoxSizePaper.addItem("")
        self.comboBoxSizePaper.setItemText(7, "A7")
        self.comboBoxSizePaper.addItem("")
        self.comboBoxSizePaper.setItemText(8, "A8")
        self.comboBoxSizePaper.addItem("")
        self.comboBoxSizePaper.setItemText(9, "A9")
        self.comboBoxSizePaper.addItem("")
        self.comboBoxSizePaper.setItemText(10, "A10")
        self.horizontalLayout_3.addWidget(self.comboBoxSizePaper)
        self.comboBoxOrientation = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxOrientation.setObjectName("comboBoxOrientation")
        self.comboBoxOrientation.addItem("")
        self.comboBoxOrientation.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBoxOrientation)
        self.comboBoxPaperDPI = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxPaperDPI.setObjectName("comboBoxPaperDPI")
        self.horizontalLayout_3.addWidget(self.comboBoxPaperDPI)
        self.spinquality = QtWidgets.QSpinBox(self.centralwidget)
        self.spinquality.setMinimum(10)
        self.spinquality.setMaximum(100)
        self.spinquality.setSingleStep(5)
        self.spinquality.setProperty("value", 90)
        self.spinquality.setObjectName("spinquality")
        self.horizontalLayout_3.addWidget(self.spinquality)
        self.checkBoxImageExtend = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxImageExtend.setEnabled(True)
        self.checkBoxImageExtend.setObjectName("checkBoxImageExtend")
        self.horizontalLayout_3.addWidget(self.checkBoxImageExtend)
        self.checkBoxImageFormatting = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxImageFormatting.setIconSize(QtCore.QSize(16, 16))
        self.checkBoxImageFormatting.setChecked(True)
        self.checkBoxImageFormatting.setObjectName("checkBoxImageFormatting")
        self.horizontalLayout_3.addWidget(self.checkBoxImageFormatting)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.toolButtonViewerVisible_2 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonViewerVisible_2.setMinimumSize(QtCore.QSize(0, 20))
        self.toolButtonViewerVisible_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.toolButtonViewerVisible_2.setObjectName("toolButtonViewerVisible_2")
        self.horizontalLayout_3.addWidget(self.toolButtonViewerVisible_2)
        self.toolButtonViewerVisible = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonViewerVisible.setMinimumSize(QtCore.QSize(0, 20))
        self.toolButtonViewerVisible.setMaximumSize(QtCore.QSize(16777215, 20))
        self.toolButtonViewerVisible.setObjectName("toolButtonViewerVisible")
        self.horizontalLayout_3.addWidget(self.toolButtonViewerVisible)
        self.toolButtonViewerVisible_1 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonViewerVisible_1.setMinimumSize(QtCore.QSize(0, 20))
        self.toolButtonViewerVisible_1.setMaximumSize(QtCore.QSize(16777215, 20))
        self.toolButtonViewerVisible_1.setObjectName("toolButtonViewerVisible_1")
        self.horizontalLayout_3.addWidget(self.toolButtonViewerVisible_1)
        self.pushButtonScan = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonScan.setObjectName("pushButtonScan")
        self.horizontalLayout_3.addWidget(self.pushButtonScan)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.toolButtonRotate = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonRotate.setMaximumSize(QtCore.QSize(16777215, 20))
        self.toolButtonRotate.setObjectName("toolButtonRotate")
        self.horizontalLayout.addWidget(self.toolButtonRotate)
        self.toolButtonAdd = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonAdd.setMinimumSize(QtCore.QSize(0, 20))
        self.toolButtonAdd.setMaximumSize(QtCore.QSize(16777215, 20))
        self.toolButtonAdd.setObjectName("toolButtonAdd")
        self.horizontalLayout.addWidget(self.toolButtonAdd)
        self.toolButtonClear = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonClear.setMinimumSize(QtCore.QSize(0, 20))
        self.toolButtonClear.setMaximumSize(QtCore.QSize(16777215, 20))
        self.toolButtonClear.setObjectName("toolButtonClear")
        self.horizontalLayout.addWidget(self.toolButtonClear)
        self.toolButtonSave = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonSave.setMaximumSize(QtCore.QSize(16777215, 20))
        self.toolButtonSave.setObjectName("toolButtonSave")
        self.horizontalLayout.addWidget(self.toolButtonSave)
        self.toolButtonRestore = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonRestore.setMinimumSize(QtCore.QSize(0, 20))
        self.toolButtonRestore.setMaximumSize(QtCore.QSize(16777215, 20))
        self.toolButtonRestore.setObjectName("toolButtonRestore")
        self.horizontalLayout.addWidget(self.toolButtonRestore)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.BasicLayout = QtWidgets.QVBoxLayout()
        self.BasicLayout.setObjectName("BasicLayout")
        self.verticalLayout.addLayout(self.BasicLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.toolButtonSecondRotate = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonSecondRotate.setMaximumSize(QtCore.QSize(16777215, 20))
        self.toolButtonSecondRotate.setObjectName("toolButtonSecondRotate")
        self.horizontalLayout_2.addWidget(self.toolButtonSecondRotate)
        self.toolButtonSecondAdd = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonSecondAdd.setMinimumSize(QtCore.QSize(0, 20))
        self.toolButtonSecondAdd.setMaximumSize(QtCore.QSize(16777215, 20))
        self.toolButtonSecondAdd.setObjectName("toolButtonSecondAdd")
        self.horizontalLayout_2.addWidget(self.toolButtonSecondAdd)
        self.toolButtonSecondClear = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonSecondClear.setMinimumSize(QtCore.QSize(0, 20))
        self.toolButtonSecondClear.setMaximumSize(QtCore.QSize(16777215, 20))
        self.toolButtonSecondClear.setObjectName("toolButtonSecondClear")
        self.horizontalLayout_2.addWidget(self.toolButtonSecondClear)
        self.toolButtonSaveSecond = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonSaveSecond.setMaximumSize(QtCore.QSize(16777215, 20))
        self.toolButtonSaveSecond.setObjectName("toolButtonSaveSecond")
        self.horizontalLayout_2.addWidget(self.toolButtonSaveSecond)
        self.toolButtonExchange = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonExchange.setMinimumSize(QtCore.QSize(0, 20))
        self.toolButtonExchange.setMaximumSize(QtCore.QSize(16777215, 20))
        self.toolButtonExchange.setObjectName("toolButtonExchange")
        self.horizontalLayout_2.addWidget(self.toolButtonExchange)
        self.toolButtonSecondView = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonSecondView.setMinimumSize(QtCore.QSize(0, 20))
        self.toolButtonSecondView.setMaximumSize(QtCore.QSize(16777215, 20))
        self.toolButtonSecondView.setObjectName("toolButtonSecondView")
        self.horizontalLayout_2.addWidget(self.toolButtonSecondView)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.SecondLayout = QtWidgets.QVBoxLayout()
        self.SecondLayout.setObjectName("SecondLayout")
        self.verticalLayout.addLayout(self.SecondLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 21))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineviewpath = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineviewpath.sizePolicy().hasHeightForWidth())
        self.lineviewpath.setSizePolicy(sizePolicy)
        self.lineviewpath.setMaximumSize(QtCore.QSize(16777215, 21))
        self.lineviewpath.setObjectName("lineviewpath")
        self.horizontalLayout_4.addWidget(self.lineviewpath)
        self.toolButtonPath = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonPath.setMaximumSize(QtCore.QSize(16777215, 21))
        self.toolButtonPath.setObjectName("toolButtonPath")
        self.horizontalLayout_4.addWidget(self.toolButtonPath)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setEnabled(True)
        self.scrollArea.setMaximumSize(QtCore.QSize(500, 16777215))
        self.scrollArea.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 462, 563))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(100, 100))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.labelView = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labelView.setGeometry(QtCore.QRect(1, 1, 131, 91))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelView.sizePolicy().hasHeightForWidth())
        self.labelView.setSizePolicy(sizePolicy)
        self.labelView.setText("")
        self.labelView.setScaledContents(False)
        self.labelView.setAlignment(QtCore.Qt.AlignCenter)
        self.labelView.setObjectName("labelView")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButtonPrint = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonPrint.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonPrint.sizePolicy().hasHeightForWidth())
        self.pushButtonPrint.setSizePolicy(sizePolicy)
        self.pushButtonPrint.setMaximumSize(QtCore.QSize(16777215, 21))
        self.pushButtonPrint.setObjectName("pushButtonPrint")
        self.horizontalLayout_6.addWidget(self.pushButtonPrint, 0, QtCore.Qt.AlignRight)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_5.setSpacing(1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6, 0, QtCore.Qt.AlignRight)
        self.toolButtonScalePlus = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonScalePlus.setMaximumSize(QtCore.QSize(16777215, 21))
        self.toolButtonScalePlus.setObjectName("toolButtonScalePlus")
        self.horizontalLayout_5.addWidget(self.toolButtonScalePlus)
        self.lineEditScale = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditScale.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditScale.sizePolicy().hasHeightForWidth())
        self.lineEditScale.setSizePolicy(sizePolicy)
        self.lineEditScale.setMaximumSize(QtCore.QSize(50, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEditScale.setFont(font)
        self.lineEditScale.setMaxLength(5)
        self.lineEditScale.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditScale.setDragEnabled(False)
        self.lineEditScale.setReadOnly(True)
        self.lineEditScale.setObjectName("lineEditScale")
        self.horizontalLayout_5.addWidget(self.lineEditScale)
        self.toolButtonScaleMinus = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonScaleMinus.setMaximumSize(QtCore.QSize(16777215, 21))
        self.toolButtonScaleMinus.setObjectName("toolButtonScaleMinus")
        self.horizontalLayout_5.addWidget(self.toolButtonScaleMinus)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.menuFile.setFont(font)
        self.menuFile.setObjectName("menuFile")
        self.menuEditor = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.menuEditor.setFont(font)
        self.menuEditor.setObjectName("menuEditor")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.menuAbout.setFont(font)
        self.menuAbout.setObjectName("menuAbout")
        self.menuView = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.menuView.setFont(font)
        self.menuView.setObjectName("menuView")
        self.menuTool = QtWidgets.QMenu(self.menubar)
        self.menuTool.setObjectName("menuTool")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.statusbar.setFont(font)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAddBasic = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionAddBasic.setFont(font)
        self.actionAddBasic.setObjectName("actionAddBasic")
        self.actionClearBasic = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionClearBasic.setFont(font)
        self.actionClearBasic.setObjectName("actionClearBasic")
        self.actionAddSecond = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionAddSecond.setFont(font)
        self.actionAddSecond.setObjectName("actionAddSecond")
        self.actionClearSecond = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionClearSecond.setFont(font)
        self.actionClearSecond.setObjectName("actionClearSecond")
        self.actionClearAll = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionClearAll.setFont(font)
        self.actionClearAll.setObjectName("actionClearAll")
        self.actionSaveTo = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionSaveTo.setFont(font)
        self.actionSaveTo.setObjectName("actionSaveTo")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionAbout.setFont(font)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionScan = QtWidgets.QAction(MainWindow)
        self.actionScan.setObjectName("actionScan")
        self.actionShortcutDesktop = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionShortcutDesktop.setFont(font)
        self.actionShortcutDesktop.setObjectName("actionShortcutDesktop")
        self.actionShortcutMenu = QtWidgets.QAction(MainWindow)
        self.actionShortcutMenu.setObjectName("actionShortcutMenu")
        self.actionViewMax = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionViewMax.setFont(font)
        self.actionViewMax.setObjectName("actionViewMax")
        self.actionViewMin = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionViewMin.setFont(font)
        self.actionViewMin.setObjectName("actionViewMin")
        self.actionViewNormal = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionViewNormal.setFont(font)
        self.actionViewNormal.setObjectName("actionViewNormal")
        self.actionSavetoImage = QtWidgets.QAction(MainWindow)
        self.actionSavetoImage.setObjectName("actionSavetoImage")
        self.actionTransformtoImage = QtWidgets.QAction(MainWindow)
        self.actionTransformtoImage.setObjectName("actionTransformtoImage")
        self.menuFile.addAction(self.actionAddBasic)
        self.menuFile.addAction(self.actionAddSecond)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSaveTo)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEditor.addAction(self.actionClearBasic)
        self.menuEditor.addAction(self.actionClearSecond)
        self.menuEditor.addSeparator()
        self.menuEditor.addAction(self.actionClearAll)
        self.menuEditor.addSeparator()
        self.menuEditor.addAction(self.actionScan)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addSeparator()
        self.menuAbout.addAction(self.actionShortcutDesktop)
        self.menuAbout.addAction(self.actionShortcutMenu)
        self.menuView.addAction(self.actionViewMax)
        self.menuView.addAction(self.actionViewNormal)
        self.menuView.addAction(self.actionViewMin)
        self.menuTool.addAction(self.actionSavetoImage)
        self.menuTool.addAction(self.actionTransformtoImage)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEditor.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menubar.addAction(self.menuTool.menuAction())

        self.retranslateUi(MainWindow)
        self.comboBoxSizePaper.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Параметры вставки изображений:"))
        self.comboBoxOrientation.setItemText(0, _translate("MainWindow", "Portret"))
        self.comboBoxOrientation.setItemText(1, _translate("MainWindow", "Landscape"))
        self.checkBoxImageExtend.setText(_translate("MainWindow", "extend"))
        self.checkBoxImageFormatting.setText(_translate("MainWindow", "formatting"))
        self.toolButtonViewerVisible_2.setToolTip(_translate("MainWindow", "видимость предпросмотра"))
        self.toolButtonViewerVisible_2.setText(_translate("MainWindow", "[+]"))
        self.toolButtonViewerVisible.setToolTip(_translate("MainWindow", "видимость предпросмотра"))
        self.toolButtonViewerVisible.setText(_translate("MainWindow", "[ ]"))
        self.toolButtonViewerVisible_1.setToolTip(_translate("MainWindow", "видимость предпросмотра"))
        self.toolButtonViewerVisible_1.setText(_translate("MainWindow", "[-]"))
        self.pushButtonScan.setText(_translate("MainWindow", "Сканировать"))
        self.label_3.setText(_translate("MainWindow", "Основное окно эскизов"))
        self.toolButtonRotate.setToolTip(_translate("MainWindow", "поворот на 90 гр. по часовой"))
        self.toolButtonRotate.setText(_translate("MainWindow", "rotate"))
        self.toolButtonAdd.setToolTip(_translate("MainWindow", "добавить из файла в основное окно"))
        self.toolButtonAdd.setText(_translate("MainWindow", "+"))
        self.toolButtonClear.setToolTip(_translate("MainWindow", "очистить основное окно"))
        self.toolButtonClear.setText(_translate("MainWindow", "-"))
        self.toolButtonSave.setToolTip(_translate("MainWindow", "сохранить страницы из основного окна"))
        self.toolButtonSave.setText(_translate("MainWindow", "Save"))
        self.toolButtonRestore.setToolTip(_translate("MainWindow", "востановить все страницы открытые в сессии и поместить в основное окно"))
        self.toolButtonRestore.setText(_translate("MainWindow", "Restore"))
        self.label_2.setText(_translate("MainWindow", "Окно эскизов"))
        self.toolButtonSecondRotate.setToolTip(_translate("MainWindow", "поворот на 90 гр. по часовой"))
        self.toolButtonSecondRotate.setText(_translate("MainWindow", "rotate"))
        self.toolButtonSecondAdd.setToolTip(_translate("MainWindow", "добавить из файла в дополнительное окно"))
        self.toolButtonSecondAdd.setText(_translate("MainWindow", "+"))
        self.toolButtonSecondClear.setToolTip(_translate("MainWindow", "очистить дополнительное окно"))
        self.toolButtonSecondClear.setText(_translate("MainWindow", "-"))
        self.toolButtonSaveSecond.setToolTip(_translate("MainWindow", "сохранить страницы из дополнительного окна"))
        self.toolButtonSaveSecond.setText(_translate("MainWindow", "Save"))
        self.toolButtonExchange.setToolTip(_translate("MainWindow", "обмен между окон"))
        self.toolButtonExchange.setText(_translate("MainWindow", "<>"))
        self.toolButtonSecondView.setToolTip(_translate("MainWindow", "скрыть/показать дополнительное окно"))
        self.toolButtonSecondView.setText(_translate("MainWindow", "^"))
        self.label_4.setText(_translate("MainWindow", "Рабочий путь:"))
        self.lineviewpath.setText(_translate("MainWindow", "..."))
        self.toolButtonPath.setText(_translate("MainWindow", "показать"))
        self.pushButtonPrint.setText(_translate("MainWindow", "Печать"))
        self.label_6.setText(_translate("MainWindow", "Масштаб:"))
        self.toolButtonScalePlus.setText(_translate("MainWindow", "+"))
        self.lineEditScale.setText(_translate("MainWindow", "1x"))
        self.toolButtonScaleMinus.setText(_translate("MainWindow", "-"))
        self.menuFile.setTitle(_translate("MainWindow", "Файл"))
        self.menuEditor.setTitle(_translate("MainWindow", "Редактор"))
        self.menuAbout.setTitle(_translate("MainWindow", "О программе"))
        self.menuView.setTitle(_translate("MainWindow", "Вид"))
        self.menuTool.setTitle(_translate("MainWindow", "Инструменты"))
        self.actionAddBasic.setText(_translate("MainWindow", "Добавить в основной"))
        self.actionClearBasic.setText(_translate("MainWindow", "Очистить основной"))
        self.actionAddSecond.setText(_translate("MainWindow", "Добавить в дополнительный"))
        self.actionClearSecond.setText(_translate("MainWindow", "Очистить дополнительный"))
        self.actionClearAll.setText(_translate("MainWindow", "Очистить всё"))
        self.actionSaveTo.setText(_translate("MainWindow", "Сохранить основной в ..."))
        self.actionAbout.setText(_translate("MainWindow", "О программе..."))
        self.actionExit.setText(_translate("MainWindow", "Выход"))
        self.actionScan.setText(_translate("MainWindow", "Сканировать"))
        self.actionShortcutDesktop.setText(_translate("MainWindow", "Добавить ярлыки на рабочий стол"))
        self.actionShortcutMenu.setText(_translate("MainWindow", "Добавить ярлыки в меню"))
        self.actionViewMax.setText(_translate("MainWindow", "Максимальный размер"))
        self.actionViewMin.setText(_translate("MainWindow", "Минимальный размер"))
        self.actionViewNormal.setText(_translate("MainWindow", "Нормальный размер"))
        self.actionSavetoImage.setText(_translate("MainWindow", "Сохранить постранично как изображения"))
        self.actionTransformtoImage.setText(_translate("MainWindow", "Преобразовать в изображения"))
