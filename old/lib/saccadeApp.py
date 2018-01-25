# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import threading as th
import subprocess as sp
# ==============
from fileHandlers import *
from PyQt4 import QtCore, QtGui
from dataModels import listModel, tableModel


# =============================================================================
# Qt Encoding
# =============================================================================
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)

except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

# =============================================================================
# ID Definitions
# =============================================================================
FILE_HOME = 0
FILE_EXEC = 1
FILE_CONF = 2
TEST_CONF = 3
TEST_LIST = 4
EXPS_CONF = 5
EXPS_LIST = 6
MAX_ID = 6


# =============================================================================
# GUI: Main Window
# =============================================================================
class mainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        # ==============
        self.config = confFile()
        # ==============
        self.setupUi()
        self.initModels()
        self.setupMenuButtons()
        # ==============
        self.selectedWidget = None
        self.changeMainWidget(FILE_HOME)

    # =================================
    def setupUi(self):
        self.setObjectName(_fromUtf8("mainWindow"))
        self.resize(500, 500)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(500, 500))
        self.setMaximumSize(QtCore.QSize(500, 500))
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(5)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.setCentralWidget(self.centralwidget)
        self.menu = QtGui.QMenuBar(self)
        self.menu.setGeometry(QtCore.QRect(0, 0, 500, 23))
        self.menu.setObjectName(_fromUtf8("menu"))
        self.itmFile = QtGui.QMenu(self.menu)
        self.itmFile.setObjectName(_fromUtf8("itmFile"))
        self.itmTest = QtGui.QMenu(self.menu)
        self.itmTest.setObjectName(_fromUtf8("itmTest"))
        self.itmExperiment = QtGui.QMenu(self.menu)
        self.itmExperiment.setObjectName(_fromUtf8("itmExperiment"))
        self.setMenuBar(self.menu)
        self.actHome = QtGui.QAction(self)
        self.actHome.setObjectName(_fromUtf8("actHome"))
        self.actExecute = QtGui.QAction(self)
        self.actExecute.setObjectName(_fromUtf8("actExecute"))
        self.actConfig = QtGui.QAction(self)
        self.actConfig.setObjectName(_fromUtf8("actConfig"))
        self.actQuit = QtGui.QAction(self)
        self.actQuit.setObjectName(_fromUtf8("actQuit"))
        self.actNewTest = QtGui.QAction(self)
        self.actNewTest.setObjectName(_fromUtf8("actNewTest"))
        self.actListTest = QtGui.QAction(self)
        self.actListTest.setObjectName(_fromUtf8("actListTest"))
        self.actNewExps = QtGui.QAction(self)
        self.actNewExps.setObjectName(_fromUtf8("actNewExps"))
        self.actListExps = QtGui.QAction(self)
        self.actListExps.setObjectName(_fromUtf8("actListExps"))
        self.itmFile.addAction(self.actHome)
        self.itmFile.addAction(self.actExecute)
        self.itmFile.addSeparator()
        self.itmFile.addAction(self.actConfig)
        self.itmFile.addSeparator()
        self.itmFile.addAction(self.actQuit)
        self.itmTest.addAction(self.actNewTest)
        self.itmTest.addAction(self.actListTest)
        self.itmExperiment.addAction(self.actNewExps)
        self.itmExperiment.addAction(self.actListExps)
        self.menu.addAction(self.itmFile.menuAction())
        self.menu.addAction(self.itmTest.menuAction())
        self.menu.addAction(self.itmExperiment.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("mainWindow", "lib", None))
        self.itmFile.setTitle(_translate("mainWindow", "File", None))
        self.itmTest.setTitle(_translate("mainWindow", "Test", None))
        self.itmExperiment.setTitle(_translate("mainWindow", "Experiments", None))
        self.actHome.setText(_translate("mainWindow", "Home", None))
        self.actExecute.setText(_translate("mainWindow", "Execute", None))
        self.actConfig.setText(_translate("mainWindow", "Configuration", None))
        self.actQuit.setText(_translate("mainWindow", "Quit", None))
        self.actNewTest.setText(_translate("mainWindow", "New...", None))
        self.actListTest.setText(_translate("mainWindow", "List", None))
        self.actNewExps.setText(_translate("mainWindow", "New...", None))
        self.actListExps.setText(_translate("mainWindow", "List", None))

    # =================================
    def getFilePath(self, filename, isTest=True):
        testPath = self.config.testDir + u'/' + filename + TEST_TYPE
        expsPath = self.config.expsDir + u'/' + filename + EXPS_TYPE
        return testPath if isTest else expsPath

    # =================================
    def initModels(self):
        self.testModel = listModel([], u'Test')
        self.expsModel = listModel([], u'Experiment')
        # ==============
        self.testModel.setDataFromPath(self.getFilePath(u'*', isTest=True))
        self.expsModel.setDataFromPath(self.getFilePath(u'*', isTest=False))

    def setupMenuButtons(self):
        self.actHome.triggered.connect(lambda: self.changeMainWidget(FILE_HOME))
        self.actExecute.triggered.connect(lambda: self.changeMainWidget(FILE_EXEC))
        self.actConfig.triggered.connect(lambda: self.changeMainWidget(FILE_CONF))
        self.actNewTest.triggered.connect(lambda: self.changeMainWidget(TEST_CONF))
        self.actListTest.triggered.connect(lambda: self.changeMainWidget(TEST_LIST))
        self.actNewExps.triggered.connect(lambda: self.changeMainWidget(EXPS_CONF))
        self.actListExps.triggered.connect(lambda: self.changeMainWidget(EXPS_LIST))
        # ==============
        self.actQuit.triggered.connect(self.appClose)

    def changeMainWidget(self, widgetIndex):
        if widgetIndex <= MAX_ID:
            if widgetIndex is FILE_HOME:
                print u'Selecting home widget...'
                self.selectedWidget = formFileHome(parent=self)
            elif widgetIndex is FILE_EXEC:
                print u'Selecting execute widget...'
                self.selectedWidget = formFileExecute(parent=self)
            elif widgetIndex is FILE_CONF:
                print u'Selecting app configuration widget...'
                self.selectedWidget = formFileConfig(parent=self)
            elif widgetIndex is TEST_CONF:
                print u'Selecting new/modify test widget...'
                self.selectedWidget = formTestConfig(parent=self)
            elif widgetIndex is TEST_LIST:
                print u'Selecting test list widget...'
                self.selectedWidget = formList(parent=self, isTest=True)
            elif widgetIndex is EXPS_CONF:
                print u'Selecting new/modify experiment widget...'
                self.selectedWidget = formExperimentConfig(parent=self)
            elif widgetIndex is EXPS_LIST:
                print u'Selecting experiment list widget...'
                self.selectedWidget = formList(parent=self, isTest=False)
            self.setCentralWidget(self.selectedWidget)
        else:
            print u'Widget ID not recognized: Check setupMenuButtons, something is wrong!!!'

    def appClose(self):
        print u'Closing the App...\n'
        self.close()


# =============================================================================
# GUI: Widgets Home
# =============================================================================
# =============================================== File
class formFileHome(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        # ==============
        self.parent = parent
        # ==============
        self.setupUi()

    # =================================
    def setupUi(self):
        self.setObjectName(_fromUtf8("formFileHome"))
        self.resize(490, 450)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(490, 450))
        self.setMaximumSize(QtCore.QSize(490, 450))
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.lblTitle = QtGui.QLabel(self)
        self.lblTitle.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lblTitle.setFont(font)
        self.lblTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lblTitle.setObjectName(_fromUtf8("lblTitle"))
        self.verticalLayout.addWidget(self.lblTitle)
        self.hLayout = QtGui.QHBoxLayout()
        self.hLayout.setContentsMargins(-1, 10, -1, 10)
        self.hLayout.setObjectName(_fromUtf8("hLayout"))
        self.lblContent = QtGui.QLabel(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblContent.sizePolicy().hasHeightForWidth())
        self.lblContent.setSizePolicy(sizePolicy)
        self.lblContent.setAlignment(QtCore.Qt.AlignCenter)
        self.lblContent.setObjectName(_fromUtf8("lblContent"))
        self.hLayout.addWidget(self.lblContent)
        self.verticalLayout.addLayout(self.hLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("formFileHome", "Form", None))
        self.lblTitle.setText(_translate("formFileHome", "lib", None))
        self.lblContent.setText(_translate("formFileHome", "Some info about the program... Fill later", None))

# ======================
class formFileExecute(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        # ==============
        self.parent = parent
        # ==============
        self.setupUi()
        self.setupActions()
        # ==============
        self.initComboBox()

    # =================================
    def setupUi(self):
        self.setObjectName(_fromUtf8("formFileExecute"))
        self.resize(490, 450)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(490, 450))
        self.setMaximumSize(QtCore.QSize(490, 450))
        self.formLayout = QtGui.QVBoxLayout(self)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.formLayout.addItem(spacerItem)
        self.hLayout1 = QtGui.QHBoxLayout()
        self.hLayout1.setContentsMargins(-1, 0, -1, -1)
        self.hLayout1.setObjectName(_fromUtf8("hLayout1"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayout1.addItem(spacerItem1)
        self.gBox = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gBox.sizePolicy().hasHeightForWidth())
        self.gBox.setSizePolicy(sizePolicy)
        self.gBox.setMinimumSize(QtCore.QSize(300, 0))
        self.gBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.gBox.setObjectName(_fromUtf8("gBox"))
        self.vLayout = QtGui.QVBoxLayout(self.gBox)
        self.vLayout.setObjectName(_fromUtf8("vLayout"))
        self.hLayout2 = QtGui.QHBoxLayout()
        self.hLayout2.setContentsMargins(0, 0, -1, -1)
        self.hLayout2.setObjectName(_fromUtf8("hLayout2"))
        self.lblExps = QtGui.QLabel(self.gBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblExps.sizePolicy().hasHeightForWidth())
        self.lblExps.setSizePolicy(sizePolicy)
        self.lblExps.setMinimumSize(QtCore.QSize(90, 25))
        self.lblExps.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lblExps.setObjectName(_fromUtf8("lblExps"))
        self.hLayout2.addWidget(self.lblExps)
        self.cBoxExps = QtGui.QComboBox(self.gBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cBoxExps.sizePolicy().hasHeightForWidth())
        self.cBoxExps.setSizePolicy(sizePolicy)
        self.cBoxExps.setMinimumSize(QtCore.QSize(0, 25))
        self.cBoxExps.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cBoxExps.setObjectName(_fromUtf8("cBoxExps"))
        self.hLayout2.addWidget(self.cBoxExps)
        self.vLayout.addLayout(self.hLayout2)
        self.hLayout3 = QtGui.QHBoxLayout()
        self.hLayout3.setObjectName(_fromUtf8("hLayout3"))
        self.lblMonitor = QtGui.QLabel(self.gBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblMonitor.sizePolicy().hasHeightForWidth())
        self.lblMonitor.setSizePolicy(sizePolicy)
        self.lblMonitor.setMinimumSize(QtCore.QSize(90, 25))
        self.lblMonitor.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lblMonitor.setObjectName(_fromUtf8("lblMonitor"))
        self.hLayout3.addWidget(self.lblMonitor)
        self.cBoxMonitor = QtGui.QComboBox(self.gBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cBoxMonitor.sizePolicy().hasHeightForWidth())
        self.cBoxMonitor.setSizePolicy(sizePolicy)
        self.cBoxMonitor.setMinimumSize(QtCore.QSize(0, 25))
        self.cBoxMonitor.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cBoxMonitor.setObjectName(_fromUtf8("cBoxMonitor"))
        self.hLayout3.addWidget(self.cBoxMonitor)
        self.vLayout.addLayout(self.hLayout3)
        self.hLayout4 = QtGui.QHBoxLayout()
        self.hLayout4.setObjectName(_fromUtf8("hLayout4"))
        self.lblMonitorConfig = QtGui.QLabel(self.gBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblMonitorConfig.sizePolicy().hasHeightForWidth())
        self.lblMonitorConfig.setSizePolicy(sizePolicy)
        self.lblMonitorConfig.setMinimumSize(QtCore.QSize(90, 25))
        self.lblMonitorConfig.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lblMonitorConfig.setObjectName(_fromUtf8("lblMonitorConfig"))
        self.hLayout4.addWidget(self.lblMonitorConfig)
        self.cBoxMonitorConfig = QtGui.QComboBox(self.gBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cBoxMonitorConfig.sizePolicy().hasHeightForWidth())
        self.cBoxMonitorConfig.setSizePolicy(sizePolicy)
        self.cBoxMonitorConfig.setMinimumSize(QtCore.QSize(0, 25))
        self.cBoxMonitorConfig.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cBoxMonitorConfig.setObjectName(_fromUtf8("cBoxMonitorConfig"))
        self.hLayout4.addWidget(self.cBoxMonitorConfig)
        self.vLayout.addLayout(self.hLayout4)
        self.btnStart = QtGui.QPushButton(self.gBox)
        self.btnStart.setMinimumSize(QtCore.QSize(0, 40))
        self.btnStart.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.btnStart.setFont(font)
        self.btnStart.setObjectName(_fromUtf8("btnStart"))
        self.vLayout.addWidget(self.btnStart)
        self.hLayout1.addWidget(self.gBox)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayout1.addItem(spacerItem2)
        self.formLayout.addLayout(self.hLayout1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.addItem(spacerItem3)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("formFileExecute", "Form", None))
        self.gBox.setTitle(_translate("formFileExecute", "Execute", None))
        self.lblExps.setText(_translate("formFileExecute", "Experiment:", None))
        self.lblMonitor.setText(_translate("formFileExecute", "Monitor:", None))
        self.lblMonitorConfig.setText(_translate("formFileExecute", "Monitor Config:", None))
        self.btnStart.setText(_translate("formFileExecute", "Start", None))

    # =================================
    def initComboBox(self):
        from psychopy import monitors
        # ==============
        self.cBoxExps.setModel(self.parent.expsModel)
        self.cBoxMonitor.addItems(self.getInstalledMonitors())
        self.cBoxMonitorConfig.addItems(monitors.getAllMonitors())

    def setupActions(self):
        self.btnStart.clicked.connect(self.startExperiment)

    def getInstalledMonitors(self):
        import pyglet
        # ==============
        screens = pyglet.window.get_platform().get_default_display().get_screens()
        # ==============
        screenNum = 1
        screenList = []
        for screen in screens:
            screenList.append(u'monitor: %s (width=%s, height=%s)' % (screenNum, screen.width, screen.height))
            screenNum += 1
        return screenList

    def startExperiment(self):
        print u'Start experiment button pressed...'
        pass

# ======================
class formFileConfig(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        # ==============
        self.parent = parent
        # ==============
        self.setupUi()
        self.initConf()
        self.setupActions()

    # =================================
    def setupUi(self):
        self.setObjectName(_fromUtf8("formFileConfig"))
        self.resize(490, 450)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(490, 450))
        self.setMaximumSize(QtCore.QSize(490, 450))
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.gBox1 = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gBox1.sizePolicy().hasHeightForWidth())
        self.gBox1.setSizePolicy(sizePolicy)
        self.gBox1.setMinimumSize(QtCore.QSize(450, 0))
        self.gBox1.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.gBox1.setObjectName(_fromUtf8("gBox1"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.gBox1)
        self.verticalLayout_3.setContentsMargins(-1, 9, -1, -1)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.hLayout2 = QtGui.QHBoxLayout()
        self.hLayout2.setContentsMargins(0, 0, -1, -1)
        self.hLayout2.setObjectName(_fromUtf8("hLayout2"))
        self.lblTest = QtGui.QLabel(self.gBox1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTest.sizePolicy().hasHeightForWidth())
        self.lblTest.setSizePolicy(sizePolicy)
        self.lblTest.setMinimumSize(QtCore.QSize(90, 25))
        self.lblTest.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lblTest.setObjectName(_fromUtf8("lblTest"))
        self.hLayout2.addWidget(self.lblTest)
        self.tBoxTest = QtGui.QLineEdit(self.gBox1)
        self.tBoxTest.setMinimumSize(QtCore.QSize(0, 25))
        self.tBoxTest.setMaximumSize(QtCore.QSize(16777215, 25))
        self.tBoxTest.setAutoFillBackground(True)
        self.tBoxTest.setReadOnly(True)
        self.tBoxTest.setObjectName(_fromUtf8("tBoxTest"))
        self.hLayout2.addWidget(self.tBoxTest)
        self.btnTest = QtGui.QPushButton(self.gBox1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnTest.sizePolicy().hasHeightForWidth())
        self.btnTest.setSizePolicy(sizePolicy)
        self.btnTest.setMinimumSize(QtCore.QSize(0, 25))
        self.btnTest.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnTest.setObjectName(_fromUtf8("btnTest"))
        self.hLayout2.addWidget(self.btnTest)
        self.verticalLayout_3.addLayout(self.hLayout2)
        self.hLayout3 = QtGui.QHBoxLayout()
        self.hLayout3.setObjectName(_fromUtf8("hLayout3"))
        self.lblExps = QtGui.QLabel(self.gBox1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblExps.sizePolicy().hasHeightForWidth())
        self.lblExps.setSizePolicy(sizePolicy)
        self.lblExps.setMinimumSize(QtCore.QSize(90, 25))
        self.lblExps.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lblExps.setObjectName(_fromUtf8("lblExps"))
        self.hLayout3.addWidget(self.lblExps)
        self.tBoxExps = QtGui.QLineEdit(self.gBox1)
        self.tBoxExps.setMinimumSize(QtCore.QSize(0, 25))
        self.tBoxExps.setMaximumSize(QtCore.QSize(16777215, 25))
        self.tBoxExps.setAutoFillBackground(True)
        self.tBoxExps.setReadOnly(True)
        self.tBoxExps.setObjectName(_fromUtf8("tBoxExps"))
        self.hLayout3.addWidget(self.tBoxExps)
        self.btnExps = QtGui.QPushButton(self.gBox1)
        self.btnExps.setMinimumSize(QtCore.QSize(0, 25))
        self.btnExps.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnExps.setObjectName(_fromUtf8("btnExps"))
        self.hLayout3.addWidget(self.btnExps)
        self.verticalLayout_3.addLayout(self.hLayout3)
        self.verticalLayout.addWidget(self.gBox1)
        self.gBox2 = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gBox2.sizePolicy().hasHeightForWidth())
        self.gBox2.setSizePolicy(sizePolicy)
        self.gBox2.setMinimumSize(QtCore.QSize(450, 60))
        self.gBox2.setObjectName(_fromUtf8("gBox2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.gBox2)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 15)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnMonitor = QtGui.QPushButton(self.gBox2)
        self.btnMonitor.setMinimumSize(QtCore.QSize(0, 40))
        self.btnMonitor.setMaximumSize(QtCore.QSize(150, 25))
        self.btnMonitor.setObjectName(_fromUtf8("btnMonitor"))
        self.horizontalLayout.addWidget(self.btnMonitor)
        self.verticalLayout.addWidget(self.gBox2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("formFileConfig", "Form", None))
        self.gBox1.setTitle(_translate("formFileConfig", "Folders", None))
        self.lblTest.setText(_translate("formFileConfig", "Tests:", None))
        self.btnTest.setText(_translate("formFileConfig", "Open Folder", None))
        self.lblExps.setText(_translate("formFileConfig", "Experiments:", None))
        self.btnExps.setText(_translate("formFileConfig", "Open Folder", None))
        self.gBox2.setTitle(_translate("formFileConfig", "Monitors", None))
        self.btnMonitor.setText(_translate("formFileConfig", "Go to PsychoPy Monitor\nCenter!", None))

    # =================================
    def initConf(self):
        self.tBoxTest.setText(self.parent.config.testDir)
        self.tBoxExps.setText(self.parent.config.expsDir)

    def setupActions(self):
        self.btnTest.clicked.connect(lambda: self.openFolder(0))
        self.btnExps.clicked.connect(lambda: self.openFolder(1))
        self.btnMonitor.clicked.connect(self.openMonitorCenter)

    def openFolder(self, select=0):
        if select is 0:
            title = u'Select Test Folder'
            folder = unicode(self.tBoxTest.text())
            print u'Changing tests folder...'
        else:
            title = u'Select Experiment Folder'
            folder = unicode(self.tBoxExps.text())
            print u'Changing experiments folder...'
        # ==============
        folderName = QtGui.QFileDialog.getExistingDirectory(self, title, folder, QtGui.QFileDialog.ShowDirsOnly)
        # ==============
        if folderName:
            folderName = unicode(folderName)
            if select is 0:
                self.tBoxTest.setText(folderName)
                self.parent.config.testDir = folderName
            else:
                self.tBoxExps.setText(folderName)
                self.parent.config.expsDir = folderName
            print u'Change in configuration succeeded!'
            self.parent.config.putConfig()
        else:
            print u'Not change made...'

    @QtCore.pyqtSlot()
    def openMonitorCenter(self):
        isClosed = True
        threads = th.enumerate()
        # ==============
        for thread in threads:
            if thread.getName() == u'MonitorCenter':
                isClosed = False
        # ==============
        if isClosed:
            print u'Opening Monitor Center...'
            command = u'python ../lib/monitorCenter.py'
            thread = th.Thread(target=lambda: sp.call(command))
            thread.setName(u'MonitorCenter')
            thread.start()
        else:
            print u'Error: Monitor Center is already open!'


# =============================================================================
# GUI: Widgets Lists
# =============================================================================
# =============================================== Tests
class formList(QtGui.QWidget):
    def __init__(self, parent, itemId=-1, isTest=True):
        QtGui.QWidget.__init__(self)
        # ==============
        self.itemId = itemId
        self.parent = parent
        self.isTest = isTest
        # ==============
        self.model = self.parent.testModel if self.isTest else self.parent.expsModel
        # ==============
        self.setupUi()
        self.initTree()
        self.setupActions()

    # =================================
    def setupUi(self):
        self.setObjectName(_fromUtf8("formList"))
        self.resize(490, 450)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(490, 450))
        self.setMaximumSize(QtCore.QSize(490, 450))
        self.formLayout = QtGui.QVBoxLayout(self)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.gBox = QtGui.QGroupBox(self)
        self.gBox.setObjectName(_fromUtf8("gBox"))
        self.hLayout = QtGui.QHBoxLayout(self.gBox)
        self.hLayout.setObjectName(_fromUtf8("hLayout"))
        self.trVrData = QtGui.QTreeView(self.gBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trVrData.sizePolicy().hasHeightForWidth())
        self.trVrData.setSizePolicy(sizePolicy)
        self.trVrData.setMinimumSize(QtCore.QSize(320, 0))
        self.trVrData.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.trVrData.setObjectName(_fromUtf8("trVrData"))
        self.hLayout.addWidget(self.trVrData)
        self.vLayout = QtGui.QVBoxLayout()
        self.vLayout.setSpacing(5)
        self.vLayout.setObjectName(_fromUtf8("vLayout"))
        self.btnNew = QtGui.QPushButton(self.gBox)
        self.btnNew.setMinimumSize(QtCore.QSize(80, 25))
        self.btnNew.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnNew.setObjectName(_fromUtf8("btnNew"))
        self.vLayout.addWidget(self.btnNew)
        self.btnCopy = QtGui.QPushButton(self.gBox)
        self.btnCopy.setMinimumSize(QtCore.QSize(80, 25))
        self.btnCopy.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnCopy.setObjectName(_fromUtf8("btnCopy"))
        self.vLayout.addWidget(self.btnCopy)
        self.btnEdit = QtGui.QPushButton(self.gBox)
        self.btnEdit.setMinimumSize(QtCore.QSize(80, 25))
        self.btnEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.vLayout.addWidget(self.btnEdit)
        self.btnRemove = QtGui.QPushButton(self.gBox)
        self.btnRemove.setMinimumSize(QtCore.QSize(80, 25))
        self.btnRemove.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnRemove.setObjectName(_fromUtf8("btnRemove"))
        self.vLayout.addWidget(self.btnRemove)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vLayout.addItem(spacerItem)
        self.hLayout.addLayout(self.vLayout)
        self.formLayout.addWidget(self.gBox)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        title = "Test list" if self.isTest else "Experiment list"
        self.setWindowTitle(_translate("formList", "Form", None))
        self.gBox.setTitle(_translate("formList", title, None))
        self.btnNew.setText(_translate("formList", "New...", None))
        self.btnCopy.setText(_translate("formList", "Copy", None))
        self.btnEdit.setText(_translate("formList", "Edit", None))
        self.btnRemove.setText(_translate("formList", "Remove", None))

    # =================================
    def initTree(self):
        itemsDir = self.parent.getFilePath(u'*', isTest=self.isTest)
        # ==============
        self.model.setDataFromPath(itemsDir)
        self.trVrData.setModel(self.model)
        self.trVrData.setSortingEnabled(True)
        # ==============
        if self.itemId is not None and 0 <= self.itemId <= self.model.rowCount():
            self.trVrData.setCurrentIndex(self.model.index(self.itemId, 0))
        else:
            self.trVrData.setCurrentIndex(self.model.index(0, 0))

    def setupActions(self):
        self.btnNew.clicked.connect(self.newItem)
        self.btnEdit.clicked.connect(self.editItem)
        self.btnCopy.clicked.connect(self.copyItem)
        self.btnRemove.clicked.connect(self.removeItem)

    # =================================
    def newItem(self):
        print u'New item...'
        self.goToConfig(itemId=-1)

    def editItem(self):
        itemTotal = self.model.rowCount()
        itemIndex = self.trVrData.currentIndex().row()
        # ==============
        if itemTotal is not 0 and itemIndex is not -1:
            print u'Modifying item...'
            self.goToConfig(itemId=itemIndex)
        else:
            print u'No item selected/available!'

    def copyItem(self):
        itemTotal = self.model.rowCount()
        itemIndex = self.trVrData.currentIndex().row()
        # ==============
        if itemTotal is not 0 and itemIndex is not -1:
            print u'Copying item...'
            # ==============
            fileExt = TEST_TYPE if self.isTest else EXPS_TYPE
            filePath = self.parent.config.testDir if self.isTest else self.parent.config.expsDir
            # ==============
            oldName = self.model.getItemById(itemIndex)
            oldPath = self.parent.getFilePath(oldName, isTest=self.isTest)
            newName, newPath = getFilePath(path=filePath, ext=fileExt, oldName=oldName, isRW=False)
            # ==============
            if newName is not None:
                print u'Ok!'
                # ==============
                auxConf = testFileConf(oldPath) if self.isTest else expsFileConf(oldPath)
                auxConf.putConf(newPath)
                self.model.addNewValue(newName)
                # ==============
                newIndex = self.model.getIdByItem(newName)
                self.trVrData.setCurrentIndex(self.model.index(newIndex, 0))
            else:
                print u'No item inserted or operation cancelled!'
        else:
            print u'No item selected/available!'

    def removeItem(self):
        itemTotal = self.model.rowCount()
        itemIndex = self.trVrData.currentIndex().row()
        # ==============
        if itemTotal is not 0 and itemIndex is not -1:
            print u'Deleting item...'
            # ==============
            fileName = unicode(self.model.getItemById(index=itemIndex))
            # ==============
            os.remove(self.parent.getFilePath(fileName, isTest=self.isTest))
            self.trVrData.model().removeValue(fileName)
            # ==============
            nextItemIndex = itemIndex-1 if itemIndex-1 >= 0 else 0
            self.trVrData.setCurrentIndex(self.trVrData.model().index(nextItemIndex, 0))
        else:
            print u'No item selected/available!'

    def goToConfig(self, itemId=-1):
        widget = formTestConfig(parent=self.parent, itemId=itemId) if self.isTest else formExperimentConfig(parent=self.parent, itemId=itemId)
        self.parent.selectedWidget = widget
        self.parent.setCentralWidget(widget)


# =============================================================================
# GUI: Widgets New/Modify
# =============================================================================
class formTable(QtGui.QWidget):
    def __init__(self, parent, itemId=-1, modelData=[], modelHeaders=[], isTest=True):
        QtGui.QWidget.__init__(self)
        # ==============
        self.parent = parent
        self.itemId = itemId
        self.isTest = isTest
        # ==============
        self.model = tableModel(data=modelData, headers=modelHeaders)

    # =================================
    def moveItemUp(self, table):
        itemTotal = self.model.rowCount()
        itemIndex = table.currentIndex().row()
        # ==============
        if itemTotal is not 0 and itemIndex > 0:
            print u'Moving the item up...'
            self.model.rotateItem(itemIndex, itemIndex-1)
            table.setCurrentIndex(self.model.index(itemIndex-1, 0))
        else:
            print u'This item is in the top!'
            table.setCurrentIndex(self.model.index(itemIndex, 0))

    def moveItemDown(self, table):
        itemTotal = self.model.rowCount()
        itemIndex = table.currentIndex().row()
        # ==============
        if itemTotal is not 0 and itemIndex < itemTotal-1 and itemIndex is not -1:
            print u'Moving the item down...'
            self.model.rotateItem(itemIndex, itemIndex + 1)
            table.setCurrentIndex(self.model.index(itemIndex + 1, 0))
        else:
            print u'This item is in the bottom!'
            table.setCurrentIndex(self.model.index(itemIndex, 0))

    def removeItem(self, table):
        itemTotal = self.model.rowCount()
        itemIndex = table.currentIndex().row()
        # ==============
        if itemTotal is not 0 and itemIndex is not -1:
            print u'Deleting item...'
            # ==============
            self.model.removeRow(itemIndex)
            # ==============
            nextItemIndex = itemIndex-1 if itemIndex-1 >= 0 else 0
            table.setCurrentIndex(self.model.index(nextItemIndex, 0))
        else:
            print u'No items to delete!'

    def saveItem(self, itemName, confData):
        listModel = self.parent.testModel if self.isTest else self.parent.expsModel
        # ==============
        fileExt = TEST_TYPE if self.isTest else EXPS_TYPE
        filePath = self.parent.config.testDir if self.isTest else self.parent.config.expsDir
        # ==============
        oldName = listModel.getItemById(index=self.itemId)
        newName, newPath = getFilePath(path=filePath, ext=fileExt, newName=itemName, oldName=oldName, isRW=True)
        # ==============
        if newName is not None and confData is not None:
            if oldName not in NOT_VALID_CHARS and oldName is not None:
                os.remove(self.parent.getFilePath(oldName, isTest=self.isTest))
                listModel.removeValue(oldName)
            confData.putConf(newPath)
            listModel.addNewValue(newName)
            # ==============
            itemIndex = listModel.getIdByItem(newName)
            self.goToList(itemId=itemIndex)
            return True
        else:
            return False

    def handleCancelBtn(self):
        print u'Cancel button pressed...'
        self.goToList(self.itemId)

    def goToList(self, itemId=-1):
        self.parent.selectedWidget = formList(parent=self.parent, itemId=itemId, isTest=self.isTest)
        self.parent.setCentralWidget(self.parent.selectedWidget)

    # =================================
    def setupUI(self):
        pass

    def retranslateUi(self):
        pass

    def setupActions(self):
        pass

    def initTable(self):
        pass

    def handleOkBtn(self):
        pass


# =============================================== Tests
class formTestConfig(formTable):
    def __init__(self, parent, itemId=-1):
        formTable.__init__(self, parent=parent, itemId=itemId, isTest=True,
                           modelData=[[u'Empty', 0.0]], modelHeaders=[u'Image', u'Time [s]'])
        # ==============
        self.setupUi()
        self.setupActions()
        self.checkIfNewTest()
        # ==============
        self.initTable()

    # =================================
    def setupUi(self):
        self.setObjectName(_fromUtf8("formTestConfig"))
        self.resize(490, 450)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(490, 450))
        self.setMaximumSize(QtCore.QSize(490, 450))
        self.formLayout = QtGui.QVBoxLayout(self)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.gBox1 = QtGui.QGroupBox(self)
        self.gBox1.setObjectName(_fromUtf8("gBox1"))
        self.hLayout1 = QtGui.QHBoxLayout(self.gBox1)
        self.hLayout1.setMargin(5)
        self.hLayout1.setSpacing(5)
        self.hLayout1.setObjectName(_fromUtf8("hLayout1"))
        self.tBoxTest = QtGui.QLineEdit(self.gBox1)
        self.tBoxTest.setMinimumSize(QtCore.QSize(300, 25))
        self.tBoxTest.setMaximumSize(QtCore.QSize(16777215, 25))
        self.tBoxTest.setAutoFillBackground(True)
        self.tBoxTest.setObjectName(_fromUtf8("tBoxTest"))
        self.hLayout1.addWidget(self.tBoxTest)
        spacerItem = QtGui.QSpacerItem(146, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayout1.addItem(spacerItem)
        self.formLayout.addWidget(self.gBox1)
        self.gBox2 = QtGui.QGroupBox(self)
        self.gBox2.setObjectName(_fromUtf8("gBox2"))
        self.hLayout2 = QtGui.QHBoxLayout(self.gBox2)
        self.hLayout2.setMargin(5)
        self.hLayout2.setSpacing(5)
        self.hLayout2.setObjectName(_fromUtf8("hLayout2"))
        self.tabVwImag = QtGui.QTableView(self.gBox2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabVwImag.sizePolicy().hasHeightForWidth())
        self.tabVwImag.setSizePolicy(sizePolicy)
        self.tabVwImag.setMinimumSize(QtCore.QSize(320, 0))
        self.tabVwImag.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tabVwImag.setObjectName(_fromUtf8("tabVwImag"))
        self.hLayout2.addWidget(self.tabVwImag)
        self.vLayout1 = QtGui.QVBoxLayout()
        self.vLayout1.setSpacing(5)
        self.vLayout1.setObjectName(_fromUtf8("vLayout1"))
        self.btnNew = QtGui.QPushButton(self.gBox2)
        self.btnNew.setMinimumSize(QtCore.QSize(80, 25))
        self.btnNew.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnNew.setObjectName(_fromUtf8("btnNew"))
        self.vLayout1.addWidget(self.btnNew)
        self.hLayout3 = QtGui.QHBoxLayout()
        self.hLayout3.setObjectName(_fromUtf8("hLayout3"))
        self.btnUp = QtGui.QPushButton(self.gBox2)
        self.btnUp.setMinimumSize(QtCore.QSize(35, 25))
        self.btnUp.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnUp.setObjectName(_fromUtf8("btnUp"))
        self.hLayout3.addWidget(self.btnUp)
        self.btnDown = QtGui.QPushButton(self.gBox2)
        self.btnDown.setMinimumSize(QtCore.QSize(35, 25))
        self.btnDown.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnDown.setObjectName(_fromUtf8("btnDown"))
        self.hLayout3.addWidget(self.btnDown)
        self.vLayout1.addLayout(self.hLayout3)
        self.btnEdit = QtGui.QPushButton(self.gBox2)
        self.btnEdit.setMinimumSize(QtCore.QSize(80, 25))
        self.btnEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.vLayout1.addWidget(self.btnEdit)
        self.btnRemove = QtGui.QPushButton(self.gBox2)
        self.btnRemove.setMinimumSize(QtCore.QSize(80, 25))
        self.btnRemove.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnRemove.setObjectName(_fromUtf8("btnRemove"))
        self.vLayout1.addWidget(self.btnRemove)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vLayout1.addItem(spacerItem1)
        self.hLayout2.addLayout(self.vLayout1)
        self.formLayout.addWidget(self.gBox2)
        self.gBox3 = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gBox3.sizePolicy().hasHeightForWidth())
        self.gBox3.setSizePolicy(sizePolicy)
        self.gBox3.setObjectName(_fromUtf8("gBox3"))
        self.vLayout2 = QtGui.QVBoxLayout(self.gBox3)
        self.vLayout2.setMargin(5)
        self.vLayout2.setSpacing(5)
        self.vLayout2.setObjectName(_fromUtf8("vLayout2"))
        self.cBoxExtra = QtGui.QCheckBox(self.gBox3)
        self.cBoxExtra.setMinimumSize(QtCore.QSize(0, 20))
        self.cBoxExtra.setMaximumSize(QtCore.QSize(16777215, 20))
        self.cBoxExtra.setObjectName(_fromUtf8("cBoxExtra"))
        self.vLayout2.addWidget(self.cBoxExtra)
        self.hLayout4 = QtGui.QHBoxLayout()
        self.hLayout4.setObjectName(_fromUtf8("hLayout4"))
        self.vLayout3 = QtGui.QVBoxLayout()
        self.vLayout3.setObjectName(_fromUtf8("vLayout3"))
        self.lblKeysAllowed = QtGui.QLabel(self.gBox3)
        self.lblKeysAllowed.setMinimumSize(QtCore.QSize(0, 20))
        self.lblKeysAllowed.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lblKeysAllowed.setObjectName(_fromUtf8("lblKeysAllowed"))
        self.vLayout3.addWidget(self.lblKeysAllowed)
        self.tBoxKeysAllowed = QtGui.QLineEdit(self.gBox3)
        self.tBoxKeysAllowed.setMinimumSize(QtCore.QSize(0, 25))
        self.tBoxKeysAllowed.setMaximumSize(QtCore.QSize(16777215, 25))
        self.tBoxKeysAllowed.setAutoFillBackground(True)
        self.tBoxKeysAllowed.setObjectName(_fromUtf8("tBoxKeysAllowed"))
        self.vLayout3.addWidget(self.tBoxKeysAllowed)
        self.hLayout4.addLayout(self.vLayout3)
        self.vLayout4 = QtGui.QVBoxLayout()
        self.vLayout4.setObjectName(_fromUtf8("vLayout4"))
        self.lblKeysCorrect = QtGui.QLabel(self.gBox3)
        self.lblKeysCorrect.setMinimumSize(QtCore.QSize(0, 20))
        self.lblKeysCorrect.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lblKeysCorrect.setObjectName(_fromUtf8("lblKeysCorrect"))
        self.vLayout4.addWidget(self.lblKeysCorrect)
        self.tBoxKeysCorrect = QtGui.QLineEdit(self.gBox3)
        self.tBoxKeysCorrect.setMinimumSize(QtCore.QSize(0, 25))
        self.tBoxKeysCorrect.setMaximumSize(QtCore.QSize(16777215, 25))
        self.tBoxKeysCorrect.setAutoFillBackground(True)
        self.tBoxKeysCorrect.setObjectName(_fromUtf8("tBoxKeysCorrect"))
        self.vLayout4.addWidget(self.tBoxKeysCorrect)
        self.hLayout4.addLayout(self.vLayout4)
        self.vLayout2.addLayout(self.hLayout4)
        self.hLayout5 = QtGui.QHBoxLayout()
        self.hLayout5.setObjectName(_fromUtf8("hLayout5"))
        self.lblImag = QtGui.QLabel(self.gBox3)
        self.lblImag.setMinimumSize(QtCore.QSize(80, 25))
        self.lblImag.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lblImag.setObjectName(_fromUtf8("lblImag"))
        self.hLayout5.addWidget(self.lblImag)
        self.tBoxImag = QtGui.QLineEdit(self.gBox3)
        self.tBoxImag.setReadOnly(True)
        self.tBoxImag.setMinimumSize(QtCore.QSize(0, 25))
        self.tBoxImag.setMaximumSize(QtCore.QSize(16777215, 25))
        self.tBoxImag.setAutoFillBackground(True)
        self.tBoxImag.setObjectName(_fromUtf8("tBoxImag"))
        self.hLayout5.addWidget(self.tBoxImag)
        self.btnImag = QtGui.QPushButton(self.gBox3)
        self.btnImag.setMinimumSize(QtCore.QSize(75, 25))
        self.btnImag.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnImag.setObjectName(_fromUtf8("btnImag"))
        self.hLayout5.addWidget(self.btnImag)
        self.vLayout2.addLayout(self.hLayout5)
        self.formLayout.addWidget(self.gBox3)
        self.hLayout6 = QtGui.QHBoxLayout()
        self.hLayout6.setObjectName(_fromUtf8("hLayout6"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayout6.addItem(spacerItem2)
        self.btnOk = QtGui.QPushButton(self)
        self.btnOk.setMinimumSize(QtCore.QSize(85, 25))
        self.btnOk.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnOk.setObjectName(_fromUtf8("btnOk"))
        self.hLayout6.addWidget(self.btnOk)
        self.btnCancel = QtGui.QPushButton(self)
        self.btnCancel.setMinimumSize(QtCore.QSize(85, 25))
        self.btnCancel.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.hLayout6.addWidget(self.btnCancel)
        self.formLayout.addLayout(self.hLayout6)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("formTestConfig", "Form", None))
        self.gBox1.setTitle(_translate("formTestConfig", "Test Name", None))
        self.gBox2.setTitle(_translate("formTestConfig", "Image list", None))
        self.btnNew.setText(_translate("formTestConfig", "New...", None))
        self.btnUp.setText(_translate("formTestConfig", "Up", None))
        self.btnDown.setText(_translate("formTestConfig", "Down", None))
        self.btnEdit.setText(_translate("formTestConfig", "Edit", None))
        self.btnRemove.setText(_translate("formTestConfig", "Remove", None))
        self.gBox3.setTitle(_translate("formTestConfig", "Optional", None))
        self.cBoxExtra.setText(_translate("formTestConfig", "This experiment require user input? (added at the end)", None))
        self.lblKeysAllowed.setText(_translate("formTestConfig", "Keys allowed:", None))
        self.lblKeysCorrect.setText(_translate("formTestConfig", "Correct answer:", None))
        self.lblImag.setText(_translate("formTestConfig", "Select image:", None))
        self.btnImag.setText(_translate("formTestConfig", "Open File", None))
        self.btnOk.setText(_translate("formTestConfig", "Ok", None))
        self.btnCancel.setText(_translate("formTestConfig", "Cancel", None))

    # =================================
    def initTable(self):
        self.tabVwImag.setModel(self.model)
        self.tabVwImag.setCurrentIndex(self.model.index(0, 0))
        # ==============
        self.tabVwImag.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Fixed)
        self.tabVwImag.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.tabVwImag.setColumnWidth(0, 230)
        self.tabVwImag.rowHeight(10)

    def setupActions(self):
        self.btnNew.clicked.connect(lambda: self.getImageItem(editMode=False))
        self.btnEdit.clicked.connect(lambda: self.getImageItem(editMode=True))
        self.btnRemove.clicked.connect(lambda: self.removeItem(table=self.tabVwImag))
        # ==============
        self.cBoxExtra.clicked.connect(self.handleCheckBox)
        # ==============
        self.btnUp.clicked.connect(lambda: self.moveItemUp(table=self.tabVwImag))
        self.btnDown.clicked.connect(lambda: self.moveItemDown(table=self.tabVwImag))
        # ==============
        self.btnImag.clicked.connect(self.getExtraImag)
        # ==============
        self.btnOk.clicked.connect(self.handleOkBtn)
        self.btnCancel.clicked.connect(self.handleCancelBtn)

    def checkIfNewTest(self):
        if self.itemId is not -1:
            print u'Test ID: %s. Getting data...' % self.itemId
            # ==============
            testName = self.parent.testModel.getItemById(self.itemId)
            testPath = self.parent.getFilePath(testName, isTest=self.isTest)
            testConf = testFileConf(testPath)
            # ==============
            self.tBoxTest.setText(testName)
            self.model.removeRows(0, 1) if testConf.imagData == [] else self.model.changeData(testConf.imagData)
            self.cBoxExtra.setChecked(testConf.extraFlag)
            self.tBoxImag.setText(testConf.extraImag)
            self.tBoxKeysAllowed.setText(u','.join(testConf.extraKeys))
            self.tBoxKeysCorrect.setText(testConf.extraCAns)
        else:
            print u'Test ID: None. No stored data!'
            self.model.removeRows(0, 1)
        self.handleCheckBox()

    # =================================
    def getExtraImag(self):
        imagPathOld = unicode(self.tBoxImag.text())
        if imagPathOld:
            basePath = os.path.split(imagPathOld)[0]
        else:
            basePath = u'.'
        # ==============
        imagPathNew = QtGui.QFileDialog.getOpenFileName(self, u'Open File', basePath, u'Images (*.png *.jpeg *.jpg)')
        # ==============
        if imagPathNew:
            self.tBoxImag.setText(unicode(imagPathNew))
        else:
            print u'No file selected or operation cancelled!'

    def getImageItem(self, editMode=False):
        if editMode:
            itemTotal = self.model.rowCount()
            itemIndex = self.tabVwImag.currentIndex().row()
            # ==============
            if itemTotal is not 0 and itemIndex is not -1:
                print u'Modifying item...'
                dialog = diagImageSelect(self, itemIdx=itemIndex)
                dialog.exec_()
            else:
                print u'No item selected/available!'
        else:
            print u'New item...'
            dialog = diagImageSelect(self, itemIdx=None)
            dialog.exec_()

    def handleCheckBox(self):
        if self.cBoxExtra.isChecked():
            self.btnImag.setEnabled(True)
            self.tBoxKeysCorrect.setEnabled(True)
            self.tBoxKeysAllowed.setEnabled(True)
        else:
            self.btnImag.setEnabled(False)
            self.tBoxKeysCorrect.setEnabled(False)
            self.tBoxKeysAllowed.setEnabled(False)

    def handleOkBtn(self):
        print u'Ok button pressed...'
        # ==============
        testConf = testFileConf()
        testConf.imagData = self.model.tableData
        testConf.extraFlag = self.cBoxExtra.isChecked()
        testConf.extraImag = unicode(self.tBoxImag.text())
        testConf.extraKeys = unicode(self.tBoxKeysAllowed.text()).split(u',')
        testConf.extraCAns = unicode(self.tBoxKeysCorrect.text())
        # ==============
        if self.saveItem(itemName=self.tBoxTest.text(), confData=testConf):
            print u'Filename accepted...'
        else:
            print u'No name inserted or operation cancelled!'


# =============================================== Experiments
class formExperimentConfig(formTable):
    def __init__(self, parent, itemId=-1):
        formTable.__init__(self, parent=parent, itemId=itemId, isTest=False,
                           modelData=[[u'Empty', 0]], modelHeaders=[u'Test', u'Reps [#]'])
        self.setupUi()
        self.setupActions()
        self.checkIfNewExps()
        # ==============
        self.initTable()

    # =================================
    def setupUi(self):
        self.setObjectName(_fromUtf8("formExperimentConfig"))
        self.resize(490, 450)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(490, 450))
        self.setMaximumSize(QtCore.QSize(490, 450))
        self.formLayout = QtGui.QVBoxLayout(self)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.gBox1 = QtGui.QGroupBox(self)
        self.gBox1.setObjectName(_fromUtf8("gBox1"))
        self.hLayout1 = QtGui.QHBoxLayout(self.gBox1)
        self.hLayout1.setMargin(5)
        self.hLayout1.setSpacing(5)
        self.hLayout1.setObjectName(_fromUtf8("hLayout1"))
        self.tBoxExps = QtGui.QLineEdit(self.gBox1)
        self.tBoxExps.setMinimumSize(QtCore.QSize(300, 25))
        self.tBoxExps.setMaximumSize(QtCore.QSize(16777215, 25))
        self.tBoxExps.setAutoFillBackground(True)
        self.tBoxExps.setObjectName(_fromUtf8("tBoxExps"))
        self.hLayout1.addWidget(self.tBoxExps)
        spacerItem = QtGui.QSpacerItem(146, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayout1.addItem(spacerItem)
        self.formLayout.addWidget(self.gBox1)
        self.gBox2 = QtGui.QGroupBox(self)
        self.gBox2.setMinimumSize(QtCore.QSize(0, 0))
        self.gBox2.setObjectName(_fromUtf8("gBox2"))
        self.hLayout2 = QtGui.QHBoxLayout(self.gBox2)
        self.hLayout2.setMargin(5)
        self.hLayout2.setSpacing(5)
        self.hLayout2.setObjectName(_fromUtf8("hLayout2"))
        self.tabVwTest = QtGui.QTableView(self.gBox2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabVwTest.sizePolicy().hasHeightForWidth())
        self.tabVwTest.setSizePolicy(sizePolicy)
        self.tabVwTest.setMinimumSize(QtCore.QSize(320, 0))
        self.tabVwTest.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tabVwTest.setObjectName(_fromUtf8("tabVwTest"))
        self.hLayout2.addWidget(self.tabVwTest)
        self.vLayout1 = QtGui.QVBoxLayout()
        self.vLayout1.setSpacing(5)
        self.vLayout1.setObjectName(_fromUtf8("vLayout1"))
        self.btnNew = QtGui.QPushButton(self.gBox2)
        self.btnNew.setMinimumSize(QtCore.QSize(80, 25))
        self.btnNew.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnNew.setObjectName(_fromUtf8("btnNew"))
        self.vLayout1.addWidget(self.btnNew)
        self.hLayout3 = QtGui.QHBoxLayout()
        self.hLayout3.setObjectName(_fromUtf8("hLayout3"))
        self.btnUp = QtGui.QPushButton(self.gBox2)
        self.btnUp.setMinimumSize(QtCore.QSize(35, 25))
        self.btnUp.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnUp.setObjectName(_fromUtf8("btnUp"))
        self.hLayout3.addWidget(self.btnUp)
        self.btnDown = QtGui.QPushButton(self.gBox2)
        self.btnDown.setMinimumSize(QtCore.QSize(35, 25))
        self.btnDown.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnDown.setObjectName(_fromUtf8("btnDown"))
        self.hLayout3.addWidget(self.btnDown)
        self.vLayout1.addLayout(self.hLayout3)
        self.btnEdit = QtGui.QPushButton(self.gBox2)
        self.btnEdit.setMinimumSize(QtCore.QSize(80, 25))
        self.btnEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.vLayout1.addWidget(self.btnEdit)
        self.btnRemove = QtGui.QPushButton(self.gBox2)
        self.btnRemove.setMinimumSize(QtCore.QSize(80, 25))
        self.btnRemove.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnRemove.setObjectName(_fromUtf8("btnRemove"))
        self.vLayout1.addWidget(self.btnRemove)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vLayout1.addItem(spacerItem1)
        self.hLayout2.addLayout(self.vLayout1)
        self.formLayout.addWidget(self.gBox2)
        self.gBox3 = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gBox3.sizePolicy().hasHeightForWidth())
        self.gBox3.setSizePolicy(sizePolicy)
        self.gBox3.setObjectName(_fromUtf8("gBox3"))
        self.hLayout4 = QtGui.QHBoxLayout(self.gBox3)
        self.hLayout4.setMargin(5)
        self.hLayout4.setSpacing(5)
        self.hLayout4.setObjectName(_fromUtf8("hLayout4"))
        self.rBtnRand = QtGui.QRadioButton(self.gBox3)
        self.rBtnRand.setMinimumSize(QtCore.QSize(0, 20))
        self.rBtnRand.setMaximumSize(QtCore.QSize(16777215, 20))
        self.rBtnRand.setChecked(True)
        self.rBtnRand.setObjectName(_fromUtf8("rBtnRand"))
        self.hLayout4.addWidget(self.rBtnRand)
        self.rBtnOrdr = QtGui.QRadioButton(self.gBox3)
        self.rBtnOrdr.setMinimumSize(QtCore.QSize(0, 20))
        self.rBtnOrdr.setMaximumSize(QtCore.QSize(16777215, 20))
        self.rBtnOrdr.setChecked(False)
        self.rBtnOrdr.setObjectName(_fromUtf8("rBtnOrdr"))
        self.hLayout4.addWidget(self.rBtnOrdr)
        self.formLayout.addWidget(self.gBox3)
        self.gBox4 = QtGui.QGroupBox(self)
        self.gBox4.setObjectName(_fromUtf8("gBox4"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gBox4)
        self.verticalLayout.setMargin(5)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cBoxRest = QtGui.QCheckBox(self.gBox4)
        self.cBoxRest.setMinimumSize(QtCore.QSize(0, 20))
        self.cBoxRest.setMaximumSize(QtCore.QSize(16777215, 20))
        self.cBoxRest.setObjectName(_fromUtf8("cBoxRest"))
        self.verticalLayout.addWidget(self.cBoxRest)
        self.hLayout5 = QtGui.QHBoxLayout()
        self.hLayout5.setSpacing(5)
        self.hLayout5.setObjectName(_fromUtf8("hLayout5"))
        self.vLayout2 = QtGui.QVBoxLayout()
        self.vLayout2.setObjectName(_fromUtf8("vLayout2"))
        self.lblNumRest = QtGui.QLabel(self.gBox4)
        self.lblNumRest.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lblNumRest.setObjectName(_fromUtf8("lblNumRest"))
        self.vLayout2.addWidget(self.lblNumRest)
        self.iBoxNumRest = QtGui.QSpinBox(self.gBox4)
        self.iBoxNumRest.setMinimumSize(QtCore.QSize(0, 25))
        self.iBoxNumRest.setMaximumSize(QtCore.QSize(16777215, 25))
        self.iBoxNumRest.setAutoFillBackground(True)
        self.iBoxNumRest.setMaximum(9999)
        self.iBoxNumRest.setObjectName(_fromUtf8("iBoxNumRest"))
        self.vLayout2.addWidget(self.iBoxNumRest)
        self.hLayout5.addLayout(self.vLayout2)
        self.vLayout3 = QtGui.QVBoxLayout()
        self.vLayout3.setObjectName(_fromUtf8("vLayout3"))
        self.lblTimeRest = QtGui.QLabel(self.gBox4)
        self.lblTimeRest.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lblTimeRest.setObjectName(_fromUtf8("lblTimeRest"))
        self.vLayout3.addWidget(self.lblTimeRest)
        self.dBoxTimeRest = QtGui.QDoubleSpinBox(self.gBox4)
        self.dBoxTimeRest.setMinimumSize(QtCore.QSize(0, 25))
        self.dBoxTimeRest.setMaximumSize(QtCore.QSize(16777215, 25))
        self.dBoxTimeRest.setAutoFillBackground(True)
        self.dBoxTimeRest.setDecimals(3)
        self.dBoxTimeRest.setMaximum(9999.0)
        self.dBoxTimeRest.setSingleStep(0.01)
        self.dBoxTimeRest.setObjectName(_fromUtf8("dBoxTimeRest"))
        self.vLayout3.addWidget(self.dBoxTimeRest)
        self.hLayout5.addLayout(self.vLayout3)
        self.verticalLayout.addLayout(self.hLayout5)
        self.formLayout.addWidget(self.gBox4)
        self.hLayout6 = QtGui.QHBoxLayout()
        self.hLayout6.setObjectName(_fromUtf8("hLayout6"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayout6.addItem(spacerItem2)
        self.btnOk = QtGui.QPushButton(self)
        self.btnOk.setMinimumSize(QtCore.QSize(85, 25))
        self.btnOk.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnOk.setObjectName(_fromUtf8("btnOk"))
        self.hLayout6.addWidget(self.btnOk)
        self.btnCancel = QtGui.QPushButton(self)
        self.btnCancel.setMinimumSize(QtCore.QSize(85, 25))
        self.btnCancel.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.hLayout6.addWidget(self.btnCancel)
        self.formLayout.addLayout(self.hLayout6)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("formExperimentConfig", "Form", None))
        self.gBox1.setTitle(_translate("formExperimentConfig", "Experiment Name", None))
        self.gBox2.setTitle(_translate("formExperimentConfig", "Test list", None))
        self.btnNew.setText(_translate("formExperimentConfig", "New...", None))
        self.btnUp.setText(_translate("formExperimentConfig", "Up", None))
        self.btnDown.setText(_translate("formExperimentConfig", "Down", None))
        self.btnEdit.setText(_translate("formExperimentConfig", "Edit", None))
        self.btnRemove.setText(_translate("formExperimentConfig", "Remove", None))
        self.gBox3.setTitle(_translate("formExperimentConfig", "Presentation order", None))
        self.rBtnRand.setText(_translate("formExperimentConfig", "Random", None))
        self.rBtnOrdr.setText(_translate("formExperimentConfig", "Sequential (as list)", None))
        self.gBox4.setTitle(_translate("formExperimentConfig", "Resting", None))
        self.cBoxRest.setText(_translate("formExperimentConfig", "Include resting time?", None))
        self.lblNumRest.setText(_translate("formExperimentConfig", "# of tests to rest:", None))
        self.lblTimeRest.setText(_translate("formExperimentConfig", "Rest time [s]:", None))
        self.btnOk.setText(_translate("formExperimentConfig", "Ok", None))
        self.btnCancel.setText(_translate("formExperimentConfig", "Cancel", None))

    # =================================
    def initTable(self):
        self.tabVwTest.setModel(self.model)
        self.tabVwTest.setCurrentIndex(self.model.index(0, 0))
        # ==============
        self.tabVwTest.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Fixed)
        self.tabVwTest.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.tabVwTest.setColumnWidth(0, 230)
        self.tabVwTest.rowHeight(10)

    def setupActions(self):
        self.btnNew.clicked.connect(lambda: self.getTestItem(editMode=False))
        self.btnEdit.clicked.connect(lambda: self.getTestItem(editMode=True))
        self.btnRemove.clicked.connect(lambda: self.removeItem(table=self.tabVwTest))
        # ==============
        self.cBoxRest.clicked.connect(self.handleCheckBox)
        self.rBtnRand.clicked.connect(self.mergeIdenticalItemRows)
        # ==============
        self.btnUp.clicked.connect(lambda: self.moveItemUp(table=self.tabVwTest))
        self.btnDown.clicked.connect(lambda: self.moveItemDown(table=self.tabVwTest))
        # ==============
        self.btnOk.clicked.connect(self.handleOkBtn)
        self.btnCancel.clicked.connect(self.handleCancelBtn)

    def checkIfNewExps(self):
        if self.itemId is not -1:
            print u'Exps ID: %s. Getting data...' % self.itemId
            # ==============
            expsName = self.parent.expsModel.getItemById(self.itemId)
            expsPath = self.parent.getFilePath(expsName, isTest=self.isTest)
            expsConf = expsFileConf(expsPath)
            # ==============
            self.tBoxExps.setText(expsName)
            self.model.removeRows(0, 1) if expsConf.testData == [] else self.model.changeData(expsConf.testData)
            self.rBtnRand.setChecked(True) if expsConf.randFlag else self.rBtnOrdr.setChecked(True)
            self.cBoxRest.setChecked(expsConf.restFlag)
            self.iBoxNumRest.setValue(expsConf.restTest)
            self.dBoxTimeRest.setValue(expsConf.restTime)
        else:
            print u'Exps ID: None. No stored data!'
            self.model.removeRows(0, 1)
        self.handleCheckBox()

    # =================================
    def getTestItem(self, editMode=False):
        if editMode:
            itemTotal = self.model.rowCount()
            itemIndex = self.tabVwTest.currentIndex().row()
            # ==============
            if itemTotal is not 0 and itemIndex is not -1:
                print u'Modifying item...'
                dialog = diagTestSelect(self, itemIdx=itemIndex)
                dialog.exec_()
            else:
                print u'No item selected/available!'
        else:
            print u'New item...'
            dialog = diagTestSelect(self, itemIdx=None)
            dialog.exec_()

    def handleCheckBox(self):
        if self.cBoxRest.isChecked():
            self.iBoxNumRest.setEnabled(True)
            self.dBoxTimeRest.setEnabled(True)
        else:
            self.iBoxNumRest.setEnabled(False)
            self.dBoxTimeRest.setEnabled(False)

    def mergeIdenticalItemRows(self):
        auxList = []
        auxTable = []
        for item in self.model.tableData:
            if not (item[0] in auxList):
                auxList.append(item[0])
                auxTable.append(item)
            else:
                itemIndex = auxList.index(item[0])
                auxTable[itemIndex][1] += item[1]
        self.model.tableData = auxTable
        self.model.reset()

    def handleOkBtn(self):
        print u'Ok button pressed...'
        # ==============
        expsConf = expsFileConf()
        expsConf.testData = self.model.tableData
        expsConf.randFlag = self.rBtnRand.isChecked()
        expsConf.restFlag = self.cBoxRest.isChecked()
        expsConf.restTime = self.dBoxTimeRest.value()
        expsConf.restTest = self.iBoxNumRest.value()
        # ==============
        if self.saveItem(itemName=self.tBoxExps.text(), confData=expsConf):
            print u'Filename accepted...'
        else:
            print u'No name inserted or operation cancelled!'

# =============================================================================
# GUI: Dialogs
# =============================================================================
# =============================================== Tests
class diagImageSelect(QtGui.QDialog):
    def __init__(self, parent, itemIdx=None):
        QtGui.QDialog.__init__(self)
        # ==============
        self.imagIndex = itemIdx
        self.parent = parent
        # ==============
        self.setupUi()
        self.setupActions()
        self.setConfigData()

    # =================================
    def setupUi(self):
        self.setObjectName(_fromUtf8("diagImageSelect"))
        self.resize(400, 150)
        self.setMinimumSize(QtCore.QSize(300, 150))
        self.setMaximumSize(QtCore.QSize(400, 200))
        self.setModal(True)
        self.formLayout = QtGui.QVBoxLayout(self)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.gBox = QtGui.QGroupBox(self)
        self.gBox.setTitle(_fromUtf8(""))
        self.gBox.setObjectName(_fromUtf8("gBox"))
        self.vLayout = QtGui.QVBoxLayout(self.gBox)
        self.vLayout.setContentsMargins(5, 0, 5, 5)
        self.vLayout.setSpacing(5)
        self.vLayout.setObjectName(_fromUtf8("vLayout"))
        self.hLayout2 = QtGui.QHBoxLayout()
        self.hLayout2.setSpacing(6)
        self.hLayout2.setObjectName(_fromUtf8("hLayout2"))
        self.lblImag = QtGui.QLabel(self.gBox)
        self.lblImag.setMinimumSize(QtCore.QSize(80, 25))
        self.lblImag.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lblImag.setObjectName(_fromUtf8("lblImag"))
        self.hLayout2.addWidget(self.lblImag)
        self.tBoxImag = QtGui.QLineEdit(self.gBox)
        self.tBoxImag.setReadOnly(True)
        self.tBoxImag.setMinimumSize(QtCore.QSize(0, 25))
        self.tBoxImag.setMaximumSize(QtCore.QSize(16777215, 25))
        self.tBoxImag.setAutoFillBackground(True)
        self.tBoxImag.setObjectName(_fromUtf8("tBoxImag"))
        self.hLayout2.addWidget(self.tBoxImag)
        self.btnImag = QtGui.QPushButton(self.gBox)
        self.btnImag.setMinimumSize(QtCore.QSize(75, 25))
        self.btnImag.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnImag.setObjectName(_fromUtf8("btnImag"))
        self.hLayout2.addWidget(self.btnImag)
        self.vLayout.addLayout(self.hLayout2)
        self.hLayout1 = QtGui.QHBoxLayout()
        self.hLayout1.setObjectName(_fromUtf8("hLayout1"))
        self.lblTime = QtGui.QLabel(self.gBox)
        self.lblTime.setMinimumSize(QtCore.QSize(80, 25))
        self.lblTime.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lblTime.setObjectName(_fromUtf8("lblTime"))
        self.hLayout1.addWidget(self.lblTime)
        self.dBoxTime = QtGui.QDoubleSpinBox(self.gBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dBoxTime.sizePolicy().hasHeightForWidth())
        self.dBoxTime.setSizePolicy(sizePolicy)
        self.dBoxTime.setMinimumSize(QtCore.QSize(0, 25))
        self.dBoxTime.setMaximumSize(QtCore.QSize(16777215, 25))
        self.dBoxTime.setAutoFillBackground(True)
        self.dBoxTime.setDecimals(3)
        self.dBoxTime.setMaximum(9999.0)
        self.dBoxTime.setSingleStep(0.01)
        self.dBoxTime.setObjectName(_fromUtf8("dBoxTime"))
        self.hLayout1.addWidget(self.dBoxTime)
        self.vLayout.addLayout(self.hLayout1)
        self.formLayout.addWidget(self.gBox)
        self.hLayout3 = QtGui.QHBoxLayout()
        self.hLayout3.setObjectName(_fromUtf8("hLayout3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayout3.addItem(spacerItem)
        self.btnOk = QtGui.QPushButton(self)
        self.btnOk.setMinimumSize(QtCore.QSize(0, 25))
        self.btnOk.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnOk.setObjectName(_fromUtf8("btnOk"))
        self.hLayout3.addWidget(self.btnOk)
        self.btnCancel = QtGui.QPushButton(self)
        self.btnCancel.setMinimumSize(QtCore.QSize(0, 25))
        self.btnCancel.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.hLayout3.addWidget(self.btnCancel)
        self.formLayout.addLayout(self.hLayout3)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("diagImageSelect", "Image Selection", None))
        self.lblImag.setText(_translate("diagImageSelect", "Select image:", None))
        self.btnImag.setText(_translate("diagImageSelect", "Open File", None))
        self.lblTime.setText(_translate("diagImageSelect", "Time [s]:", None))
        self.btnOk.setText(_translate("diagImageSelect", "Ok", None))
        self.btnCancel.setText(_translate("diagImageSelect", "Cancel", None))

    # =================================
    def setupActions(self):
        self.btnImag.clicked.connect(self.loadImage)
        self.btnOk.clicked.connect(self.handleOkButton)
        self.btnCancel.clicked.connect(self.handleCancelButton)

    def setConfigData(self):
        if self.imagIndex is not None:
            print u'Modify Image...'
            imagData = self.parent.testModel.getItemById(self.imagIndex)
            self.tBoxImag.setText(imagData[0])
            self.dBoxTime.setValue(imagData[1])
        else:
            print u'New Image...'

    def loadImage(self):
        imagPathOld = unicode(self.tBoxImag.text())
        if imagPathOld:
            basePath = os.path.split(imagPathOld)[0]
        else:
            basePath = u'.'
        # ==============
        imagPathNew = QtGui.QFileDialog.getOpenFileName(self, u'Open File', basePath, u'Images (*.png *.jpeg *.jpg)')
        # ==============
        if imagPathNew:
            self.tBoxImag.setText(unicode(imagPathNew))
        else:
            print u'No file selected or operation cancelled!'

    def handleOkButton(self):
        print u'Ok button pressed...'
        # ==============
        imagPath = self.tBoxImag.text()
        imagTime = self.dBoxTime.value()
        # ==============
        if imagPath is not u'' and imagTime > 0:
            if self.imagIndex is not None:
                print u'Updating item...'
                self.parent.testModel.changeValue(self.imagIndex, [imagPath, imagTime])
            else:
                print u'Adding new item...'
                self.parent.testModel.addNewValue([imagPath, imagTime])
            # ==============
            self.close()
        else:
            QtGui.QMessageBox.warning(self, u'Cannot add the image', u'There is no image selected\nor the time is too low.')

    def handleCancelButton(self):
        print u'Cancel button pressed...'
        self.close()


# =============================================== Experiments
class diagTestSelect(QtGui.QDialog):
    def __init__(self, parent, itemIdx=None):
        QtGui.QDialog.__init__(self)
        # ==============
        self.testIndex = itemIdx
        self.parent = parent
        self.mainParent = self.parent.parent
        # ==============
        self.setupUi()
        self.setupActions()
        self.setConfigData()
        # ==============
        self.initComboBox()

    # =================================
    def setupUi(self):
        self.setObjectName(_fromUtf8("diagTestSelect"))
        self.resize(400, 150)
        self.setMinimumSize(QtCore.QSize(300, 150))
        self.setMaximumSize(QtCore.QSize(400, 200))
        self.setModal(True)
        self.formLayout = QtGui.QVBoxLayout(self)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.gBox = QtGui.QGroupBox(self)
        self.gBox.setTitle(_fromUtf8(""))
        self.gBox.setObjectName(_fromUtf8("gBox"))
        self.vLayout = QtGui.QVBoxLayout(self.gBox)
        self.vLayout.setContentsMargins(5, 0, 5, 5)
        self.vLayout.setSpacing(5)
        self.vLayout.setObjectName(_fromUtf8("vLayout"))
        self.hLayout1 = QtGui.QHBoxLayout()
        self.hLayout1.setObjectName(_fromUtf8("hLayout1"))
        self.lblTest = QtGui.QLabel(self.gBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTest.sizePolicy().hasHeightForWidth())
        self.lblTest.setSizePolicy(sizePolicy)
        self.lblTest.setMinimumSize(QtCore.QSize(80, 25))
        self.lblTest.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lblTest.setObjectName(_fromUtf8("lblTest"))
        self.hLayout1.addWidget(self.lblTest)
        self.cBoxTest = QtGui.QComboBox(self.gBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cBoxTest.sizePolicy().hasHeightForWidth())
        self.cBoxTest.setSizePolicy(sizePolicy)
        self.cBoxTest.setMinimumSize(QtCore.QSize(0, 25))
        self.cBoxTest.setMaximumSize(QtCore.QSize(16777215, 25))
        self.cBoxTest.setAutoFillBackground(True)
        self.cBoxTest.setObjectName(_fromUtf8("cBoxTest"))
        self.hLayout1.addWidget(self.cBoxTest)
        self.vLayout.addLayout(self.hLayout1)
        self.hLayout2 = QtGui.QHBoxLayout()
        self.hLayout2.setObjectName(_fromUtf8("hLayout2"))
        self.lblReps = QtGui.QLabel(self.gBox)
        self.lblReps.setMinimumSize(QtCore.QSize(80, 25))
        self.lblReps.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lblReps.setObjectName(_fromUtf8("lblReps"))
        self.hLayout2.addWidget(self.lblReps)
        self.iBoxReps = QtGui.QSpinBox(self.gBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iBoxReps.sizePolicy().hasHeightForWidth())
        self.iBoxReps.setSizePolicy(sizePolicy)
        self.iBoxReps.setMinimumSize(QtCore.QSize(0, 25))
        self.iBoxReps.setMaximumSize(QtCore.QSize(16777215, 25))
        self.iBoxReps.setAutoFillBackground(True)
        self.iBoxReps.setMaximum(9999)
        self.iBoxReps.setObjectName(_fromUtf8("iBoxReps"))
        self.hLayout2.addWidget(self.iBoxReps)
        self.vLayout.addLayout(self.hLayout2)
        self.formLayout.addWidget(self.gBox)
        self.hLayout3 = QtGui.QHBoxLayout()
        self.hLayout3.setObjectName(_fromUtf8("hLayout3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayout3.addItem(spacerItem)
        self.btnOk = QtGui.QPushButton(self)
        self.btnOk.setMinimumSize(QtCore.QSize(0, 25))
        self.btnOk.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnOk.setObjectName(_fromUtf8("btnOk"))
        self.hLayout3.addWidget(self.btnOk)
        self.btnCancel = QtGui.QPushButton(self)
        self.btnCancel.setMinimumSize(QtCore.QSize(0, 25))
        self.btnCancel.setMaximumSize(QtCore.QSize(16777215, 25))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.hLayout3.addWidget(self.btnCancel)
        self.formLayout.addLayout(self.hLayout3)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("diagTestSelect", "Test Selection", None))
        self.lblTest.setText(_translate("diagTestSelect", "Select test:", None))
        self.lblReps.setText(_translate("diagTestSelect", "# Repetitions:", None))
        self.btnOk.setText(_translate("diagTestSelect", "Ok", None))
        self.btnCancel.setText(_translate("diagTestSelect", "Cancel", None))

    # =================================
    def initComboBox(self):
        self.cBoxTest.setModel(self.mainParent.testModel)
        self.cBoxTest.show()

    def setupActions(self):
        self.btnOk.clicked.connect(self.handleOkButton)
        self.btnCancel.clicked.connect(self.handleCancelButton)

    def setConfigData(self):
        if self.testIndex is not None:
            print u'Modify test...'
            testData = self.parent.model.getItemById(self.testIndex)
            self.cBoxTest.setCurrentIndex(self.mainParent.testModel.getIdByItem(testData[0]))
            self.iBoxReps.setValue(testData[1])
        else:
            print u'New test...'

    def handleOkButton(self):
        print u'Ok button pressed...'
        # ==============
        testName = self.mainParent.testModel.getItemById(self.cBoxTest.currentIndex())
        testReps = self.iBoxReps.value()
        # ==============
        if testName is not u'' and testReps > 0:
            if self.testIndex is not None:
                print u'Updating item...'
                self.parent.model.changeValue(self.testIndex, [testName, testReps])
            else:
                tests = [item[0] for item in self.parent.model.tableData]
                if self.parent.rBtnRand.isChecked() and testName in tests:
                    print u'Updating item...'
                    selIndex = self.parent.model.getIdByItem(testName)
                    self.parent.model.tableData[selIndex][1] += testReps
                else:
                    print u'Adding new item...'
                    self.parent.model.addNewValue([testName, testReps])
            # ==============
            self.close()
        else:
            QtGui.QMessageBox.warning(self, u'Cannot add the test', u'The reps are too low.')

    def handleCancelButton(self):
        print u'Cancel button pressed...'
        self.close()
