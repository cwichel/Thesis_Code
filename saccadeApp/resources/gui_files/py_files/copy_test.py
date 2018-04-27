# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files\copy_test.ui'
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

class Ui_dlg_test_copy(object):
    def setupUi(self):
        self.setObjectName(_fromUtf8("dlg_test_copy"))
        self.resize(400, 200)
        self.setMinimumSize(QtCore.QSize(400, 200))
        self.setMaximumSize(QtCore.QSize(400, 200))
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbx_copy = QtGui.QGroupBox(self)
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
        self.lbl_copy_from = QtGui.QLabel(self.gbx_copy)
        self.lbl_copy_from.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_copy_from.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_copy_from.setObjectName(_fromUtf8("lbl_copy_from"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_copy_from)
        self.hly_01 = QtGui.QHBoxLayout()
        self.hly_01.setObjectName(_fromUtf8("hly_01"))
        self.rbt_selection = QtGui.QRadioButton(self.gbx_copy)
        self.rbt_selection.setMinimumSize(QtCore.QSize(0, 25))
        self.rbt_selection.setMaximumSize(QtCore.QSize(16777215, 25))
        self.rbt_selection.setChecked(True)
        self.rbt_selection.setObjectName(_fromUtf8("rbt_selection"))
        self.gbt_copy_from = QtGui.QButtonGroup(self)
        self.gbt_copy_from.setObjectName(_fromUtf8("gbt_copy_from"))
        self.gbt_copy_from.addButton(self.rbt_selection)
        self.hly_01.addWidget(self.rbt_selection)
        self.rbt_experiment = QtGui.QRadioButton(self.gbx_copy)
        self.rbt_experiment.setMinimumSize(QtCore.QSize(0, 25))
        self.rbt_experiment.setMaximumSize(QtCore.QSize(16777215, 25))
        self.rbt_experiment.setObjectName(_fromUtf8("rbt_experiment"))
        self.gbt_copy_from.addButton(self.rbt_experiment)
        self.hly_01.addWidget(self.rbt_experiment)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.hly_01)
        self.cmb_experiment = QtGui.QComboBox(self.gbx_copy)
        self.cmb_experiment.setMinimumSize(QtCore.QSize(0, 25))
        self.cmb_experiment.setMaximumSize(QtCore.QSize(16777215, 25))
        self.cmb_experiment.setObjectName(_fromUtf8("cmb_experiment"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cmb_experiment)
        self.cmb_test = QtGui.QComboBox(self.gbx_copy)
        self.cmb_test.setMinimumSize(QtCore.QSize(0, 25))
        self.cmb_test.setMaximumSize(QtCore.QSize(16777215, 25))
        self.cmb_test.setObjectName(_fromUtf8("cmb_test"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.cmb_test)
        self.lbl_experiment = QtGui.QLabel(self.gbx_copy)
        self.lbl_experiment.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_experiment.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_experiment.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_experiment.setObjectName(_fromUtf8("lbl_experiment"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.lbl_experiment)
        self.lbl_test = QtGui.QLabel(self.gbx_copy)
        self.lbl_test.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_test.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_test.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_test.setObjectName(_fromUtf8("lbl_test"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.lbl_test)
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
        self.setWindowTitle(_translate("dlg_test_copy", "Copy", None))
        self.gbx_copy.setTitle(_translate("dlg_test_copy", "Copy", None))
        self.lbl_name.setText(_translate("dlg_test_copy", "New Name:", None))
        self.lbl_copy_from.setText(_translate("dlg_test_copy", "Copy from: ", None))
        self.rbt_selection.setText(_translate("dlg_test_copy", "Selection...", None))
        self.rbt_experiment.setText(_translate("dlg_test_copy", "Experiment...", None))
        self.lbl_experiment.setText(_translate("dlg_test_copy", "Experiment:", None))
        self.lbl_test.setText(_translate("dlg_test_copy", "Test:", None))

