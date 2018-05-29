# -*- coding: utf-8 -*-
# =============================================================================
# Modules
# =============================================================================
import sys
from PyQt4 import QtCore, QtGui, uic

# ===========================
# Internal:
# ===========================
from gui_models import *
from saccadeapp.core import *
from saccadeapp.script import *

# =============================================================================
# Qt GUI Modules
# =============================================================================
gui_folder = Utils.get_file_path()+u"/resources/gui_files/"
SaccadeBase, SaccadeForm = uic.loadUiType(Utils.format_path(gui_folder+u"saccadeApp.ui"))
ExperimentBase, ExperimentForm = uic.loadUiType(Utils.format_path(gui_folder+u"experiment.ui"))
TestBase, TestForm = uic.loadUiType(Utils.format_path(gui_folder+u"test.ui"))
FrameBase, FrameForm = uic.loadUiType(Utils.format_path(gui_folder+u"frame.ui"))
ComponentBase, ComponentForm = uic.loadUiType(Utils.format_path(gui_folder+u"component.ui"))
ConfigurationBase, ConfigurationForm = uic.loadUiType(Utils.format_path(gui_folder+u"configuration.ui"))
ExperimentCopyBase, ExperimentCopyForm = uic.loadUiType(Utils.format_path(gui_folder+u"copy_experiment.ui"))
TestCopyBase, TestCopyForm = uic.loadUiType(Utils.format_path(gui_folder+u"copy_test.ui"))
ItemListCopyBase, ItemListCopyForm = uic.loadUiType(Utils.format_path(gui_folder+u"copy_listitem.ui"))
SequenceItemBase, SequenceItemForm = uic.loadUiType(Utils.format_path(gui_folder+u"sequence_item.ui"))
AboutBase, AboutForm = uic.loadUiType(Utils.format_path(gui_folder+u"about.ui"))


# =============================================================================
# Main App Class: saccadeapp
# =============================================================================
class SaccadeApp(SaccadeBase, SaccadeForm):
    def __init__(self):
        super(SaccadeApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.database = SaccadeDB()
        self.model_configuration = ListModel(items=[], header=u"Profile")
        self.model_experiment = ExperimentTreeModel(items=None)
        # -------------------
        self.__setup_menu()
        self.__setup_configuration()
        self.__setup_experiment()
        self.__setup_execution()

    # =================================
    def __setup_menu(self):
        self.mac_documentation.triggered.connect(self.__app_documentation)
        self.mac_about.triggered.connect(self.__app_about)
        self.mac_exit.triggered.connect(self.__app_close)

    @staticmethod
    def __app_documentation():
        Utils.open_documentation()

    @staticmethod
    def __app_about():
        dialog = AboutApp()
        dialog.exec_()

    @staticmethod
    def __app_close():
        sys.exit()

    # =================================
    def __setup_execution(self):
        self.pbt_execute.clicked.connect(self.__handle_execute_experiment)
        self.cmb_execution_profile.setModel(self.model_configuration)

    def __handle_execute_experiment(self):
        print u"Executing the selected experiment..."

    # =================================
    def __setup_experiment(self):
        self.pbt_experiment_new.clicked.connect(self.__handle_experiment_new)
        self.pbt_experiment_edit.clicked.connect(self.__handle_experiment_edit)
        self.pbt_experiment_copy.clicked.connect(self.__handle_experiment_copy)
        self.pbt_experiment_remove.clicked.connect(self.__handle_experiment_remove)
        self.trv_experiment.setModel(self.model_experiment)
        self.trv_experiment.setColumnWidth(0, 160)
        self.trv_experiment.setColumnWidth(1, 120)
        self.trv_experiment.setColumnWidth(2, 120)
        self.update_experiment_model()
        if self.model_experiment.rowCount() > 0:
            base_index = self.model_experiment.index(0, 0, QtCore.QModelIndex())
            self.trv_experiment.setCurrentIndex(self.model_experiment.index(0, 0, base_index))

    def __handle_experiment_new(self):
        dialog = ExperimentApp(parent=self)
        dialog.exec_()

    def __handle_experiment_edit(self):
        this_node = self.model_experiment.get_node(index=self.trv_experiment.currentIndex())
        if this_node.get_code() is not None:
            dialog = ExperimentApp(parent=self, experiment_code=unicode(this_node.get_code()))
            dialog.exec_()

    def __handle_experiment_copy(self):
        this_node = self.model_experiment.get_node(index=self.trv_experiment.currentIndex())
        if this_node.get_code() is not None:
            dialog = ExperimentCopyApp(parent=self, experiment_code=this_node.get_code())
            dialog.exec_()

    def __handle_experiment_remove(self):
        this_node = self.model_experiment.get_node(index=self.trv_experiment.currentIndex())
        if this_node.get_code() is not None:
            parent_node = this_node.get_parent()
            name = parent_node.get_mask()
            version = this_node.get_mask()
            diag_tit = u"Remove"
            diag_msg = u"Do you really want to remove this\nexperiment (%s %s)?" % (name, version)
            diag_res = QtGui.QMessageBox.question(self, diag_tit, diag_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if diag_res == QtGui.QMessageBox.Yes:
                experiment = Experiment(db=self.database, code=this_node.get_code())
                experiment.remove()
                self.update_experiment_model()

    def update_experiment_model(self):
        exp_list = Experiment.get_list(db=self.database)
        root_node = None
        if exp_list is not None:
            exp_name = u""
            root_node = ExperimentNode(mask=u"Experiments")
            for item in exp_list:
                if exp_name != item[1]:
                    exp_name = item[1]
                    base_node = ExperimentNode(mask=exp_name, parent=root_node)
                new_node = ExperimentNode(mask=item[2], code=item[0], date_created=item[3], date_updated=item[4],
                                          parent=base_node)
        self.model_experiment.update_items(node=root_node)
        self.trv_experiment.expandAll()

    # =================================
    def __setup_configuration(self):
        self.pbt_monitor_center.clicked.connect(self.__handle_monitor_center)
        self.pbt_configuration_new.clicked.connect(self.__handle_configuration_new)
        self.pbt_configuration_edit.clicked.connect(self.__handle_configuration_edit)
        self.pbt_configuration_copy.clicked.connect(self.__handle_configuration_copy)
        self.pbt_configuration_remove.clicked.connect(self.__handle_configuration_remove)
        self.lsv_configuration.setModel(self.model_configuration)
        self.update_configuration_model()
        if self.model_configuration.rowCount() > 0:
            self.lsv_configuration.setCurrentIndex(self.model_configuration.index(0, 0))

    def __handle_monitor_center(self):
        Utils.open_psychopy_monitor_center()

    def __handle_configuration_new(self):
        dialog = ConfigurationApp(parent=self, profile_name=u"")
        dialog.exec_()

    def __handle_configuration_edit(self):
        index = self.lsv_configuration.currentIndex().row()
        if index != -1:
            profile = self.model_configuration.get_item(index)
            dialog = ConfigurationApp(parent=self, profile_name=profile)
            dialog.exec_()

    def __handle_configuration_copy(self):
        index = self.lsv_configuration.currentIndex().row()
        if index != -1:
            dialog = ItemListCopyApp(model=self.model_configuration, index=index)
            dialog.exec_()
            new_name = dialog.get_new_name()
            if new_name != u"":
                profile_base = Configuration(db=self.database, name=self.model_configuration.get_item(index=index))
                profile_copy = profile_base.copy(new_name=new_name)
                profile_copy.save()
                self.update_configuration_model()
                index = self.model_configuration.get_index(item=new_name)
                self.lsv_configuration.setCurrentIndex(self.model_configuration.index(index, 0))

    def __handle_configuration_remove(self):
        index = self.lsv_configuration.currentIndex().row()
        if index != -1:
            name = self.model_configuration.get_item(index=index)
            diag_tit = u"Remove"
            diag_msg = u"Do you really want to remove this\nconfiguration profile (%s)?" % name
            diag_res = QtGui.QMessageBox.question(self, diag_tit, diag_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if diag_res == QtGui.QMessageBox.Yes:
                profile = Configuration(db=self.database, name=name)
                profile.remove()
                self.update_configuration_model()
                index = index-1 if index > 0 else 0
                self.lsv_configuration.setCurrentIndex(self.model_configuration.index(index, 0))

    def update_configuration_model(self):
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
class ExperimentApp(ExperimentBase, ExperimentForm):
    def __init__(self, parent=SaccadeApp, experiment_code=u""):
        super(ExperimentApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__is_edit = False
        # -------------------
        self.__parent = parent
        self.experiment = Experiment(db=parent.database)
        self.model_test_data = ListModel(items=[], header=u"Test")
        self.model_test_sequence = TableModel(items=[], header=[u"Test", u"Qty"])
        # -------------------
        self.__setup_experiment()
        self.__check_code(code=experiment_code)
        # -------------------
        self.__handle_rest_checkbox()
        self.__handle_dialog_checkbox()

    # =================================
    def __setup_experiment(self):
        self.bbt_save.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.__handle_save_action)
        self.bbt_save.button(QtGui.QDialogButtonBox.Close).clicked.connect(self.__handle_close_action)
        self.pbt_dat_new.clicked.connect(self.__handle_test_new)
        self.pbt_dat_edit.clicked.connect(self.__handle_test_edit)
        self.pbt_dat_copy.clicked.connect(self.__handle_test_copy)
        self.pbt_dat_remove.clicked.connect(self.__handle_test_remove)
        self.pbt_dat_up.clicked.connect(self.__handle_test_move_up)
        self.pbt_dat_down.clicked.connect(self.__handle_test_move_down)
        self.pbt_seq_add.clicked.connect(self.__handle_sequence_add)
        self.pbt_seq_edit.clicked.connect(self.__handle_sequence_edit)
        self.pbt_seq_copy.clicked.connect(self.__handle_sequence_copy)
        self.pbt_seq_remove.clicked.connect(self.__handle_sequence_remove)
        self.pbt_seq_up.clicked.connect(self.__handle_sequence_move_up)
        self.pbt_seq_down.clicked.connect(self.__handle_sequence_move_down)
        self.cbt_rest_active.clicked.connect(self.__handle_rest_checkbox)
        self.cbt_dialog_active.clicked.connect(self.__handle_dialog_checkbox)
        self.lsv_test_dat.setModel(self.model_test_data)
        self.tbv_test_seq.setModel(self.model_test_sequence)
        self.tbv_test_seq.setColumnWidth(0, 80)
        self.tbv_test_seq.setColumnWidth(1, 45)

    def __handle_save_action(self):
        pass

    def __handle_close_action(self):
        pass

    def __handle_test_new(self):
        dialog = TestApp(parent=self)
        dialog.exec_()

    def __handle_test_edit(self):
        index = self.lsv_test_dat.currentIndex().row()
        if index != -1:
            dialog = TestApp(parent=self, test_id=index)
            dialog.exec_()

    def __handle_test_copy(self):
        dialog = TestCopyApp(parent=self)
        dialog.exec_()

    def __handle_test_remove(self):
        index = self.lsv_test_dat.currentIndex().row()
        if index != -1:
            name = self.model_test_data.get_item(index=index)
            diag_tit = u"Remove"
            diag_msg = u"Do you really want to remove this\ntest (%s)?" % name
            diag_res = QtGui.QMessageBox.question(self, diag_tit, diag_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if diag_res == QtGui.QMessageBox.Yes:
                self.experiment.item_remove(item_id=index)
                self.update_data_model()
                self.update_sequence_model()
                index = index-1 if index > 0 else 0
                self.lsv_test_dat.setCurrentIndex(self.model_test_data.index(index, 0))
                self.tbv_test_seq.setCurrentIndex(self.model_test_sequence.index(0, 0))

    def __handle_test_move_up(self):
        index = self.lsv_test_dat.currentIndex().row()
        if self.experiment.item_move_up(item_id=index):
            self.update_data_model()
            self.lsv_test_dat.setCurrentIndex(self.model_test_data.index(index-1, 0))

    def __handle_test_move_down(self):
        index = self.lsv_test_dat.currentIndex().row()
        if self.experiment.item_move_down(item_id=index):
            self.update_data_model()
            self.lsv_test_dat.setCurrentIndex(self.model_test_data.index(index+1, 0))

    def __handle_sequence_add(self):
        dialog = SequenceItemApp(parent=self)
        dialog.exec_()

    def __handle_sequence_edit(self):
        index = self.tbv_test_seq.currentIndex().row()
        if index != -1:
            dialog = SequenceItemApp(parent=self, index=index)
            dialog.exec_()

    def __handle_sequence_copy(self):
        index = self.tbv_test_seq.currentIndex().row()
        if index != -1:
            item_count = self.experiment.get_sequence_length()
            item = self.experiment.get_sequence()[index]
            self.experiment.sequence_add(item_id=self.experiment.get_items().index(item[0]), quantity=item[1])
            self.update_sequence_model()
            self.tbv_test_seq.setCurrentIndex(self.model_test_sequence.index(item_count, 0))

    def __handle_sequence_remove(self):
        index = self.tbv_test_seq.currentIndex().row()
        if index != -1:
            self.experiment.sequence_remove(index=index)
            self.update_sequence_model()
            index = index-1 if index > 0 else 0
            self.tbv_test_seq.setCurrentIndex(self.model_test_sequence.index(index, 0))

    def __handle_sequence_move_up(self):
        index = self.tbv_test_seq.currentIndex().row()
        if self.experiment.sequence_move_up(index=index):
            self.update_sequence_model()
            self.tbv_test_seq.setCurrentIndex(self.model_test_sequence.index(index-1, 0))

    def __handle_sequence_move_down(self):
        index = self.tbv_test_seq.currentIndex().row()
        if self.experiment.sequence_move_down(index=index):
            self.update_sequence_model()
            self.tbv_test_seq.setCurrentIndex(self.model_test_sequence.index(index+1, 0))

    def __handle_rest_checkbox(self):
        if not self.cbt_rest_active.isChecked():
            self.isb_rest_period.setEnabled(False)
            self.dsb_rest_time.setEnabled(False)
        else:
            self.isb_rest_period.setEnabled(True)
            self.dsb_rest_time.setEnabled(True)

    def __handle_dialog_checkbox(self):
        if not self.cbt_dialog_active.isChecked():
            self.cbt_age.setEnabled(False)
            self.cbt_eyes.setEnabled(False)
            self.cbt_gender.setEnabled(False)
            self.cbt_glasses.setEnabled(False)
        else:
            self.cbt_age.setEnabled(True)
            self.cbt_eyes.setEnabled(True)
            self.cbt_gender.setEnabled(True)
            self.cbt_glasses.setEnabled(True)

    def __check_code(self, code=u""):
        if code != u"":
            self.__is_edit = True
            self.experiment.load(code=code)
        self.led_name.setText(self.experiment.get_name())
        self.led_code.setText(self.experiment.get_code())
        self.led_version.setText(self.experiment.get_version())
        self.led_comments.setText(self.experiment.get_comments())
        self.ted_description.setPlainText(self.experiment.get_description())
        self.ted_instructions.setPlainText(self.experiment.get_instructions())
        self.cbt_use_space_key.setChecked(self.experiment.is_space_start())
        self.cbt_random_active.setChecked(self.experiment.is_random())
        self.cbt_rest_active.setChecked(self.experiment.is_rest())
        self.cbt_dialog_active.setChecked(self.experiment.is_dialog_active())
        self.cbt_age.setChecked(self.experiment.is_ask_age())
        self.cbt_eyes.setChecked(self.experiment.is_ask_eye_color())
        self.cbt_gender.setChecked(self.experiment.is_ask_gender())
        self.cbt_glasses.setChecked(self.experiment.is_ask_glasses())
        self.isb_rest_period.setValue(self.experiment.get_rest_period())
        self.dsb_rest_time.setValue(self.experiment.get_rest_time())
        self.update_data_model()
        if self.model_test_data.rowCount() > 0:
            self.lsv_test_dat.setCurrentIndex(self.model_test_data.index(0, 0))
        self.update_sequence_model()
        if self.model_test_sequence.rowCount() > 0:
            self.tbv_test_seq.setCurrentIndex(self.model_test_sequence.index(0, 0))

    def update_data_model(self):
        test_lst = self.experiment.get_items()
        if test_lst:
            test_lst = [item.get_name() for item in test_lst]
            self.model_test_data.update_items(items=test_lst)
        else:
            self.model_test_data.update_items(items=[])

    def update_sequence_model(self):
        sequence_lst = self.experiment.get_sequence()
        if sequence_lst:
            sequence_lst = [[item[0].get_name(), item[1]] for item in sequence_lst]
            self.model_test_sequence.update_items(items=sequence_lst)
        else:
            self.model_test_sequence.update_items(items=[])

    def __remove_experiment(self, code):
        pass


# ===============================================
# Class: TestApp
# ===============================================
class TestApp(TestBase, TestForm):
    def __init__(self, parent=ExperimentApp, test_id=-1):
        super(TestApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__is_edit = False
        # -------------------
        self.__parent = parent
        self.test = Test()
        self.model_frame = ListModel(items=[], header=u"Frame")
        # -------------------
        self.__setup_test()
        self.__check_id(test_id=test_id)

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
        self.lsv_frame.setModel(self.model_frame)

    def __handle_save_action(self):
        pass

    def __handle_close_action(self):
        self.close()

    def __handle_frame_new(self):
        dialog = FrameApp(parent=self)
        dialog.exec_()

    def __handle_frame_edit(self):
        index = self.lsv_frame.currentIndex().row()
        if index != -1:
            dialog = FrameApp(parent=self, frame_id=index)
            dialog.exec_()

    def __handle_frame_copy(self):
        index = self.lsv_frame.currentIndex().row()
        if index != -1:
            dialog = ItemListCopyApp(model=self.model_frame, index=index)
            dialog.exec_()
            new_name = dialog.get_new_name()
            if new_name != u"":
                new_index = self.test.get_items_length()
                frame_base = self.test.get_item(item_id=index)
                frame_copy = frame_base.copy()
                frame_copy.set_name(name=new_name)
                self.test.item_add(item=frame_copy)
                self.update_frame_model()
                self.lsv_frame.setCurrentIndex(self.model_frame.index(new_index, 0))

    def __handle_frame_remove(self):
        index = self.lsv_frame.currentIndex().row()
        if index != -1:
            name = self.model_frame.get_item(index=index)
            diag_tit = u"Remove"
            diag_msg = u"Do you really want to remove this\nframe (%s)?" % name
            diag_res = QtGui.QMessageBox.question(self, diag_tit, diag_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if diag_res == QtGui.QMessageBox.Yes:
                self.test.item_remove(item_id=index)
                self.update_frame_model()
                index = index-1 if index > 0 else 0
                self.lsv_frame.setCurrentIndex(self.model_frame.index(index, 0))

    def __handle_frame_move_up(self):
        index = self.lsv_frame.currentIndex().row()
        if self.test.item_move_up(item_id=index):
            self.update_frame_model()
            self.lsv_frame.setCurrentIndex(self.model_frame.index(index-1, 0))

    def __handle_frame_move_down(self):
        index = self.lsv_frame.currentIndex().row()
        if self.test.item_move_down(item_id=index):
            self.update_frame_model()
            self.lsv_frame.setCurrentIndex(self.model_frame.index(index+1, 0))

    def __handle_preview(self):
        print u"Preview Test..."

    def __check_id(self, test_id=-1):
        if test_id != -1:
            self.__is_edit = True
            self.test = self.__parent.experiment.get_item(item_id=test_id)
        self.led_name.setText(self.test.get_name())
        self.ted_description.setPlainText(self.test.get_description())
        self.update_frame_model()
        if self.model_frame.rowCount() > 0:
            self.lsv_frame.setCurrentIndex(self.model_frame.index(0, 0))

    def update_frame_model(self):
        frame_lst = self.test.get_items()
        if frame_lst:
            frame_lst = [item.get_name() for item in frame_lst]
            self.model_frame.update_items(items=frame_lst)
        else:
            self.model_frame.update_items(items=[])


# ===============================================
# Class: FrameApp
# ===============================================
class FrameApp(FrameBase, FrameForm):
    def __init__(self, parent=TestApp, frame_id=-1):
        super(FrameApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__is_edit = False
        # -------------------
        self.__parent = parent
        self.frame = Frame()
        self.model_colors = ColorListModel()
        self.model_component = TableModel(items=[], header=[u"Component", u"Shape"])
        # -------------------
        self.__setup_frame()
        self.__check_id(frame_id=frame_id)

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
        self.rbt_task.clicked.connect(self.__handle_task_select)
        self.rbt_time.clicked.connect(self.__handle_task_select)
        self.pbt_preview.clicked.connect(self.__handle_preview)
        self.cmb_background.setModel(self.model_colors)
        self.tbv_component.setModel(self.model_component)
        self.tbv_component.setColumnWidth(0, 160)
        self.tbv_component.setColumnWidth(1, 50)

    def __handle_save_action(self):
        pass

    def __handle_close_action(self):
        self.close()

    def __handle_component_new(self):
        dialog = ComponentApp(parent=self)
        dialog.exec_()

    def __handle_component_edit(self):
        index = self.tbv_component.currentIndex().row()
        if index != -1:
            dialog = ComponentApp(parent=self, component_id=index)
            dialog.exec_()

    def __handle_component_copy(self):
        index = self.tbv_component.currentIndex().row()
        if index != -1:
            dialog = ItemListCopyApp(model=self.model_component, index=index)
            dialog.exec_()
            new_name = dialog.get_new_name()
            if new_name != u"":
                new_index = self.frame.get_items_length()
                component_base = self.frame.get_item(item_id=index)
                component_copy = component_base.copy()
                component_copy.set_name(name=new_name)
                self.frame.item_add(item=component_copy)
                self.update_component_model()
                self.tbv_component.setCurrentIndex(self.model_component.index(new_index, 0))

    def __handle_component_remove(self):
        index = self.tbv_component.currentIndex().row()
        if index != -1:
            name = self.model_component.get_item(index=index)[0]
            diag_tit = u"Remove"
            diag_msg = u"Do you really want to remove this\ncomponent (%s)?" % name
            diag_res = QtGui.QMessageBox.question(self, diag_tit, diag_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if diag_res == QtGui.QMessageBox.Yes:
                self.frame.item_remove(item_id=index)
                self.update_component_model()
                index = index-1 if index > 0 else 0
                self.tbv_component.setCurrentIndex(self.model_component.index(index, 0))

    def __handle_component_move_up(self):
        index = self.tbv_component.currentIndex().row()
        if self.frame.item_move_up(item_id=index):
            self.update_component_model()
            self.tbv_component.setCurrentIndex(self.model_component.index(index-1, 0))

    def __handle_component_move_down(self):
        index = self.tbv_component.currentIndex().row()
        if self.frame.item_move_down(item_id=index):
            self.update_component_model()
            self.tbv_component.setCurrentIndex(self.model_component.index(index+1, 0))

    def __handle_task_select(self):
        if self.rbt_task.isChecked():
            self.dsb_time.setValue(0.0)
            self.dsb_time.setEnabled(False)
            self.led_keys_allowed.setEnabled(True)
            self.led_keys_selected.setEnabled(True)
        else:
            self.led_keys_allowed.setText(u"")
            self.led_keys_selected.setText(u"")
            self.dsb_time.setEnabled(True)
            self.led_keys_allowed.setEnabled(False)
            self.led_keys_selected.setEnabled(False)

    def __handle_preview(self):
        print u"Preview Frame..."

    def __check_id(self, frame_id=-1):
        if frame_id != -1:
            self.__is_edit = True
            self.frame = self.__parent.test.get_item(item_id=frame_id)
        self.led_name.setText(self.frame.get_name())
        self.rbt_task.setChecked(self.frame.is_task())
        self.rbt_time.setChecked(not self.frame.is_task())
        color_index = self.cmb_background.findText(self.frame.get_color(), QtCore.Qt.MatchFixedString)
        self.cmb_background.setCurrentIndex(color_index)
        self.__handle_task_select()
        self.dsb_time.setValue(self.frame.get_time())
        self.led_keys_allowed.setText(self.frame.get_keys_allowed())
        self.led_keys_selected.setText(self.frame.get_keys_selected())
        self.update_component_model()
        if self.model_component.rowCount() > 0:
            self.tbv_component.setCurrentIndex(self.model_component.index(0, 0))

    def update_component_model(self):
        component_lst = self.frame.get_items()
        if component_lst:
            component_lst = [[item.get_name(), item.get_shape()] for item in component_lst]
            self.model_component.update_items(items=component_lst)
        else:
            self.model_component.update_items(items=[])


# ===============================================
# Class: ComponentApp
# ===============================================
class ComponentApp(ComponentBase, ComponentForm):
    def __init__(self, parent=FrameApp, component_id=-1):
        super(ComponentApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__is_edit = False
        # -------------------
        self.__parent = parent
        self.component = Component()
        # -------------------
        self.__setup_component()
        self.__check_id(component_id=component_id)

    # =================================
    def __setup_component(self):
        self.bbt_save.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.__handle_save_action)
        self.bbt_save.button(QtGui.QDialogButtonBox.Close).clicked.connect(self.__handle_close_action)
        self.pbt_image_open.clicked.connect(self.__handle_image_open)
        self.pbt_image_zoom.clicked.connect(self.__handle_image_zoom)
        self.pbt_preview.clicked.connect(self.__handle_preview)

    def __handle_save_action(self):
        pass

    def __handle_close_action(self):
        pass

    def __handle_image_open(self):
        pass

    def __handle_image_zoom(self):
        pass

    def __handle_preview(self):
        pass

    def __check_id(self, component_id=-1):
        if component_id != -1:
            self.__is_edit = True
            self.component = self.__parent.frame.get_item(item_id=component_id)
        self.led_name.setText(self.component.get_name())


# =============================================================================
# Configuration related Class: ConfigurationApp
# =============================================================================
class ConfigurationApp(ConfigurationBase, ConfigurationForm):
    def __init__(self, parent=SaccadeApp, profile_name=u""):
        super(ConfigurationApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__is_edit = False
        # -------------------
        self.__parent = parent
        self.__profile = Configuration(db=parent.database)
        self.__model_tracker = ListModel(Utils.get_available_trackers())
        self.__model_monitor = ListModel(Utils.get_available_monitors())
        self.__model_screen = ListModel(Utils.get_available_screens())
        # -------------------
        self.__setup_dialog()
        self.__check_name(name=profile_name)

    # =================================
    def __setup_dialog(self):
        self.bbt_save.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.__handle_save_action)
        self.pbt_path_browse.clicked.connect(self.__handle_path_browse)
        self.cmb_tracker.setModel(self.__model_tracker)
        self.cmb_monitor.setModel(self.__model_monitor)
        self.cmb_screen.setModel(self.__model_screen)

    def __handle_save_action(self):
        self.__profile.set_events_path(self.led_path.text())
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
        if not self.__profile.in_database():    # Profile already exists...
            diag_tit = u"Error"
            diag_msg = u"Name already used. Do you want to overwrite?"
            diag_res = QtGui.QMessageBox.question(self, diag_tit, diag_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if diag_res == QtGui.QMessageBox.Yes:                # Overwrite!
                if self.__is_edit:
                    self.__remove_profile(old_name)
                self.__remove_profile(new_name)
                self.__profile.set_name(new_name)
                self.__profile.save()
            else:                                               # Find new name!
                is_ready = False
                while not is_ready:
                    diag_tit = u"New name"
                    diag_msg = u"New profile name:"
                    new_name, is_ok = QtGui.QInputDialog.getText(None, diag_tit, diag_msg, text=new_name)
                    new_name = unicode(new_name)
                    if is_ok:
                        if self.__profile.set_name(new_name):
                            self.__profile.save()
                            is_ready = True
                        else:
                            diag_tit = u"Error"
                            diag_msg = u"This name already exists.\nTry another one."
                            QtGui.QMessageBox.warning(self, diag_tit, diag_msg)
                    else:
                        new_name = None
                        is_ready = True
        if self.__profile.in_database():
            self.__parent.update_configuration_model()
            index = self.__parent.model_configuration.get_index(new_name)
            self.__parent.lsv_configuration.setCurrentIndex(self.__parent.model_configuration.index(index, 0))

    def __handle_path_browse(self):
        title = u"Select events save directory..."
        folder = QtGui.QFileDialog.getExistingDirectory(self, title, self.led_path.text(),
                                                        QtGui.QFileDialog.ShowDirsOnly)
        if folder:
            self.led_path.setText(unicode(folder))

    def __check_name(self, name=u""):
        if name != u"":
            self.__is_edit = True
            self.__profile.load(name=name)
        screen_index = self.cmb_screen.findText(self.__profile.get_screen(), QtCore.Qt.MatchFixedString)
        monitor_index = self.cmb_monitor.findText(self.__profile.get_monitor(), QtCore.Qt.MatchFixedString)
        tracker_index = self.cmb_tracker.findText(self.__profile.get_tracker_name(), QtCore.Qt.MatchFixedString)
        self.cmb_screen.setCurrentIndex(screen_index)
        self.cmb_monitor.setCurrentIndex(monitor_index)
        self.cmb_tracker.setCurrentIndex(tracker_index)
        self.led_name.setText(self.__profile.get_name())
        self.led_path.setText(self.__profile.get_events_path())

    def __remove_profile(self, name):
        profile = Configuration(db=self.__parent.database, name=name)
        profile.remove()


# =============================================================================
# Utility Classes:
# =============================================================================
# ===============================================
# Class: ExperimentCopyApp
# ===============================================
class ExperimentCopyApp(ExperimentCopyBase, ExperimentCopyForm):
    def __init__(self, parent=SaccadeApp, experiment_code=u""):
        super(ExperimentCopyApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__parent = parent
        self.__experiment = Experiment(db=parent.database, code=experiment_code)
        # -------------------
        self.__setup_dialog()

    # =================================
    def __setup_dialog(self):
        self.pbt_ok.clicked.connect(self.__handle_ok_action)
        self.pbt_cancel.clicked.connect(self.__handle_cancel_action)
        self.lbl_code.setText(u"Base experiment code: "+self.__experiment.get_code()+u".\n\nNew code:")
        self.lbl_version.setText(u"Base experiment version: "+self.__experiment.get_version()+u".\n\nNew version:")
        self.led_code.setText(self.__experiment.get_code())
        self.led_version.setText(self.__experiment.get_version())

    def __handle_ok_action(self):
        new_code = unicode(self.led_code.text())
        new_version = unicode(self.led_version.text())
        new_experiment = self.__experiment.copy(code=new_code, version=new_version)
        if new_experiment is not None:
            new_experiment.save()
            self.__parent.update_experiment_model()
            new_index = self.__parent.model_experiment.get_index_by_code(code=new_code)
            self.__parent.trv_experiment.setCurrentIndex(new_index)
            self.close()
        else:
            diag_tit = u"Error"
            diag_msg = u"Code or version value already\nused for this type of experiment."
            QtGui.QMessageBox.warning(self, diag_tit, diag_msg)

    def __handle_cancel_action(self):
        self.close()


# ===============================================
# Class: TestCopyApp
# ===============================================
class TestCopyApp(TestCopyBase, TestCopyForm):
    def __init__(self, parent=TestApp):
        super(TestCopyApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.parent = parent
        # -------------------
        self.__setup_dialog()

    # =================================
    def __setup_dialog(self):
        pass


# ===============================================
# Class: ItemListCopyApp
# ===============================================
class ItemListCopyApp(ItemListCopyBase, ItemListCopyForm):
    def __init__(self, model, index=-1):
        super(ItemListCopyApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__item_list = model.get_list()
        self.__item_name = self.__item_list[index]
        self.__new_name = u""
        # -------------------
        self.__setup_dialog()

    def __setup_dialog(self):
        self.pbt_ok.clicked.connect(self.__handle_ok_action)
        self.pbt_cancel.clicked.connect(self.__handle_cancel_action)
        self.lbl_copy.setText(u"Old name: "+self.__item_name+u".\n\nNew name:")
        self.led_copy.setText(self.__item_name)

    def __handle_ok_action(self):
        new_name = unicode(self.led_copy.text())
        if new_name not in self.__item_list:
            self.__new_name = new_name
            self.close()
        else:
            diag_tit = u"Error"
            diag_msg = u"Name already used for this\ntype of item."
            QtGui.QMessageBox.warning(self, diag_tit, diag_msg)

    def __handle_cancel_action(self):
        self.close()

    def get_new_name(self):
        return self.__new_name


# ===============================================
# Class: SequenceItemApp
# ===============================================
class SequenceItemApp(SequenceItemBase, SequenceItemForm):
    def __init__(self, parent=ExperimentApp, index=-1):
        super(SequenceItemApp, self).__init__(parent=None)
        self.setupUi(self)
        # -------------------
        self.__parent = parent
        self.__is_edit = False
        self.__index = index
        # -------------------
        self.__setup_dialog()
        self.__check_index()

    def __setup_dialog(self):
        self.pbt_ok.clicked.connect(self.__handle_ok_action)
        self.pbt_cancel.clicked.connect(self.__handle_cancel_action)
        self.cmb_test.setModel(self.__parent.model_test_data)

    def __handle_ok_action(self):
        test_id = self.cmb_test.currentIndex()
        test_quantity = self.isb_quantity.value()
        if self.__is_edit:
            self.__parent.experiment.sequence_edit(index=self.__index, item_id=test_id, quantity=test_quantity)
        else:
            self.__parent.experiment.sequence_add(item_id=test_id, quantity=test_quantity)
            self.__index = self.__parent.experiment.get_sequence_length()-1
        self.__parent.update_sequence_model()
        self.__parent.tbv_test_seq.setCurrentIndex(self.__parent.model_test_sequence.index(self.__index, 0))
        self.close()

    def __handle_cancel_action(self):
        self.close()

    def __check_index(self):
        if self.__index != -1:
            self.__is_edit = True
            item = self.__parent.experiment.get_sequence_item(index=self.__index)
            self.cmb_test.setCurrentIndex(self.cmb_test.findText(item[0].get_name(), QtCore.Qt.MatchFixedString))
            self.isb_quantity.setValue(item[1])


# ===============================================
# Class: About
# ===============================================
class AboutApp(AboutBase, AboutForm):
    def __init__(self):
        super(AboutApp, self).__init__(parent=None)
        self.setupUi(self)
