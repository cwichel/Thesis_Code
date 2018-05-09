# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import sys
from PyQt4 import QtGui

# ===========================
# Internal:
# ===========================
from gui_models import *
from saccadeapp.core import *
from saccadeapp.script import *

# =============================================================================
# Qt Encoding
# =============================================================================
try:
    _from_utf8 = QtCore.QString._from_utf8
except AttributeError:
    def _from_utf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)

except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


# =============================================================================
# Main App Class: saccadeapp
# =============================================================================
class SaccadeApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.__setup_ui()
        # -------------------
        self.database = SaccadeDB()
        self.model_experiment = ListModel([], header=u"Experiment")
        self.model_configuration = ListModel([], header=u"Profile")
        # -------------------
        self.__setup_menu()
        self.__setup_configuration()
        self.__setup_experiment()
        self.__setup_execution()

    # =================================
    def __setup_ui(self):
        self.setObjectName(_from_utf8("saccadeapp"))
        self.resize(530, 350)
        self.setMinimumSize(QtCore.QSize(530, 350))
        self.setMaximumSize(QtCore.QSize(530, 850))
        self.vly_01 = QtGui.QWidget(self)
        self.vly_01.setObjectName(_from_utf8("vly_01"))
        self.verticalLayout = QtGui.QVBoxLayout(self.vly_01)
        self.verticalLayout.setObjectName(_from_utf8("verticalLayout"))
        self.tab_main = QtGui.QTabWidget(self.vly_01)
        self.tab_main.setMinimumSize(QtCore.QSize(0, 0))
        self.tab_main.setObjectName(_from_utf8("tab_main"))
        self.wdg_experiment = QtGui.QWidget()
        self.wdg_experiment.setObjectName(_from_utf8("wdg_experiment"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.wdg_experiment)
        self.horizontalLayout.setObjectName(_from_utf8("horizontalLayout"))
        self.trv_experiment = QtGui.QTreeView(self.wdg_experiment)
        self.trv_experiment.setMinimumSize(QtCore.QSize(250, 200))
        self.trv_experiment.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.trv_experiment.setObjectName(_from_utf8("trv_experiment"))
        self.horizontalLayout.addWidget(self.trv_experiment)
        self.vly_02 = QtGui.QVBoxLayout()
        self.vly_02.setSpacing(3)
        self.vly_02.setObjectName(_from_utf8("vly_02"))
        self.pbt_experiment_new = QtGui.QPushButton(self.wdg_experiment)
        self.pbt_experiment_new.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_experiment_new.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_experiment_new.setObjectName(_from_utf8("pbt_experiment_new"))
        self.vly_02.addWidget(self.pbt_experiment_new)
        self.pbt_experiment_edit = QtGui.QPushButton(self.wdg_experiment)
        self.pbt_experiment_edit.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_experiment_edit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_experiment_edit.setObjectName(_from_utf8("pbt_experiment_edit"))
        self.vly_02.addWidget(self.pbt_experiment_edit)
        self.pbt_experiment_copy = QtGui.QPushButton(self.wdg_experiment)
        self.pbt_experiment_copy.setMinimumSize(QtCore.QSize(0, 25))
        self.pbt_experiment_copy.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_experiment_copy.setObjectName(_from_utf8("pbt_experiment_copy"))
        self.vly_02.addWidget(self.pbt_experiment_copy)
        self.pbt_experiment_remove = QtGui.QPushButton(self.wdg_experiment)
        self.pbt_experiment_remove.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_experiment_remove.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_experiment_remove.setObjectName(_from_utf8("pbt_experiment_remove"))
        self.vly_02.addWidget(self.pbt_experiment_remove)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vly_02.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.vly_02)
        self.tab_main.addTab(self.wdg_experiment, _from_utf8(""))
        self.wdg_configuration = QtGui.QWidget()
        self.wdg_configuration.setObjectName(_from_utf8("wdg_configuration"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.wdg_configuration)
        self.verticalLayout_2.setObjectName(_from_utf8("verticalLayout_2"))
        self.gbx_configuration_basic = QtGui.QGroupBox(self.wdg_configuration)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_configuration_basic.sizePolicy().hasHeightForWidth())
        self.gbx_configuration_basic.setSizePolicy(sizePolicy)
        self.gbx_configuration_basic.setObjectName(_from_utf8("gbx_configuration_basic"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.gbx_configuration_basic)
        self.horizontalLayout_3.setObjectName(_from_utf8("horizontalLayout_3"))
        self.lbl_monitor_center = QtGui.QLabel(self.gbx_configuration_basic)
        self.lbl_monitor_center.setMinimumSize(QtCore.QSize(80, 25))
        self.lbl_monitor_center.setMaximumSize(QtCore.QSize(80, 25))
        self.lbl_monitor_center.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_monitor_center.setObjectName(_from_utf8("lbl_monitor_center"))
        self.horizontalLayout_3.addWidget(self.lbl_monitor_center)
        self.pbt_monitor_center = QtGui.QPushButton(self.gbx_configuration_basic)
        self.pbt_monitor_center.setMinimumSize(QtCore.QSize(150, 25))
        self.pbt_monitor_center.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_monitor_center.setObjectName(_from_utf8("pbt_monitor_center"))
        self.horizontalLayout_3.addWidget(self.pbt_monitor_center)
        self.verticalLayout_2.addWidget(self.gbx_configuration_basic)
        self.gbx_configuration_profile = QtGui.QGroupBox(self.wdg_configuration)
        self.gbx_configuration_profile.setObjectName(_from_utf8("gbx_configuration_profile"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.gbx_configuration_profile)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(_from_utf8("horizontalLayout_2"))
        self.lsv_configuration = QtGui.QListView(self.gbx_configuration_profile)
        self.lsv_configuration.setMinimumSize(QtCore.QSize(230, 150))
        self.lsv_configuration.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lsv_configuration.setObjectName(_from_utf8("lsv_configuration"))
        self.horizontalLayout_2.addWidget(self.lsv_configuration)
        self.vly_03 = QtGui.QVBoxLayout()
        self.vly_03.setSpacing(3)
        self.vly_03.setObjectName(_from_utf8("vly_03"))
        self.pbt_configuration_new = QtGui.QPushButton(self.gbx_configuration_profile)
        self.pbt_configuration_new.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_configuration_new.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_configuration_new.setObjectName(_from_utf8("pbt_configuration_new"))
        self.vly_03.addWidget(self.pbt_configuration_new)
        self.pbt_configuration_edit = QtGui.QPushButton(self.gbx_configuration_profile)
        self.pbt_configuration_edit.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_configuration_edit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_configuration_edit.setObjectName(_from_utf8("pbt_configuration_edit"))
        self.vly_03.addWidget(self.pbt_configuration_edit)
        self.pbt_configuration_copy = QtGui.QPushButton(self.gbx_configuration_profile)
        self.pbt_configuration_copy.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_configuration_copy.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_configuration_copy.setObjectName(_from_utf8("pbt_configuration_copy"))
        self.vly_03.addWidget(self.pbt_configuration_copy)
        self.pbt_configuration_remove = QtGui.QPushButton(self.gbx_configuration_profile)
        self.pbt_configuration_remove.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_configuration_remove.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_configuration_remove.setObjectName(_from_utf8("pbt_configuration_remove"))
        self.vly_03.addWidget(self.pbt_configuration_remove)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vly_03.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.vly_03)
        self.verticalLayout_2.addWidget(self.gbx_configuration_profile)
        self.tab_main.addTab(self.wdg_configuration, _from_utf8(""))
        self.wdg_execution = QtGui.QWidget()
        self.wdg_execution.setObjectName(_from_utf8("wdg_execution"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.wdg_execution)
        self.verticalLayout_3.setObjectName(_from_utf8("verticalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.hly_01 = QtGui.QHBoxLayout()
        self.hly_01.setObjectName(_from_utf8("hly_01"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hly_01.addItem(spacerItem3)
        self.gbx_execution = QtGui.QGroupBox(self.wdg_execution)
        self.gbx_execution.setMinimumSize(QtCore.QSize(0, 160))
        self.gbx_execution.setMaximumSize(QtCore.QSize(16777215, 160))
        self.gbx_execution.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gbx_execution.setTitle(_from_utf8(""))
        self.gbx_execution.setAlignment(QtCore.Qt.AlignCenter)
        self.gbx_execution.setObjectName(_from_utf8("gbx_execution"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.gbx_execution)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName(_from_utf8("verticalLayout_4"))
        self.fly_01 = QtGui.QFormLayout()
        self.fly_01.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.fly_01.setHorizontalSpacing(5)
        self.fly_01.setVerticalSpacing(3)
        self.fly_01.setObjectName(_from_utf8("fly_01"))
        self.lbl_execution_experiment = QtGui.QLabel(self.gbx_execution)
        self.lbl_execution_experiment.setMinimumSize(QtCore.QSize(0, 25))
        self.lbl_execution_experiment.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lbl_execution_experiment.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_execution_experiment.setObjectName(_from_utf8("lbl_execution_experiment"))
        self.fly_01.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_execution_experiment)
        self.cmb_execution_experiment = QtGui.QComboBox(self.gbx_execution)
        self.cmb_execution_experiment.setMinimumSize(QtCore.QSize(200, 25))
        self.cmb_execution_experiment.setMaximumSize(QtCore.QSize(16777215, 25))
        self.cmb_execution_experiment.setObjectName(_from_utf8("cmb_execution_experiment"))
        self.fly_01.setWidget(0, QtGui.QFormLayout.FieldRole, self.cmb_execution_experiment)
        self.lbl_execution_profile = QtGui.QLabel(self.gbx_execution)
        self.lbl_execution_profile.setMinimumSize(QtCore.QSize(0, 25))
        self.lbl_execution_profile.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lbl_execution_profile.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_execution_profile.setObjectName(_from_utf8("lbl_execution_profile"))
        self.fly_01.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_execution_profile)
        self.cmb_execution_profile = QtGui.QComboBox(self.gbx_execution)
        self.cmb_execution_profile.setMinimumSize(QtCore.QSize(200, 25))
        self.cmb_execution_profile.setMaximumSize(QtCore.QSize(16777215, 25))
        self.cmb_execution_profile.setObjectName(_from_utf8("cmb_execution_profile"))
        self.fly_01.setWidget(1, QtGui.QFormLayout.FieldRole, self.cmb_execution_profile)
        self.cbt_execution_save = QtGui.QCheckBox(self.gbx_execution)
        self.cbt_execution_save.setObjectName(_from_utf8("cbt_execution_save"))
        self.fly_01.setWidget(2, QtGui.QFormLayout.FieldRole, self.cbt_execution_save)
        self.verticalLayout_4.addLayout(self.fly_01)
        self.hly_02 = QtGui.QHBoxLayout()
        self.hly_02.setSpacing(0)
        self.hly_02.setObjectName(_from_utf8("hly_02"))
        self.pbt_execute = QtGui.QPushButton(self.gbx_execution)
        self.pbt_execute.setMinimumSize(QtCore.QSize(80, 40))
        self.pbt_execute.setMaximumSize(QtCore.QSize(100, 40))
        self.pbt_execute.setObjectName(_from_utf8("pbt_execute"))
        self.hly_02.addWidget(self.pbt_execute)
        self.verticalLayout_4.addLayout(self.hly_02)
        self.hly_01.addWidget(self.gbx_execution)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hly_01.addItem(spacerItem4)
        self.verticalLayout_3.addLayout(self.hly_01)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)
        self.tab_main.addTab(self.wdg_execution, _from_utf8(""))
        self.verticalLayout.addWidget(self.tab_main)
        self.setCentralWidget(self.vly_01)
        self.mbr_menu = QtGui.QMenuBar(self)
        self.mbr_menu.setGeometry(QtCore.QRect(0, 0, 530, 21))
        self.mbr_menu.setObjectName(_from_utf8("mbr_menu"))
        self.mnu_file = QtGui.QMenu(self.mbr_menu)
        self.mnu_file.setObjectName(_from_utf8("mnu_file"))
        self.mnu_help = QtGui.QMenu(self.mbr_menu)
        self.mnu_help.setObjectName(_from_utf8("mnu_help"))
        self.setMenuBar(self.mbr_menu)
        self.mac_exit = QtGui.QAction(self)
        self.mac_exit.setObjectName(_from_utf8("mac_exit"))
        self.mac_documentation = QtGui.QAction(self)
        self.mac_documentation.setObjectName(_from_utf8("mac_documentation"))
        self.mac_about = QtGui.QAction(self)
        self.mac_about.setObjectName(_from_utf8("mac_about"))
        self.actionSome_shit = QtGui.QAction(self)
        self.actionSome_shit.setObjectName(_from_utf8("actionSome_shit"))
        self.mnu_file.addAction(self.mac_exit)
        self.mnu_help.addAction(self.mac_documentation)
        self.mnu_help.addSeparator()
        self.mnu_help.addAction(self.mac_about)
        self.mbr_menu.addAction(self.mnu_file.menuAction())
        self.mbr_menu.addAction(self.mnu_help.menuAction())

        self.__retranslate_ui()
        self.tab_main.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(self)

    def __retranslate_ui(self):
        self.setWindowTitle(_translate("saccadeapp", "saccadeapp", None))
        self.pbt_experiment_new.setText(_translate("saccadeapp", "New", None))
        self.pbt_experiment_edit.setText(_translate("saccadeapp", "Edit", None))
        self.pbt_experiment_copy.setText(_translate("saccadeapp", "Copy", None))
        self.pbt_experiment_remove.setText(_translate("saccadeapp", "Remove", None))
        self.tab_main.setTabText(self.tab_main.indexOf(self.wdg_experiment), _translate("saccadeapp", "Experiments", None))
        self.gbx_configuration_basic.setTitle(_translate("saccadeapp", "Basic Configuration", None))
        self.lbl_monitor_center.setText(_translate("saccadeapp", "Monitor Center:", None))
        self.pbt_monitor_center.setText(_translate("saccadeapp", "Open", None))
        self.gbx_configuration_profile.setTitle(_translate("saccadeapp", "Configuration Profiles", None))
        self.pbt_configuration_new.setText(_translate("saccadeapp", "New", None))
        self.pbt_configuration_edit.setText(_translate("saccadeapp", "Edit", None))
        self.pbt_configuration_copy.setText(_translate("saccadeapp", "Copy", None))
        self.pbt_configuration_remove.setText(_translate("saccadeapp", "Remove", None))
        self.tab_main.setTabText(self.tab_main.indexOf(self.wdg_configuration), _translate("saccadeapp", "Configuration", None))
        self.lbl_execution_experiment.setText(_translate("saccadeapp", "Experiment:", None))
        self.lbl_execution_profile.setText(_translate("saccadeapp", "Configuration:", None))
        self.cbt_execution_save.setText(_translate("saccadeapp", "Save experiment frames", None))
        self.pbt_execute.setText(_translate("saccadeapp", "Execute", None))
        self.tab_main.setTabText(self.tab_main.indexOf(self.wdg_execution), _translate("saccadeapp", "Execution", None))
        self.mnu_file.setTitle(_translate("saccadeapp", "File", None))
        self.mnu_help.setTitle(_translate("saccadeapp", "Help", None))
        self.mac_exit.setText(_translate("saccadeapp", "Exit", None))
        self.mac_documentation.setText(_translate("saccadeapp", "Documentation", None))
        self.mac_about.setText(_translate("saccadeapp", "About", None))
        self.actionSome_shit.setText(_translate("saccadeapp", "Some shit", None))

    # =================================
    def __setup_menu(self):
        self.mac_documentation.triggered.connect(self.__app_documentation)
        self.mac_about.triggered.connect(self.__app_about)
        self.mac_exit.triggered.connect(self.__app_close)

    @staticmethod
    def __app_documentation():
        import os
        from saccadeapp.core import Utils
        # -------------------
        print u"Opening docs file..."
        path_docu = Utils.format_path(Utils.get_main_path()+u'/../docs/saccadeApp_docu.pdf')
        os.startfile(path_docu)

    @staticmethod
    def __app_about():
        print u"Opening about window..."
        dialog = AboutApp()
        dialog.exec_()

    @staticmethod
    def __app_close():
        print u"Closing the App..."
        sys.exit()

    # =================================
    def __setup_execution(self):
        self.pbt_execute.clicked.connect(self.__handle_execute_experiment)

        self.cmb_execution_profile.setModel(self.model_configuration)
        self.cmb_execution_experiment.setModel(self.model_experiment)

    def __handle_execute_experiment(self):
        print u"Executing the selected experiment..."

    # =================================
    def __setup_experiment(self):
        self.pbt_experiment_new.clicked.connect(self.__handle_experiment_new)
        self.pbt_experiment_edit.clicked.connect(self.__handle_experiment_edit)
        self.pbt_experiment_copy.clicked.connect(self.__handle_experiment_copy)
        self.pbt_experiment_remove.clicked.connect(self.__handle_experiment_remove)

    def __handle_experiment_new(self):
        print u"Creating experiment..."
        dialog = ExperimentApp(parent=self)
        dialog.exec_()

    def __handle_experiment_edit(self):
        print u"Editing experiment..."
        dialog = ExperimentApp(parent=self)
        dialog.exec_()

    def __handle_experiment_copy(self):
        print u"Copying experiment..."
        dialog = ExperimentCopyApp(parent=self)
        dialog.exec_()

    def __handle_experiment_remove(self):
        print u"Removing experiment..."

    def update_experiment_view(self):
        pass

    # =================================
    def __setup_configuration(self):
        self.pbt_monitor_center.clicked.connect(self.__handle_monitor_center)
        self.pbt_configuration_new.clicked.connect(self.__handle_configuration_new)
        self.pbt_configuration_edit.clicked.connect(self.__handle_configuration_edit)
        self.pbt_configuration_copy.clicked.connect(self.__handle_configuration_copy)
        self.pbt_configuration_remove.clicked.connect(self.__handle_configuration_remove)
        self.lsv_configuration.setModel(self.model_configuration)
        self.update_configuration_view()
        if self.model_configuration.rowCount() > 0:
            self.lsv_configuration.setCurrentIndex(self.model_configuration.index(0, 0))

    def __handle_monitor_center(self):
        Utils.open_psychopy_monitor_center()

    def __handle_configuration_new(self):
        print u"Creating configuration profile..."
        dialog = ConfigurationApp(parent=self, item_id=-1)
        dialog.exec_()

    def __handle_configuration_edit(self):
        items = self.model_configuration.rowCount()
        index = self.lsv_configuration.currentIndex().row()
        if items is not 0 and index is not -1:
            print u"Editing configuration profile..."
            dialog = ConfigurationApp(parent=self, item_id=index)
            dialog.exec_()

    def __handle_configuration_copy(self):
        items = self.model_configuration.rowCount()
        index = self.lsv_configuration.currentIndex().row()
        if items is not 0 and index is not -1:
            print u"Copying configuration profile..."
            name = self.model_configuration.get_item(index=index)
            profile_base = Configuration(db=self.database, name=name)
            profile_copy = None
            is_ready = False
            while not is_ready:
                name, is_ok = QtGui.QInputDialog.getText(None, u'Copying profile...', u'New name:', text=name)
                name = unicode(name)
                if is_ok:
                    profile_copy = profile_base.copy(name=name)
                    if profile_copy is not None:
                        profile_copy.save()
                        is_ready = True
                    else:
                        QtGui.QMessageBox.warning(self, u'Error', u'Name already used!\nTry again.')
                else:
                    is_ready = True
            if profile_copy is not None:
                self.update_configuration_view()
                index = self.model_configuration.get_index(item=name)
                self.lsv_configuration.setCurrentIndex(self.model_configuration.index(index, 0))

    def __handle_configuration_remove(self):
        print u"Removing configuration profile..."
        items = self.model_configuration.rowCount()
        index = self.lsv_configuration.currentIndex().row()
        if items is not 0 and index is not -1:
            name = self.model_configuration.get_item(index=index)
            profile = Configuration(db=self.database, name=name)
            profile.remove()
            self.update_configuration_view()
            index = index-1 if index > 0 else 0
            self.lsv_configuration.setCurrentIndex(self.model_configuration.index(index, 0))

    def update_configuration_view(self):
        conf_list = Configuration.get_list(db=self.database)
        if conf_list is not None:
            conf_list = [item[0] for item in conf_list]
            self.model_configuration.update_items(items=conf_list)
        else:
            self.model_configuration.update_items(items=[])


# =============================================================================
# Experiment related Classes:
# =============================================================================
# ===============================================
# Class: ExperimentApp
# ===============================================
class ExperimentApp(QtGui.QDialog):
    def __init__(self, parent=SaccadeApp):
        QtGui.QDialog.__init__(self)
        self.__setup_ui()
        # ==============
        self.parent = parent
        # ==============
        self.__setup_experiment()

    # =================================
    def __setup_ui(self):
        self.setObjectName(_from_utf8("ExperimentApp"))
        self.resize(530, 650)
        self.setMinimumSize(QtCore.QSize(530, 630))
        self.setMaximumSize(QtCore.QSize(530, 850))
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName(_from_utf8("verticalLayout"))
        self.gbx_experiment = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_experiment.sizePolicy().hasHeightForWidth())
        self.gbx_experiment.setSizePolicy(sizePolicy)
        self.gbx_experiment.setMinimumSize(QtCore.QSize(0, 230))
        self.gbx_experiment.setMaximumSize(QtCore.QSize(16777215, 230))
        self.gbx_experiment.setObjectName(_from_utf8("gbx_experiment"))
        self.formLayout_2 = QtGui.QFormLayout(self.gbx_experiment)
        self.formLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.formLayout_2.setHorizontalSpacing(5)
        self.formLayout_2.setVerticalSpacing(3)
        self.formLayout_2.setObjectName(_from_utf8("formLayout_2"))
        self.hly_01 = QtGui.QHBoxLayout()
        self.hly_01.setObjectName(_from_utf8("hly_01"))
        self.led_code = QtGui.QLineEdit(self.gbx_experiment)
        self.led_code.setMinimumSize(QtCore.QSize(0, 25))
        self.led_code.setBaseSize(QtCore.QSize(0, 0))
        self.led_code.setMaxLength(10)
        self.led_code.setObjectName(_from_utf8("led_code"))
        self.hly_01.addWidget(self.led_code)
        self.lbl_version = QtGui.QLabel(self.gbx_experiment)
        self.lbl_version.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_version.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_version.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_version.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_version.setObjectName(_from_utf8("lbl_version"))
        self.hly_01.addWidget(self.lbl_version)
        self.led_version = QtGui.QLineEdit(self.gbx_experiment)
        self.led_version.setMinimumSize(QtCore.QSize(0, 25))
        self.led_version.setBaseSize(QtCore.QSize(0, 0))
        self.led_version.setMaxLength(10)
        self.led_version.setObjectName(_from_utf8("led_version"))
        self.hly_01.addWidget(self.led_version)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.hly_01)
        self.lbl_name = QtGui.QLabel(self.gbx_experiment)
        self.lbl_name.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_name.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_name.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_name.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_name.setObjectName(_from_utf8("lbl_name"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_name)
        self.led_name = QtGui.QLineEdit(self.gbx_experiment)
        self.led_name.setMinimumSize(QtCore.QSize(0, 25))
        self.led_name.setBaseSize(QtCore.QSize(0, 0))
        self.led_name.setMaxLength(50)
        self.led_name.setObjectName(_from_utf8("led_name"))
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
        self.lbl_description.setObjectName(_from_utf8("lbl_description"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.lbl_description)
        self.lbl_code = QtGui.QLabel(self.gbx_experiment)
        self.lbl_code.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_code.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_code.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_code.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_code.setObjectName(_from_utf8("lbl_code"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_code)
        self.ted_description = QtGui.QPlainTextEdit(self.gbx_experiment)
        self.ted_description.setMinimumSize(QtCore.QSize(0, 50))
        self.ted_description.setMaximumSize(QtCore.QSize(16777215, 50))
        self.ted_description.setObjectName(_from_utf8("ted_description"))
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
        self.lbl_instructions.setObjectName(_from_utf8("lbl_instructions"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.lbl_instructions)
        self.ted_instructions = QtGui.QPlainTextEdit(self.gbx_experiment)
        self.ted_instructions.setMinimumSize(QtCore.QSize(0, 50))
        self.ted_instructions.setMaximumSize(QtCore.QSize(16777215, 50))
        self.ted_instructions.setObjectName(_from_utf8("ted_instructions"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.ted_instructions)
        self.lbl_comments = QtGui.QLabel(self.gbx_experiment)
        self.lbl_comments.setObjectName(_from_utf8("lbl_comments"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.lbl_comments)
        self.led_comments = QtGui.QLineEdit(self.gbx_experiment)
        self.led_comments.setMinimumSize(QtCore.QSize(0, 25))
        self.led_comments.setMaximumSize(QtCore.QSize(16777215, 25))
        self.led_comments.setObjectName(_from_utf8("led_comments"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.led_comments)
        self.verticalLayout.addWidget(self.gbx_experiment)
        self.hly_02 = QtGui.QHBoxLayout()
        self.hly_02.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.hly_02.setSpacing(5)
        self.hly_02.setObjectName(_from_utf8("hly_02"))
        self.gbx_extra = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_extra.sizePolicy().hasHeightForWidth())
        self.gbx_extra.setSizePolicy(sizePolicy)
        self.gbx_extra.setMinimumSize(QtCore.QSize(0, 125))
        self.gbx_extra.setMaximumSize(QtCore.QSize(16777215, 125))
        self.gbx_extra.setObjectName(_from_utf8("gbx_extra"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.gbx_extra)
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(_from_utf8("horizontalLayout_3"))
        self.vly_01 = QtGui.QVBoxLayout()
        self.vly_01.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.vly_01.setObjectName(_from_utf8("vly_01"))
        self.cbt_use_space_key = QtGui.QCheckBox(self.gbx_extra)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbt_use_space_key.sizePolicy().hasHeightForWidth())
        self.cbt_use_space_key.setSizePolicy(sizePolicy)
        self.cbt_use_space_key.setMinimumSize(QtCore.QSize(120, 25))
        self.cbt_use_space_key.setMaximumSize(QtCore.QSize(150, 25))
        self.cbt_use_space_key.setObjectName(_from_utf8("cbt_use_space_key"))
        self.vly_01.addWidget(self.cbt_use_space_key)
        self.cbt_random_active = QtGui.QCheckBox(self.gbx_extra)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbt_random_active.sizePolicy().hasHeightForWidth())
        self.cbt_random_active.setSizePolicy(sizePolicy)
        self.cbt_random_active.setMinimumSize(QtCore.QSize(120, 25))
        self.cbt_random_active.setMaximumSize(QtCore.QSize(150, 25))
        self.cbt_random_active.setObjectName(_from_utf8("cbt_random_active"))
        self.vly_01.addWidget(self.cbt_random_active)
        self.horizontalLayout_3.addLayout(self.vly_01)
        self.lne_01 = QtGui.QFrame(self.gbx_extra)
        self.lne_01.setFrameShape(QtGui.QFrame.VLine)
        self.lne_01.setFrameShadow(QtGui.QFrame.Sunken)
        self.lne_01.setObjectName(_from_utf8("lne_01"))
        self.horizontalLayout_3.addWidget(self.lne_01)
        self.vly_02 = QtGui.QVBoxLayout()
        self.vly_02.setObjectName(_from_utf8("vly_02"))
        self.cbt_rest_active = QtGui.QCheckBox(self.gbx_extra)
        self.cbt_rest_active.setMinimumSize(QtCore.QSize(130, 25))
        self.cbt_rest_active.setMaximumSize(QtCore.QSize(16777215, 25))
        self.cbt_rest_active.setObjectName(_from_utf8("cbt_rest_active"))
        self.vly_02.addWidget(self.cbt_rest_active)
        self.fly_01 = QtGui.QFormLayout()
        self.fly_01.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.fly_01.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.fly_01.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fly_01.setObjectName(_from_utf8("fly_01"))
        self.lbl_rest_period = QtGui.QLabel(self.gbx_extra)
        self.lbl_rest_period.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_rest_period.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lbl_rest_period.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_rest_period.setObjectName(_from_utf8("lbl_rest_period"))
        self.fly_01.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_rest_period)
        self.isb_rest_period = QtGui.QSpinBox(self.gbx_extra)
        self.isb_rest_period.setMinimumSize(QtCore.QSize(0, 25))
        self.isb_rest_period.setMaximumSize(QtCore.QSize(16777215, 25))
        self.isb_rest_period.setMinimum(1)
        self.isb_rest_period.setMaximum(9999)
        self.isb_rest_period.setProperty("value", 1)
        self.isb_rest_period.setObjectName(_from_utf8("isb_rest_period"))
        self.fly_01.setWidget(0, QtGui.QFormLayout.FieldRole, self.isb_rest_period)
        self.lbl_rest_time = QtGui.QLabel(self.gbx_extra)
        self.lbl_rest_time.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_rest_time.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lbl_rest_time.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_rest_time.setObjectName(_from_utf8("lbl_rest_time"))
        self.fly_01.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_rest_time)
        self.dsb_rest_time = QtGui.QDoubleSpinBox(self.gbx_extra)
        self.dsb_rest_time.setMinimumSize(QtCore.QSize(0, 25))
        self.dsb_rest_time.setMaximumSize(QtCore.QSize(16777215, 25))
        self.dsb_rest_time.setMaximum(3600.0)
        self.dsb_rest_time.setProperty("value", 5.0)
        self.dsb_rest_time.setObjectName(_from_utf8("dsb_rest_time"))
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
        self.gbx_dialog.setObjectName(_from_utf8("gbx_dialog"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.gbx_dialog)
        self.verticalLayout_3.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(_from_utf8("verticalLayout_3"))
        self.cbt_dialog_active = QtGui.QCheckBox(self.gbx_dialog)
        self.cbt_dialog_active.setMinimumSize(QtCore.QSize(0, 25))
        self.cbt_dialog_active.setMaximumSize(QtCore.QSize(120, 25))
        self.cbt_dialog_active.setObjectName(_from_utf8("cbt_dialog_active"))
        self.verticalLayout_3.addWidget(self.cbt_dialog_active)
        self.fly_02 = QtGui.QFormLayout()
        self.fly_02.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.fly_02.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.fly_02.setSpacing(3)
        self.fly_02.setObjectName(_from_utf8("fly_02"))
        self.cbt_age = QtGui.QCheckBox(self.gbx_dialog)
        self.cbt_age.setMinimumSize(QtCore.QSize(90, 25))
        self.cbt_age.setMaximumSize(QtCore.QSize(120, 25))
        self.cbt_age.setObjectName(_from_utf8("cbt_age"))
        self.fly_02.setWidget(0, QtGui.QFormLayout.LabelRole, self.cbt_age)
        self.cbt_gender = QtGui.QCheckBox(self.gbx_dialog)
        self.cbt_gender.setMinimumSize(QtCore.QSize(90, 25))
        self.cbt_gender.setMaximumSize(QtCore.QSize(120, 25))
        self.cbt_gender.setObjectName(_from_utf8("cbt_gender"))
        self.fly_02.setWidget(0, QtGui.QFormLayout.FieldRole, self.cbt_gender)
        self.cbt_glasses = QtGui.QCheckBox(self.gbx_dialog)
        self.cbt_glasses.setMinimumSize(QtCore.QSize(90, 25))
        self.cbt_glasses.setMaximumSize(QtCore.QSize(120, 25))
        self.cbt_glasses.setObjectName(_from_utf8("cbt_glasses"))
        self.fly_02.setWidget(1, QtGui.QFormLayout.LabelRole, self.cbt_glasses)
        self.cbt_eyes = QtGui.QCheckBox(self.gbx_dialog)
        self.cbt_eyes.setMinimumSize(QtCore.QSize(90, 25))
        self.cbt_eyes.setMaximumSize(QtCore.QSize(120, 25))
        self.cbt_eyes.setObjectName(_from_utf8("cbt_eyes"))
        self.fly_02.setWidget(1, QtGui.QFormLayout.FieldRole, self.cbt_eyes)
        self.verticalLayout_3.addLayout(self.fly_02)
        self.hly_02.addWidget(self.gbx_dialog)
        self.verticalLayout.addLayout(self.hly_02)
        self.gbx_tests = QtGui.QGroupBox(self)
        self.gbx_tests.setMinimumSize(QtCore.QSize(0, 180))
        self.gbx_tests.setObjectName(_from_utf8("gbx_tests"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.gbx_tests)
        self.horizontalLayout.setObjectName(_from_utf8("horizontalLayout"))
        self.tbv_test = QtGui.QTableView(self.gbx_tests)
        self.tbv_test.setMinimumSize(QtCore.QSize(380, 120))
        self.tbv_test.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tbv_test.setObjectName(_from_utf8("tbv_test"))
        self.horizontalLayout.addWidget(self.tbv_test)
        self.vly_03 = QtGui.QVBoxLayout()
        self.vly_03.setSpacing(3)
        self.vly_03.setObjectName(_from_utf8("vly_03"))
        self.pbt_new = QtGui.QPushButton(self.gbx_tests)
        self.pbt_new.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_new.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_new.setObjectName(_from_utf8("pbt_new"))
        self.vly_03.addWidget(self.pbt_new)
        self.hly_03 = QtGui.QHBoxLayout()
        self.hly_03.setSpacing(4)
        self.hly_03.setObjectName(_from_utf8("hly_03"))
        self.pbt_up = QtGui.QPushButton(self.gbx_tests)
        self.pbt_up.setMinimumSize(QtCore.QSize(38, 25))
        self.pbt_up.setMaximumSize(QtCore.QSize(38, 25))
        self.pbt_up.setObjectName(_from_utf8("pbt_up"))
        self.hly_03.addWidget(self.pbt_up)
        self.pbt_down = QtGui.QPushButton(self.gbx_tests)
        self.pbt_down.setMinimumSize(QtCore.QSize(38, 25))
        self.pbt_down.setMaximumSize(QtCore.QSize(38, 25))
        self.pbt_down.setObjectName(_from_utf8("pbt_down"))
        self.hly_03.addWidget(self.pbt_down)
        self.vly_03.addLayout(self.hly_03)
        self.pbt_edit = QtGui.QPushButton(self.gbx_tests)
        self.pbt_edit.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_edit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_edit.setObjectName(_from_utf8("pbt_edit"))
        self.vly_03.addWidget(self.pbt_edit)
        self.pbt_copy = QtGui.QPushButton(self.gbx_tests)
        self.pbt_copy.setMinimumSize(QtCore.QSize(0, 25))
        self.pbt_copy.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_copy.setObjectName(_from_utf8("pbt_copy"))
        self.vly_03.addWidget(self.pbt_copy)
        self.pbt_remove = QtGui.QPushButton(self.gbx_tests)
        self.pbt_remove.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_remove.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_remove.setObjectName(_from_utf8("pbt_remove"))
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
        self.bbt_save.setObjectName(_from_utf8("bbt_save"))
        self.verticalLayout.addWidget(self.bbt_save)

        self.__retranslate_ui()
        QtCore.QObject.connect(self.bbt_save, QtCore.SIGNAL(_from_utf8("accepted()")), self.accept)
        QtCore.QObject.connect(self.bbt_save, QtCore.SIGNAL(_from_utf8("rejected()")), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def __retranslate_ui(self):
        self.setWindowTitle(_translate("ExperimentApp", "Experiment", None))
        self.gbx_experiment.setTitle(_translate("ExperimentApp", "Experiment", None))
        self.lbl_version.setText(_translate("ExperimentApp", "Version:", None))
        self.lbl_name.setText(_translate("ExperimentApp", "Name:", None))
        self.lbl_description.setText(_translate("ExperimentApp", "Description:", None))
        self.lbl_code.setText(_translate("ExperimentApp", "Code:", None))
        self.lbl_instructions.setText(_translate("ExperimentApp", "Instructions:", None))
        self.lbl_comments.setText(_translate("ExperimentApp", "Comments:", None))
        self.gbx_extra.setTitle(_translate("ExperimentApp", "Extra settings", None))
        self.cbt_use_space_key.setText(_translate("ExperimentApp", "Press space before\n"
"every test", None))
        self.cbt_random_active.setText(_translate("ExperimentApp", "Randomize tests", None))
        self.cbt_rest_active.setText(_translate("ExperimentApp", "Allow resting between\n"
"tests.", None))
        self.lbl_rest_period.setText(_translate("ExperimentApp", "Rest period:", None))
        self.lbl_rest_time.setText(_translate("ExperimentApp", "Rest time [s]:", None))
        self.gbx_dialog.setTitle(_translate("ExperimentApp", "Dialog settings", None))
        self.cbt_dialog_active.setText(_translate("ExperimentApp", "Use the dialog", None))
        self.cbt_age.setText(_translate("ExperimentApp", "Ask age", None))
        self.cbt_gender.setText(_translate("ExperimentApp", "Ask gender", None))
        self.cbt_glasses.setText(_translate("ExperimentApp", "Ask glasses", None))
        self.cbt_eyes.setText(_translate("ExperimentApp", "Ask eye color", None))
        self.gbx_tests.setTitle(_translate("ExperimentApp", "Tests", None))
        self.pbt_new.setText(_translate("ExperimentApp", "New", None))
        self.pbt_up.setText(_translate("ExperimentApp", "Up", None))
        self.pbt_down.setText(_translate("ExperimentApp", "Down", None))
        self.pbt_edit.setText(_translate("ExperimentApp", "Edit", None))
        self.pbt_copy.setText(_translate("ExperimentApp", "Copy", None))
        self.pbt_remove.setText(_translate("ExperimentApp", "Remove", None))

    # =================================
    def __setup_experiment(self):
        self.bbt_save.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.__handle_save_action)
        self.bbt_save.button(QtGui.QDialogButtonBox.Close).clicked.connect(self.__handle_close_action)
        self.pbt_new.clicked.connect(self.__handle_test_new)
        self.pbt_edit.clicked.connect(self.__handle_test_edit)
        self.pbt_copy.clicked.connect(self.__handle_test_copy)
        self.pbt_remove.clicked.connect(self.__handle_test_remove)
        self.pbt_up.clicked.connect(self.__handle_test_move_up)
        self.pbt_down.clicked.connect(self.__handle_test_move_down)

    def __handle_save_action(self):
        print u"Saving experiment..."

    def __handle_close_action(self):
        print u"Cancel operation..."

    def __handle_test_new(self):
        print u"Creating test..."
        dialog = TestApp(parent=self)
        dialog.exec_()

    def __handle_test_edit(self):
        print u"Editing test..."
        dialog = TestApp(parent=self)
        dialog.exec_()

    def __handle_test_copy(self):
        print u"Copying test..."
        dialog = TestCopyApp(parent=self)
        dialog.exec_()

    def __handle_test_remove(self):
        print u"Removing test..."

    def __handle_test_move_up(self):
        print u"Moving up test..."

    def __handle_test_move_down(self):
        print u"Moving down test..."


# ===============================================
# Class: TestApp
# ===============================================
class TestApp(QtGui.QDialog):
    def __init__(self, parent=ExperimentApp):
        QtGui.QDialog.__init__(self)
        self.__setup_ui()
        # ==============
        self.experiment = parent
        self.parent = self.experiment.parent
        # ==============
        self.__setup_test()

    # =================================
    def __setup_ui(self):
        self.setObjectName(_from_utf8("TestApp"))
        self.resize(530, 500)
        self.setMinimumSize(QtCore.QSize(530, 380))
        self.setMaximumSize(QtCore.QSize(530, 850))
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName(_from_utf8("verticalLayout"))
        self.gbx_test = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_test.sizePolicy().hasHeightForWidth())
        self.gbx_test.setSizePolicy(sizePolicy)
        self.gbx_test.setMinimumSize(QtCore.QSize(0, 145))
        self.gbx_test.setMaximumSize(QtCore.QSize(16777215, 145))
        self.gbx_test.setObjectName(_from_utf8("gbx_test"))
        self.formLayout_2 = QtGui.QFormLayout(self.gbx_test)
        self.formLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.formLayout_2.setHorizontalSpacing(5)
        self.formLayout_2.setVerticalSpacing(3)
        self.formLayout_2.setObjectName(_from_utf8("formLayout_2"))
        self.lbl_name = QtGui.QLabel(self.gbx_test)
        self.lbl_name.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_name.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_name.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_name.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_name.setObjectName(_from_utf8("lbl_name"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_name)
        self.led_name = QtGui.QLineEdit(self.gbx_test)
        self.led_name.setMinimumSize(QtCore.QSize(0, 25))
        self.led_name.setBaseSize(QtCore.QSize(0, 0))
        self.led_name.setMaxLength(50)
        self.led_name.setObjectName(_from_utf8("led_name"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.led_name)
        self.ted_description = QtGui.QPlainTextEdit(self.gbx_test)
        self.ted_description.setMinimumSize(QtCore.QSize(0, 50))
        self.ted_description.setMaximumSize(QtCore.QSize(16777215, 50))
        self.ted_description.setObjectName(_from_utf8("ted_description"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.ted_description)
        self.lbl_quantity = QtGui.QLabel(self.gbx_test)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_quantity.sizePolicy().hasHeightForWidth())
        self.lbl_quantity.setSizePolicy(sizePolicy)
        self.lbl_quantity.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_quantity.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_quantity.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_quantity.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_quantity.setObjectName(_from_utf8("lbl_quantity"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.lbl_quantity)
        self.isb_quantity = QtGui.QSpinBox(self.gbx_test)
        self.isb_quantity.setMinimumSize(QtCore.QSize(0, 25))
        self.isb_quantity.setMaximumSize(QtCore.QSize(65, 25))
        self.isb_quantity.setObjectName(_from_utf8("isb_quantity"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.isb_quantity)
        self.lbl_description = QtGui.QLabel(self.gbx_test)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_description.sizePolicy().hasHeightForWidth())
        self.lbl_description.setSizePolicy(sizePolicy)
        self.lbl_description.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_description.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_description.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_description.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_description.setObjectName(_from_utf8("lbl_description"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_description)
        self.verticalLayout.addWidget(self.gbx_test)
        self.gbx_frames = QtGui.QGroupBox(self)
        self.gbx_frames.setMinimumSize(QtCore.QSize(0, 180))
        self.gbx_frames.setObjectName(_from_utf8("gbx_frames"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.gbx_frames)
        self.horizontalLayout.setObjectName(_from_utf8("horizontalLayout"))
        self.tbv_frames = QtGui.QTableView(self.gbx_frames)
        self.tbv_frames.setMinimumSize(QtCore.QSize(380, 120))
        self.tbv_frames.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tbv_frames.setObjectName(_from_utf8("tbv_frames"))
        self.horizontalLayout.addWidget(self.tbv_frames)
        self.vly_01 = QtGui.QVBoxLayout()
        self.vly_01.setSpacing(3)
        self.vly_01.setObjectName(_from_utf8("vly_01"))
        self.pbt_new = QtGui.QPushButton(self.gbx_frames)
        self.pbt_new.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_new.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_new.setObjectName(_from_utf8("pbt_new"))
        self.vly_01.addWidget(self.pbt_new)
        self.hly_01 = QtGui.QHBoxLayout()
        self.hly_01.setSpacing(4)
        self.hly_01.setObjectName(_from_utf8("hly_01"))
        self.pbt_up = QtGui.QPushButton(self.gbx_frames)
        self.pbt_up.setMinimumSize(QtCore.QSize(38, 25))
        self.pbt_up.setMaximumSize(QtCore.QSize(38, 25))
        self.pbt_up.setObjectName(_from_utf8("pbt_up"))
        self.hly_01.addWidget(self.pbt_up)
        self.pbt_down = QtGui.QPushButton(self.gbx_frames)
        self.pbt_down.setMinimumSize(QtCore.QSize(38, 25))
        self.pbt_down.setMaximumSize(QtCore.QSize(38, 25))
        self.pbt_down.setObjectName(_from_utf8("pbt_down"))
        self.hly_01.addWidget(self.pbt_down)
        self.vly_01.addLayout(self.hly_01)
        self.pbt_edit = QtGui.QPushButton(self.gbx_frames)
        self.pbt_edit.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_edit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_edit.setObjectName(_from_utf8("pbt_edit"))
        self.vly_01.addWidget(self.pbt_edit)
        self.pbt_copy = QtGui.QPushButton(self.gbx_frames)
        self.pbt_copy.setMinimumSize(QtCore.QSize(0, 25))
        self.pbt_copy.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_copy.setObjectName(_from_utf8("pbt_copy"))
        self.vly_01.addWidget(self.pbt_copy)
        self.pbt_remove = QtGui.QPushButton(self.gbx_frames)
        self.pbt_remove.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_remove.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_remove.setObjectName(_from_utf8("pbt_remove"))
        self.vly_01.addWidget(self.pbt_remove)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vly_01.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.vly_01)
        self.verticalLayout.addWidget(self.gbx_frames)
        self.hly_02 = QtGui.QHBoxLayout()
        self.hly_02.setObjectName(_from_utf8("hly_02"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hly_02.addItem(spacerItem1)
        self.pbt_preview = QtGui.QPushButton(self)
        self.pbt_preview.setMinimumSize(QtCore.QSize(155, 25))
        self.pbt_preview.setMaximumSize(QtCore.QSize(155, 25))
        self.pbt_preview.setObjectName(_from_utf8("pbt_preview"))
        self.hly_02.addWidget(self.pbt_preview)
        self.verticalLayout.addLayout(self.hly_02)
        self.bbt_save = QtGui.QDialogButtonBox(self)
        self.bbt_save.setMinimumSize(QtCore.QSize(0, 25))
        self.bbt_save.setMaximumSize(QtCore.QSize(16777215, 25))
        self.bbt_save.setOrientation(QtCore.Qt.Horizontal)
        self.bbt_save.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.bbt_save.setObjectName(_from_utf8("bbt_save"))
        self.verticalLayout.addWidget(self.bbt_save)

        self.__retranslate_ui()
        QtCore.QObject.connect(self.bbt_save, QtCore.SIGNAL(_from_utf8("accepted()")), self.accept)
        QtCore.QObject.connect(self.bbt_save, QtCore.SIGNAL(_from_utf8("rejected()")), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def __retranslate_ui(self):
        self.setWindowTitle(_translate("TestApp", "Test", None))
        self.gbx_test.setTitle(_translate("TestApp", "Test", None))
        self.lbl_name.setText(_translate("TestApp", "Name:", None))
        self.lbl_quantity.setText(_translate("TestApp", "Quantity:", None))
        self.lbl_description.setText(_translate("TestApp", "Description:", None))
        self.gbx_frames.setTitle(_translate("TestApp", "Frames", None))
        self.pbt_new.setText(_translate("TestApp", "New", None))
        self.pbt_up.setText(_translate("TestApp", "Up", None))
        self.pbt_down.setText(_translate("TestApp", "Down", None))
        self.pbt_edit.setText(_translate("TestApp", "Edit", None))
        self.pbt_copy.setText(_translate("TestApp", "Copy", None))
        self.pbt_remove.setText(_translate("TestApp", "Remove", None))
        self.pbt_preview.setText(_translate("TestApp", "PreView", None))

    # =================================
    def __setup_test(self):
        self.bbt_save.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.__handle_save_action)
        self.bbt_save.button(QtGui.QDialogButtonBox.Close).clicked.connect(self.__handle_close_action)
        self.pbt_new.clicked.connect(self.__handle_frame_new)
        self.pbt_edit.clicked.connect(self.__handle_frame_edit)
        self.pbt_copy.clicked.connect(self.__handle_frame_copy)
        self.pbt_remove.clicked.connect(self.__handle_frame_remove)
        self.pbt_up.clicked.connect(self.__handle_frame_move_up)
        self.pbt_down.clicked.connect(self.__handle_frame_move_down)
        self.pbt_preview.clicked.connect(self.__handle_preview)

    def __handle_save_action(self):
        print u"Saving test..."

    def __handle_close_action(self):
        print u"Cancel operation..."

    def __handle_frame_new(self):
        print u"Creating frame..."
        dialog = FrameApp(parent=self)
        dialog.exec_()

    def __handle_frame_edit(self):
        print u"Editing frame..."
        dialog = FrameApp(parent=self)
        dialog.exec_()

    def __handle_frame_copy(self):
        print u"Copying frame..."

    def __handle_frame_remove(self):
        print u"Removing frame..."

    def __handle_frame_move_up(self):
        print u"Moving up frame..."

    def __handle_frame_move_down(self):
        print u"Moving down frame..."

    def __handle_preview(self):
        print u"Preview Test..."


# ===============================================
# Class: FrameApp
# ===============================================
class FrameApp(QtGui.QDialog):
    def __init__(self, parent=TestApp):
        QtGui.QDialog.__init__(self)
        self.__setup_ui()
        # ==============
        self.test = parent
        self.parent = self.test.parent
        # ==============
        self.__setup_frame()

    # =================================
    def __setup_ui(self):
        self.setObjectName(_from_utf8("FrameApp"))
        self.resize(530, 500)
        self.setMinimumSize(QtCore.QSize(530, 380))
        self.setMaximumSize(QtCore.QSize(530, 850))
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName(_from_utf8("verticalLayout"))
        self.gbx_frame = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_frame.sizePolicy().hasHeightForWidth())
        self.gbx_frame.setSizePolicy(sizePolicy)
        self.gbx_frame.setMinimumSize(QtCore.QSize(0, 120))
        self.gbx_frame.setMaximumSize(QtCore.QSize(16777215, 120))
        self.gbx_frame.setObjectName(_from_utf8("gbx_frame"))
        self.formLayout_2 = QtGui.QFormLayout(self.gbx_frame)
        self.formLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.formLayout_2.setHorizontalSpacing(5)
        self.formLayout_2.setVerticalSpacing(3)
        self.formLayout_2.setObjectName(_from_utf8("formLayout_2"))
        self.lbl_name = QtGui.QLabel(self.gbx_frame)
        self.lbl_name.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_name.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_name.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_name.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_name.setObjectName(_from_utf8("lbl_name"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_name)
        self.led_name = QtGui.QLineEdit(self.gbx_frame)
        self.led_name.setMinimumSize(QtCore.QSize(0, 25))
        self.led_name.setBaseSize(QtCore.QSize(0, 0))
        self.led_name.setMaxLength(50)
        self.led_name.setObjectName(_from_utf8("led_name"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.led_name)
        self.lbl_background = QtGui.QLabel(self.gbx_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_background.sizePolicy().hasHeightForWidth())
        self.lbl_background.setSizePolicy(sizePolicy)
        self.lbl_background.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_background.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_background.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_background.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_background.setObjectName(_from_utf8("lbl_background"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.lbl_background)
        self.cmb_background = QtGui.QComboBox(self.gbx_frame)
        self.cmb_background.setMinimumSize(QtCore.QSize(0, 25))
        self.cmb_background.setMaximumSize(QtCore.QSize(200, 25))
        self.cmb_background.setObjectName(_from_utf8("cmb_background"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.cmb_background)
        self.lbl_type = QtGui.QLabel(self.gbx_frame)
        self.lbl_type.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_type.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_type.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_type.setObjectName(_from_utf8("lbl_type"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_type)
        self.hly_01 = QtGui.QHBoxLayout()
        self.hly_01.setObjectName(_from_utf8("hly_01"))
        self.rbt_time = QtGui.QRadioButton(self.gbx_frame)
        self.rbt_time.setMinimumSize(QtCore.QSize(150, 25))
        self.rbt_time.setMaximumSize(QtCore.QSize(150, 25))
        self.rbt_time.setChecked(True)
        self.rbt_time.setObjectName(_from_utf8("rbt_time"))
        self.gbt_frame_type = QtGui.QButtonGroup(self)
        self.gbt_frame_type.setObjectName(_from_utf8("gbt_frame_type"))
        self.gbt_frame_type.addButton(self.rbt_time)
        self.hly_01.addWidget(self.rbt_time)
        self.rbt_task = QtGui.QRadioButton(self.gbx_frame)
        self.rbt_task.setMinimumSize(QtCore.QSize(150, 25))
        self.rbt_task.setMaximumSize(QtCore.QSize(150, 25))
        self.rbt_task.setObjectName(_from_utf8("rbt_task"))
        self.gbt_frame_type.addButton(self.rbt_task)
        self.hly_01.addWidget(self.rbt_task)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hly_01.addItem(spacerItem)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.hly_01)
        self.verticalLayout.addWidget(self.gbx_frame)
        self.hly_02 = QtGui.QHBoxLayout()
        self.hly_02.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.hly_02.setSpacing(5)
        self.hly_02.setObjectName(_from_utf8("hly_02"))
        self.gbx_timed = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_timed.sizePolicy().hasHeightForWidth())
        self.gbx_timed.setSizePolicy(sizePolicy)
        self.gbx_timed.setMinimumSize(QtCore.QSize(0, 90))
        self.gbx_timed.setMaximumSize(QtCore.QSize(16777215, 90))
        self.gbx_timed.setObjectName(_from_utf8("gbx_timed"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.gbx_timed)
        self.verticalLayout_2.setObjectName(_from_utf8("verticalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.fly_02 = QtGui.QFormLayout()
        self.fly_02.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.fly_02.setObjectName(_from_utf8("fly_02"))
        self.lbl_time = QtGui.QLabel(self.gbx_timed)
        self.lbl_time.setMinimumSize(QtCore.QSize(60, 25))
        self.lbl_time.setMaximumSize(QtCore.QSize(50, 25))
        self.lbl_time.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_time.setObjectName(_from_utf8("lbl_time"))
        self.fly_02.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_time)
        self.dsb_time = QtGui.QDoubleSpinBox(self.gbx_timed)
        self.dsb_time.setMinimumSize(QtCore.QSize(100, 25))
        self.dsb_time.setMaximumSize(QtCore.QSize(16777215, 25))
        self.dsb_time.setObjectName(_from_utf8("dsb_time"))
        self.fly_02.setWidget(0, QtGui.QFormLayout.FieldRole, self.dsb_time)
        self.verticalLayout_2.addLayout(self.fly_02)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.hly_02.addWidget(self.gbx_timed)
        self.gbx_task = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_task.sizePolicy().hasHeightForWidth())
        self.gbx_task.setSizePolicy(sizePolicy)
        self.gbx_task.setMinimumSize(QtCore.QSize(0, 90))
        self.gbx_task.setMaximumSize(QtCore.QSize(16777215, 90))
        self.gbx_task.setObjectName(_from_utf8("gbx_task"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.gbx_task)
        self.verticalLayout_3.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(_from_utf8("verticalLayout_3"))
        self.fly_03 = QtGui.QFormLayout()
        self.fly_03.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.fly_03.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.fly_03.setVerticalSpacing(6)
        self.fly_03.setObjectName(_from_utf8("fly_03"))
        self.led_keys_allowed = QtGui.QLineEdit(self.gbx_task)
        self.led_keys_allowed.setMinimumSize(QtCore.QSize(200, 25))
        self.led_keys_allowed.setMaximumSize(QtCore.QSize(16777215, 25))
        self.led_keys_allowed.setObjectName(_from_utf8("led_keys_allowed"))
        self.fly_03.setWidget(0, QtGui.QFormLayout.FieldRole, self.led_keys_allowed)
        self.led_keys_selected = QtGui.QLineEdit(self.gbx_task)
        self.led_keys_selected.setMinimumSize(QtCore.QSize(200, 25))
        self.led_keys_selected.setMaximumSize(QtCore.QSize(16777215, 25))
        self.led_keys_selected.setObjectName(_from_utf8("led_keys_selected"))
        self.fly_03.setWidget(1, QtGui.QFormLayout.FieldRole, self.led_keys_selected)
        self.lbl_keys_allowed = QtGui.QLabel(self.gbx_task)
        self.lbl_keys_allowed.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_keys_allowed.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_keys_allowed.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_keys_allowed.setObjectName(_from_utf8("lbl_keys_allowed"))
        self.fly_03.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_keys_allowed)
        self.lbl_keys_selected = QtGui.QLabel(self.gbx_task)
        self.lbl_keys_selected.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_keys_selected.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_keys_selected.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_keys_selected.setObjectName(_from_utf8("lbl_keys_selected"))
        self.fly_03.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_keys_selected)
        self.verticalLayout_3.addLayout(self.fly_03)
        self.hly_02.addWidget(self.gbx_task)
        self.verticalLayout.addLayout(self.hly_02)
        self.gbx_components = QtGui.QGroupBox(self)
        self.gbx_components.setMinimumSize(QtCore.QSize(0, 180))
        self.gbx_components.setObjectName(_from_utf8("gbx_components"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.gbx_components)
        self.horizontalLayout.setObjectName(_from_utf8("horizontalLayout"))
        self.tbv_component = QtGui.QTableView(self.gbx_components)
        self.tbv_component.setMinimumSize(QtCore.QSize(380, 120))
        self.tbv_component.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tbv_component.setObjectName(_from_utf8("tbv_component"))
        self.horizontalLayout.addWidget(self.tbv_component)
        self.vly_01 = QtGui.QVBoxLayout()
        self.vly_01.setSpacing(3)
        self.vly_01.setObjectName(_from_utf8("vly_01"))
        self.pbt_new = QtGui.QPushButton(self.gbx_components)
        self.pbt_new.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_new.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_new.setObjectName(_from_utf8("pbt_new"))
        self.vly_01.addWidget(self.pbt_new)
        self.hly_04 = QtGui.QHBoxLayout()
        self.hly_04.setSpacing(4)
        self.hly_04.setObjectName(_from_utf8("hly_04"))
        self.pbt_up = QtGui.QPushButton(self.gbx_components)
        self.pbt_up.setMinimumSize(QtCore.QSize(38, 25))
        self.pbt_up.setMaximumSize(QtCore.QSize(38, 25))
        self.pbt_up.setObjectName(_from_utf8("pbt_up"))
        self.hly_04.addWidget(self.pbt_up)
        self.pbt_down = QtGui.QPushButton(self.gbx_components)
        self.pbt_down.setMinimumSize(QtCore.QSize(38, 25))
        self.pbt_down.setMaximumSize(QtCore.QSize(38, 25))
        self.pbt_down.setObjectName(_from_utf8("pbt_down"))
        self.hly_04.addWidget(self.pbt_down)
        self.vly_01.addLayout(self.hly_04)
        self.pbt_edit = QtGui.QPushButton(self.gbx_components)
        self.pbt_edit.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_edit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_edit.setObjectName(_from_utf8("pbt_edit"))
        self.vly_01.addWidget(self.pbt_edit)
        self.pbt_copy = QtGui.QPushButton(self.gbx_components)
        self.pbt_copy.setMinimumSize(QtCore.QSize(0, 25))
        self.pbt_copy.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_copy.setObjectName(_from_utf8("pbt_copy"))
        self.vly_01.addWidget(self.pbt_copy)
        self.pbt_remove = QtGui.QPushButton(self.gbx_components)
        self.pbt_remove.setMinimumSize(QtCore.QSize(80, 25))
        self.pbt_remove.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_remove.setObjectName(_from_utf8("pbt_remove"))
        self.vly_01.addWidget(self.pbt_remove)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vly_01.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.vly_01)
        self.verticalLayout.addWidget(self.gbx_components)
        self.hly_03 = QtGui.QHBoxLayout()
        self.hly_03.setObjectName(_from_utf8("hly_03"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hly_03.addItem(spacerItem4)
        self.pbt_preview = QtGui.QPushButton(self)
        self.pbt_preview.setMinimumSize(QtCore.QSize(155, 25))
        self.pbt_preview.setMaximumSize(QtCore.QSize(155, 25))
        self.pbt_preview.setObjectName(_from_utf8("pbt_preview"))
        self.hly_03.addWidget(self.pbt_preview)
        self.verticalLayout.addLayout(self.hly_03)
        self.bbt_save = QtGui.QDialogButtonBox(self)
        self.bbt_save.setOrientation(QtCore.Qt.Horizontal)
        self.bbt_save.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.bbt_save.setObjectName(_from_utf8("bbt_save"))
        self.verticalLayout.addWidget(self.bbt_save)
        self.bbt_save.raise_()
        self.gbx_frame.raise_()
        self.gbx_components.raise_()

        self.__retranslate_ui()
        QtCore.QObject.connect(self.bbt_save, QtCore.SIGNAL(_from_utf8("accepted()")), self.accept)
        QtCore.QObject.connect(self.bbt_save, QtCore.SIGNAL(_from_utf8("rejected()")), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def __retranslate_ui(self):
        self.setWindowTitle(_translate("FrameApp", "Frame", None))
        self.gbx_frame.setTitle(_translate("FrameApp", "Frame", None))
        self.lbl_name.setText(_translate("FrameApp", "Name:", None))
        self.lbl_background.setText(_translate("FrameApp", "Background:", None))
        self.lbl_type.setText(_translate("FrameApp", "Type:", None))
        self.rbt_time.setText(_translate("FrameApp", "Timed", None))
        self.rbt_task.setText(_translate("FrameApp", "User response / Task", None))
        self.gbx_timed.setTitle(_translate("FrameApp", "Timed", None))
        self.lbl_time.setText(_translate("FrameApp", "Frame time:", None))
        self.gbx_task.setTitle(_translate("FrameApp", "Task", None))
        self.lbl_keys_allowed.setText(_translate("FrameApp", "Allowed keys:", None))
        self.lbl_keys_selected.setText(_translate("FrameApp", "Selected keys:", None))
        self.gbx_components.setTitle(_translate("FrameApp", "Components", None))
        self.pbt_new.setText(_translate("FrameApp", "New", None))
        self.pbt_up.setText(_translate("FrameApp", "Up", None))
        self.pbt_down.setText(_translate("FrameApp", "Down", None))
        self.pbt_edit.setText(_translate("FrameApp", "Edit", None))
        self.pbt_copy.setText(_translate("FrameApp", "Copy", None))
        self.pbt_remove.setText(_translate("FrameApp", "Remove", None))
        self.pbt_preview.setText(_translate("FrameApp", "PreView", None))

    # =================================
    def __setup_frame(self):
        self.bbt_save.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.__handle_save_action)
        self.bbt_save.button(QtGui.QDialogButtonBox.Close).clicked.connect(self.__handle_close_action)
        self.pbt_new.clicked.connect(self.__handle_component_new)
        self.pbt_edit.clicked.connect(self.__handle_component_edit)
        self.pbt_copy.clicked.connect(self.__handle_component_copy)
        self.pbt_remove.clicked.connect(self.__handle_component_remove)
        self.pbt_up.clicked.connect(self.__handle_component_move_up)
        self.pbt_down.clicked.connect(self.__handle_component_move_down)
        self.pbt_preview.clicked.connect(self.__handle_preview)

    def __handle_save_action(self):
        print u"Saving frame..."

    def __handle_close_action(self):
        print u"Cancel operation..."

    def __handle_component_new(self):
        print u"Creating component..."
        dialog = ComponentApp(parent=self)
        dialog.exec_()

    def __handle_component_edit(self):
        print u"Editing component..."
        dialog = ComponentApp(parent=self)
        dialog.exec_()

    def __handle_component_copy(self):
        print u"Copying component..."

    def __handle_component_remove(self):
        print u"Removing component..."

    def __handle_component_move_up(self):
        print u"Moving up component..."

    def __handle_component_move_down(self):
        print u"Moving down component..."

    def __handle_preview(self):
        print u"Preview Frame..."


# ===============================================
# Class: ComponentApp
# ===============================================
class ComponentApp(QtGui.QDialog):
    def __init__(self, parent=FrameApp):
        QtGui.QDialog.__init__(self)
        self.__setup_ui()
        # ==============
        self.frame = parent
        self.parent = self.frame.parent
        # ==============
        self.__setup_component()

    # =================================
    def __setup_ui(self):
        self.setObjectName(_from_utf8("ComponentApp"))
        self.resize(530, 360)
        self.setMinimumSize(QtCore.QSize(530, 360))
        self.setMaximumSize(QtCore.QSize(530, 360))
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName(_from_utf8("verticalLayout"))
        self.gbx_component = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_component.sizePolicy().hasHeightForWidth())
        self.gbx_component.setSizePolicy(sizePolicy)
        self.gbx_component.setMinimumSize(QtCore.QSize(0, 120))
        self.gbx_component.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gbx_component.setObjectName(_from_utf8("gbx_component"))
        self.formLayout_2 = QtGui.QFormLayout(self.gbx_component)
        self.formLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.formLayout_2.setHorizontalSpacing(5)
        self.formLayout_2.setVerticalSpacing(3)
        self.formLayout_2.setObjectName(_from_utf8("formLayout_2"))
        self.lbl_name = QtGui.QLabel(self.gbx_component)
        self.lbl_name.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_name.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_name.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_name.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_name.setObjectName(_from_utf8("lbl_name"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_name)
        self.led_name = QtGui.QLineEdit(self.gbx_component)
        self.led_name.setMinimumSize(QtCore.QSize(0, 25))
        self.led_name.setBaseSize(QtCore.QSize(0, 0))
        self.led_name.setMaxLength(50)
        self.led_name.setObjectName(_from_utf8("led_name"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.led_name)
        self.lbl_units = QtGui.QLabel(self.gbx_component)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_units.sizePolicy().hasHeightForWidth())
        self.lbl_units.setSizePolicy(sizePolicy)
        self.lbl_units.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_units.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_units.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_units.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_units.setObjectName(_from_utf8("lbl_units"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_units)
        self.hly_01 = QtGui.QHBoxLayout()
        self.hly_01.setSpacing(5)
        self.hly_01.setObjectName(_from_utf8("hly_01"))
        self.cmb_units = QtGui.QComboBox(self.gbx_component)
        self.cmb_units.setMinimumSize(QtCore.QSize(160, 25))
        self.cmb_units.setMaximumSize(QtCore.QSize(150, 25))
        self.cmb_units.setObjectName(_from_utf8("cmb_units"))
        self.hly_01.addWidget(self.cmb_units)
        self.lne_01 = QtGui.QFrame(self.gbx_component)
        self.lne_01.setMinimumSize(QtCore.QSize(20, 0))
        self.lne_01.setFrameShape(QtGui.QFrame.VLine)
        self.lne_01.setFrameShadow(QtGui.QFrame.Sunken)
        self.lne_01.setObjectName(_from_utf8("lne_01"))
        self.hly_01.addWidget(self.lne_01)
        self.lbl_size = QtGui.QLabel(self.gbx_component)
        self.lbl_size.setMinimumSize(QtCore.QSize(30, 25))
        self.lbl_size.setMaximumSize(QtCore.QSize(30, 25))
        self.lbl_size.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_size.setObjectName(_from_utf8("lbl_size"))
        self.hly_01.addWidget(self.lbl_size)
        self.dsb_size = QtGui.QDoubleSpinBox(self.gbx_component)
        self.dsb_size.setMinimumSize(QtCore.QSize(125, 25))
        self.dsb_size.setMaximumSize(QtCore.QSize(115, 25))
        self.dsb_size.setObjectName(_from_utf8("dsb_size"))
        self.hly_01.addWidget(self.dsb_size)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hly_01.addItem(spacerItem)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.hly_01)
        self.lbl_position = QtGui.QLabel(self.gbx_component)
        self.lbl_position.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_position.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_position.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_position.setObjectName(_from_utf8("lbl_position"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.lbl_position)
        self.hly_02 = QtGui.QHBoxLayout()
        self.hly_02.setSpacing(5)
        self.hly_02.setObjectName(_from_utf8("hly_02"))
        self.lbl_posx = QtGui.QLabel(self.gbx_component)
        self.lbl_posx.setMinimumSize(QtCore.QSize(30, 25))
        self.lbl_posx.setMaximumSize(QtCore.QSize(30, 25))
        self.lbl_posx.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_posx.setObjectName(_from_utf8("lbl_posx"))
        self.hly_02.addWidget(self.lbl_posx)
        self.dsb_posx = QtGui.QDoubleSpinBox(self.gbx_component)
        self.dsb_posx.setMinimumSize(QtCore.QSize(125, 25))
        self.dsb_posx.setMaximumSize(QtCore.QSize(115, 25))
        self.dsb_posx.setObjectName(_from_utf8("dsb_posx"))
        self.hly_02.addWidget(self.dsb_posx)
        self.lne_02 = QtGui.QFrame(self.gbx_component)
        self.lne_02.setMinimumSize(QtCore.QSize(20, 0))
        self.lne_02.setFrameShape(QtGui.QFrame.VLine)
        self.lne_02.setFrameShadow(QtGui.QFrame.Sunken)
        self.lne_02.setObjectName(_from_utf8("lne_02"))
        self.hly_02.addWidget(self.lne_02)
        self.lbl_posy = QtGui.QLabel(self.gbx_component)
        self.lbl_posy.setMinimumSize(QtCore.QSize(30, 25))
        self.lbl_posy.setMaximumSize(QtCore.QSize(30, 25))
        self.lbl_posy.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_posy.setObjectName(_from_utf8("lbl_posy"))
        self.hly_02.addWidget(self.lbl_posy)
        self.dsb_posy = QtGui.QDoubleSpinBox(self.gbx_component)
        self.dsb_posy.setMinimumSize(QtCore.QSize(125, 25))
        self.dsb_posy.setMaximumSize(QtCore.QSize(115, 25))
        self.dsb_posy.setObjectName(_from_utf8("dsb_posy"))
        self.hly_02.addWidget(self.dsb_posy)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hly_02.addItem(spacerItem1)
        self.formLayout_2.setLayout(2, QtGui.QFormLayout.FieldRole, self.hly_02)
        self.lbl_rotation = QtGui.QLabel(self.gbx_component)
        self.lbl_rotation.setObjectName(_from_utf8("lbl_rotation"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.lbl_rotation)
        self.dsb_rotation = QtGui.QDoubleSpinBox(self.gbx_component)
        self.dsb_rotation.setMinimumSize(QtCore.QSize(160, 25))
        self.dsb_rotation.setMaximumSize(QtCore.QSize(150, 25))
        self.dsb_rotation.setObjectName(_from_utf8("dsb_rotation"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.dsb_rotation)
        self.lbl_type = QtGui.QLabel(self.gbx_component)
        self.lbl_type.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_type.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_type.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_type.setObjectName(_from_utf8("lbl_type"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.lbl_type)
        self.hly_03 = QtGui.QHBoxLayout()
        self.hly_03.setSpacing(5)
        self.hly_03.setObjectName(_from_utf8("hly_03"))
        self.rbt_shape = QtGui.QRadioButton(self.gbx_component)
        self.rbt_shape.setMinimumSize(QtCore.QSize(100, 25))
        self.rbt_shape.setMaximumSize(QtCore.QSize(150, 25))
        self.rbt_shape.setChecked(True)
        self.rbt_shape.setObjectName(_from_utf8("rbt_shape"))
        self.gbt_component_type = QtGui.QButtonGroup(self)
        self.gbt_component_type.setObjectName(_from_utf8("gbt_component_type"))
        self.gbt_component_type.addButton(self.rbt_shape)
        self.hly_03.addWidget(self.rbt_shape)
        self.rbt_image = QtGui.QRadioButton(self.gbx_component)
        self.rbt_image.setMinimumSize(QtCore.QSize(100, 25))
        self.rbt_image.setMaximumSize(QtCore.QSize(150, 25))
        self.rbt_image.setObjectName(_from_utf8("rbt_image"))
        self.gbt_component_type.addButton(self.rbt_image)
        self.hly_03.addWidget(self.rbt_image)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hly_03.addItem(spacerItem2)
        self.formLayout_2.setLayout(4, QtGui.QFormLayout.FieldRole, self.hly_03)
        self.verticalLayout.addWidget(self.gbx_component)
        self.hly_04 = QtGui.QHBoxLayout()
        self.hly_04.setObjectName(_from_utf8("hly_04"))
        self.gbx_shape = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_shape.sizePolicy().hasHeightForWidth())
        self.gbx_shape.setSizePolicy(sizePolicy)
        self.gbx_shape.setMinimumSize(QtCore.QSize(0, 0))
        self.gbx_shape.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gbx_shape.setObjectName(_from_utf8("gbx_shape"))
        self.formLayout = QtGui.QFormLayout(self.gbx_shape)
        self.formLayout.setObjectName(_from_utf8("formLayout"))
        self.lbl_shape = QtGui.QLabel(self.gbx_shape)
        self.lbl_shape.setMinimumSize(QtCore.QSize(50, 25))
        self.lbl_shape.setMaximumSize(QtCore.QSize(50, 25))
        self.lbl_shape.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_shape.setObjectName(_from_utf8("lbl_shape"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_shape)
        self.lbl_shape_color = QtGui.QLabel(self.gbx_shape)
        self.lbl_shape_color.setMinimumSize(QtCore.QSize(50, 25))
        self.lbl_shape_color.setMaximumSize(QtCore.QSize(50, 25))
        self.lbl_shape_color.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_shape_color.setObjectName(_from_utf8("lbl_shape_color"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_shape_color)
        self.cmb_shape_color = QtGui.QComboBox(self.gbx_shape)
        self.cmb_shape_color.setMinimumSize(QtCore.QSize(0, 25))
        self.cmb_shape_color.setMaximumSize(QtCore.QSize(150, 25))
        self.cmb_shape_color.setObjectName(_from_utf8("cmb_shape_color"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.cmb_shape_color)
        self.cmb_shape = QtGui.QComboBox(self.gbx_shape)
        self.cmb_shape.setMinimumSize(QtCore.QSize(0, 25))
        self.cmb_shape.setMaximumSize(QtCore.QSize(150, 25))
        self.cmb_shape.setObjectName(_from_utf8("cmb_shape"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cmb_shape)
        self.hly_04.addWidget(self.gbx_shape)
        self.gbx_image = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_image.sizePolicy().hasHeightForWidth())
        self.gbx_image.setSizePolicy(sizePolicy)
        self.gbx_image.setObjectName(_from_utf8("gbx_image"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.gbx_image)
        self.horizontalLayout_4.setObjectName(_from_utf8("horizontalLayout_4"))
        self.lbl_image_status = QtGui.QLabel(self.gbx_image)
        self.lbl_image_status.setMinimumSize(QtCore.QSize(120, 60))
        self.lbl_image_status.setMaximumSize(QtCore.QSize(70, 60))
        self.lbl_image_status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_image_status.setObjectName(_from_utf8("lbl_image_status"))
        self.horizontalLayout_4.addWidget(self.lbl_image_status)
        self.vly_01 = QtGui.QVBoxLayout()
        self.vly_01.setSpacing(3)
        self.vly_01.setObjectName(_from_utf8("vly_01"))
        self.pbt_image_open = QtGui.QPushButton(self.gbx_image)
        self.pbt_image_open.setMinimumSize(QtCore.QSize(0, 25))
        self.pbt_image_open.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_image_open.setObjectName(_from_utf8("pbt_image_open"))
        self.vly_01.addWidget(self.pbt_image_open)
        self.pbt_image_zoom = QtGui.QPushButton(self.gbx_image)
        self.pbt_image_zoom.setMinimumSize(QtCore.QSize(0, 25))
        self.pbt_image_zoom.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_image_zoom.setObjectName(_from_utf8("pbt_image_zoom"))
        self.vly_01.addWidget(self.pbt_image_zoom)
        self.horizontalLayout_4.addLayout(self.vly_01)
        self.hly_04.addWidget(self.gbx_image)
        self.verticalLayout.addLayout(self.hly_04)
        self.hly_05 = QtGui.QHBoxLayout()
        self.hly_05.setObjectName(_from_utf8("hly_05"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hly_05.addItem(spacerItem3)
        self.pbt_preview = QtGui.QPushButton(self)
        self.pbt_preview.setMinimumSize(QtCore.QSize(155, 25))
        self.pbt_preview.setMaximumSize(QtCore.QSize(155, 25))
        self.pbt_preview.setObjectName(_from_utf8("pbt_preview"))
        self.hly_05.addWidget(self.pbt_preview)
        self.verticalLayout.addLayout(self.hly_05)
        self.bbt_save = QtGui.QDialogButtonBox(self)
        self.bbt_save.setMinimumSize(QtCore.QSize(0, 25))
        self.bbt_save.setMaximumSize(QtCore.QSize(16777215, 25))
        self.bbt_save.setOrientation(QtCore.Qt.Horizontal)
        self.bbt_save.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.bbt_save.setObjectName(_from_utf8("bbt_save"))
        self.verticalLayout.addWidget(self.bbt_save)
        self.bbt_save.raise_()
        self.gbx_component.raise_()

        self.__retranslate_ui()
        QtCore.QObject.connect(self.bbt_save, QtCore.SIGNAL(_from_utf8("accepted()")), self.accept)
        QtCore.QObject.connect(self.bbt_save, QtCore.SIGNAL(_from_utf8("rejected()")), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def __retranslate_ui(self):
        self.setWindowTitle(_translate("ComponentApp", "Component", None))
        self.gbx_component.setTitle(_translate("ComponentApp", "Component", None))
        self.lbl_name.setText(_translate("ComponentApp", "Name:", None))
        self.lbl_units.setText(_translate("ComponentApp", "Units:", None))
        self.lbl_size.setText(_translate("ComponentApp", "Size:", None))
        self.lbl_position.setText(_translate("ComponentApp", "Position:", None))
        self.lbl_posx.setText(_translate("ComponentApp", "X:", None))
        self.lbl_posy.setText(_translate("ComponentApp", "Y:", None))
        self.lbl_rotation.setText(_translate("ComponentApp", "Rotation:", None))
        self.lbl_type.setText(_translate("ComponentApp", "Type:", None))
        self.rbt_shape.setText(_translate("ComponentApp", "Shape", None))
        self.rbt_image.setText(_translate("ComponentApp", "Image", None))
        self.gbx_shape.setTitle(_translate("ComponentApp", "Shape", None))
        self.lbl_shape.setText(_translate("ComponentApp", "Shape:", None))
        self.lbl_shape_color.setText(_translate("ComponentApp", "Color:", None))
        self.gbx_image.setTitle(_translate("ComponentApp", "Image", None))
        self.lbl_image_status.setText(_translate("ComponentApp", "No Image", None))
        self.pbt_image_open.setText(_translate("ComponentApp", "Open", None))
        self.pbt_image_zoom.setText(_translate("ComponentApp", "Zoom", None))
        self.pbt_preview.setText(_translate("ComponentApp", "PreView", None))

    # =================================
    def __setup_component(self):
        self.bbt_save.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.__handle_save_action)
        self.bbt_save.button(QtGui.QDialogButtonBox.Close).clicked.connect(self.__handle_close_action)
        self.pbt_image_open.clicked.connect(self.__handle_image_open)
        self.pbt_image_zoom.clicked.connect(self.__handle_image_zoom)
        self.pbt_preview.clicked.connect(self.__handle_preview)

    def __handle_save_action(self):
        print u"Saving component..."

    def __handle_close_action(self):
        print u"Cancel operation..."

    def __handle_image_open(self):
        print u"Browse for a new image..."

    def __handle_image_zoom(self):
        print u"Open zoomed image..."

    def __handle_preview(self):
        print u"Preview Component..."


# =============================================================================
# Configuration related Class: ConfigurationApp
# =============================================================================
class ConfigurationApp(QtGui.QDialog):
    def __init__(self, parent=SaccadeApp, item_id=-1):
        QtGui.QDialog.__init__(self)
        self.__setup_ui()
        # -------------------
        self.__is_edit = False
        self.__item_id = item_id
        # -------------------
        self.__parent = parent
        self.__profile = Configuration(db=parent.database)
        self.__model_tracker = ListModel(Utils.get_available_trackers())
        self.__model_monitor = ListModel(Utils.get_available_monitors())
        self.__model_screen = ListModel(Utils.get_available_screens())
        # -------------------
        self.__setup_dialog()
        self.__check_itemid()

    # =================================
    def __setup_ui(self):
        self.setObjectName(_from_utf8("ConfigurationApp"))
        self.resize(530, 230)
        self.setMinimumSize(QtCore.QSize(530, 230))
        self.setMaximumSize(QtCore.QSize(530, 230))
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName(_from_utf8("verticalLayout"))
        self.gbox_configuration = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbox_configuration.sizePolicy().hasHeightForWidth())
        self.gbox_configuration.setSizePolicy(sizePolicy)
        self.gbox_configuration.setMinimumSize(QtCore.QSize(0, 180))
        self.gbox_configuration.setMaximumSize(QtCore.QSize(16777215, 180))
        self.gbox_configuration.setObjectName(_from_utf8("gbox_configuration"))
        self.formLayout_2 = QtGui.QFormLayout(self.gbox_configuration)
        self.formLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.formLayout_2.setHorizontalSpacing(5)
        self.formLayout_2.setVerticalSpacing(3)
        self.formLayout_2.setObjectName(_from_utf8("formLayout_2"))
        self.lbl_name = QtGui.QLabel(self.gbox_configuration)
        self.lbl_name.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_name.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_name.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_name.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_name.setObjectName(_from_utf8("lbl_name"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_name)
        self.lbl_screen = QtGui.QLabel(self.gbox_configuration)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_screen.sizePolicy().hasHeightForWidth())
        self.lbl_screen.setSizePolicy(sizePolicy)
        self.lbl_screen.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_screen.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_screen.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_screen.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_screen.setObjectName(_from_utf8("lbl_screen"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.lbl_screen)
        self.lbl_monitor = QtGui.QLabel(self.gbox_configuration)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_monitor.sizePolicy().hasHeightForWidth())
        self.lbl_monitor.setSizePolicy(sizePolicy)
        self.lbl_monitor.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_monitor.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_monitor.setBaseSize(QtCore.QSize(0, 0))
        self.lbl_monitor.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_monitor.setObjectName(_from_utf8("lbl_monitor"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.lbl_monitor)
        self.lbl_tracker = QtGui.QLabel(self.gbox_configuration)
        self.lbl_tracker.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_tracker.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_tracker.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_tracker.setObjectName(_from_utf8("lbl_tracker"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.lbl_tracker)
        self.led_name = QtGui.QLineEdit(self.gbox_configuration)
        self.led_name.setMinimumSize(QtCore.QSize(0, 25))
        self.led_name.setMaximumSize(QtCore.QSize(16777215, 25))
        self.led_name.setObjectName(_from_utf8("led_name"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.led_name)
        self.lbl_path = QtGui.QLabel(self.gbox_configuration)
        self.lbl_path.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_path.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_path.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_path.setObjectName(_from_utf8("lbl_path"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_path)
        self.cmb_monitor = QtGui.QComboBox(self.gbox_configuration)
        self.cmb_monitor.setMinimumSize(QtCore.QSize(0, 25))
        self.cmb_monitor.setMaximumSize(QtCore.QSize(16777215, 25))
        self.cmb_monitor.setObjectName(_from_utf8("cmb_monitor"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.cmb_monitor)
        self.cmb_screen = QtGui.QComboBox(self.gbox_configuration)
        self.cmb_screen.setMinimumSize(QtCore.QSize(0, 25))
        self.cmb_screen.setMaximumSize(QtCore.QSize(16777215, 25))
        self.cmb_screen.setObjectName(_from_utf8("cmb_screen"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.cmb_screen)
        self.cmb_tracker = QtGui.QComboBox(self.gbox_configuration)
        self.cmb_tracker.setMinimumSize(QtCore.QSize(0, 25))
        self.cmb_tracker.setMaximumSize(QtCore.QSize(16777215, 25))
        self.cmb_tracker.setObjectName(_from_utf8("cmb_tracker"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.cmb_tracker)
        self.hly_01 = QtGui.QHBoxLayout()
        self.hly_01.setObjectName(_from_utf8("hly_01"))
        self.led_path = QtGui.QLineEdit(self.gbox_configuration)
        self.led_path.setMinimumSize(QtCore.QSize(0, 25))
        self.led_path.setMaximumSize(QtCore.QSize(16777215, 25))
        self.led_path.setReadOnly(True)
        self.led_path.setObjectName(_from_utf8("led_path"))
        self.hly_01.addWidget(self.led_path)
        self.pbt_path_browse = QtGui.QPushButton(self.gbox_configuration)
        self.pbt_path_browse.setMinimumSize(QtCore.QSize(0, 25))
        self.pbt_path_browse.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pbt_path_browse.setObjectName(_from_utf8("pbt_path_browse"))
        self.hly_01.addWidget(self.pbt_path_browse)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.hly_01)
        self.verticalLayout.addWidget(self.gbox_configuration)
        self.bbt_save = QtGui.QDialogButtonBox(self)
        self.bbt_save.setMinimumSize(QtCore.QSize(0, 25))
        self.bbt_save.setMaximumSize(QtCore.QSize(16777215, 25))
        self.bbt_save.setOrientation(QtCore.Qt.Horizontal)
        self.bbt_save.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.bbt_save.setObjectName(_from_utf8("bbt_save"))
        self.verticalLayout.addWidget(self.bbt_save)

        self.__retranslate_ui()
        QtCore.QObject.connect(self.bbt_save, QtCore.SIGNAL(_from_utf8("accepted()")), self.accept)
        QtCore.QObject.connect(self.bbt_save, QtCore.SIGNAL(_from_utf8("rejected()")), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def __retranslate_ui(self):
        self.setWindowTitle(_translate("ConfigurationApp", "Configuration Profile", None))
        self.gbox_configuration.setTitle(_translate("ConfigurationApp", "Configuration Profile", None))
        self.lbl_name.setText(_translate("ConfigurationApp", "Name:", None))
        self.lbl_screen.setText(_translate("ConfigurationApp", "Screen:", None))
        self.lbl_monitor.setText(_translate("ConfigurationApp", "Monitor:", None))
        self.lbl_tracker.setText(_translate("ConfigurationApp", "Eye Tracker:", None))
        self.lbl_path.setText(_translate("ConfigurationApp", "Events Path:", None))
        self.pbt_path_browse.setText(_translate("ConfigurationApp", "Browse...", None))

    # =================================
    def __setup_dialog(self):
        self.bbt_save.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.__handle_save_action)
        self.bbt_save.button(QtGui.QDialogButtonBox.Close).clicked.connect(self.__handle_close_action)
        self.pbt_path_browse.clicked.connect(self.__handle_path_browse)
        self.cmb_tracker.setModel(self.__model_tracker)
        self.cmb_monitor.setModel(self.__model_monitor)
        self.cmb_screen.setModel(self.__model_screen)

    def __handle_save_action(self):
        print u"Saving configuration profile..."
        self.__profile.set_experiment_path(unicode(self.led_path.text()))
        self.__profile.set_monitor(self.cmb_monitor.currentText())
        self.__profile.set_tracker(self.cmb_tracker.currentText())
        self.__profile.set_screen(self.cmb_screen.currentIndex())

        old_name = self.__profile.get_name()
        new_name = unicode(self.led_name.text())
        is_name_ok = self.__profile.set_name(new_name)
        if self.__is_edit:
            if old_name == new_name:            # Edit maintain name
                self.__profile.save()
            elif is_name_ok:                    # Edit and change name
                self.__remove_profile(old_name)
                self.__profile.save()
        elif is_name_ok:                        # New profile and name is not used
            self.__profile.save()

        if not self.__profile.is_on_database(): # Profile already exists...
            print u"Error: Name already used..."
            err_msg = u"Name already used. Do you want to overwrite?"
            err_res = QtGui.QMessageBox.question(self, u"Error", err_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if err_res == QtGui.QMessageBox.Yes:                # Overwrite!
                print u"Configuration profile overwritten!"
                if self.__is_edit:
                    self.__remove_profile(old_name)
                self.__remove_profile(new_name)
                self.__profile.set_name(new_name)
                self.__profile.save()
            else:                                               # Find new name!
                print u"Waiting for new name..."
                is_ready = False
                while not is_ready:
                    new_name, is_ok = QtGui.QInputDialog.getText(None, u'New profile name', u'New name:', text=new_name)
                    new_name = unicode(new_name)
                    if is_ok:
                        if self.__profile.set_name(new_name):
                            print u"New name defined. Saving profile..."
                            self.__profile.save()
                    else:
                        print u"Operation canceled..."
                        new_name = None
                        is_ready = True
        if self.__profile.is_on_database():
            self.__parent.update_configuration_view()
            index = self.__parent.model_configuration.get_index(new_name)
            self.__parent.lsv_configuration.setCurrentIndex(self.__parent.model_configuration.index(index, 0))

    def __handle_close_action(self):
        print u"Operation canceled..."
        if self.__is_edit:
            self.__parent.lsv_configuration.setCurrentIndex(self.__parent.model_configuration.index(self.__item_id, 0))

    def __handle_path_browse(self):
        print u"Browsing for new events folder..."
        title = u"Select events save directory..."
        folder = QtGui.QFileDialog.getExistingDirectory(self, title, self.led_path.text(),
                                                        QtGui.QFileDialog.ShowDirsOnly)
        if folder:
            print u"Folder selected."
            self.led_path.setText(unicode(folder))
        else:
            print u"Operation canceled..."

    def __check_itemid(self):
        if self.__item_id is not -1:
            self.__is_edit = True
            self.__profile.load(self.__parent.model_configuration.get_item(index=self.__item_id))
            screen_index = self.cmb_screen.findText(self.__profile.get_screen(), QtCore.Qt.MatchFixedString)
            monitor_index = self.cmb_monitor.findText(self.__profile.get_monitor(), QtCore.Qt.MatchFixedString)
            tracker_index = self.cmb_tracker.findText(self.__profile.get_tracker_name(), QtCore.Qt.MatchFixedString)
            self.cmb_screen.setCurrentIndex(screen_index)
            self.cmb_monitor.setCurrentIndex(monitor_index)
            self.cmb_tracker.setCurrentIndex(tracker_index)
        self.led_name.setText(self.__profile.get_name())
        self.led_path.setText(self.__profile.get_experiment_path())

    def __remove_profile(self, name):
        profile = Configuration(db=self.__parent.database, name=name)
        profile.remove()


# =============================================================================
# Utility Classes:
# =============================================================================
# ===============================================
# Class: ExperimentCopyApp
# ===============================================
class ExperimentCopyApp(QtGui.QDialog):
    def __init__(self, parent=ExperimentApp):
        QtGui.QDialog.__init__(self)
        self.__setup_ui()
        # ==============
        self.parent = parent
        # ==============
        self.__setup_copy()

    # =================================
    def __setup_ui(self):
        self.setObjectName(_from_utf8("ExperimentCopyApp"))
        self.resize(400, 140)
        self.setMinimumSize(QtCore.QSize(400, 140))
        self.setMaximumSize(QtCore.QSize(400, 140))
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName(_from_utf8("verticalLayout"))
        self.gbx_copy = QtGui.QGroupBox(self)
        self.gbx_copy.setObjectName(_from_utf8("gbx_copy"))
        self.formLayout = QtGui.QFormLayout(self.gbx_copy)
        self.formLayout.setObjectName(_from_utf8("formLayout"))
        self.lbl_code = QtGui.QLabel(self.gbx_copy)
        self.lbl_code.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_code.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_code.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_code.setObjectName(_from_utf8("lbl_code"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_code)
        self.led_code = QtGui.QLineEdit(self.gbx_copy)
        self.led_code.setMinimumSize(QtCore.QSize(0, 25))
        self.led_code.setMaximumSize(QtCore.QSize(16777215, 25))
        self.led_code.setMaxLength(10)
        self.led_code.setObjectName(_from_utf8("led_code"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.led_code)
        self.lbl_version = QtGui.QLabel(self.gbx_copy)
        self.lbl_version.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_version.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_version.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_version.setObjectName(_from_utf8("lbl_version"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_version)
        self.led_version = QtGui.QLineEdit(self.gbx_copy)
        self.led_version.setMinimumSize(QtCore.QSize(0, 25))
        self.led_version.setMaximumSize(QtCore.QSize(16777215, 25))
        self.led_version.setMaxLength(10)
        self.led_version.setObjectName(_from_utf8("led_version"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.led_version)
        self.verticalLayout.addWidget(self.gbx_copy)
        self.bbt_dialog = QtGui.QDialogButtonBox(self)
        self.bbt_dialog.setOrientation(QtCore.Qt.Horizontal)
        self.bbt_dialog.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbt_dialog.setObjectName(_from_utf8("bbt_dialog"))
        self.verticalLayout.addWidget(self.bbt_dialog)

        self.__retranslate_ui()
        QtCore.QObject.connect(self.bbt_dialog, QtCore.SIGNAL(_from_utf8("accepted()")), self.accept)
        QtCore.QObject.connect(self.bbt_dialog, QtCore.SIGNAL(_from_utf8("rejected()")), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def __retranslate_ui(self):
        self.setWindowTitle(_translate("ExperimentCopyApp", "Copy", None))
        self.gbx_copy.setTitle(_translate("ExperimentCopyApp", "Experiment copy...", None))
        self.lbl_code.setText(_translate("ExperimentCopyApp", "New Code:", None))
        self.lbl_version.setText(_translate("ExperimentCopyApp", "New Version:", None))

    # =================================
    def __setup_copy(self):
        self.bbt_dialog.clicked.connect(self.__handle_ok_box)

    def __handle_ok_box(self):
        if self.bbt_dialog.Ok:
            pass
        if self.bbt_dialog.Cancel:
            pass


# ===============================================
# Class: TestCopyApp
# ===============================================
class TestCopyApp(QtGui.QDialog):
    def __init__(self, parent=TestApp):
        QtGui.QDialog.__init__(self)
        self.__setup_ui()
        # ==============
        self.parent = parent
        # ==============
        self.__setup_copy()

    # =================================
    def __setup_ui(self):
        self.setObjectName(_from_utf8("TestCopyApp"))
        self.resize(400, 200)
        self.setMinimumSize(QtCore.QSize(400, 200))
        self.setMaximumSize(QtCore.QSize(400, 200))
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName(_from_utf8("verticalLayout"))
        self.gbx_copy = QtGui.QGroupBox(self)
        self.gbx_copy.setObjectName(_from_utf8("gbx_copy"))
        self.formLayout = QtGui.QFormLayout(self.gbx_copy)
        self.formLayout.setObjectName(_from_utf8("formLayout"))
        self.lbl_name = QtGui.QLabel(self.gbx_copy)
        self.lbl_name.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_name.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_name.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_name.setObjectName(_from_utf8("lbl_name"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_name)
        self.led_name = QtGui.QLineEdit(self.gbx_copy)
        self.led_name.setMinimumSize(QtCore.QSize(0, 25))
        self.led_name.setMaximumSize(QtCore.QSize(16777215, 25))
        self.led_name.setObjectName(_from_utf8("led_name"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.led_name)
        self.lbl_copy_from = QtGui.QLabel(self.gbx_copy)
        self.lbl_copy_from.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_copy_from.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_copy_from.setObjectName(_from_utf8("lbl_copy_from"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_copy_from)
        self.hly_01 = QtGui.QHBoxLayout()
        self.hly_01.setObjectName(_from_utf8("hly_01"))
        self.rbt_selection = QtGui.QRadioButton(self.gbx_copy)
        self.rbt_selection.setMinimumSize(QtCore.QSize(0, 25))
        self.rbt_selection.setMaximumSize(QtCore.QSize(16777215, 25))
        self.rbt_selection.setChecked(True)
        self.rbt_selection.setObjectName(_from_utf8("rbt_selection"))
        self.gbt_copy_from = QtGui.QButtonGroup(self)
        self.gbt_copy_from.setObjectName(_from_utf8("gbt_copy_from"))
        self.gbt_copy_from.addButton(self.rbt_selection)
        self.hly_01.addWidget(self.rbt_selection)
        self.rbt_experiment = QtGui.QRadioButton(self.gbx_copy)
        self.rbt_experiment.setMinimumSize(QtCore.QSize(0, 25))
        self.rbt_experiment.setMaximumSize(QtCore.QSize(16777215, 25))
        self.rbt_experiment.setObjectName(_from_utf8("rbt_experiment"))
        self.gbt_copy_from.addButton(self.rbt_experiment)
        self.hly_01.addWidget(self.rbt_experiment)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.hly_01)
        self.cmb_experiment = QtGui.QComboBox(self.gbx_copy)
        self.cmb_experiment.setMinimumSize(QtCore.QSize(0, 25))
        self.cmb_experiment.setMaximumSize(QtCore.QSize(16777215, 25))
        self.cmb_experiment.setObjectName(_from_utf8("cmb_experiment"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cmb_experiment)
        self.cmb_test = QtGui.QComboBox(self.gbx_copy)
        self.cmb_test.setMinimumSize(QtCore.QSize(0, 25))
        self.cmb_test.setMaximumSize(QtCore.QSize(16777215, 25))
        self.cmb_test.setObjectName(_from_utf8("cmb_test"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.cmb_test)
        self.lbl_experiment = QtGui.QLabel(self.gbx_copy)
        self.lbl_experiment.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_experiment.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_experiment.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_experiment.setObjectName(_from_utf8("lbl_experiment"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.lbl_experiment)
        self.lbl_test = QtGui.QLabel(self.gbx_copy)
        self.lbl_test.setMinimumSize(QtCore.QSize(70, 25))
        self.lbl_test.setMaximumSize(QtCore.QSize(70, 25))
        self.lbl_test.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_test.setObjectName(_from_utf8("lbl_test"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.lbl_test)
        self.verticalLayout.addWidget(self.gbx_copy)
        self.bbt_dialog = QtGui.QDialogButtonBox(self)
        self.bbt_dialog.setOrientation(QtCore.Qt.Horizontal)
        self.bbt_dialog.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbt_dialog.setObjectName(_from_utf8("bbt_dialog"))
        self.verticalLayout.addWidget(self.bbt_dialog)

        self.__retranslate_ui()
        QtCore.QObject.connect(self.bbt_dialog, QtCore.SIGNAL(_from_utf8("accepted()")), self.accept)
        QtCore.QObject.connect(self.bbt_dialog, QtCore.SIGNAL(_from_utf8("rejected()")), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def __retranslate_ui(self):
        self.setWindowTitle(_translate("TestCopyApp", "Copy", None))
        self.gbx_copy.setTitle(_translate("TestCopyApp", "Copy", None))
        self.lbl_name.setText(_translate("TestCopyApp", "New Name:", None))
        self.lbl_copy_from.setText(_translate("TestCopyApp", "Copy from: ", None))
        self.rbt_selection.setText(_translate("TestCopyApp", "Selection...", None))
        self.rbt_experiment.setText(_translate("TestCopyApp", "Experiment...", None))
        self.lbl_experiment.setText(_translate("TestCopyApp", "Experiment:", None))
        self.lbl_test.setText(_translate("TestCopyApp", "Test:", None))

    # =================================
    def __setup_copy(self):
        self.bbt_dialog.clicked.connect(self.__handle_ok_box)

    def __handle_ok_box(self):
        if self.bbt_dialog.Ok:
            pass
        if self.bbt_dialog.Cancel:
            pass


# ===============================================
# Class: About
# ===============================================
class AboutApp(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self._setup_ui()

    # =================================
    def _setup_ui(self):
        self.setObjectName(_from_utf8("AboutApp"))
        self.resize(283, 256)
        self.verticalLayout_2 = QtGui.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName(_from_utf8("verticalLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.lbl_app_name = QtGui.QLabel(self)
        self.lbl_app_name.setMinimumSize(QtCore.QSize(0, 50))
        self.lbl_app_name.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_app_name.setFont(font)
        self.lbl_app_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_app_name.setObjectName(_from_utf8("lbl_app_name"))
        self.verticalLayout_2.addWidget(self.lbl_app_name)
        self.lbl_app_version = QtGui.QLabel(self)
        self.lbl_app_version.setMinimumSize(QtCore.QSize(0, 25))
        self.lbl_app_version.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_app_version.setFont(font)
        self.lbl_app_version.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_app_version.setObjectName(_from_utf8("lbl_app_version"))
        self.verticalLayout_2.addWidget(self.lbl_app_version)
        self.line = QtGui.QFrame(self)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_from_utf8("line"))
        self.verticalLayout_2.addWidget(self.line)
        self.hly_01 = QtGui.QHBoxLayout()
        self.hly_01.setSpacing(5)
        self.hly_01.setObjectName(_from_utf8("hly_01"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hly_01.addItem(spacerItem1)
        self.fly_01 = QtGui.QFormLayout()
        self.fly_01.setHorizontalSpacing(3)
        self.fly_01.setVerticalSpacing(5)
        self.fly_01.setObjectName(_from_utf8("fly_01"))
        self.lbl_author = QtGui.QLabel(self)
        self.lbl_author.setMinimumSize(QtCore.QSize(40, 20))
        self.lbl_author.setMaximumSize(QtCore.QSize(40, 20))
        self.lbl_author.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_author.setObjectName(_from_utf8("lbl_author"))
        self.fly_01.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_author)
        self.lbl_author_dat = QtGui.QLabel(self)
        self.lbl_author_dat.setMinimumSize(QtCore.QSize(0, 20))
        self.lbl_author_dat.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lbl_author_dat.setObjectName(_from_utf8("lbl_author_dat"))
        self.fly_01.setWidget(0, QtGui.QFormLayout.FieldRole, self.lbl_author_dat)
        self.lbl_mail = QtGui.QLabel(self)
        self.lbl_mail.setMinimumSize(QtCore.QSize(40, 20))
        self.lbl_mail.setMaximumSize(QtCore.QSize(40, 20))
        self.lbl_mail.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_mail.setObjectName(_from_utf8("lbl_mail"))
        self.fly_01.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_mail)
        self.lbl_mail_dat = QtGui.QLabel(self)
        self.lbl_mail_dat.setMinimumSize(QtCore.QSize(0, 20))
        self.lbl_mail_dat.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lbl_mail_dat.setObjectName(_from_utf8("lbl_mail_dat"))
        self.fly_01.setWidget(1, QtGui.QFormLayout.FieldRole, self.lbl_mail_dat)
        self.hly_01.addLayout(self.fly_01)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hly_01.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.hly_01)
        self.bbt_close = QtGui.QDialogButtonBox(self)
        self.bbt_close.setOrientation(QtCore.Qt.Horizontal)
        self.bbt_close.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.bbt_close.setCenterButtons(True)
        self.bbt_close.setObjectName(_from_utf8("bbt_close"))
        self.verticalLayout_2.addWidget(self.bbt_close)

        self._retranslate_ui()
        QtCore.QObject.connect(self.bbt_close, QtCore.SIGNAL(_from_utf8("accepted()")), self.accept)
        QtCore.QObject.connect(self.bbt_close, QtCore.SIGNAL(_from_utf8("rejected()")), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def _retranslate_ui(self):
        self.setWindowTitle(_translate("AboutApp", "About", None))
        self.lbl_app_name.setText(_translate("AboutApp", "saccadeapp", None))
        self.lbl_app_version.setText(_translate("AboutApp", "v1.0", None))
        self.lbl_author.setText(_translate("AboutApp", "Author:", None))
        self.lbl_author_dat.setText(_translate("AboutApp", "Christian Wiche", None))
        self.lbl_mail.setText(_translate("AboutApp", "Mail:", None))
        self.lbl_mail_dat.setText(_translate("AboutApp", "cwichel@gmail.com", None))

    # =================================
