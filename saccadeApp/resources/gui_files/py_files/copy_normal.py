# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files\copy_normal.ui'
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

class Ui_dlg_copy(object):
    def setupUi(self, dlg_copy):
        dlg_copy.setObjectName(_fromUtf8("dlg_copy"))
        dlg_copy.resize(400, 115)
        dlg_copy.setMinimumSize(QtCore.QSize(400, 115))
        dlg_copy.setMaximumSize(QtCore.QSize(400, 115))
        self.verticalLayout = QtGui.QVBoxLayout(dlg_copy)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbx_copy = QtGui.QGroupBox(dlg_copy)
        self.gbx_copy.setObjectName(_fromUtf8("gbx_copy"))
        self.formLayout = QtGui.QFormLayout(self.gbx_copy)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lbl_name = QtGui.QLabel(self.gbx_copy)
        self.lbl_name.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_name.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_name.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_name.setObjectName(_fromUtf8("lbl_name"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_name)
        self.led_name = QtGui.QLineEdit(self.gbx_copy)
        self.led_name.setMinimumSize(QtCore.QSize(0, 25))
        self.led_name.setMaximumSize(QtCore.QSize(16777215, 25))
        self.led_name.setObjectName(_fromUtf8("led_name"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.led_name)
        self.verticalLayout.addWidget(self.gbx_copy)
        self.bbt_dialog = QtGui.QDialogButtonBox(dlg_copy)
        self.bbt_dialog.setOrientation(QtCore.Qt.Horizontal)
        self.bbt_dialog.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbt_dialog.setObjectName(_fromUtf8("bbt_dialog"))
        self.verticalLayout.addWidget(self.bbt_dialog)

        self.retranslateUi(dlg_copy)
        QtCore.QObject.connect(self.bbt_dialog, QtCore.SIGNAL(_fromUtf8("accepted()")), dlg_copy.accept)
        QtCore.QObject.connect(self.bbt_dialog, QtCore.SIGNAL(_fromUtf8("rejected()")), dlg_copy.reject)
        QtCore.QMetaObject.connectSlotsByName(dlg_copy)

    def retranslateUi(self, dlg_copy):
        dlg_copy.setWindowTitle(_translate("dlg_copy", "Copy", None))
        self.gbx_copy.setTitle(_translate("dlg_copy", "Copy", None))
        self.lbl_name.setText(_translate("dlg_copy", "New Name:", None))

