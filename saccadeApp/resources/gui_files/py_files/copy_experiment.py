# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files\copy_experiment.ui'
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

class Ui_dlg_experiment_copy(object):
    def setupUi(self):
        self.setObjectName(_fromUtf8("dlg_experiment_copy"))
        self.resize(400, 140)
        self.setMinimumSize(QtCore.QSize(400, 140))
        self.setMaximumSize(QtCore.QSize(400, 140))
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbx_copy = QtGui.QGroupBox(self)
        self.gbx_copy.setObjectName(_fromUtf8("gbx_copy"))
        self.formLayout = QtGui.QFormLayout(self.gbx_copy)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lbl_code = QtGui.QLabel(self.gbx_copy)
        self.lbl_code.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_code.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_code.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_code.setObjectName(_fromUtf8("lbl_code"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_code)
        self.led_code = QtGui.QLineEdit(self.gbx_copy)
        self.led_code.setMinimumSize(QtCore.QSize(0, 25))
        self.led_code.setMaximumSize(QtCore.QSize(16777215, 25))
        self.led_code.setMaxLength(10)
        self.led_code.setObjectName(_fromUtf8("led_code"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.led_code)
        self.lbl_version = QtGui.QLabel(self.gbx_copy)
        self.lbl_version.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_version.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_version.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_version.setObjectName(_fromUtf8("lbl_version"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_version)
        self.led_version = QtGui.QLineEdit(self.gbx_copy)
        self.led_version.setMinimumSize(QtCore.QSize(0, 25))
        self.led_version.setMaximumSize(QtCore.QSize(16777215, 25))
        self.led_version.setMaxLength(10)
        self.led_version.setObjectName(_fromUtf8("led_version"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.led_version)
        self.verticalLayout.addWidget(self.gbx_copy)
        self.bbt_dialog = QtGui.QDialogButtonBox(self)
        self.bbt_dialog.setOrientation(QtCore.Qt.Horizontal)
        self.bbt_dialog.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbt_dialog.setObjectName(_fromUtf8("bbt_dialog"))
        self.verticalLayout.addWidget(self.bbt_dialog)

        self.retranslateUi()
        QtCore.QObject.connect(self.bbt_dialog, QtCore.SIGNAL(_fromUtf8("accepted()")), self.accept)
        QtCore.QObject.connect(self.bbt_dialog, QtCore.SIGNAL(_fromUtf8("rejected()")), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("dlg_experiment_copy", "Copy", None))
        self.gbx_copy.setTitle(_translate("dlg_experiment_copy", "Experiment copy...", None))
        self.lbl_code.setText(_translate("dlg_experiment_copy", "New Code:", None))
        self.lbl_version.setText(_translate("dlg_experiment_copy", "New Version:", None))

