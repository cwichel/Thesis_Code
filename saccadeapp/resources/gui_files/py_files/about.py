# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files\about.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_dlg_about(object):
    def setupUi(self, dlg_about):
        dlg_about.setObjectName(_fromUtf8("dlg_about"))
        dlg_about.resize(283, 256)
        self.verticalLayout_2 = QtGui.QVBoxLayout(dlg_about)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.lbl_app_name = QtGui.QLabel(dlg_about)
        self.lbl_app_name.setMinimumSize(QtCore.QSize(0, 50))
        self.lbl_app_name.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_app_name.setFont(font)
        self.lbl_app_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_app_name.setObjectName(_fromUtf8("lbl_app_name"))
        self.verticalLayout_2.addWidget(self.lbl_app_name)
        self.lbl_app_version = QtGui.QLabel(dlg_about)
        self.lbl_app_version.setMinimumSize(QtCore.QSize(0, 25))
        self.lbl_app_version.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_app_version.setFont(font)
        self.lbl_app_version.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_app_version.setObjectName(_fromUtf8("lbl_app_version"))
        self.verticalLayout_2.addWidget(self.lbl_app_version)
        self.line = QtGui.QFrame(dlg_about)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_2.addWidget(self.line)
        self.hly_01 = QtGui.QHBoxLayout()
        self.hly_01.setSpacing(5)
        self.hly_01.setObjectName(_fromUtf8("hly_01"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hly_01.addItem(spacerItem1)
        self.fly_01 = QtGui.QFormLayout()
        self.fly_01.setHorizontalSpacing(3)
        self.fly_01.setVerticalSpacing(5)
        self.fly_01.setObjectName(_fromUtf8("fly_01"))
        self.lbl_author = QtGui.QLabel(dlg_about)
        self.lbl_author.setMinimumSize(QtCore.QSize(40, 20))
        self.lbl_author.setMaximumSize(QtCore.QSize(40, 20))
        self.lbl_author.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_author.setObjectName(_fromUtf8("lbl_author"))
        self.fly_01.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_author)
        self.lbl_author_dat = QtGui.QLabel(dlg_about)
        self.lbl_author_dat.setMinimumSize(QtCore.QSize(0, 20))
        self.lbl_author_dat.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lbl_author_dat.setObjectName(_fromUtf8("lbl_author_dat"))
        self.fly_01.setWidget(0, QtGui.QFormLayout.FieldRole, self.lbl_author_dat)
        self.lbl_mail = QtGui.QLabel(dlg_about)
        self.lbl_mail.setMinimumSize(QtCore.QSize(40, 20))
        self.lbl_mail.setMaximumSize(QtCore.QSize(40, 20))
        self.lbl_mail.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_mail.setObjectName(_fromUtf8("lbl_mail"))
        self.fly_01.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_mail)
        self.lbl_mail_dat = QtGui.QLabel(dlg_about)
        self.lbl_mail_dat.setMinimumSize(QtCore.QSize(0, 20))
        self.lbl_mail_dat.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lbl_mail_dat.setObjectName(_fromUtf8("lbl_mail_dat"))
        self.fly_01.setWidget(1, QtGui.QFormLayout.FieldRole, self.lbl_mail_dat)
        self.hly_01.addLayout(self.fly_01)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hly_01.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.hly_01)
        self.bbt_close = QtGui.QDialogButtonBox(dlg_about)
        self.bbt_close.setOrientation(QtCore.Qt.Horizontal)
        self.bbt_close.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.bbt_close.setCenterButtons(True)
        self.bbt_close.setObjectName(_fromUtf8("bbt_close"))
        self.verticalLayout_2.addWidget(self.bbt_close)

        self.retranslateUi(dlg_about)
        QtCore.QObject.connect(self.bbt_close, QtCore.SIGNAL(_fromUtf8("accepted()")), dlg_about.accept)
        QtCore.QObject.connect(self.bbt_close, QtCore.SIGNAL(_fromUtf8("rejected()")), dlg_about.reject)
        QtCore.QMetaObject.connectSlotsByName(dlg_about)

    def retranslateUi(self, dlg_about):
        dlg_about.setWindowTitle(_translate("dlg_about", "About", None))
        self.lbl_app_name.setText(_translate("dlg_about", "saccadeapp", None))
        self.lbl_app_version.setText(_translate("dlg_about", "v1.0", None))
        self.lbl_author.setText(_translate("dlg_about", "Author:", None))
        self.lbl_author_dat.setText(_translate("dlg_about", "Christian Wiche", None))
        self.lbl_mail.setText(_translate("dlg_about", "Mail:", None))
        self.lbl_mail_dat.setText(_translate("dlg_about", "cwichel@gmail.com", None))

