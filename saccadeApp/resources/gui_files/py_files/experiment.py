# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files\experiment.ui'
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

class Ui_dlg_experiment(object):
    def setupUi(self):
        self.setObjectName(_fromUtf8("dlg_experiment"))
        self.resize(530, 650)
        self.setMinimumSize(QtCore.QSize(530, 630))
        self.setMaximumSize(QtCore.QSize(530, 850))
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbx_experiment = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_experiment.sizePolicy().hasHeightForWidth())
        self.gbx_experiment.setSizePolicy(sizePolicy)
        self.gbx_experiment.setMinimumSize(QtCore.QSize(0, 230))
        self.gbx_experiment.setMaximumSize(QtCore.QSize(16777215, 230))
        self.gbx_experiment.setObjectName(_fromUtf8("gbx_experiment"))
        self.formLayout_2 = QtGui.QFormLayout(self.gbx_experiment)
        self.formLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.formLayout_2.setHorizontalSpacing(5)
        self.formLayout_2.setVerticalSpacing(3)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.hly_01 = QtGui.QHBoxLayout()
        self.hly_01.setObjectName(_fromUtf8("hly_01"))
        self.led_code = QtGui.QLineEdit(self.gbx_experiment)
        self.led_code.setMinimumSize(QtCore.QSize(0, 25))
        self.led_code.setBaseSize(QtCore.QSize(0, 0))
        self.led_code.setMaxLength(10)
        self.led_code.setObjectName(_fromUtf8("led_code"))
        self.hly_01.addWidget(self.led_code)
        self.lbl_version = QtGui.QLabel(self.gbx_experiment)
        self.lbl_version.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_version.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_version.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_version.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_version.setObjectName(_fromUtf8("lbl_version"))
        self.hly_01.addWidget(self.lbl_version)
        self.led_version = QtGui.QLineEdit(self.gbx_experiment)
        self.led_version.setMinimumSize(QtCore.QSize(0, 25))
        self.led_version.setBaseSize(QtCore.QSize(0, 0))
        self.led_version.setMaxLength(10)
        self.led_version.setObjectName(_fromUtf8("led_version"))
        self.hly_01.addWidget(self.led_version)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.hly_01)
        self.lbl_name = QtGui.QLabel(self.gbx_experiment)
        self.lbl_name.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_name.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_name.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_name.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_name.setObjectName(_fromUtf8("lbl_name"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_name)
        self.led_name = QtGui.QLineEdit(self.gbx_experiment)
        self.led_name.setMinimumSize(QtCore.QSize(0, 25))
        self.led_name.setBaseSize(QtCore.QSize(0, 0))
        self.led_name.setMaxLength(50)
        self.led_name.setObjectName(_fromUtf8("led_name"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.led_name)
        self.lbl_description = QtGui.QLabel(self.gbx_experiment)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_description.sizePolicy().hasHeightForWidth())
        self.lbl_description.setSizePolicy(sizePolicy)
        self.lbl_description.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_description.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_description.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_description.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_description.setObjectName(_fromUtf8("lbl_description"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.lbl_description)
        self.lbl_code = QtGui.QLabel(self.gbx_experiment)
        self.lbl_code.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_code.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_code.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_code.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_code.setObjectName(_fromUtf8("lbl_code"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_code)
        self.ted_description = QtGui.QPlainTextEdit(self.gbx_experiment)
        self.ted_description.setMinimumSize(QtCore.QSize(0, 50))
        self.ted_description.setMaximumSize(QtCore.QSize(16777215, 50))
        self.ted_description.setObjectName(_fromUtf8("ted_description"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.ted_description)
        self.lbl_instructions = QtGui.QLabel(self.gbx_experiment)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_instructions.sizePolicy().hasHeightForWidth())
        self.lbl_instructions.setSizePolicy(sizePolicy)
        self.lbl_instructions.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_instructions.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_instructions.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_instructions.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_instructions.setObjectName(_fromUtf8("lbl_instructions"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.lbl_instructions)
        self.ted_instructions = QtGui.QPlainTextEdit(self.gbx_experiment)
        self.ted_instructions.setMinimumSize(QtCore.QSize(0, 50))
        self.ted_instructions.setMaximumSize(QtCore.QSize(16777215, 50))
        self.ted_instructions.setObjectName(_fromUtf8("ted_instructions"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.ted_instructions)
        self.lbl_comments = QtGui.QLabel(self.gbx_experiment)
        self.lbl_comments.setObjectName(_fromUtf8("lbl_comments"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.lbl_comments)
        self.led_comments = QtGui.QLineEdit(self.gbx_experiment)
        self.led_comments.setMinimumSize(QtCore.QSize(0, 25))
        self.led_comments.setMaximumSize(QtCore.QSize(16777215, 25))
        self.led_comments.setObjectName(_fromUtf8("led_comments"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.led_comments)
        self.verticalLayout.addWidget(self.gbx_experiment)
        self.hly_02 = QtGui.QHBoxLayout()
        self.hly_02.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.hly_02.setSpacing(5)
        self.hly_02.setObjectName(_fromUtf8("hly_02"))
        self.gbx_extra = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_extra.sizePolicy().hasHeightForWidth())
        self.gbx_extra.setSizePolicy(sizePolicy)
        self.gbx_extra.setMinimumSize(QtCore.QSize(0, 125))
        self.gbx_extra.setMaximumSize(QtCore.QSize(16777215, 125))
        self.gbx_extra.setObjectName(_fromUtf8("gbx_extra"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.gbx_extra)
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.vly_01 = QtGui.QVBoxLayout()
        self.vly_01.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.vly_01.setObjectName(_fromUtf8("vly_01"))
        self.cbt_use_space_key = QtGui.QCheckBox(self.gbx_extra)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbt_use_space_key.sizePolicy().hasHeightForWidth())
        self.cbt_use_space_key.setSizePolicy(sizePolicy)
        self.cbt_use_space_key.setMinimumSize(QtCore.QSize(120, 25))
        self.cbt_use_space_key.setMaximumSize(QtCore.QSize(150, 25))
        self.cbt_use_space_key.setObjectName(_fromUtf8("cbt_use_space_key"))
        self.vly_01.addWidget(self.cbt_use_space_key)
        self.cbt_random_active = QtGui.QCheckBox(self.gbx_extra)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbt_random_active.sizePolicy().hasHeightForWidth())
        self.cbt_random_active.setSizePolicy(sizePolicy)
        self.cbt_random_active.setMinimumSize(QtCore.QSize(120, 25))
        self.cbt_random_active.setMaximumSize(QtCore.QSize(150, 25))
        self.cbt_random_active.setObjectName(_fromUtf8("cbt_random_active"))
        self.vly_01.addWidget(self.cbt_random_active)
        self.horizontalLayout_3.addLayout(self.vly_01)
        self.lne_01 = QtGui.QFrame(self.gbx_extra)
        self.lne_01.setFrameShape(QtGui.QFrame.VLine)
        self.lne_01.setFrameShadow(QtGui.QFrame.Sunken)
        self.lne_01.setObjectName(_fromUtf8("lne_01"))
        self.horizontalLayout_3.addWidget(self.lne_01)
        self.vly_02 = QtGui.QVBoxLayout()
        self.vly_02.setObjectName(_fromUtf8("vly_02"))
        self.cbt_rest_active = QtGui.QCheckBox(self.gbx_extra)
        self.cbt_rest_active.setMinimumSize(QtCore.QSize(130, 25))
        self.cbt_rest_active.setMaximumSize(QtCore.QSize(16777215, 25))
        self.cbt_rest_active.setObjectName(_fromUtf8("cbt_rest_active"))
        self.vly_02.addWidget(self.cbt_rest_active)
        self.fly_01 = QtGui.QFormLayout()
        self.fly_01.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.fly_01.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.fly_01.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fly_01.setObjectName(_fromUtf8("fly_01"))
        self.lbl_rest_period = QtGui.QLabel(self.gbx_extra)
        self.lbl_rest_period.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_rest_period.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lbl_rest_period.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_rest_period.setObjectName(_fromUtf8("lbl_rest_period"))
        self.fly_01.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_rest_period)
        self.isb_rest_period = QtGui.QSpinBox(self.gbx_extra)
        self.isb_rest_period.setMinimumSize(QtCore.QSize(0, 25))
        self.isb_rest_period.setMaximumSize(QtCore.QSize(16777215, 25))
        self.isb_rest_period.setMinimum(1)
        self.isb_rest_period.setMaximum(9999)
        self.isb_rest_period.setProperty("value", 1)
        self.isb_rest_period.setObjectName(_fromUtf8("isb_rest_period"))
        self.fly_01.setWidget(0, QtGui.QFormLayout.FieldRole, self.isb_rest_period)
        self.lbl_rest_time = QtGui.QLabel(self.gbx_extra)
        self.lbl_rest_time.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_rest_time.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lbl_rest_time.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_rest_time.setObjectName(_fromUtf8("lbl_rest_time"))
        self.fly_01.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_rest_time)
        self.dsb_rest_time = QtGui.QDoubleSpinBox(self.gbx_extra)
        self.dsb_rest_time.setMinimumSize(QtCore.QSize(0, 25))
        self.dsb_rest_time.setMaximumSize(QtCore.QSize(16777215, 25))
        self.dsb_rest_time.setMaximum(3600.0)
        self.dsb_rest_time.setProperty("value", 5.0)
        self.dsb_rest_time.setObjectName(_fromUtf8("dsb_rest_time"))
        self.fly_01.setWidget(1, QtGui.QFormLayout.FieldRole, self.dsb_rest_time)
        self.vly_02.addLayout(self.fly_01)
        self.horizontalLayout_3.addLayout(self.vly_02)
        self.hly_02.addWidget(self.gbx_extra)
        self.gbx_dialog = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_dialog.sizePolicy().hasHeightForWidth())
        self.gbx_dialog.setSizePolicy(sizePolicy)
        self.gbx_dialog.setMinimumSize(QtCore.QSize(0, 125))
        self.gbx_dialog.setMaximumSize(QtCore.QSize(16777215, 125))
        self.gbx_dialog.setObjectName(_fromUtf8("gbx_dialog"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.gbx_dialog)
        self.verticalLayout_3.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.cbt_dialog_active = QtGui.QCheckBox(self.gbx_dialog)
        self.cbt_dialog_active.setMinimumSize(QtCore.QSize(0, 25))
        self.cbt_dialog_active.setMaximumSize(QtCore.QSize(120, 25))
        self.cbt_dialog_active.setObjectName(_fromUtf8("cbt_dialog_active"))
        self.verticalLayout_3.addWidget(self.cbt_dialog_active)
        self.fly_02 = QtGui.QFormLayout()
        self.fly_02.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.fly_02.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.fly_02.setSpacing(3)
        self.fly_02.setObjectName(_fromUtf8("fly_02"))
        self.cbt_age = QtGui.QCheckBox(self.gbx_dialog)
        self.cbt_age.setMinimumSize(QtCore.QSize(90, 25))
        self.cbt_age.setMaximumSize(QtCore.QSize(120, 25))
        self.cbt_age.setObjectName(_fromUtf8("cbt_age"))
        self.fly_02.setWidget(0, QtGui.QFormLayout.LabelRole, self.cbt_age)
        self.cbt_gender = QtGui.QCheckBox(self.gbx_dialog)
        self.cbt_gender.setMinimumSize(QtCore.QSize(90, 25))
        self.cbt_gender.setMaximumSize(QtCore.QSize(120, 25))
        self.cbt_gender.setObjectName(_fromUtf8("cbt_gender"))
        self.fly_02.setWidget(0, QtGui.QFormLayout.FieldRole, self.cbt_gender)
        self.cbt_glasses = QtGui.QCheckBox(self.gbx_dialog)
        self.cbt_glasses.setMinimumSize(QtCore.QSize(90, 25))
        self.cbt_glasses.setMaximumSize(QtCore.QSize(120, 25))
        self.cbt_glasses.setObjectName(_fromUtf8("cbt_glasses"))
        self.fly_02.setWidget(1, QtGui.QFormLayout.LabelRole, self.cbt_glasses)
        self.cbt_eyes = QtGui.QCheckBox(self.gbx_dialog)
        self.cbt_eyes.setMinimumSize(QtCore.QSize(90, 25))
        self.cbt_eyes.setMaximumSize(QtCore.QSize(120, 25))
        self.cbt_eyes.setObjectName(_fromUtf8("cbt_eyes"))
        self.fly_02.setWidget(1, QtGui.QFormLayout.FieldRole, self.cbt_eyes)
        self.verticalLayout_3.addLayout(self.fly_02)
        self.hly_02.addWidget(self.gbx_dialog)
        self.verticalLayout.addLayout(self.hly_02)
        self.gbx_tests = QtGui.QGroupBox(self)
        self.gbx_tests.setMinimumSize(QtCore.QSize(0, 180))
        self.gbx_tests.setObjectName(_fromUtf8("gbx_tests"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.gbx_tests)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tbv_test = QtGui.QTableView(self.gbx_tests)
        self.tbv_test.setMinimumSize(QtCore.QSize(380, 120))
        self.tbv_test.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tbv_test.setObjectName(_fromUtf8("tbv_test"))
        self.horizontalLayout.addWidget(self.tbv_test)
        self.vly_03 = QtGui.QVBoxLayout()
        self.vly_03.setSpacing(3)
        self.vly_03.setObjectName(_fromUtf8("vly_03"))
        self.pbt_new = QtGui.QPushButton(self.gbx_tests)
        self.pbt_new.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_new.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_new.setObjectName(_fromUtf8("pbt_new"))
        self.vly_03.addWidget(self.pbt_new)
        self.hly_03 = QtGui.QHBoxLayout()
        self.hly_03.setSpacing(4)
        self.hly_03.setObjectName(_fromUtf8("hly_03"))
        self.pbt_up = QtGui.QPushButton(self.gbx_tests)
        self.pbt_up.setMinimumSize(QtCore.QSize(38, 25))
        self.pbt_up.setMaximumSize(QtCore.QSize(38, 25))
        self.pbt_up.setObjectName(_fromUtf8("pbt_up"))
        self.hly_03.addWidget(self.pbt_up)
        self.pbt_down = QtGui.QPushButton(self.gbx_tests)
        self.pbt_down.setMinimumSize(QtCore.QSize(38, 25))
        self.pbt_down.setMaximumSize(QtCore.QSize(38, 25))
        self.pbt_down.setObjectName(_fromUtf8("pbt_down"))
        self.hly_03.addWidget(self.pbt_down)
        self.vly_03.addLayout(self.hly_03)
        self.pbt_edit = QtGui.QPushButton(self.gbx_tests)
        self.pbt_edit.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_edit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_edit.setObjectName(_fromUtf8("pbt_edit"))
        self.vly_03.addWidget(self.pbt_edit)
        self.pbt_copy = QtGui.QPushButton(self.gbx_tests)
        self.pbt_copy.setMinimumSize(QtCore.QSize(0, 25))
        self.pbt_copy.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_copy.setObjectName(_fromUtf8("pbt_copy"))
        self.vly_03.addWidget(self.pbt_copy)
        self.pbt_remove = QtGui.QPushButton(self.gbx_tests)
        self.pbt_remove.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_remove.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_remove.setObjectName(_fromUtf8("pbt_remove"))
        self.vly_03.addWidget(self.pbt_remove)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vly_03.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.vly_03)
        self.verticalLayout.addWidget(self.gbx_tests)
        self.bbt_save = QtGui.QDialogButtonBox(self)
        self.bbt_save.setMinimumSize(QtCore.QSize(0, 25))
        self.bbt_save.setMaximumSize(QtCore.QSize(16777215, 25))
        self.bbt_save.setOrientation(QtCore.Qt.Horizontal)
        self.bbt_save.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.bbt_save.setObjectName(_fromUtf8("bbt_save"))
        self.verticalLayout.addWidget(self.bbt_save)

        self.retranslateUi()
        QtCore.QObject.connect(self.bbt_save, QtCore.SIGNAL(_fromUtf8("accepted()")), self.accept)
        QtCore.QObject.connect(self.bbt_save, QtCore.SIGNAL(_fromUtf8("rejected()")), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("dlg_experiment", "Experiment", None))
        self.gbx_experiment.setTitle(_translate("dlg_experiment", "Experiment", None))
        self.lbl_version.setText(_translate("dlg_experiment", "Version:", None))
        self.lbl_name.setText(_translate("dlg_experiment", "Name:", None))
        self.lbl_description.setText(_translate("dlg_experiment", "Description:", None))
        self.lbl_code.setText(_translate("dlg_experiment", "Code:", None))
        self.lbl_instructions.setText(_translate("dlg_experiment", "Instructions:", None))
        self.lbl_comments.setText(_translate("dlg_experiment", "Comments:", None))
        self.gbx_extra.setTitle(_translate("dlg_experiment", "Extra settings", None))
        self.cbt_use_space_key.setText(_translate("dlg_experiment", "Press space before\n"
"every test", None))
        self.cbt_random_active.setText(_translate("dlg_experiment", "Randomize tests", None))
        self.cbt_rest_active.setText(_translate("dlg_experiment", "Allow resting between\n"
"tests.", None))
        self.lbl_rest_period.setText(_translate("dlg_experiment", "Rest period:", None))
        self.lbl_rest_time.setText(_translate("dlg_experiment", "Rest time [s]:", None))
        self.gbx_dialog.setTitle(_translate("dlg_experiment", "Dialog settings", None))
        self.cbt_dialog_active.setText(_translate("dlg_experiment", "Use the dialog", None))
        self.cbt_age.setText(_translate("dlg_experiment", "ask age", None))
        self.cbt_gender.setText(_translate("dlg_experiment", "ask gender", None))
        self.cbt_glasses.setText(_translate("dlg_experiment", "ask glasses", None))
        self.cbt_eyes.setText(_translate("dlg_experiment", "ask eye color", None))
        self.gbx_tests.setTitle(_translate("dlg_experiment", "Tests", None))
        self.pbt_new.setText(_translate("dlg_experiment", "New", None))
        self.pbt_up.setText(_translate("dlg_experiment", "Up", None))
        self.pbt_down.setText(_translate("dlg_experiment", "Down", None))
        self.pbt_edit.setText(_translate("dlg_experiment", "Edit", None))
        self.pbt_copy.setText(_translate("dlg_experiment", "Copy", None))
        self.pbt_remove.setText(_translate("dlg_experiment", "Remove", None))

